"""Stable-Baselines3 scientific-state adapters for protocol-v2 pilots.

This module is intentionally optional.  The historical/default thesis runtime
must not import Stable-Baselines3 unless the ``protocol-v2-pilot`` dependency
group is installed.

The adapters add protocol-v2 semantics that a normal SB3 ``model.save()`` does
not provide on its own:

* CPU-only execution on the validated thesis-machine contract;
* virtual per-adapter Python/NumPy/PyTorch/action-space RNG state so branch
  clones do not silently share process-global RNG streams;
* DQN replay-buffer persistence in addition to the normal model zip;
* explicit legal checkpoint/update-boundary validation;
* deterministic live-state fingerprints over parameters, optimizer, replay,
  counters, RNG and declared configuration; and
* continuation to a predeclared *total actual interaction* target without
  resetting the SB3 learning schedule.

No hyperparameter defaults are selected here.  Callers must construct the SB3
model with an explicit protocol configuration and pass the same configuration
mapping to the adapter for provenance validation.
"""
from __future__ import annotations

import base64
import contextlib
import hashlib
import io
import json
import random
import struct
import zipfile
from dataclasses import dataclass
from typing import Any, Callable, Iterator, Mapping

SB3_SCIENTIFIC_STATE_SCHEMA_VERSION = 1
SUPPORTED_SB3_VERSION = "2.9.0"


def _imports() -> tuple[Any, Any, Any, Any]:
    try:
        import numpy as np
        import stable_baselines3 as sb3
        import torch
        from stable_baselines3 import DQN, PPO
    except ImportError as exc:  # pragma: no cover - exercised by optional-dependency boundary
        raise RuntimeError(
            "protocol-v2 SB3 adapters require the optional protocol-v2-pilot dependency group"
        ) from exc
    if sb3.__version__ != SUPPORTED_SB3_VERSION:
        raise RuntimeError(
            f"unsupported Stable-Baselines3 version {sb3.__version__!r}; "
            f"expected {SUPPORTED_SB3_VERSION!r}"
        )
    return np, torch, DQN, PPO


def _json_copy(value: Any, *, field: str) -> Any:
    try:
        return json.loads(
            json.dumps(
                value,
                ensure_ascii=False,
                allow_nan=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be finite JSON-compatible data") from exc


def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def _unb64(value: Any, *, field: str) -> bytes:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be non-empty base64 text")
    try:
        return base64.b64decode(value.encode("ascii"), validate=True)
    except (UnicodeEncodeError, ValueError) as exc:
        raise ValueError(f"{field} must be valid base64") from exc


def _tuple_tree(value: Any) -> Any:
    if isinstance(value, list):
        return tuple(_tuple_tree(item) for item in value)
    return value


def _list_tree(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_list_tree(item) for item in value]
    if isinstance(value, list):
        return [_list_tree(item) for item in value]
    return value


def _numpy_rng_to_json(np: Any, state: tuple[Any, ...]) -> Mapping[str, Any]:
    if len(state) != 5:
        raise ValueError("unexpected NumPy legacy RNG state")
    name, keys, pos, has_gauss, cached_gaussian = state
    return {
        "bit_generator": str(name),
        "keys": [int(item) for item in np.asarray(keys, dtype=np.uint32).tolist()],
        "pos": int(pos),
        "has_gauss": int(has_gauss),
        "cached_gaussian": float(cached_gaussian),
    }


def _numpy_rng_from_json(np: Any, value: Mapping[str, Any]) -> tuple[Any, ...]:
    expected = {"bit_generator", "keys", "pos", "has_gauss", "cached_gaussian"}
    if not isinstance(value, Mapping) or set(value) != expected:
        raise ValueError("invalid NumPy RNG state")
    return (
        str(value["bit_generator"]),
        np.asarray(value["keys"], dtype=np.uint32),
        int(value["pos"]),
        int(value["has_gauss"]),
        float(value["cached_gaussian"]),
    )


def _action_space_rng_to_json(model: Any) -> Mapping[str, Any] | None:
    rng = getattr(model.action_space, "np_random", None)
    if rng is None:
        return None
    return _json_copy(rng.bit_generator.state, field="action-space RNG state")


def _restore_action_space_rng(model: Any, state: Mapping[str, Any] | None) -> None:
    if state is None:
        return
    rng = getattr(model.action_space, "np_random", None)
    if rng is None:
        _ = model.action_space.sample()
        rng = model.action_space.np_random
    rng.bit_generator.state = _json_copy(state, field="action-space RNG state")


def _capture_global_rng() -> Mapping[str, Any]:
    np, torch, _, _ = _imports()
    return {
        "python": _list_tree(random.getstate()),
        "numpy": _numpy_rng_to_json(np, np.random.get_state()),
        "torch_cpu": [int(item) for item in torch.get_rng_state().cpu().tolist()],
    }


def _restore_global_rng(state: Mapping[str, Any]) -> None:
    np, torch, _, _ = _imports()
    expected = {"python", "numpy", "torch_cpu"}
    if not isinstance(state, Mapping) or set(state) != expected:
        raise ValueError("invalid global RNG state")
    random.setstate(_tuple_tree(state["python"]))
    np.random.set_state(_numpy_rng_from_json(np, state["numpy"]))
    torch_state = torch.tensor(state["torch_cpu"], dtype=torch.uint8, device="cpu")
    torch.set_rng_state(torch_state)


def _canonicalize_zip(data: bytes) -> bytes:
    """Normalize zip member order/timestamps for stable checkpoint artifacts."""

    source = io.BytesIO(data)
    target = io.BytesIO()
    with zipfile.ZipFile(source, "r") as incoming, zipfile.ZipFile(
        target, "w", compression=zipfile.ZIP_STORED
    ) as outgoing:
        for name in sorted(incoming.namelist()):
            info = zipfile.ZipInfo(name)
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o600 << 16
            outgoing.writestr(info, incoming.read(name))
    return target.getvalue()


def _save_model_bytes(model: Any) -> bytes:
    handle = io.BytesIO()
    model.save(handle)
    return _canonicalize_zip(handle.getvalue())


def _save_replay_bytes(model: Any) -> bytes:
    handle = io.BytesIO()
    model.save_replay_buffer(handle)
    return handle.getvalue()


def _hash_scalar(hasher: Any, tag: str, value: Any) -> None:
    hasher.update(tag.encode("utf-8"))
    hasher.update(b"\0")
    hasher.update(str(value).encode("utf-8"))
    hasher.update(b"\0")


def _hash_value(hasher: Any, value: Any) -> None:
    np, torch, _, _ = _imports()
    if value is None:
        hasher.update(b"N")
    elif isinstance(value, bool):
        _hash_scalar(hasher, "B", int(value))
    elif isinstance(value, int):
        _hash_scalar(hasher, "I", value)
    elif isinstance(value, float):
        hasher.update(b"F")
        hasher.update(struct.pack("!d", value))
    elif isinstance(value, str):
        _hash_scalar(hasher, "S", value)
    elif isinstance(value, bytes):
        hasher.update(b"Y")
        hasher.update(len(value).to_bytes(8, "big"))
        hasher.update(value)
    elif isinstance(value, torch.Tensor):
        tensor = value.detach().cpu().contiguous()
        _hash_scalar(hasher, "T-DTYPE", str(tensor.dtype))
        _hash_value(hasher, tuple(int(item) for item in tensor.shape))
        hasher.update(tensor.numpy().tobytes(order="C"))
    elif isinstance(value, np.ndarray):
        array = np.ascontiguousarray(value)
        _hash_scalar(hasher, "A-DTYPE", str(array.dtype))
        _hash_value(hasher, tuple(int(item) for item in array.shape))
        hasher.update(array.tobytes(order="C"))
    elif isinstance(value, Mapping):
        hasher.update(b"M")
        for key in sorted(value, key=lambda item: repr(item)):
            _hash_value(hasher, key)
            _hash_value(hasher, value[key])
    elif isinstance(value, (list, tuple)):
        hasher.update(b"L" if isinstance(value, list) else b"Q")
        _hash_scalar(hasher, "LEN", len(value))
        for item in value:
            _hash_value(hasher, item)
    else:
        raise TypeError(f"unsupported scientific fingerprint value: {type(value)!r}")


def _digest_value(value: Any) -> str:
    hasher = hashlib.sha256()
    _hash_value(hasher, value)
    return hasher.hexdigest()


def _replay_fingerprint(model: Any) -> Mapping[str, Any] | None:
    replay = getattr(model, "replay_buffer", None)
    if replay is None:
        return None
    fields = {
        "buffer_size": int(replay.buffer_size),
        "pos": int(replay.pos),
        "full": bool(replay.full),
        "n_envs": int(replay.n_envs),
        "observations": replay.observations,
        "actions": replay.actions,
        "rewards": replay.rewards,
        "dones": replay.dones,
    }
    if getattr(replay, "next_observations", None) is not None:
        fields["next_observations"] = replay.next_observations
    if getattr(replay, "timeouts", None) is not None:
        fields["timeouts"] = replay.timeouts
    return fields


def _counter_snapshot(model: Any, *, method_id: str) -> Mapping[str, Any]:
    counters: dict[str, Any] = {
        "num_timesteps": int(model.num_timesteps),
        "n_updates": int(model._n_updates),
        "current_progress_remaining": float(model._current_progress_remaining),
        "total_timesteps": int(model._total_timesteps),
        "n_envs": int(model.n_envs),
    }
    if method_id == "dqn":
        counters["exploration_rate"] = float(model.exploration_rate)
        replay = model.replay_buffer
        counters["replay_pos"] = int(replay.pos)
        counters["replay_full"] = bool(replay.full)
    else:
        rollout = model.rollout_buffer
        counters["rollout_pos"] = int(rollout.pos)
        counters["rollout_full"] = bool(rollout.full)
        counters["rollout_buffer_size"] = int(rollout.buffer_size)
    return counters


@dataclass(frozen=True)
class SB3AdapterProvenance:
    method_id: str
    implementation: str = "stable-baselines3"
    version: str = SUPPORTED_SB3_VERSION
    device: str = "cpu"

    def __post_init__(self) -> None:
        if self.method_id not in {"dqn", "ppo"}:
            raise ValueError("SB3 adapter method_id must be dqn or ppo")
        if self.version != SUPPORTED_SB3_VERSION:
            raise ValueError("unsupported SB3 provenance version")
        if self.device != "cpu":
            raise ValueError("protocol-v2 SB3 pilot adapters are CPU-only")


class SB3ScientificStateAdapter:
    """Exact learner-state adapter for SB3 DQN or PPO on CPU."""

    def __init__(
        self,
        *,
        method_id: str,
        model: Any,
        configuration: Mapping[str, Any],
        environment_factory: Callable[[], Any] | None = None,
        rng_state: Mapping[str, Any] | None = None,
    ) -> None:
        np, torch, DQN, PPO = _imports()
        del np, torch
        expected_type = DQN if method_id == "dqn" else PPO if method_id == "ppo" else None
        if expected_type is None or not isinstance(model, expected_type):
            raise ValueError(f"model must be an SB3 {method_id.upper()} instance")
        if str(model.device) != "cpu":
            raise ValueError("protocol-v2 SB3 pilot adapters require device='cpu'")
        if int(model.n_envs) != 1:
            raise ValueError("protocol-v2 interaction accounting currently requires n_envs=1")
        self.method_id = method_id
        self.model = model
        self.configuration = _json_copy(configuration, field="SB3 configuration")
        self.environment_factory = environment_factory
        self.provenance = SB3AdapterProvenance(method_id=method_id)
        self._rng_state = _json_copy(
            rng_state if rng_state is not None else _capture_global_rng(),
            field="SB3 RNG state",
        )
        self._action_space_rng_state = _action_space_rng_to_json(model)
        self._validate_boundary()

    def _validate_boundary(self) -> None:
        if self.method_id == "dqn":
            if self.model.replay_buffer is None:
                raise ValueError("DQN scientific state requires an initialized replay buffer")
            unit = getattr(getattr(self.model, "train_freq", None), "unit", None)
            unit_value = getattr(unit, "value", unit)
            if str(unit_value) != "step":
                raise ValueError("DQN protocol-v2 requires step-based train_freq")
        else:
            rollout = self.model.rollout_buffer
            legal_initial = int(self.model.num_timesteps) == 0 and int(rollout.pos) == 0
            legal_completed_update = bool(rollout.full) and int(rollout.pos) == int(
                rollout.buffer_size
            )
            if not (legal_initial or legal_completed_update):
                raise ValueError(
                    "PPO scientific checkpoints are legal only before training or after a completed rollout/update"
                )

    @contextlib.contextmanager
    def _rng_scope(self) -> Iterator[None]:
        process_rng = _capture_global_rng()
        process_action_rng = _action_space_rng_to_json(self.model)
        _restore_global_rng(self._rng_state)
        _restore_action_space_rng(self.model, self._action_space_rng_state)
        try:
            yield
        finally:
            self._rng_state = _json_copy(_capture_global_rng(), field="SB3 RNG state")
            self._action_space_rng_state = _action_space_rng_to_json(self.model)
            _restore_global_rng(process_rng)
            _restore_action_space_rng(self.model, process_action_rng)

    def _live_fingerprint_payload(self) -> Mapping[str, Any]:
        payload: dict[str, Any] = {
            "schema_version": SB3_SCIENTIFIC_STATE_SCHEMA_VERSION,
            "method_id": self.method_id,
            "provenance": self.provenance.__dict__,
            "configuration": self.configuration,
            "parameters": self.model.get_parameters(),
            "counters": _counter_snapshot(self.model, method_id=self.method_id),
            "rng_state": self._rng_state,
            "action_space_rng_state": self._action_space_rng_state,
        }
        if self.method_id == "dqn":
            payload["replay"] = _replay_fingerprint(self.model)
        return payload

    def state_sha256(self) -> str:
        return _digest_value(self._live_fingerprint_payload())

    def export_state(self) -> Mapping[str, Any]:
        self._validate_boundary()
        model_bytes = _save_model_bytes(self.model)
        state: dict[str, Any] = {
            "schema_version": SB3_SCIENTIFIC_STATE_SCHEMA_VERSION,
            "method_id": self.method_id,
            "provenance": _json_copy(self.provenance.__dict__, field="SB3 provenance"),
            "configuration": self.configuration,
            "model_zip_b64": _b64(model_bytes),
            "rng_state": self._rng_state,
            "action_space_rng_state": self._action_space_rng_state,
            "counters": _json_copy(
                _counter_snapshot(self.model, method_id=self.method_id),
                field="SB3 counters",
            ),
            "state_sha256": self.state_sha256(),
        }
        if self.method_id == "dqn":
            state["replay_buffer_b64"] = _b64(_save_replay_bytes(self.model))
        else:
            state["replay_buffer_b64"] = None
        return _json_copy(state, field="SB3 scientific state")

    def restore_state(self, state: Mapping[str, Any]) -> None:
        expected = {
            "schema_version",
            "method_id",
            "provenance",
            "configuration",
            "model_zip_b64",
            "replay_buffer_b64",
            "rng_state",
            "action_space_rng_state",
            "counters",
            "state_sha256",
        }
        if not isinstance(state, Mapping) or set(state) != expected:
            raise ValueError("invalid SB3 scientific state keys")
        if state["schema_version"] != SB3_SCIENTIFIC_STATE_SCHEMA_VERSION:
            raise ValueError("unsupported SB3 scientific state schema_version")
        if state["method_id"] != self.method_id:
            raise ValueError("SB3 scientific state method mismatch")
        if state["configuration"] != self.configuration:
            raise ValueError("SB3 scientific state configuration mismatch")
        if state["provenance"] != self.provenance.__dict__:
            raise ValueError("SB3 scientific state provenance mismatch")

        _, _, DQN, PPO = _imports()
        algorithm = DQN if self.method_id == "dqn" else PPO
        env = self.environment_factory() if self.environment_factory is not None else None
        model_data = io.BytesIO(_unb64(state["model_zip_b64"], field="model_zip_b64"))
        loaded = algorithm.load(
            model_data,
            env=env,
            device="cpu",
            force_reset=False,
        )
        if self.method_id == "dqn":
            replay_data = state["replay_buffer_b64"]
            if replay_data is None:
                raise ValueError("DQN scientific state requires replay_buffer_b64")
            loaded.load_replay_buffer(
                io.BytesIO(_unb64(replay_data, field="replay_buffer_b64"))
            )
        elif state["replay_buffer_b64"] is not None:
            raise ValueError("PPO scientific state must not contain a replay buffer")

        self.model = loaded
        self._rng_state = _json_copy(state["rng_state"], field="SB3 RNG state")
        self._action_space_rng_state = _json_copy(
            state["action_space_rng_state"], field="action-space RNG state"
        ) if state["action_space_rng_state"] is not None else None
        _restore_action_space_rng(self.model, self._action_space_rng_state)
        self._validate_boundary()
        if _counter_snapshot(self.model, method_id=self.method_id) != state["counters"]:
            raise ValueError("SB3 scientific state counters failed round-trip validation")
        if self.state_sha256() != state["state_sha256"]:
            raise ValueError("SB3 scientific state failed exact fingerprint validation")

    def clone(self) -> "SB3ScientificStateAdapter":
        state = self.export_state()
        clone = object.__new__(SB3ScientificStateAdapter)
        clone.method_id = self.method_id
        clone.model = self.model
        clone.configuration = self.configuration
        clone.environment_factory = self.environment_factory
        clone.provenance = self.provenance
        clone._rng_state = self._rng_state
        clone._action_space_rng_state = self._action_space_rng_state
        clone.restore_state(state)
        return clone

    def predict(self, observation: Any, *, deterministic: bool) -> Any:
        with self._rng_scope():
            action, _ = self.model.predict(observation, deterministic=deterministic)
        return action

    def _require_compatible_target(self, target_interactions: int) -> int:
        if (
            not isinstance(target_interactions, int)
            or isinstance(target_interactions, bool)
            or target_interactions < int(self.model.num_timesteps)
        ):
            raise ValueError("target_interactions must be an integer >= current interactions")
        delta = target_interactions - int(self.model.num_timesteps)
        if delta == 0:
            return 0
        if self.method_id == "ppo":
            quantum = int(self.model.n_steps) * int(self.model.n_envs)
            if delta % quantum != 0:
                raise ValueError(
                    "PPO target interaction index must align with completed rollout/update boundaries"
                )
        else:
            frequency = int(self.model.train_freq.frequency) * int(self.model.n_envs)
            if delta % frequency != 0:
                raise ValueError(
                    "DQN target interaction index must align with step train_freq boundaries"
                )
        return delta

    def learn_to_total_interactions(
        self,
        target_interactions: int,
        *,
        callback: Any = None,
    ) -> None:
        delta = self._require_compatible_target(target_interactions)
        if delta == 0:
            return
        if self.model.get_env() is None:
            if self.environment_factory is None:
                raise RuntimeError("continued learning requires an attached environment")
            self.model.set_env(self.environment_factory(), force_reset=False)
        with self._rng_scope():
            self.model.learn(
                total_timesteps=delta,
                callback=callback,
                reset_num_timesteps=False,
                progress_bar=False,
            )
        if int(self.model.num_timesteps) != target_interactions:
            raise RuntimeError(
                "SB3 learner did not stop at the requested actual interaction index"
            )
        self._validate_boundary()


def dqn_state_adapter(
    model: Any,
    *,
    configuration: Mapping[str, Any],
    environment_factory: Callable[[], Any] | None = None,
) -> SB3ScientificStateAdapter:
    return SB3ScientificStateAdapter(
        method_id="dqn",
        model=model,
        configuration=configuration,
        environment_factory=environment_factory,
    )


def ppo_state_adapter(
    model: Any,
    *,
    configuration: Mapping[str, Any],
    environment_factory: Callable[[], Any] | None = None,
) -> SB3ScientificStateAdapter:
    return SB3ScientificStateAdapter(
        method_id="ppo",
        model=model,
        configuration=configuration,
        environment_factory=environment_factory,
    )

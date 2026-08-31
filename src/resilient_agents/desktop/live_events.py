"""Transient, lossy live-presentation stream for the T-528 desktop worker.

The stream is explicitly not Study evidence. It lives outside ``results/studies``
and ``results/runs`` and may drop frames whenever the consumer/writer cannot keep
up. Scientific execution must never wait for this sink.
"""
from __future__ import annotations

import json
import queue
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

LIVE_SCHEMA_VERSION = 1


def live_state_path(writable_root: Path, study_id: str) -> Path:
    return (
        Path(writable_root).resolve()
        / "results"
        / "presentation"
        / study_id
        / "live-state.json"
    )


class DroppingLiveEventSink:
    """Non-blocking queue + background latest-state writer.

    ``emit`` uses ``put_nowait`` only. A full queue increments a drop counter and
    returns immediately. The background thread collapses events by stream_id and
    periodically writes one atomic latest-state snapshot.
    """

    def __init__(
        self,
        *,
        writable_root: Path,
        study_id: str,
        queue_size: int = 512,
        flush_interval_seconds: float = 0.05,
    ) -> None:
        if not isinstance(study_id, str) or not study_id.strip():
            raise ValueError("study_id must be non-empty")
        if queue_size <= 0:
            raise ValueError("queue_size must be > 0")
        if flush_interval_seconds <= 0:
            raise ValueError("flush_interval_seconds must be > 0")
        self.study_id = study_id
        self.path = live_state_path(writable_root, study_id)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.unlink(missing_ok=True)
        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_size)
        self._flush_interval = float(flush_interval_seconds)
        self._stop = threading.Event()
        self._dropped = 0
        self._sequence = 0
        self._thread = threading.Thread(
            target=self._writer_loop,
            name=f"t528-live-{study_id}",
            daemon=True,
        )
        self._thread.start()

    @property
    def dropped_events(self) -> int:
        return self._dropped

    def emit(self, event: Mapping[str, Any]) -> None:
        if not isinstance(event, Mapping):
            return
        payload = dict(event)
        stream_id = payload.get("stream_id")
        if not isinstance(stream_id, str) or not stream_id:
            return
        try:
            self._queue.put_nowait(payload)
        except queue.Full:
            self._dropped += 1

    def close(self) -> None:
        self._stop.set()
        self._thread.join(timeout=2.0)

    def _writer_loop(self) -> None:
        latest: dict[str, dict[str, Any]] = {}
        dirty = False
        last_flush = time.monotonic()
        while not self._stop.is_set() or not self._queue.empty():
            timeout = max(0.005, self._flush_interval - (time.monotonic() - last_flush))
            try:
                event = self._queue.get(timeout=timeout)
            except queue.Empty:
                event = None
            if event is not None:
                stream_id = str(event["stream_id"])
                self._sequence += 1
                event = dict(event)
                event["presentation_sequence"] = self._sequence
                latest[stream_id] = event
                dirty = True

            now = time.monotonic()
            if dirty and (now - last_flush >= self._flush_interval or self._stop.is_set()):
                self._write_snapshot(latest)
                dirty = False
                last_flush = now

        if dirty:
            self._write_snapshot(latest)

    def _write_snapshot(self, latest: Mapping[str, Mapping[str, Any]]) -> None:
        snapshot = {
            "schema_version": LIVE_SCHEMA_VERSION,
            "purpose": "transient-presentation-only-not-scientific-evidence",
            "study_id": self.study_id,
            "dropped_events": self._dropped,
            "latest_by_stream": dict(latest),
        }
        temporary = self.path.with_suffix(".json.tmp")
        try:
            temporary.write_text(
                json.dumps(snapshot, allow_nan=False, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            temporary.replace(self.path)
        except Exception:
            # Filesystem/UI presentation failures are intentionally unable to
            # propagate back to scientific execution. A later frame may succeed.
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass


@dataclass(frozen=True)
class LiveGridFrame:
    stream_id: str
    phase: str
    method_id: str
    root_id: str
    layout_id: str
    branch: str | None
    episode_index: int
    interaction_index: int
    environment_step: int
    width: int
    height: int
    start: tuple[int, int]
    goal: tuple[int, int]
    obstacles: tuple[tuple[int, int], ...]
    true_state: tuple[int, int]
    delivered_observation: tuple[int, int]
    intended_action: str
    executed_action: str
    reward: float
    terminated: bool
    truncated: bool
    regime_id: str | None
    disturbance_flags: Mapping[str, bool]
    change_event_ids: tuple[str, ...]
    presentation_sequence: int


class DesktopLiveReadModel:
    """Read only the transient presentation snapshot for one selected Study."""

    def __init__(self, *, writable_root: Path) -> None:
        self.writable_root = Path(writable_root).resolve()

    @staticmethod
    def _coordinate(value: Any, *, field: str) -> tuple[int, int]:
        if (
            not isinstance(value, list)
            or len(value) != 2
            or not all(isinstance(item, int) and not isinstance(item, bool) for item in value)
        ):
            raise RuntimeError(f"{field} must be a two-integer coordinate")
        return int(value[0]), int(value[1])

    def latest(self, study_id: str) -> tuple[LiveGridFrame, ...]:
        path = live_state_path(self.writable_root, study_id)
        if not path.is_file():
            return ()
        try:
            root = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            # Atomic writer replacement can race a read on some filesystems.
            # A transient presentation read failure should render as unavailable,
            # never as a scientific/application failure.
            return ()
        if not isinstance(root, dict):
            return ()
        if root.get("schema_version") != LIVE_SCHEMA_VERSION or root.get("study_id") != study_id:
            return ()
        streams = root.get("latest_by_stream")
        if not isinstance(streams, dict):
            return ()
        frames: list[LiveGridFrame] = []
        for stream_id, value in streams.items():
            try:
                event = dict(value)
                if event.get("event_type") != "gridworld-transition":
                    continue
                grid = dict(event["grid"])
                flags = dict(event.get("disturbance_flags", {}))
                frame = LiveGridFrame(
                    stream_id=str(stream_id),
                    phase=str(event["phase"]),
                    method_id=str(event["method_id"]),
                    root_id=str(event["root_id"]),
                    layout_id=str(event["layout_id"]),
                    branch=None if event.get("branch") is None else str(event["branch"]),
                    episode_index=int(event["episode_index"]),
                    interaction_index=int(event["interaction_index"]),
                    environment_step=int(event["environment_step"]),
                    width=int(grid["width"]),
                    height=int(grid["height"]),
                    start=self._coordinate(grid["start"], field="grid.start"),
                    goal=self._coordinate(grid["goal"], field="grid.goal"),
                    obstacles=tuple(
                        self._coordinate(item, field="grid.obstacles")
                        for item in grid.get("obstacles", [])
                    ),
                    true_state=self._coordinate(event["true_state"], field="true_state"),
                    delivered_observation=self._coordinate(
                        event["delivered_observation"], field="delivered_observation"
                    ),
                    intended_action=str(event["intended_action"]),
                    executed_action=str(event["executed_action"]),
                    reward=float(event["reward"]),
                    terminated=bool(event["terminated"]),
                    truncated=bool(event["truncated"]),
                    regime_id=None if event.get("regime_id") is None else str(event["regime_id"]),
                    disturbance_flags={str(k): bool(v) for k, v in flags.items()},
                    change_event_ids=tuple(str(item) for item in event.get("change_event_ids", [])),
                    presentation_sequence=int(event.get("presentation_sequence", 0)),
                )
                if frame.width <= 0 or frame.height <= 0:
                    continue
                frames.append(frame)
            except (KeyError, TypeError, ValueError, RuntimeError):
                continue
        return tuple(sorted(frames, key=lambda item: item.presentation_sequence, reverse=True))

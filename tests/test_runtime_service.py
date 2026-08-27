from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from resilient_agents.contracts import ProtocolStage  # noqa: E402
from resilient_agents.runtime_observer import RuntimeTelemetrySink  # noqa: E402
from resilient_agents.runtime_service import RuntimeService, RuntimeStatus  # noqa: E402
from resilient_agents.v11_protocol import load_v11_candidate_protocol  # noqa: E402

PROTOCOL_PATH = ROOT / "configs" / "protocols" / "protocol-v1.1.json"
PROTOCOL = load_v11_candidate_protocol(PROTOCOL_PATH)
DEV_ROOTS = PROTOCOL.root_seeds_for(ProtocolStage.DEVELOPMENT)


def minimal_request(run_id: str) -> dict[str, object]:
    return {
        "run_id": run_id,
        "stage": "development",
        "layout_id": "dev-l01",
        "condition_id": "nominal",
        "root_seeds": list(DEV_ROOTS),
        "agent_ids": ["f0"],
        "q_learning_rate": 0.5,
        "discount_factor": 0.96875,
        "exploration_epsilon": 0.125,
        "training_episodes_per_layout": 512,
        "pre_change_episodes": 16,
        "post_change_episodes": 32,
        "immediate_window": 1,
        "worst_window": 2,
        "terminal_window": 4,
        "recovery_tolerance": 0.0,
        "recovery_stability_episodes": 2,
        "retention_policy": "events",
        "auto_publish": False,
        "execution_timeout_seconds": None,
        "agent_configuration_ids": {"f0": "f0-base-v1"},
    }


class RuntimeServiceTests(unittest.TestCase):
    def _service(self, root: Path) -> RuntimeService:
        return RuntimeService(root)

    def test_queue_cancel_restart_is_capability_based_and_persistent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            service = self._service(root)
            queued = service.enqueue_v11_candidate(
                protocol_path=PROTOCOL_PATH,
                request=minimal_request("RUNTIME-QUEUE"),
            )
            self.assertEqual(queued.status, RuntimeStatus.QUEUED)
            self.assertTrue(queued.capabilities.can_cancel)
            self.assertFalse(queued.capabilities.can_restart)
            self.assertFalse(queued.capabilities.can_pause)
            self.assertFalse(queued.capabilities.can_resume)

            cancelled = service.cancel("RUNTIME-QUEUE")
            self.assertEqual(cancelled.status, RuntimeStatus.CANCELLED)
            self.assertFalse(cancelled.capabilities.can_cancel)
            self.assertTrue(cancelled.capabilities.can_restart)

            restarted = service.restart("RUNTIME-QUEUE")
            self.assertEqual(restarted.status, RuntimeStatus.QUEUED)
            self.assertEqual(restarted.attempt, 2)
            self.assertIn("telemetry-attempt-2.ndjson", restarted.telemetry_path or "")

            # A new application session must not silently execute an old queue.
            reopened = RuntimeService(root).get_run("RUNTIME-QUEUE")
            self.assertEqual(reopened.status, RuntimeStatus.INTERRUPTED)

    def test_invalid_candidate_request_fails_before_runtime_record_is_created(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            request = minimal_request("RUNTIME-INVALID")
            request["root_seeds"] = list(DEV_ROOTS[:-1])
            with self.assertRaises(ValueError):
                RuntimeService(root).enqueue_v11_candidate(
                    protocol_path=PROTOCOL_PATH,
                    request=request,
                )
            self.assertFalse((root / "results" / "runtime" / "RUNTIME-INVALID").exists())

    def test_start_next_uses_owned_entrypoint_without_shell(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            script = root / "scripts" / "run_v11_candidate_runtime.py"
            script.parent.mkdir(parents=True)
            script.write_text("# test fixture\n", encoding="utf-8")
            service = self._service(root)
            service.enqueue_v11_candidate(
                protocol_path=PROTOCOL_PATH,
                request=minimal_request("RUNTIME-START"),
            )
            process = Mock()
            process.pid = 4321
            process.poll.return_value = None
            with patch(
                "resilient_agents.runtime_service.subprocess.Popen",
                return_value=process,
            ) as popen:
                started = service.start_next()

            self.assertIsNotNone(started)
            assert started is not None
            self.assertEqual(started.status, RuntimeStatus.RUNNING)
            self.assertEqual(started.process_id, 4321)
            args, kwargs = popen.call_args
            command = args[0]
            self.assertIn(str(script), command)
            self.assertIn("--protocol", command)
            self.assertIn("--request", command)
            self.assertIn("--telemetry", command)
            self.assertFalse(kwargs["shell"])
            self.assertEqual(kwargs["cwd"], root.resolve())

    def test_progress_comes_from_runner_state_and_latest_real_telemetry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            service = self._service(root)
            snapshot = service.enqueue_v11_candidate(
                protocol_path=PROTOCOL_PATH,
                request=minimal_request("RUNTIME-PROGRESS"),
            )
            telemetry = Path(snapshot.telemetry_path or "")
            sink = RuntimeTelemetrySink(telemetry)
            sink.emit(
                {
                    "event": "gridworld_step",
                    "run_id": "RUNTIME-PROGRESS",
                    "phase": "post-change",
                    "episode_index": 4,
                    "step": 7,
                }
            )
            run_dir = root / "results" / "runs" / "RUNTIME-PROGRESS"
            run_dir.mkdir(parents=True)
            (run_dir / "runner-state.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "resume_generation": 0,
                        "completed_root_seeds": [DEV_ROOTS[0]],
                        "root_results": [{"root_seed": DEV_ROOTS[0]}],
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            current = service.get_run("RUNTIME-PROGRESS")
            self.assertEqual(current.progress.completed_roots, 1)
            self.assertEqual(current.progress.total_roots, len(DEV_ROOTS))
            self.assertEqual(
                current.progress.fraction_complete,
                1 / len(DEV_ROOTS),
            )
            self.assertEqual(current.progress.latest_phase, "post-change")
            self.assertEqual(current.progress.latest_episode_index, 4)
            self.assertEqual(current.progress.latest_step, 7)
            self.assertEqual(current.latest_telemetry_sequence, 0)
            rows = service.tail_telemetry("RUNTIME-PROGRESS", after_sequence=-1)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["event"], "gridworld_step")

    def test_historical_unfinished_bundle_is_visible_but_not_falsely_restartable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir = root / "results" / "runs" / "OLD-UNFINISHED"
            run_dir.mkdir(parents=True)
            (run_dir / "manifest.json").write_text(
                json.dumps(
                    {
                        "run_id": "OLD-UNFINISHED",
                        "status": "running",
                        "started_at_utc": "2026-01-01T00:00:00+00:00",
                        "finished_at_utc": None,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            item = next(
                snapshot
                for snapshot in RuntimeService(root).list_runs()
                if snapshot.run_id == "OLD-UNFINISHED"
            )
            self.assertEqual(item.status, RuntimeStatus.INTERRUPTED)
            self.assertFalse(item.capabilities.can_cancel)
            self.assertFalse(item.capabilities.can_restart)

    def test_orphaned_runtime_record_reconciles_finalized_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            service = self._service(root)
            service.enqueue_v11_candidate(
                protocol_path=PROTOCOL_PATH,
                request=minimal_request("RUNTIME-FINISHED-WHILE-CLOSED"),
            )
            metadata_path = (
                root
                / "results"
                / "runtime"
                / "RUNTIME-FINISHED-WHILE-CLOSED"
                / "runtime.json"
            )
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            metadata["status"] = "running"
            metadata["process_id"] = 9999
            metadata_path.write_text(
                json.dumps(metadata) + "\n",
                encoding="utf-8",
            )
            run_dir = root / "results" / "runs" / "RUNTIME-FINISHED-WHILE-CLOSED"
            run_dir.mkdir(parents=True)
            (run_dir / "manifest.json").write_text(
                json.dumps(
                    {
                        "run_id": "RUNTIME-FINISHED-WHILE-CLOSED",
                        "status": "completed",
                        "started_at_utc": "2026-01-01T00:00:00+00:00",
                        "finished_at_utc": "2026-01-01T00:01:00+00:00",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            (run_dir / "FINALIZED").write_text(
                "schema_version=1\nstatus=completed\n",
                encoding="utf-8",
            )
            reopened = RuntimeService(root).get_run("RUNTIME-FINISHED-WHILE-CLOSED")
            self.assertEqual(reopened.status, RuntimeStatus.COMPLETED)
            self.assertIsNone(reopened.process_id)

    def test_finalized_historical_status_is_not_rewritten_by_runtime_registry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir = root / "results" / "runs" / "OLD-COMPLETED"
            run_dir.mkdir(parents=True)
            (run_dir / "manifest.json").write_text(
                json.dumps(
                    {
                        "run_id": "OLD-COMPLETED",
                        "status": "completed",
                        "started_at_utc": "2026-01-01T00:00:00+00:00",
                        "finished_at_utc": "2026-01-01T00:01:00+00:00",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            (run_dir / "FINALIZED").write_text(
                "schema_version=1\nstatus=completed\n", encoding="utf-8"
            )
            item = next(
                snapshot
                for snapshot in RuntimeService(root).list_runs()
                if snapshot.run_id == "OLD-COMPLETED"
            )
            self.assertEqual(item.status, RuntimeStatus.COMPLETED)
            self.assertFalse(item.capabilities.can_restart)

    def test_pause_and_resume_are_explicitly_unsupported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            service = RuntimeService(Path(temporary))
            with self.assertRaises(NotImplementedError):
                service.pause("RUN-1")
            with self.assertRaises(NotImplementedError):
                service.resume("RUN-1")


if __name__ == "__main__":
    unittest.main()

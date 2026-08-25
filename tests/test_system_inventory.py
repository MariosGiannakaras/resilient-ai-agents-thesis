from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import system_inventory  # noqa: E402


class SystemInventoryTests(unittest.TestCase):
    def test_parse_nvidia_smi_supports_multiple_devices(self) -> None:
        output = (
            "NVIDIA RTX Example, 12288, 600.12\n"
            "NVIDIA T4, 15360, 600.12\n"
        )

        devices = system_inventory.parse_nvidia_smi(output)

        self.assertEqual(len(devices), 2)
        self.assertEqual(devices[0]["index"], 0)
        self.assertEqual(devices[0]["name"], "NVIDIA RTX Example")
        self.assertEqual(devices[0]["memory_total_mib"], 12288)
        self.assertEqual(devices[1]["memory_total_mib"], 15360)

    def test_parse_nvidia_smi_handles_unparseable_memory_without_failing(self) -> None:
        devices = system_inventory.parse_nvidia_smi(
            "NVIDIA Example, Not Supported, 600.12\n"
        )

        self.assertEqual(len(devices), 1)
        self.assertIsNone(devices[0]["memory_total_mib"])

    def test_repository_state_distinguishes_clean_repository_from_failed_probe(self) -> None:
        with mock.patch.object(
            system_inventory,
            "run_command",
            side_effect=["a" * 40, "", "results/runs/local\0artifacts/table.csv\0"],
        ):
            state = system_inventory.repository_state()

        self.assertEqual(state["commit"], "a" * 40)
        self.assertFalse(state["tracked_changes_present"])
        self.assertFalse(state["untracked_nonoutput_present"])

        with mock.patch.object(
            system_inventory,
            "run_command",
            side_effect=["a" * 40, "", "results/runs/local\0src/local.py\0"],
        ):
            dirty = system_inventory.repository_state()

        self.assertTrue(dirty["untracked_nonoutput_present"])

        with mock.patch.object(
            system_inventory,
            "run_command",
            side_effect=[None, None, None],
        ):
            unavailable = system_inventory.repository_state()

        self.assertIsNone(unavailable["commit"])
        self.assertIsNone(unavailable["tracked_changes_present"])
        self.assertIsNone(unavailable["untracked_nonoutput_present"])

    def test_collect_inventory_has_stable_privacy_minimal_shape(self) -> None:
        disk = mock.Mock(total=1_000_000, free=400_000)
        with (
            mock.patch.object(system_inventory.shutil, "disk_usage", return_value=disk),
            mock.patch.object(
                system_inventory,
                "detect_nvidia_gpus",
                return_value=([{"index": 0, "name": "GPU", "memory_total_mib": 8192, "driver_version": "1"}], True),
            ),
            mock.patch.object(system_inventory, "detect_cpu_model", return_value="CPU"),
            mock.patch.object(
                system_inventory, "detect_windows_physical_cores", return_value=8
            ),
            mock.patch.object(
                system_inventory, "detect_windows_display_adapters", return_value=[]
            ),
            mock.patch.object(system_inventory, "detect_total_memory_bytes", return_value=16_000_000),
            mock.patch.object(
                system_inventory,
                "run_command",
                side_effect=[
                    "git version 2.50.0",
                    "git-lfs/3.7.1",
                    "v24.0.0",
                    None,
                    "uv 0.10.10",
                ],
            ),
            mock.patch.object(
                system_inventory,
                "package_versions",
                return_value={"numpy": "2.0.0"},
            ),
            mock.patch.object(
                system_inventory,
                "repository_state",
                return_value={
                    "commit": "b" * 40,
                    "tracked_changes_present": False,
                    "untracked_nonoutput_present": False,
                },
            ),
        ):
            report = system_inventory.collect_inventory()

        self.assertEqual(report["schema_version"], 2)
        self.assertEqual(report["memory"]["total_bytes"], 16_000_000)
        self.assertEqual(report["storage"]["repository_filesystem_free_bytes"], 400_000)
        self.assertEqual(report["accelerators"]["nvidia"]["devices"][0]["name"], "GPU")
        self.assertEqual(report["repository"]["commit"], "b" * 40)
        self.assertEqual(report["tools"]["uv"], "uv 0.10.10")
        self.assertFalse(report["repository"]["untracked_nonoutput_present"])

        serialized = json.dumps(report).casefold()
        for forbidden in (
            "username",
            "hostname",
            "ip_address",
            "machine_id",
            "environment_variables",
            "home_directory",
        ):
            self.assertNotIn(forbidden, serialized)

    def test_windows_cpu_model_prefers_registry_description(self) -> None:
        with (
            mock.patch.object(system_inventory.platform, "system", return_value="Windows"),
            mock.patch.object(
                system_inventory,
                "detect_windows_cpu_model",
                return_value="Example CPU",
            ),
            mock.patch.object(
                system_inventory.platform,
                "processor",
                return_value="Generic processor identifier",
            ),
        ):
            self.assertEqual(system_inventory.detect_cpu_model(), "Example CPU")

    def test_positive_int_rejects_legacy_sentinel_values(self) -> None:
        self.assertEqual(system_inventory._positive_int(8_589_934_592), 8_589_934_592)
        self.assertIsNone(system_inventory._positive_int(0))
        self.assertIsNone(system_inventory._positive_int("8589934592"))

    def test_write_report_writes_valid_json_atomically(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "nested" / "inventory.json"
            report = {"schema_version": 1, "system": {"os": "Example"}}

            system_inventory.write_report(report, output)

            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), report)
            self.assertNotIn(b"\r\n", output.read_bytes())
            self.assertFalse(output.with_name(output.name + ".tmp").exists())


if __name__ == "__main__":
    unittest.main()

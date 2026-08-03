#!/usr/bin/env python3
"""Collect a reproducible, privacy-minimal capability snapshot of the target system.

The collector intentionally avoids usernames, hostnames, network identifiers,
environment dumps, and machine IDs. It uses only the Python standard library and
best-effort external version probes. A missing probe is reported as unavailable;
it is never interpreted as proof that the hardware does not exist.
"""
from __future__ import annotations

import argparse
import csv
import ctypes
import importlib.metadata
import io
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

SCHEMA_VERSION = 1
ROOT = Path(__file__).resolve().parents[1]
PACKAGE_PROBES = ("numpy", "scipy", "pandas", "torch", "gymnasium", "minigrid")


def run_command(command: Sequence[str], timeout: int = 5) -> Optional[str]:
    """Run a short read-only command when its executable is available."""
    executable = shutil.which(command[0])
    if executable is None:
        return None
    try:
        result = subprocess.run(
            [executable, *command[1:]],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or result.stderr.strip()


def detect_cpu_model() -> Optional[str]:
    value = platform.processor().strip()
    if value:
        return value

    system = platform.system()
    if system == "Linux":
        try:
            for line in Path("/proc/cpuinfo").read_text(
                encoding="utf-8", errors="replace"
            ).splitlines():
                key, separator, raw = line.partition(":")
                if separator and key.strip().casefold() in {"model name", "hardware"}:
                    model = raw.strip()
                    if model:
                        return model
        except OSError:
            return None
    elif system == "Darwin":
        output = run_command(["sysctl", "-n", "machdep.cpu.brand_string"])
        if output:
            return output.splitlines()[0].strip() or None
    elif system == "Windows":
        output = run_command(["wmic", "cpu", "get", "name", "/value"])
        if output:
            for line in output.splitlines():
                if line.startswith("Name="):
                    return line.partition("=")[2].strip() or None
    return None


def detect_total_memory_bytes() -> Optional[int]:
    if platform.system() == "Windows":
        class MemoryStatusEx(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        status = MemoryStatusEx()
        status.dwLength = ctypes.sizeof(MemoryStatusEx)
        try:
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
                return int(status.ullTotalPhys)
        except (AttributeError, OSError):
            return None
        return None

    try:
        page_size = int(os.sysconf("SC_PAGE_SIZE"))
        page_count = int(os.sysconf("SC_PHYS_PAGES"))
    except (AttributeError, OSError, ValueError):
        return None
    total = page_size * page_count
    return total if total > 0 else None


def parse_nvidia_smi(output: Optional[str]) -> List[Dict[str, object]]:
    if not output:
        return []
    devices: List[Dict[str, object]] = []
    reader = csv.reader(io.StringIO(output))
    for index, row in enumerate(reader):
        if len(row) != 3:
            continue
        name, memory_mib, driver = (item.strip() for item in row)
        try:
            memory_value: Optional[int] = int(memory_mib)
        except ValueError:
            memory_value = None
        devices.append(
            {
                "index": index,
                "name": name or None,
                "memory_total_mib": memory_value,
                "driver_version": driver or None,
            }
        )
    return devices


def detect_nvidia_gpus() -> Tuple[List[Dict[str, object]], bool]:
    executable_present = shutil.which("nvidia-smi") is not None
    output = run_command(
        [
            "nvidia-smi",
            "--query-gpu=name,memory.total,driver_version",
            "--format=csv,noheader,nounits",
        ]
    )
    return parse_nvidia_smi(output), executable_present


def package_versions(names: Iterable[str] = PACKAGE_PROBES) -> Dict[str, Optional[str]]:
    versions: Dict[str, Optional[str]] = {}
    for name in names:
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = None
    return versions


def repository_state() -> Dict[str, object]:
    commit = run_command(["git", "-C", str(ROOT), "rev-parse", "HEAD"])
    status = run_command(
        ["git", "-C", str(ROOT), "status", "--porcelain", "--untracked-files=no"]
    )
    return {
        "commit": commit.splitlines()[0] if commit else None,
        "tracked_changes_present": bool(status) if status is not None else None,
    }


def collect_inventory() -> Dict[str, object]:
    disk = shutil.disk_usage(ROOT)
    nvidia_devices, nvidia_smi_present = detect_nvidia_gpus()
    git_version = run_command(["git", "--version"])
    node_version = run_command(["node", "--version"])
    nvcc_output = run_command(["nvcc", "--version"])

    return {
        "schema_version": SCHEMA_VERSION,
        "collected_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "privacy_policy": "no-user-host-network-or-machine-identifiers",
        "system": {
            "os": platform.system() or None,
            "os_release": platform.release() or None,
            "architecture": platform.machine() or None,
            "python_implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
        },
        "cpu": {
            "logical_processors": os.cpu_count(),
            "model": detect_cpu_model(),
        },
        "memory": {"total_bytes": detect_total_memory_bytes()},
        "storage": {
            "repository_filesystem_total_bytes": int(disk.total),
            "repository_filesystem_free_bytes": int(disk.free),
        },
        "accelerators": {
            "nvidia": {
                "probe": "nvidia-smi",
                "probe_executable_present": nvidia_smi_present,
                "devices": nvidia_devices,
            },
            "other_gpu_families": {
                "status": "not-enumerated-by-schema-v1",
                "note": "Absence from this report is not proof that no non-NVIDIA GPU exists.",
            },
        },
        "tools": {
            "git": git_version.splitlines()[0] if git_version else None,
            "node": node_version.splitlines()[0] if node_version else None,
            "nvcc": nvcc_output.splitlines()[-1] if nvcc_output else None,
        },
        "python_packages": package_versions(),
        "repository": repository_state(),
    }


def write_report(report: Dict[str, object], output: Optional[Path]) -> None:
    payload = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if output is None:
        sys.stdout.write(payload)
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + ".tmp")
    temporary.write_text(payload, encoding="utf-8")
    temporary.replace(output)
    print(f"Wrote system capability inventory: {output}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Collect a privacy-minimal hardware/software capability snapshot."
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write JSON atomically to this path instead of stdout.",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    write_report(collect_inventory(), args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

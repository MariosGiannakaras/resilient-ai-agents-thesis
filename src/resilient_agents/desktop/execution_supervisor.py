"""Qt subprocess supervisor for truthful DEVELOPMENT Study execution."""
from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QObject, QProcess, Signal


class DesktopExecutionSupervisor(QObject):
    """Own at most one local Study worker without blocking the Qt event loop."""

    started = Signal(str)
    output = Signal(str, str)
    finished = Signal(str, int, str)

    def __init__(
        self,
        *,
        repo_root: Path,
        writable_root: Path,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self.repo_root = Path(repo_root).resolve()
        self.writable_root = Path(writable_root).resolve()
        self._process: QProcess | None = None
        self._study_id: str | None = None
        self._buffer = ""
        self._completion_emitted = False

    @property
    def busy(self) -> bool:
        return (
            self._process is not None
            and self._process.state() != QProcess.ProcessState.NotRunning
        )

    @property
    def active_study_id(self) -> str | None:
        return self._study_id if self.busy else None

    def start_or_resume(self, study_id: str) -> None:
        self._launch(study_id, retry_infrastructure=False)

    def retry_and_resume(self, study_id: str) -> None:
        self._launch(study_id, retry_infrastructure=True)

    def _launch(self, study_id: str, *, retry_infrastructure: bool) -> None:
        if self.busy:
            raise RuntimeError(
                f"another Study worker is already active: {self.active_study_id}"
            )
        if not isinstance(study_id, str) or not study_id.strip():
            raise ValueError("study_id must be non-empty")

        process = QProcess(self)
        process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        process.setWorkingDirectory(str(self.repo_root))
        process.setProgram(sys.executable)
        arguments = [
            "-m",
            "resilient_agents.desktop.study_worker",
            "--repo-root",
            str(self.repo_root),
            "--writable-root",
            str(self.writable_root),
            "--study-id",
            study_id,
        ]
        if retry_infrastructure:
            arguments.append("--retry-infrastructure")
        process.setArguments(arguments)

        self._process = process
        self._study_id = study_id
        self._buffer = ""
        self._completion_emitted = False
        process.started.connect(self._on_started)
        process.readyReadStandardOutput.connect(self._read_output)
        process.finished.connect(self._on_finished)
        process.errorOccurred.connect(self._on_error)
        process.start()

    def _on_started(self) -> None:
        if self._study_id is not None:
            self.started.emit(self._study_id)

    def _read_output(self) -> None:
        process = self._process
        study_id = self._study_id
        if process is None or study_id is None:
            return
        chunk = bytes(process.readAllStandardOutput()).decode("utf-8", errors="replace")
        if not chunk:
            return
        self._buffer += chunk
        if len(self._buffer) > 12000:
            self._buffer = self._buffer[-12000:]
        self.output.emit(study_id, chunk)

    def _on_finished(
        self,
        exit_code: int,
        _exit_status: QProcess.ExitStatus,
    ) -> None:
        self._read_output()
        self._emit_finished(int(exit_code))

    def _on_error(self, error: QProcess.ProcessError) -> None:
        if error != QProcess.ProcessError.FailedToStart:
            return
        process = self._process
        detail = process.errorString() if process is not None else "worker failed to start"
        if detail:
            self._buffer = (self._buffer + "\n" + detail).strip()
        self._emit_finished(-1)

    def _emit_finished(self, exit_code: int) -> None:
        if self._completion_emitted:
            return
        self._completion_emitted = True
        study_id = self._study_id or ""
        output = self._buffer.strip()
        self.finished.emit(study_id, exit_code, output)

        process = self._process
        self._process = None
        self._study_id = None
        if process is not None:
            process.deleteLater()

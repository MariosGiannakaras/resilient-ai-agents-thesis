# Application-only requirements

The root `pyproject.toml` and `uv.lock` are historical scientific-authority inputs and are intentionally not modified by T-528 UI work.

`application-ui.txt` is a presentation/runtime overlay for the PySide6 desktop application. CI restores the historical locked project environment first, then installs this exact-pinned overlay into that environment without updating the root lock.

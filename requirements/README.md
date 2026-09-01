# Application-only requirements

The root `pyproject.toml` and `uv.lock` remain the locked scientific/runtime authority and are not rewritten by desktop presentation work.

`application-ui.txt` is the exact-pinned presentation/runtime overlay for the accepted PySide6 desktop application. CI restores the locked project environment first, then installs this overlay without updating the root lock.

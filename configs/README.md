# Configurations

Version-controlled, validated configurations. Every run stores a copy of its resolved configuration.

- `protocols/pilot-v0.1.json` is the machine-readable pre-final pilot authority. Load it through `resilient_agents.load_pilot_protocol`; missing, unknown, overlapping, privileged, or scientifically inconsistent required state fails closed.
- Its rationale and lifecycle are documented in `docs/experiments/PILOT_PROTOCOL_V0_1.md`.

import sys

with open('src/resilient_agents/pilot_protocol.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(
    'if payload["status"] != "pilot-unfrozen":\n        raise ValueError("pilot protocol status must be pilot-unfrozen")',
    'if payload["status"] not in ("pilot-unfrozen", "frozen"):\n        raise ValueError("pilot protocol status must be pilot-unfrozen or frozen")'
)

code = code.replace(
    'analysis = _object(payload["pilot_analysis"], field="pilot_analysis")',
    'analysis_key = "pilot_analysis" if "pilot_analysis" in payload else "statistical_analysis_plan"\n    analysis = _object(payload[analysis_key], field=analysis_key)'
)

code = code.replace(
    'field="pilot_analysis",',
    'field=analysis_key,'
)

code = code.replace(
    'field=f"pilot_analysis.{field}"',
    'field=f"{analysis_key}.{field}"'
)

code = code.replace(
    'if analysis["inferential_claims_allowed"] is not False:\n        raise ValueError("pilot analysis cannot authorize inferential claims")',
    'if analysis_key == "pilot_analysis" and analysis["inferential_claims_allowed"] is not False:\n        raise ValueError("pilot analysis cannot authorize inferential claims")'
)

code = code.replace(
    '"failed_or_invalid_handling",\n        },',
    '"failed_or_invalid_handling",\n        } | ({"estimands"} if analysis_key == "statistical_analysis_plan" else set()),'
)

with open('src/resilient_agents/pilot_protocol.py', 'w', encoding='utf-8') as f:
    f.write(code)

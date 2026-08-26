import sys

with open('src/resilient_agents/pilot_protocol.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix scientific scope
scope_validation_old = """    _exact_keys(
        scope,
        {"primary_question", "pilot_purpose", "final_evidence_use"},
        field="scientific_scope",
    )
    _nonempty_string(scope["primary_question"], field="primary_question")
    _nonempty_string(scope["pilot_purpose"], field="pilot_purpose")
    if scope["final_evidence_use"] is not False:
        raise ValueError("pilot protocol cannot authorize final evidence use")"""

scope_validation_new = """    expected_scope_keys = {"primary_question", "final_evidence_use"}
    if "pilot_purpose" in scope:
        expected_scope_keys.add("pilot_purpose")
    _exact_keys(
        scope,
        expected_scope_keys,
        field="scientific_scope",
    )
    _nonempty_string(scope["primary_question"], field="primary_question")
    if "pilot_purpose" in scope:
        _nonempty_string(scope["pilot_purpose"], field="pilot_purpose")
    if payload["status"] == "pilot-unfrozen" and scope["final_evidence_use"] is not False:
        raise ValueError("pilot protocol cannot authorize final evidence use")
    if payload["status"] == "frozen" and scope["final_evidence_use"] is not True:
        raise ValueError("frozen protocol must authorize final evidence use")"""

code = code.replace(scope_validation_old, scope_validation_new)

with open('src/resilient_agents/pilot_protocol.py', 'w', encoding='utf-8') as f:
    f.write(code)

import sys

with open('src/resilient_agents/pilot_protocol.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(
    'if tuning["robust_set_policy"] != "fixed-declared-set-no-pilot-outcome-tuning":',
    'if "robust_set_policy" in tuning and tuning["robust_set_policy"] != "fixed-declared-set-no-pilot-outcome-tuning":'
)

with open('src/resilient_agents/pilot_protocol.py', 'w', encoding='utf-8') as f:
    f.write(code)

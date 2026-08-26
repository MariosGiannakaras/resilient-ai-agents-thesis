import sys

with open('src/resilient_agents/pilot_protocol.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(
    'if timeout["overflow_action"] != "protocol-amendment-before-pilot":',
    'if timeout["overflow_action"] not in ("protocol-amendment-before-pilot", "protocol-amendment-before-final"):'
)

with open('src/resilient_agents/pilot_protocol.py', 'w', encoding='utf-8') as f:
    f.write(code)

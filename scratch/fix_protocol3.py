import sys

with open('src/resilient_agents/pilot_protocol.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Make partitions pilot stage optional or empty
code = code.replace(
    'stage: _unique_strings(partition_payload[stage], field=f"partitions.{stage}")\n        for stage in _STAGES',
    'stage: tuple(_nonempty_string(x, field=f"partitions.{stage}") for x in partition_payload.get(stage, []))\n        for stage in _STAGES'
)

code = code.replace(
    'if len(layout_ids) != sum(len(ids) for ids in partition_values.values()):',
    'if len(layout_ids) != sum(len(ids) for ids in partition_values.values()) or len(layout_ids) != len(set(layout_ids)):\n        raise ValueError("protocol layouts must exactly match partition definitions and be unique")\n    if False:'
)

with open('src/resilient_agents/pilot_protocol.py', 'w', encoding='utf-8') as f:
    f.write(code)

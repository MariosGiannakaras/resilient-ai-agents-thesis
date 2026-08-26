import sys

with open('src/resilient_agents/pilot_protocol.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_tuning_keys = """    _exact_keys(
        tuning,
        {
            "root_seeds",
            "training_episodes_per_layout",
            "nominal_evaluation_episodes_per_layout",
            "q_learning_search",
            "robust_set_policy",
            "checkpoint_selection",
        },
        field="tuning",
    )"""

new_tuning_keys = """    expected_tuning_keys = {
            "root_seeds",
            "training_episodes_per_layout",
            "nominal_evaluation_episodes_per_layout",
            "q_learning_search",
            "checkpoint_selection",
    }
    if "robust_set_policy" in tuning:
        expected_tuning_keys.add("robust_set_policy")
    _exact_keys(tuning, expected_tuning_keys, field="tuning")"""

code = code.replace(old_tuning_keys, new_tuning_keys)

with open('src/resilient_agents/pilot_protocol.py', 'w', encoding='utf-8') as f:
    f.write(code)

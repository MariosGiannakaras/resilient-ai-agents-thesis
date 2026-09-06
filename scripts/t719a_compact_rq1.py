from __future__ import annotations

import t719a_targeted_final_pass as build

# Keep the requested examiner-facing interpretation while minimizing pagination pressure.
# The content remains a semantic clarification only: no result, protocol value, estimand,
# threshold, horizon, seed, layout, root, budget, or registered asset changes.
build.RQ1_EXPLANATION = (
    "Με βέλτιστη διαδρομή 12 ενεργειών, το −0,100 είναι η απόδοση μιας shortest-path "
    "επίλυσης του task: 11×(−0,1)+1,0=−0,1, αφού το goal reward +1,0 αντικαθιστά το "
    "final step reward."
)

if __name__ == "__main__":
    build.main()

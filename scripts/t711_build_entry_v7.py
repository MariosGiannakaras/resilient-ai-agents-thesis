#!/usr/bin/env python3
"""T-711 inherited-QA cache alignment.

v6 produces the complete 24-figure document, but the v3 QA function retains a module-
local reference to its earlier 11-figure cache helper. Align that inherited QA lookup
with the v5 canonical 24-figure cache. No document content or scientific data changes.
"""

import t711_build_entry_v6 as v6


# v3._enhanced_qa resolves this helper in the v3 module namespace, not through the
# v1/t711 module patched by v5. Point both namespaces at the same canonical cache.
v6.v5.v4.v3._mentioned_figure_cache_lines = v6.v5._figure_cache_lines
v6.v5.t711._mentioned_figure_cache_lines = v6.v5._figure_cache_lines


if __name__ == "__main__":
    v6.t711.builder.main()

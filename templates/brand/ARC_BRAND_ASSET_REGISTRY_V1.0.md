# ARC BRAND ASSET REGISTRY V1.0
DATE: 2026-09-18
STATUS: ACTIVE-DEV

Canonical full-cover lockups are immutable Drive assets.

| Product | File | Drive ID | Pixels | SHA-256 |
|---|---|---|---:|---|
| ARC CORE | ARC_CORE_LOCKUP_MASTER.png | 1J2ojEjyXKCJlRs21SW6gAekaCZvEJ4vE | 555×380 | a5c4e373e506060a47c5232571151696aad97b6747d2063bb4d87a1a8a12611b |
| ARC N° | ARC_N_LOCKUP_MASTER.png | 12389-txbX5JzYuyj1cjbw7MUO7--f9JE | 565×380 | a61269f152a79343b91f37e75f987f0b5a82d53dc7d9d3a4d067c9830df3bde4 |
| ARC FINAL | ARC_FINAL_LOCKUP_MASTER.png | 1q9WyXajXA6V13yOYhnPqBBdLkEUwcbcB | 580×380 | e1a5e62f125592f258dfc3fd7224155da5a6c9ef4f92dc164994dd1dcc832b9e |

Hard rules:
- use exact asset by Drive ID
- verify SHA-256 before final release
- preserve aspect ratio
- no crop into mark
- no redraw/retype/trace/vector reconstruction/recolor/generative recreation
- no substitute if inaccessible

Release gates:
BRAND_ASSET_ID_MATCH=PASS
BRAND_HASH_MATCH=PASS
ASPECT_RATIO_PRESERVED=PASS
NO_SYNTHETIC_LOGO=PASS

Failure codes:
BRAND_ASSET_MISSING
BRAND_HASH_MISMATCH

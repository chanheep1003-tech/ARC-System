# ARC BRAND ASSET REGISTRY V1.0
DATE: 2026-09-18
STATUS: ACTIVE-DEV

Canonical full-cover lockups are immutable Drive assets.

| Product | File | Drive ID | Pixels | SHA-256 |
|---|---|---|---:|---|
| ARC CORE | ARC_CORE_LOCKUP_MASTER.png | 1J2ojEjyXKCJlRs21SW6gAekaCZvEJ4vE | 555×380 | a5c4e373e506060a47c5232571151696aad97b6747d2063bb4d87a1a8a12611b |
| ARC N° | ARC_N_LOCKUP_MASTER.png | 12389-txbX5JzYuyj1cjbw7MUO7--f9JE | 565×380 | a61269f152a79343b91f37e75f987f0b5a82d53dc7d9d3a4d067c9830df3bde4 |
| ARC N° (B/W, ARC_N cover) | ARC_N_LOCKUP_MASTER_BW.png | PENDING_DRIVE_UPLOAD (repo copy registered) | 565×380 | ca124dc9d1c2b4f03fbb7080cf29c8ad3adee75030eacd9b4b4862d5f840ad8d |
| ARC FINAL | ARC_FINAL_LOCKUP_MASTER.png | 1q9WyXajXA6V13yOYhnPqBBdLkEUwcbcB | 580×380 | e1a5e62f125592f258dfc3fd7224155da5a6c9ef4f92dc164994dd1dcc832b9e |

Repository copies (byte-identical, fetched from the Drive ID above and hash-checked on 2026-09-25) so the
production pipeline and CI can render and verify covers offline:
- ARC FINAL: templates/brand/assets/ARC_FINAL_LOCKUP_MASTER.png (SHA-256 e1a5e62f…832b9e)
- ARC N° color: templates/brand/assets/ARC_N_LOCKUP_MASTER.png (fetched by Drive ID 2026-11-08, SHA-256 a61269f1…bde4 verified; source of the B/W derivative)
- ARC N° B/W: templates/brand/assets/ARC_N_LOCKUP_MASTER_BW.png (SHA-256 ca124dc9…ad8d)

## ARC N° B/W derivative (user-directed, 2026-11-08)
The "no recolor" rule is excepted once, by explicit user instruction ("로고 만들어주고"), for the ARC_N B/W cover only.
Method (deterministic, no redraw/trace/regeneration): source = ARC_N_LOCKUP_MASTER.png (hash-verified);
gray = clamp((0.299R+0.587G+0.114B − 70)/(255−70))×255, alpha channel untouched, geometry/pixel grid unchanged.
Navy and burgundy both map to black, white to white; anti-aliased edges are kept (edge ink ≈1.7% larger than the color master because of the contrast stretch).
Pending: upload this exact file to Drive, then replace PENDING_DRIVE_UPLOAD with its Drive ID. Until then the registry's Drive-ID rule is met only by the repo copy.
The B/W file is used only on the ARC_N cover; CORE/FINAL covers keep their own masters.

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

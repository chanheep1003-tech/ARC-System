'use strict';
// ARC Academic B-type styles (derived from templates/n/ARC_N_master_v0.2.html).
module.exports = `
:root{--navy:#1F2A44;--warm:#E9E7E1;--burg:#7A2E35;--ink:#17191d;--muted:#666c74;--rule:#d9dbde}
*{box-sizing:border-box}
@page{size:A4}
html,body{margin:0;padding:0;background:#fff;color:var(--ink);font-family:"Pretendard","Noto Sans KR","Noto Sans",sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.en{font-family:Inter,"Pretendard",Arial,sans-serif}
/* cover / toc pages (fixed A4 pages, zero margin render) */
.page{width:210mm;height:297mm;position:relative;background:#fff;page-break-after:always;overflow:hidden}
.page:last-child{page-break-after:auto}
.cover{padding:24mm 20mm 18mm}
.kicker{font-family:Inter,Arial,sans-serif;font-size:10.5pt;font-weight:700;letter-spacing:.11em;color:var(--navy)}
.toprule{height:.7pt;background:var(--navy);margin-top:7mm}
.accent{position:absolute;left:20mm;top:82mm;width:12mm;height:1.2mm;background:var(--burg)}
.covermain{margin-top:53mm}
.covermain h1{margin:0;font-size:30pt;line-height:1.15;letter-spacing:-.045em;font-weight:700}
.covermain .csub{margin-top:5mm;font-size:12.5pt;color:var(--navy);font-weight:500;letter-spacing:-.02em}
.covermeta{margin-top:12mm;font-size:10pt;line-height:1.85;color:#3d4248}
.year{position:absolute;left:20mm;bottom:24mm;font-family:Inter;font-size:10pt;color:var(--muted);letter-spacing:.08em}
.series{position:absolute;right:20mm;bottom:24mm;font-family:Inter;font-size:8pt;color:var(--navy);font-weight:700;letter-spacing:.05em}
.tocpage{padding:24mm 20mm 18mm}
.toctitle{font-size:14pt;font-weight:700;color:var(--navy);letter-spacing:-.02em;border-bottom:.7pt solid var(--navy);padding-bottom:4mm;margin-bottom:6mm}
.toc{width:100%;border-collapse:collapse;font-size:9.6pt}
.toc td{padding:3.1mm 1.5mm;border-bottom:.4pt solid var(--rule);vertical-align:baseline}
.toc td.no{font-family:Inter;font-weight:700;color:var(--navy);width:16mm}
.toc td.rng{font-family:Inter;color:var(--muted);text-align:right;width:30mm;font-size:8.6pt}
.toc td.gen{color:var(--muted);width:38mm;font-size:8.6pt;white-space:nowrap}
.tocnote{margin-top:8mm;font-size:8.4pt;color:var(--muted);line-height:1.7}
/* body: two-column flow (native fragmentation, page margins set by PDF options) */
.sec{column-count:2;column-gap:8.4mm;column-rule:.35pt solid #dcdee1;column-fill:auto;font-size:8.55pt}
.band{column-span:all;border-top:.7pt solid var(--navy);border-bottom:.45pt solid var(--rule);padding:2.6mm 0 2.8mm;margin-bottom:5mm;font-size:9pt;font-weight:700;color:var(--navy);break-after:avoid}
.band .rng{font-family:Inter;letter-spacing:.02em;margin-right:2mm}
.band .sm{font-weight:500;color:var(--muted);font-size:8.2pt;margin-left:2mm}
.passage{margin-bottom:6mm}
.ptitle{font-size:8.9pt;font-weight:700;color:var(--ink);margin-bottom:1mm;break-after:avoid;line-height:1.5}
.psrc{font-size:6.9pt;color:#7b8086;margin-bottom:3mm;break-after:avoid}
.pbody{font-size:8.55pt;line-height:1.66;letter-spacing:-.018em;color:#23272c}
.pbody p{margin:0 0 2.1mm;text-align:justify;text-justify:inter-character;word-break:keep-all;orphans:2;widows:2}
.pbody p.verse{padding-left:3mm;margin:1.2mm 0 2.6mm;break-inside:avoid}
.pbody .stanza{margin-bottom:2.6mm;break-inside:avoid}
.pbody .pl{padding-left:3.2mm;text-indent:-3.2mm;word-break:keep-all;line-height:1.72}
.kind-poem .pbody{font-size:8.7pt}
.kind-poem .stanza{padding:0 0 0 0}
.plabel{font-family:"Pretendard";font-weight:700;color:var(--navy);margin:3mm 0 1.4mm;break-after:avoid}
.summary{border:.5pt solid #cfd2d6;background:#f6f5f2;padding:2.4mm 2.8mm;margin:0 0 3mm;font-size:8.1pt;line-height:1.62;text-align:justify;word-break:keep-all}
.summary b{color:var(--navy)}
.sub{font-size:8.6pt;font-weight:700;color:var(--navy);margin:3mm 0 1.6mm;padding-bottom:.8mm;border-bottom:.4pt solid var(--rule);break-after:avoid}
.sub2{font-size:8.4pt;font-weight:700;color:var(--burg);margin:2.6mm 0 1.4mm;break-after:avoid}
.bl{margin:0 0 2.4mm;padding:0;list-style:none}
.bl li{position:relative;padding-left:3mm;margin-bottom:1.3mm;text-align:justify;word-break:keep-all;line-height:1.6}
.bl li:before{content:"";position:absolute;left:.3mm;top:2.05mm;width:1mm;height:1mm;background:var(--navy)}
.nl{margin:0 0 2.4mm}
.nl div{display:grid;grid-template-columns:4.2mm 1fr;margin-bottom:1.2mm;word-break:keep-all}
.nl .n{font-family:Inter;font-weight:600;color:var(--navy)}
.anno{font-size:7.4pt;color:#6a7178;letter-spacing:-.01em;display:inline-block;margin-top:.6mm}
.pnotes,.pextra{margin-top:3mm;border-top:.4pt solid var(--rule);padding-top:2mm;font-size:7.5pt;line-height:1.58;color:#4a5057;break-inside:auto}
.pnotes .pn{padding-left:2.6mm;text-indent:-2.6mm;margin-bottom:.6mm;word-break:keep-all}
.pnotes .pn:before{content:"· "}
.pnh{font-weight:700;color:var(--navy);margin-bottom:1mm;font-size:7.7pt;break-after:avoid}
.pextra{border:.5pt solid #cfd2d6;padding:2.4mm 2.8mm;margin-top:4mm;background:#fafaf8}
.pextra p{margin:0;text-align:justify;word-break:keep-all;font-size:8.1pt;line-height:1.62}
/* questions */
.q{break-inside:avoid;page-break-inside:avoid;margin:0 0 7.2mm}
.qnum{font-family:Inter;font-size:9.3pt;font-weight:700;color:var(--navy);margin-bottom:2.2mm;break-after:avoid}
.stem{font-size:8.95pt;line-height:1.58;font-weight:500;letter-spacing:-.018em;margin-bottom:3mm;word-break:keep-all;break-after:avoid}
.box{border:.5pt solid #cfd2d6;padding:3mm 3.4mm 3.2mm;margin:2.4mm 0 3.2mm;break-inside:avoid}
.boxlabel{text-align:center;font-size:8pt;font-weight:600;color:var(--navy);margin-bottom:1.8mm}
.bl2{font-size:8.3pt;line-height:1.62;letter-spacing:-.018em;color:#2d3136;padding-left:3.2mm;text-indent:-3.2mm;word-break:keep-all;text-align:justify;margin-bottom:.7mm}
.box .bl2:only-child{padding-left:0;text-indent:0}
.choices{font-size:8.55pt;line-height:1.62;margin-top:2.6mm}
.choice{display:grid;grid-template-columns:4.7mm 1fr;gap:.6mm;margin-bottom:1.5mm;word-break:keep-all;letter-spacing:-.018em}
.choice .cn{font-family:"Pretendard","Noto Sans KR"}
/* answer booklet */
.atable{width:100%;border-collapse:collapse;margin:0 0 6mm;font-size:8.6pt;break-inside:avoid}
.atable th,.atable td{border:.45pt solid #d6d8db;padding:1.9mm 1mm;text-align:center}
.atable th{background:#f6f5f2;font-weight:600;font-family:Inter}
.atable td.k{font-family:Inter;font-weight:700;color:var(--navy);background:#fbfaf7}
.atable td.a{font-family:"Pretendard";font-weight:700;color:var(--burg)}
.atable caption{text-align:left;font-weight:700;color:var(--navy);font-size:8.8pt;margin-bottom:1.6mm;caption-side:top}
.ex{break-inside:avoid;margin:0 0 5.2mm;font-size:8.1pt;line-height:1.58}
.exh{font-size:8.8pt;font-weight:700;color:var(--navy);margin-bottom:1.2mm}
.exh .ans{color:var(--burg);margin-left:1.5mm}
.exh .meta{font-weight:500;color:var(--muted);font-size:7.2pt;margin-left:2mm}
.exl{display:grid;grid-template-columns:4.7mm 1fr;margin-bottom:.9mm;word-break:keep-all;letter-spacing:-.015em}
.exl.c .t{font-weight:600}
.exl .cn{color:var(--muted)}
.exl.c .cn{color:var(--burg);font-weight:700}
`;

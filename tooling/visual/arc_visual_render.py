#!/usr/bin/env python3
import argparse
import hashlib
import html
import json
from pathlib import Path

import matplotlib.pyplot as plt
import yaml

def load_spec(path):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    return json.loads(text)

def spec_hash(spec):
    raw = json.dumps(spec, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def save_manifest(out_path, manifest):
    Path(out_path).write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

def render_graph(spec, out):
    data = spec["data"]
    fig, ax = plt.subplots(figsize=tuple(spec.get("figsize", [5.2, 3.2])))
    series_manifest = []
    for s in data["series"]:
        x = list(s["x"])
        y = list(s["y"])
        if len(x) != len(y):
            raise ValueError("x/y length mismatch")
        ax.plot(x, y, marker="o", label=s.get("label") or None)
        series_manifest.append({"label": s.get("label"), "x": x, "y": y})
    ax.set_xlabel(spec["axes"]["x_label"])
    ax.set_ylabel(spec["axes"]["y_label"])
    if spec["axes"].get("title"):
        ax.set_title(spec["axes"]["title"])
    if any(s.get("label") for s in data["series"]):
        ax.legend()
    ax.grid(False)
    fig.tight_layout()
    fig.savefig(out, format="svg")
    plt.close(fig)
    return {
        "semantic": {
            "series": series_manifest,
            "x_label": spec["axes"]["x_label"],
            "y_label": spec["axes"]["y_label"],
            "x_unit": spec["axes"].get("x_unit"),
            "y_unit": spec["axes"].get("y_unit"),
        }
    }

def svg_header(w,h):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'

def render_particle(spec, out):
    panels = spec.get("panels", [])
    if not panels:
        raise ValueError("SCI-PARTICLE requires panels")
    w = int(spec.get("width", 760))
    h = int(spec.get("height", 300))
    gap = 20
    pw = (w - gap*(len(panels)+1)) / len(panels)
    body = [svg_header(w,h), '<rect x="0" y="0" width="100%" height="100%" fill="white"/>']
    counts = {}
    for pi,panel in enumerate(panels):
        x0 = gap + pi*(pw+gap)
        body.append(f'<rect x="{x0}" y="45" width="{pw}" height="{h-70}" fill="none" stroke="black"/>')
        body.append(f'<text x="{x0+pw/2}" y="28" text-anchor="middle" font-size="16">{html.escape(str(panel.get("label","")))}</text>')
        cursor = 0
        counts[panel.get("id", str(pi))] = {}
        for sp in panel.get("species", []):
            sid = str(sp["id"])
            count = int(sp["count"])
            counts[panel.get("id", str(pi))][sid] = count
            for k in range(count):
                col = cursor % 8
                row = cursor // 8
                cx = x0 + 28 + col*32
                cy = 70 + row*32
                body.append(
                    f'<circle cx="{cx}" cy="{cy}" r="10" fill="white" stroke="black" '
                    f'data-species="{html.escape(sid)}" data-panel="{html.escape(str(panel.get("id",pi)))}" data-index="{k}"/>'
                )
                body.append(f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-size="8">{html.escape(str(sp.get("label",sid)))}</text>')
                cursor += 1
    body.append("</svg>")
    Path(out).write_text("\n".join(body), encoding="utf-8")
    return {"semantic": {"panel_species_counts": counts}}

def node_layout(nodes, width, y=70):
    n=max(1,len(nodes))
    step=width/(n+1)
    return {str(node["id"]):(step*(i+1),y) for i,node in enumerate(nodes)}

def render_flow(spec, out):
    nodes=spec["nodes"]
    edges=spec["edges"]
    w=int(spec.get("width",800)); h=int(spec.get("height",260))
    pos=node_layout(nodes,w,y=90)
    body=[svg_header(w,h),'<rect x="0" y="0" width="100%" height="100%" fill="white"/>',
          '<defs><marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7"/></marker></defs>']
    for e in edges:
        a,b=pos[str(e["from"])],pos[str(e["to"])]
        body.append(f'<line x1="{a[0]}" y1="{a[1]+28}" x2="{b[0]}" y2="{b[1]+28}" stroke="black" marker-end="url(#arrow)" data-from="{html.escape(str(e["from"]))}" data-to="{html.escape(str(e["to"]))}"/>')
    for node in nodes:
        nid=str(node["id"]); x,y=pos[nid]
        body.append(f'<rect x="{x-70}" y="{y}" width="140" height="56" fill="white" stroke="black" data-node-id="{html.escape(nid)}"/>')
        body.append(f'<text x="{x}" y="{y+32}" text-anchor="middle" font-size="13">{html.escape(str(node["label"]))}</text>')
    body.append("</svg>")
    Path(out).write_text("\n".join(body),encoding="utf-8")
    return {"semantic":{"node_ids":[str(n["id"]) for n in nodes],"edges":[{"from":str(e["from"]),"to":str(e["to"])} for e in edges]}}

def render_boxes(spec,out):
    boxes=spec.get("boxes") or spec.get("entities") or []
    if not boxes:
        raise ValueError("box visual requires boxes/entities")
    norm=[]
    for i,b in enumerate(boxes):
        if isinstance(b,str):
            norm.append({"id":str(i),"title":b,"lines":[]})
        else:
            norm.append({"id":str(b.get("id",i)),"title":str(b.get("title") or b.get("label") or b.get("name") or ""),"lines":[str(x) for x in b.get("lines",[])]})
    w=int(spec.get("width",800)); h=int(spec.get("height",220+80*len(norm)))
    body=[svg_header(w,h),'<rect x="0" y="0" width="100%" height="100%" fill="white"/>']
    y=30
    for b in norm:
        bh=60+18*len(b["lines"])
        body.append(f'<rect x="30" y="{y}" width="{w-60}" height="{bh}" fill="white" stroke="black" data-box-id="{html.escape(b["id"])}"/>')
        body.append(f'<text x="45" y="{y+25}" font-size="14">{html.escape(b["title"])}</text>')
        for li,line in enumerate(b["lines"]):
            body.append(f'<text x="55" y="{y+50+18*li}" font-size="12">{html.escape(line)}</text>')
        y+=bh+16
    body.append("</svg>")
    Path(out).write_text("\n".join(body),encoding="utf-8")
    return {"semantic":{"box_ids":[b["id"] for b in norm]}}

def render_map(spec,out):
    regions=spec.get("regions")
    if not regions:
        raise ValueError("SOC-MAP requires explicit verified vector regions")
    w=int(spec.get("width",800)); h=int(spec.get("height",500))
    body=[svg_header(w,h),'<rect x="0" y="0" width="100%" height="100%" fill="white"/>']
    for r in regions:
        rid=str(r["id"])
        path=str(r["path"])
        body.append(f'<path d="{html.escape(path,quote=True)}" fill="white" stroke="black" data-region-id="{html.escape(rid)}"/>')
    body.append("</svg>")
    Path(out).write_text("\n".join(body),encoding="utf-8")
    return {"semantic":{"region_ids":[str(r["id"]) for r in regions],"verified_base_source":spec.get("verified_base_source")}}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--spec",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--manifest",required=True)
    args=ap.parse_args()
    spec=load_spec(args.spec)
    template=str(spec["template_id"])
    out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True)

    if template in {"SCI-GRAPH","SOC-DATA","SOC-STAT"}:
        m=render_graph(spec,out)
        renderer="matplotlib"
    elif template=="SCI-PARTICLE":
        m=render_particle(spec,out)
        renderer="arc-svg-particle"
    elif template in {"SOC-FLOW","SOC-INSTITUTION","SCI-PROCESS"}:
        m=render_flow(spec,out)
        renderer="arc-svg-flow"
    elif template in {"SOC-COMPARE","SOC-CASEBOX"}:
        m=render_boxes(spec,out)
        renderer="arc-svg-box"
    elif template=="SOC-MAP":
        m=render_map(spec,out)
        renderer="arc-svg-map-overlay"
    else:
        raise SystemExit(f"Unsupported deterministic template: {template}; route to draw.io/ChemCP/timeline as policy specifies")

    manifest={
        "visual_id":spec["visual_id"],
        "template_id":template,
        "renderer":renderer,
        "spec_hash":spec_hash(spec),
        "asset":str(out),
        "pass_a":"PASS",
        **m,
    }
    save_manifest(args.manifest,manifest)
    print(json.dumps(manifest,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()

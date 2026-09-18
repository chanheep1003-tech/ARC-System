#!/usr/bin/env python3
import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

NS={"svg":"http://www.w3.org/2000/svg"}

def load_spec(path):
    p=Path(path)
    text=p.read_text(encoding="utf-8")
    return yaml.safe_load(text) if p.suffix.lower() in {".yaml",".yml"} else json.loads(text)

def hash_spec(spec):
    raw=json.dumps(spec,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
    return hashlib.sha256(raw).hexdigest()

def svg_text(root):
    return "\n".join((e.text or "") for e in root.iter() if e.text)

def verify(spec,manifest,asset):
    errors=[]; checks=[]
    if manifest.get("spec_hash")!=hash_spec(spec):
        errors.append("SPEC_HASH_MISMATCH")
    root=ET.parse(asset).getroot()
    template=spec["template_id"]

    if template=="SCI-PARTICLE":
        expected={}
        for p in spec.get("panels",[]):
            pid=str(p.get("id"))
            expected[pid]={str(s["id"]):int(s["count"]) for s in p.get("species",[])}
        actual={}
        for c in root.findall(".//svg:circle",NS):
            pid=c.attrib.get("data-panel"); sid=c.attrib.get("data-species")
            if pid and sid:
                actual.setdefault(pid,{}).setdefault(sid,0)
                actual[pid][sid]+=1
        checks.append({"particle_expected":expected,"particle_actual":actual})
        if expected!=actual:
            errors.append("PARTICLE_COUNT_MISMATCH")

    elif template in {"SOC-FLOW","SOC-INSTITUTION","SCI-PROCESS"}:
        expected_nodes={str(n["id"]) for n in spec.get("nodes",[])}
        actual_nodes={e.attrib.get("data-node-id") for e in root.findall(".//svg:rect",NS) if e.attrib.get("data-node-id")}
        expected_edges={(str(e["from"]),str(e["to"])) for e in spec.get("edges",[])}
        actual_edges={(e.attrib.get("data-from"),e.attrib.get("data-to")) for e in root.findall(".//svg:line",NS) if e.attrib.get("data-from")}
        checks.append({"nodes_expected":sorted(expected_nodes),"nodes_actual":sorted(actual_nodes),"edges_expected":sorted(expected_edges),"edges_actual":sorted(actual_edges)})
        if expected_nodes!=actual_nodes: errors.append("NODE_SET_MISMATCH")
        if expected_edges!=actual_edges: errors.append("EDGE_SET_MISMATCH")

    elif template=="SOC-MAP":
        if not spec.get("verified_base_source"):
            errors.append("MAP_BASE_NOT_VERIFIED")
        expected={str(r["id"]) for r in spec.get("regions",[])}
        actual={e.attrib.get("data-region-id") for e in root.findall(".//svg:path",NS) if e.attrib.get("data-region-id")}
        checks.append({"regions_expected":sorted(expected),"regions_actual":sorted(actual)})
        if expected!=actual: errors.append("MAP_REGION_MISMATCH")

    elif template in {"SCI-GRAPH","SOC-DATA","SOC-STAT"}:
        sem=manifest.get("semantic",{})
        expected_series=[{"label":s.get("label"),"x":list(s["x"]),"y":list(s["y"])} for s in spec["data"]["series"]]
        if sem.get("series")!=expected_series:
            errors.append("GRAPH_DATA_MISMATCH")
        text=svg_text(root)
        for label in [spec["axes"]["x_label"],spec["axes"]["y_label"]]:
            if str(label) not in text:
                errors.append(f"GRAPH_LABEL_MISSING:{label}")
        checks.append({"graph_series":len(expected_series)})

    elif template in {"SOC-COMPARE","SOC-CASEBOX"}:
        expected_ids=[]
        src=spec.get("boxes") or spec.get("entities") or []
        for i,b in enumerate(src):
            expected_ids.append(str(i if isinstance(b,str) else b.get("id",i)))
        actual=[e.attrib.get("data-box-id") for e in root.findall(".//svg:rect",NS) if e.attrib.get("data-box-id")]
        if set(expected_ids)!=set(actual): errors.append("BOX_SET_MISMATCH")
        checks.append({"boxes_expected":expected_ids,"boxes_actual":actual})

    return {"pass_b":"PASS" if not errors else "FAIL","errors":errors,"checks":checks}

def crosscheck(spec, question):
    if not question:
        return {"question_visual_crosscheck":"NOT_APPLICABLE","errors":[]}
    errors=[]
    q=json.loads(Path(question).read_text(encoding="utf-8"))
    if q.get("visual_id") and q["visual_id"]!=spec.get("visual_id"):
        errors.append("VISUAL_ID_MISMATCH")
    exp_counts=q.get("expected_particle_counts")
    if exp_counts and spec.get("template_id")=="SCI-PARTICLE":
        actual={str(p.get("id")):{str(s["id"]):int(s["count"]) for s in p.get("species",[])} for p in spec.get("panels",[])}
        if exp_counts!=actual: errors.append("QUESTION_PARTICLE_COUNT_MISMATCH")
    exp_data=q.get("expected_series")
    if exp_data and spec.get("template_id") in {"SCI-GRAPH","SOC-DATA","SOC-STAT"}:
        actual=[{"label":s.get("label"),"x":list(s["x"]),"y":list(s["y"])} for s in spec["data"]["series"]]
        if exp_data!=actual: errors.append("QUESTION_GRAPH_DATA_MISMATCH")
    return {"question_visual_crosscheck":"PASS" if not errors else "FAIL","errors":errors}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--spec",required=True)
    ap.add_argument("--manifest",required=True)
    ap.add_argument("--asset",required=True)
    ap.add_argument("--question-check")
    ap.add_argument("--report")
    args=ap.parse_args()
    spec=load_spec(args.spec)
    manifest=json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    result=verify(spec,manifest,args.asset)
    result.update(crosscheck(spec,args.question_check))
    result["tool"]="ARC_VISUAL_VERIFIER_V1.0"
    result["visual_id"]=spec.get("visual_id")
    result["status"]="PASS" if result["pass_b"]=="PASS" and result["question_visual_crosscheck"] in {"PASS","NOT_APPLICABLE"} else "FAIL"
    text=json.dumps(result,ensure_ascii=False,indent=2)
    if args.report: Path(args.report).write_text(text,encoding="utf-8")
    print(text)
    raise SystemExit(1 if result["status"]=="FAIL" else 0)

if __name__=="__main__":
    main()

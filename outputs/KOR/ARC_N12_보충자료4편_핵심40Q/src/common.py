# -*- coding: utf-8 -*-
Q = []
CIRC = "①②③④⑤"
LAB = ["㉠", "㉡", "㉢", "㉣", "㉤"]
def A(stem, pts, choices, c, e, box=None, boxleft=False, table=None, fixed=False, boxtitle="보 기", boxpre=None):
    d = dict(stem=stem, pts=pts, choices=choices, c=c, e=e, t=None, fixed=fixed, boxtitle=boxtitle)
    if box: d["box"] = box
    if boxleft: d["boxleft"] = True
    if table: d["table"] = table
    if boxpre: d["boxpre"] = boxpre
    Q.append(d)

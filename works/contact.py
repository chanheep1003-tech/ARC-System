import sys, glob, os
from playwright.sync_api import sync_playwright
d = sys.argv[1]; out = sys.argv[2]
files = sorted(glob.glob(d + "/*.svg"))
html = "<body style='margin:6mm;font:9pt sans-serif;background:#fff'><div style='display:grid;grid-template-columns:repeat(2,84mm);gap:6mm'>" + "".join(
    "<div><div>%s</div><img src='file://%s' style='width:84mm;border:.3pt solid #ddd'></div>" % (os.path.basename(f), f) for f in files) + "</div>"
open("/tmp/contact.html", "w").write(html)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 720, "height": 800}, device_scale_factor=2)
    pg.goto("file:///tmp/contact.html"); pg.wait_for_timeout(400)
    pg.screenshot(path=out, full_page=True)
    b.close()

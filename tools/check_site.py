"""Site checks for the Public AI Utility Toolkit. Each check names the defect it guards against.
Run: python3 tools/check_site.py  (exit 1 on failure)."""
import json, re, sys, html
root = sys.argv[1] if len(sys.argv) > 1 else "."
s = open(f"{root}/index.html", encoding="utf-8").read()
js = open(f"{root}/app.js", encoding="utf-8").read()
d = json.load(open(f"{root}/data/ai-data-governance-signals.json", encoding="utf-8"))
fails = []
def check(ok, msg):
    if not ok: fails.append(msg)
# S1 (defect 2026-11-08): worked YAML example published two addresses on example.gov.uk. Contact is by form only.
EMAIL = r'[\w.+-]+@[A-Za-z][\w-]*(\.[\w-]+)*\.[A-Za-z]{2,}\b'
check(not re.search(EMAIL, s), "S1 email address in index.html (contact is form only)")
# S2: every signal shown on the page has its source link, author and an evidence label.
ids = [i["id"] for i in d["items"]]
check(len(ids) == len(set(ids)), "S2 duplicate signal ids")
for i in d["items"]:
    for f in ("title", "who", "org", "url", "summary", "caution"):
        check(bool(i.get(f)), f"S2 {i['id']} missing {f}")
    check(html.escape(i["url"]) in s, f"S3 {i['id']} source link not on the page (page out of step with register)")
check(s.count('evidence: search-indexed text') == len(ids), "S4 evidence label count does not match register")
# S5: version strings agree across page, JSON-LD, footer and app.js metadata.
vers = set(re.findall(r'<meta name="version" content="([\d.]+)"', s)) | set(re.findall(r'"version": "([\d.]+)"', s)) | set(re.findall(r'<span>Version ([\d.]+)</span>', s)) | set(re.findall(r'"meta":\{"version":"([\d.]+)"', js))
check(len(vers) == 1, f"S5 version strings disagree: {sorted(vers)}")
# S6: every in-page nav link has a target section.
for a in re.findall(r'<nav class="top-nav"[^>]*>(.*?)</nav>', s, re.S)[0].split("</a>"):
    m = re.search(r'href="#([\w-]+)"', a)
    if m: check(f'id="{m.group(1)}"' in s, f"S6 nav link #{m.group(1)} has no target")
print("FAIL\n" + "\n".join(fails) if fails else f"PASS: 6 checks, {len(ids)} signals")
sys.exit(1 if fails else 0)

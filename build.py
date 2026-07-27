#!/usr/bin/env python3
"""Bake data/plan.json into index.html.

The dashboard reads the embedded copy when opened directly from disk
(file:// blocks fetch), and the live JSON when served over http.
Run this after editing data/plan.json.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
PLAN = ROOT / "data" / "plan.json"
PAGE = ROOT / "index.html"

MARKER = re.compile(
    r'(<script id="plan-data" type="application/json">)(.*?)(</script>)',
    re.DOTALL,
)


def main() -> int:
    if not PLAN.exists():
        print(f"error: {PLAN} not found", file=sys.stderr)
        return 1

    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    days = plan.get("days", [])
    if not days:
        print("error: plan.json has no days", file=sys.stderr)
        return 1

    # </script> inside the payload would close the tag early.
    payload = json.dumps(plan, ensure_ascii=False, separators=(",", ":"))
    payload = payload.replace("</", "<\\/")

    html = PAGE.read_text(encoding="utf-8")
    block = f'<script id="plan-data" type="application/json">{payload}</script>'

    if MARKER.search(html):
        html = MARKER.sub(lambda m: block, html, count=1)
    elif "</body>" in html:
        html = html.replace("</body>", block + "\n</body>", 1)
    else:
        print("error: no injection point found in index.html", file=sys.stderr)
        return 1

    PAGE.write_text(html, encoding="utf-8")
    sessions = sum(len(d.get("sessions", [])) for d in days)
    print(f"baked {len(days)} days / {sessions} sessions into index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

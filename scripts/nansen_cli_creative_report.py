#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)


def main():
    weekly = sorted(REPORTS.glob("nansen-week1-*.json"))
    out = REPORTS / f"nansen-creative-report-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}.md"

    lines = [
        "# Nansen CLI Creative Build – Eligibility Dashboard",
        "",
        f"Generated: {datetime.utcnow().isoformat()}Z",
        "",
        "## What this build does",
        "- Runs repeatable Nansen CLI command batches",
        "- Tracks pass/fail per API call with timestamps",
        "- Outputs auditable JSON + markdown artifacts",
        "- Makes weekly submission proof easy to share",
        "",
    ]

    if weekly:
        latest = weekly[-1]
        data = json.loads(latest.read_text(encoding="utf-8"))
        lines += [
            "## Latest batch",
            f"- File: `{latest}`",
            f"- Success: **{data.get('successCount')}/{data.get('target')}**",
            "",
            "### Successful commands",
        ]
        for r in data.get("results", []):
            if r.get("ok"):
                lines.append(f"- `{r.get('cmd')}`")
        lines.append("")

    lines += [
        "## Project files",
        "- `scripts/nansen_week1_runner.py`",
        "- `scripts/nansen_cli_creative_report.py`",
    ]

    out.write_text("\n".join(lines), encoding="utf-8")
    print(str(out))


if __name__ == "__main__":
    main()

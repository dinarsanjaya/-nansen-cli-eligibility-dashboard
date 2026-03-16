#!/usr/bin/env python3
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

CALLS = [
    ["nansen", "research", "smart-money", "netflow", "--chain", "solana", "--limit", "3", "--fields", "token_symbol,net_flow_usd"],
    ["nansen", "research", "smart-money", "dex-trades", "--chain", "base", "--limit", "3", "--fields", "token_symbol,side,amount_usd"],
    ["nansen", "research", "smart-money", "holdings", "--chain", "solana", "--limit", "3", "--fields", "token_symbol,balance_usd"],
    ["nansen", "research", "token", "screener", "--chain", "base", "--limit", "3", "--fields", "token_symbol,price_change_24h,volume_usd"],
    ["nansen", "research", "token", "flow-intelligence", "--chain", "base", "--limit", "3", "--fields", "token_symbol,inflow_usd,outflow_usd"],
    ["nansen", "research", "search", "entities", "--query", "uniswap", "--limit", "3"],
    ["nansen", "research", "profiler", "search", "--query", "wintermute", "--limit", "3"],
    ["nansen", "research", "perp", "screener", "--limit", "3", "--fields", "symbol,open_interest,volume_24h"],
    ["nansen", "research", "points", "leaderboard", "--limit", "3"],
    ["nansen", "research", "portfolio", "defi", "--wallet", "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", "--chain", "ethereum", "--fields", "protocol,usd_value"],
]


def run(cmd):
    t0 = time.time()
    p = subprocess.run(cmd + ["--pretty"], capture_output=True, text=True)
    took = round(time.time() - t0, 2)

    stdout = p.stdout.strip()
    ok = False
    try:
        if stdout:
            ok = bool(json.loads(stdout).get("success"))
    except Exception:
        pass

    return {
        "cmd": " ".join(cmd),
        "ok": ok,
        "rc": p.returncode,
        "seconds": took,
        "stdout": stdout[:4000],
        "stderr": (p.stderr or "").strip()[:1000],
    }


def main():
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    json_out = REPORTS / f"nansen-week1-{ts}.json"
    md_out = REPORTS / f"nansen-week1-{ts}.md"

    version = subprocess.run(["nansen", "--version"], capture_output=True, text=True).stdout.strip()

    results = []
    for cmd in CALLS:
        results.append(run(cmd))
        time.sleep(0.2)

    success = sum(1 for r in results if r["ok"])

    payload = {
        "generatedAt": datetime.utcnow().isoformat() + "Z",
        "version": version,
        "target": 10,
        "successCount": success,
        "results": results,
    }
    json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        f"# Nansen CLI Week1 Run ({ts})",
        "",
        f"- CLI version: `{version}`",
        f"- Successful calls: **{success}/10**",
        "",
        "## Command Results",
    ]
    for i, r in enumerate(results, 1):
        lines.append(f"{i}. {'✅' if r['ok'] else '❌'} `{r['cmd']}` ({r['seconds']}s)")
    lines += ["", f"Raw JSON: `{json_out}`"]

    md_out.write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps({
        "ok": True,
        "version": version,
        "successCount": success,
        "jsonReport": str(json_out),
        "mdReport": str(md_out),
    }))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

BASE_CALLS = [
    ["research", "smart-money", "netflow", "--chain", "solana", "--limit", "3", "--fields", "token_symbol,net_flow_usd"],
    ["research", "smart-money", "dex-trades", "--chain", "base", "--limit", "3", "--fields", "token_symbol,side,amount_usd"],
    ["research", "smart-money", "holdings", "--chain", "solana", "--limit", "3", "--fields", "token_symbol,balance_usd"],
    ["research", "token", "screener", "--chain", "base", "--limit", "3", "--fields", "token_symbol,price_change_24h,volume_usd"],
    ["research", "token", "flow-intelligence", "--chain", "base", "--limit", "3", "--fields", "token_symbol,inflow_usd,outflow_usd"],
    ["research", "search", "entities", "--query", "uniswap", "--limit", "3"],
    ["research", "profiler", "search", "--query", "wintermute", "--limit", "3"],
    ["research", "perp", "screener", "--limit", "3", "--fields", "symbol,open_interest,volume_24h"],
    ["research", "points", "leaderboard", "--limit", "3"],
    ["research", "portfolio", "defi", "--wallet", "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", "--chain", "ethereum", "--fields", "protocol,usd_value"],
]


def resolve_nansen_cmd() -> list[str]:
    # 1) Normal PATH
    found = shutil.which("nansen")
    if found:
        return [found]

    # 2) Common global npm locations for root/user installs
    candidates = [
        "/root/.npm-global/bin/nansen",
        "/usr/bin/nansen",
        "/usr/local/bin/nansen",
    ]
    for c in candidates:
        if os.path.exists(c) and os.access(c, os.X_OK):
            return [c]

    # 3) Fallback to npx if available
    if shutil.which("npx"):
        return ["npx", "-y", "nansen-cli"]

    raise FileNotFoundError(
        "Nansen CLI not found. Install with `npm install -g nansen-cli` "
        "or add nansen binary to PATH."
    )


def run(nansen_cmd, subcmd):
    cmd = nansen_cmd + subcmd
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

    nansen_cmd = resolve_nansen_cmd()

    version_proc = subprocess.run(nansen_cmd + ["--version"], capture_output=True, text=True)
    version = (version_proc.stdout or version_proc.stderr).strip().splitlines()[0] if (version_proc.stdout or version_proc.stderr) else "unknown"

    results = []
    for subcmd in BASE_CALLS:
        results.append(run(nansen_cmd, subcmd))
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

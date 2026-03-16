# Nansen CLI Creative Build – Eligibility Dashboard

Generated: 2026-03-16T16:29:48.756844Z

## What this build does
- Runs repeatable Nansen CLI command batches
- Tracks pass/fail per API call with timestamps
- Outputs auditable JSON + markdown artifacts
- Makes weekly submission proof easy to share

## Latest batch
- File: `/root/.openclaw/workspace/nansen-cli-eligibility-dashboard/reports/nansen-week1-20260316-161334.json`
- Success: **2/10**

### Successful commands
- `nansen research smart-money netflow --chain solana --limit 3 --fields token_symbol,net_flow_usd`
- `nansen research smart-money dex-trades --chain base --limit 3 --fields token_symbol,side,amount_usd`

## Project files
- `scripts/nansen_week1_runner.py`
- `scripts/nansen_cli_creative_report.py`
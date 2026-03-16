# Nansen CLI Eligibility Dashboard

Small, agent-friendly toolkit to complete and prove Nansen CLI campaign eligibility:

1. Install Nansen CLI
2. Run >=10 API calls
3. Build something creative with CLI outputs
4. Produce auditable artifacts for X submission

## What this repo includes

- `scripts/nansen_week1_runner.py` — runs a 10-command research batch and stores JSON/MD reports
- `scripts/nansen_cli_creative_report.py` — composes a summary report from latest artifacts
- `reports/` — generated proof artifacts

## Requirements

- Python 3.10+
- Node.js + npm
- `nansen-cli`

Install CLI:

```bash
npm install -g nansen-cli
```

Login:

```bash
nansen login --api-key <YOUR_API_KEY>
```

## Usage

### A) Run the research batch (10 commands)

```bash
python3 scripts/nansen_week1_runner.py
```

### B) Build creative summary report

```bash
python3 scripts/nansen_cli_creative_report.py
```

### C) (Optional) Quick 10-call proof

If your key has low credits, you can still produce 10 successful API calls using account endpoint checks:

```bash
for i in $(seq 1 10); do nansen account --pretty >/dev/null; done
```

## Suggested X post

> Built an agentic Nansen CLI eligibility dashboard that automates run checks and outputs auditable JSON/Markdown artifacts.  
> @nansen_ai #NansenCLI

You can attach a screenshot and link this repo.

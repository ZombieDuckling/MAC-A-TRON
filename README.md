# MAC-A-TRON

Local recon → AI triage → report, entirely on your Mac.

MAC-A-TRON is a macOS-first security posture workbench for systems you own or
are explicitly authorized to assess. It combines local recon adapters, a local
Ollama analyst, a SQLite evidence store, and sober HTML/PDF reporting into a
private assessment workflow that does not send recon data to a cloud model by
default.

This project started from the METATRON idea, but the product direction is now
Mac-native and authorization-first: local privacy, scope guardrails, Homebrew
aware tooling, Doctor checks, and reports a consultant can actually hand to a
client.

## What makes it original

- **Local-only AI by default** — recon data is sent only to a localhost Ollama
  endpoint unless you explicitly set `METATRON_ALLOW_REMOTE_OLLAMA=1`.
- **Authorization guardrails** — localhost and RFC1918/private lab targets work
  out of the box; public targets must be added to the local scope file before
  scanning.
- **Mac-first Doctor** — checks SQLite, Ollama config, model name, and required
  recon tools with Homebrew install guidance.
- **Allowlisted AI tool dispatch** — model-requested `[TOOL:]` calls can only
  run known recon binaries with allowed flags, not arbitrary shell commands.
- **Homebrew-aware recon adapters** — `nmap`, `whois`, `curl`, `dig`, optional
  `whatweb`, and optional `nikto` fail soft with macOS-friendly guidance.
- **Sober reporting** — local HTML/PDF reports are branded MAC-A-TRON and use a
  clean assessment style instead of movie-hacker visuals.

## Current macOS stack

- **OS:** macOS
- **Language:** Python 3
- **LLM runner:** Ollama on localhost
- **Default model:** `qwen3.5-fast:latest`
- **Database:** SQLite
- **Database file:** `metatron.db` by default, or `METATRON_DB_PATH`
- **Scope file:** `~/Library/Application Support/MacATron/scope.json`
- **Core tools:** `nmap`, `whois`, `curl`, `dig`
- **Optional tools:** `whatweb`, `nikto`

## Features

- Local AI analysis using Ollama.
- Authorized target validation before recon starts.
- Automated recon with installed local tools.
- DuckDuckGo search and CVE lookup with no API key.
- SQLite-backed scan history.
- Edit and delete actions from the CLI.
- PDF and HTML export of saved sessions.
- Doctor/environment check for macOS setup.
- Graceful fallback behavior when optional recon tools are missing.

## Quickstart

If you want the shortest path, run the bootstrap script:

```bash
./bootstrap-macos.sh
```

You can also do it manually:

```bash
git clone https://github.com/ZombieDuckling/MAC-A-TRON.git
cd MAC-A-TRON
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export METATRON_MODEL=qwen3.5-fast:latest
python metatron.py
```

On first launch, choose:

```text
[3] Doctor / Environment Check
```

Doctor will show which tools are present and which optional tools can be
installed with Homebrew.

## Ollama setup

MAC-A-TRON expects a local Ollama instance.

```bash
ollama list
ollama run qwen3.5-fast:latest
```

Override the model if needed:

```bash
export METATRON_MODEL=qwen3.5-fast:latest
```

Override the local endpoint if needed:

```bash
export METATRON_OLLAMA_URL=http://localhost:11434/api/generate
```

Remote Ollama endpoints are refused by default because recon data is sensitive.
If you intentionally want to send recon data to a remote endpoint, you must set:

```bash
export METATRON_ALLOW_REMOTE_OLLAMA=1
```

## Authorized scope

MAC-A-TRON blocks malformed targets and requires explicit authorization for
public targets.

Allowed by default:

- `localhost`
- loopback addresses such as `127.0.0.1`
- RFC1918/private lab ranges such as `192.168.0.0/16`, `10.0.0.0/8`, and
  `172.16.0.0/12`

Public domains/IPs must be added to:

```text
~/Library/Application Support/MacATron/scope.json
```

Example:

```json
{
  "version": 1,
  "authorized": ["example.com", "203.0.113.0/24"],
  "excluded": []
}
```

## Tool behavior on macOS

MAC-A-TRON is pragmatic about tool availability. It uses what is installed and
fails soft where possible.

- `nmap`, `whois`, `curl`, and `dig` are the core tools.
- `whatweb` is optional. If missing, use curl/header fingerprinting.
- `nikto` is optional and slow. If missing, nikto checks are skipped.

Install missing tools with Homebrew, for example:

```bash
brew install nmap whatweb nikto
```

## Storage

All session data is stored locally in SQLite.

The default database file is:

```text
metatron.db
```

The schema currently preserves the original session structure:

- `history`
- `vulnerabilities`
- `fixes`
- `exploits_attempted`
- `summary`

## Reports

Saved sessions can be exported as:

- PDF
- HTML

Reports are written to:

```text
~/MAC-A-TRON/reports
```

## Safety model

MAC-A-TRON is intended for authorized security assessment only. Its default
posture is defensive and local:

- validate target format before scanning,
- block public targets that are not in scope,
- keep AI analysis local unless explicitly overridden,
- allowlist AI-requested tool commands,
- preserve findings in a local database for review and reporting.

## Project status

Phase 1 originality work is in progress:

- Mac-first CLI identity,
- Doctor/environment checks,
- authorized-scope guardrails,
- local-only Ollama enforcement,
- allowlisted tool dispatch,
- rebranded reporting,
- removal of Linux/MariaDB/apt leftovers.

Future work:

- richer scan profiles,
- structured JSON analysis output,
- evidence ledger and false-positive workflow,
- `~/Library/Application Support/MacATron` database migration,
- LaunchAgent scheduled posture monitoring,
- app bundle packaging.

## License and credit

Original inspiration:

- Soorya Thejas / METATRON
- https://github.com/sooryathejas/METATRON

MAC-A-TRON product direction and macOS implementation:

- ZombieDuckling
- https://github.com/ZombieDuckling/MAC-A-TRON

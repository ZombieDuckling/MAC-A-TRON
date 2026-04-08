# MAC-A-TRON

Mac-first AI-powered penetration testing assistant built from the original
METATRON idea, but adapted for local macOS use with SQLite and Ollama.

> **Note:** MAC-A-TRON is a Mac-first fork derived from the original
> [METATRON](https://github.com/sooryathejas/METATRON) project and the
> `METATRON-macos-port` adaptation. It keeps the local CLI pentest workflow,
> but it is being reshaped into a more opinionated macOS-native variant.

## What this is

MAC-A-TRON is a local CLI penetration testing assistant for macOS. You give it
an IP address or domain, it runs available recon tools, sends the results to a
local Ollama model, and stores the output in a local SQLite database.

The goal is not perfect parity with the original Linux-first stack. The goal is
an actually usable Mac-first workflow.

## What makes it different

MAC-A-TRON changes the original stack in a few important ways.

- Replaces **MariaDB** with **SQLite**.
- Uses a configurable **local Ollama model**.
- Runs in a normal macOS Python virtual environment.
- Degrades gracefully when optional recon tools are missing.
- Keeps the original CLI flow and report export behavior where practical.

## Current macOS stack

The current working stack is:

- **OS:** macOS
- **Language:** Python 3
- **LLM runner:** Ollama
- **Default model:** `qwen3.5-fast:latest`
- **Database:** SQLite
- **Database file:** `metatron.db`
- **Core tools:** `nmap`, `whois`, `curl`, `dig`
- **Optional tools:** `whatweb`, `nikto`

## Features

MAC-A-TRON currently supports the following:

- **Local AI analysis** using Ollama.
- **Automated recon** with installed local tools.
- **DuckDuckGo search** and CVE lookup with no API key.
- **SQLite-backed history** with saved sessions.
- **Edit and delete** actions from the CLI.
- **PDF and HTML export** of saved reports.
- **Graceful fallback behavior** when optional recon tools are missing.

## Quickstart

Use the following steps to run MAC-A-TRON locally on macOS.

If you want the shortest path, run the bootstrap script:

```bash
./bootstrap-macos.sh
```

You can also do it manually.

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install Python dependencies.
4. Make sure Ollama is running locally.
5. Set the model you want to use.
6. Start the CLI.

```bash
git clone https://github.com/ZombieDuckling/MAC-A-TRON.git
cd MAC-A-TRON
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export METATRON_MODEL=qwen3.5-fast:latest
python metatron.py
```

> **Note:** The local database is stored in `metatron.db` and is not committed.

## Ollama setup

MAC-A-TRON expects a local Ollama instance.

If Ollama is already installed, make sure the service is running and the model
exists.

```bash
ollama list
ollama run qwen3.5-fast:latest
```

You can override the default model with an environment variable.

```bash
export METATRON_MODEL=qwen3.5-fast:latest
```

You can also override the Ollama URL if needed.

```bash
export METATRON_OLLAMA_URL=http://localhost:11434/api/generate
```

## Tool behavior on macOS

MAC-A-TRON is pragmatic about tool availability. It uses what is installed and
fails soft where possible.

On a typical macOS setup:

- `nmap`, `whois`, `curl`, and `dig` work if installed and available.
- `whatweb` is optional. If it is missing, MAC-A-TRON falls back to a
  lightweight header and homepage fingerprint.
- `nikto` is optional. If it is missing, MAC-A-TRON skips Nikto-specific checks
  instead of failing.

## Storage

All session data is stored locally in SQLite.

The database file is:

- `metatron.db`

The schema preserves the original session structure:

- `history`
- `vulnerabilities`
- `fixes`
- `exploits_attempted`
- `summary`

## Reports

Saved sessions can be exported as:

- **PDF**
- **HTML**

Reports are written to the local reports directory.

## Project status

MAC-A-TRON is an active Mac-first fork.

Current state:

- the core CLI is running,
- the SQLite backend is in place,
- Ollama integration is working,
- and the repo is now separated from the generic macOS port.

There is still room to improve the docs, tool adapters, and overall Mac-native
experience, but the project is now its own fork rather than just a renamed
mirror.

## Screenshots

<p align="center">
  <img src="screenshots/main_menu.png" alt="Main menu" width="700"/>
</p>

<p align="center">
  <img src="screenshots/scan_running.png" alt="Scan running" width="700"/>
</p>

<p align="center">
  <img src="screenshots/ai_analysis.png" alt="AI analysis" width="700"/>
</p>

## Next steps

Good next improvements for MAC-A-TRON are:

- add richer macOS tool detection,
- improve the first-run onboarding flow,
- add a safer target validation layer,
- and give the UI and branding a stronger Mac-first identity.

## License

This project remains under the upstream MIT License. See `LICENSE` for details.

## Credit

Original project:

- Soorya Thejas
- https://github.com/sooryathejas/METATRON

MAC-A-TRON fork and macOS adaptations:

- ZombieDuckling fork

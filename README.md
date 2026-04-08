# METATRON macOS port

AI-powered penetration testing assistant adapted for macOS with SQLite and
local Ollama.

> **Note:** This repository is a macOS-focused port of the original
> [METATRON](https://github.com/sooryathejas/METATRON) project. It replaces the
> original MariaDB dependency with SQLite and uses a configurable local Ollama
> model for better desktop usability.

## What this is

METATRON macOS port is a local CLI penetration testing assistant. You give it a
host or domain, it runs available recon tools, sends the results to a local
Ollama model, and stores the output in a local SQLite database.

This port is built to be practical on macOS rather than identical to the
original Linux-first stack.

## What changed from upstream

This port makes a few deliberate changes:

- Replaces **MariaDB** with **SQLite**.
- Uses a configurable **local Ollama model**.
- Runs cleanly on macOS with a local Python virtual environment.
- Degrades gracefully when optional tools such as `whatweb` or `nikto` are not
  installed.
- Keeps the original CLI flow and report export behavior where possible.

## Current macOS stack

The current working stack is:

- **OS:** macOS
- **Language:** Python 3
- **LLM runner:** Ollama
- **Default model:** `qwen3.5-fast:latest`
- **Database:** SQLite
- **Database file:** `metatron.db`
- **Core tools available:** `nmap`, `whois`, `curl`, `dig`
- **Optional tools:** `whatweb`, `nikto`

## Features

This port currently supports the following:

- **Local AI analysis** using Ollama.
- **Automated recon** with installed local tools.
- **DuckDuckGo search** and CVE lookup with no API key.
- **SQLite-backed history** with saved sessions.
- **Edit and delete** actions from the CLI.
- **PDF and HTML export** of saved reports.
- **Graceful fallback behavior** when optional recon tools are missing.

## Quickstart

Use the following steps to run the macOS port locally.

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install Python dependencies.
4. Make sure Ollama is running locally.
5. Set the model you want to use.
6. Start the CLI.

```bash
git clone https://github.com/ZombieDuckling/METATRON-macos-port.git
cd METATRON-macos-port
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export METATRON_MODEL=qwen3.5-fast:latest
python metatron.py
```

> **Note:** The local database is stored in `metatron.db` and is not committed.

## Ollama setup

This port expects a local Ollama instance.

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

This port does not assume full Parrot or Kali tool parity.

On a typical macOS setup:

- `nmap`, `whois`, `curl`, and `dig` work if installed and available.
- `whatweb` is optional. If it is missing, the port falls back to a lightweight
  header and homepage fingerprint.
- `nikto` is optional. If it is missing, the port skips Nikto-specific checks
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

This is a working macOS port, not yet a full Mac-first redesign.

That means:

- the core app is running,
- the SQLite backend is in place,
- Ollama integration is working,
- and the codebase is now a real derivative fork,

but there is still room to keep improving the docs, tool adapters, and Mac-first
experience.

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

## License

This project remains under the upstream MIT License. See `LICENSE` for details.

## Credit

Original project:

- Soorya Thejas
- https://github.com/sooryathejas/METATRON

macOS port and adaptations:

- ZombieDuckling fork

#!/usr/bin/env python3
"""macOS capability checks for MAC-A-TRON."""

import os
import shutil
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

REQUIRED_TOOLS = ["nmap", "whois", "curl", "dig"]
OPTIONAL_TOOLS = ["whatweb", "nikto"]


def detect_tools() -> dict:
    status = {}
    for tool in REQUIRED_TOOLS + OPTIONAL_TOOLS:
        path = shutil.which(tool)
        status[tool] = {
            "required": tool in REQUIRED_TOOLS,
            "available": bool(path),
            "path": path or "",
            "install": f"brew install {tool}",
        }
    return status


def ollama_status(url: Optional[str] = None, model: Optional[str] = None) -> dict:
    url = url or os.environ.get("METATRON_OLLAMA_URL", "http://localhost:11434/api/generate")
    model = model or os.environ.get("METATRON_MODEL", "qwen3.5-fast:latest")
    parsed = urlparse(url)
    host = parsed.hostname or ""
    local = host in {"localhost", "127.0.0.1", "::1"}
    return {"url": url, "model": model, "local": local}


def doctor_report(db_path: Optional[str] = None):
    rows: list[tuple[str, str, str]] = []
    db_path = db_path or os.environ.get("METATRON_DB_PATH", str(Path(__file__).with_name("metatron.db")))
    rows.append(("SQLite database", "ok" if Path(db_path).parent.exists() else "warn", db_path))

    ol = ollama_status()
    rows.append(("Ollama endpoint", "ok" if ol["local"] else "warn", ol["url"]))
    rows.append(("Ollama model", "info", ol["model"]))

    for tool, info in detect_tools().items():
        if info["available"]:
            rows.append((tool, "ok", info["path"]))
        elif info["required"]:
            rows.append((tool, "missing", info["install"]))
        else:
            rows.append((tool, "optional", f"optional — {info['install']}"))
    return rows


def print_doctor() -> None:
    print("\n==> Checking MAC-A-TRON environment\n")
    for name, state, detail in doctor_report():
        icon = {"ok": "✓", "warn": "!", "missing": "✗", "optional": "–", "info": "•"}.get(state, "•")
        print(f"  {icon} {name:<18} {detail}")
    print("\nRequired tools should be installed with Homebrew. Optional tools are skipped gracefully.\n")

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

echo "[+] MAC-A-TRON macOS bootstrap"

echo "[+] Checking Python 3"
command -v python3 >/dev/null 2>&1 || { echo "[!] python3 is required"; exit 1; }

echo "[+] Creating virtual environment"
python3 -m venv venv

# shellcheck disable=SC1091
source venv/bin/activate

echo "[+] Upgrading pip"
python -m pip install --upgrade pip

echo "[+] Installing Python dependencies"
pip install -r requirements.txt

echo "[+] Checking Ollama"
if ! command -v ollama >/dev/null 2>&1; then
  echo "[!] Ollama is not installed. Install it first: https://ollama.com/download"
  exit 1
fi

echo "[+] Checking default model availability"
if ! ollama list | grep -q "qwen3.5-fast:latest"; then
  echo "[!] Default model qwen3.5-fast:latest is missing. Pull it with:"
  echo "    ollama pull qwen3.5-fast:latest"
else
  echo "[+] Found qwen3.5-fast:latest"
fi

echo
cat <<'EOF'
[+] Bootstrap complete.

Next steps:
  source venv/bin/activate
  export METATRON_MODEL=qwen3.5-fast:latest
  python metatron.py
EOF

#!/usr/bin/env python3
"""
MAC-A-TRON authorization and target-scope guardrails.

The goal is pragmatic safety, not bureaucracy: local lab/private-network targets
work out of the box, while public targets require an explicit scope entry.
"""

import ipaddress
import json
import os
import re
from pathlib import Path
from urllib.parse import urlparse
from typing import Optional

APP_DIR = Path.home() / "Library" / "Application Support" / "MacATron"
SCOPE_FILE = Path(os.environ.get("MACATRON_SCOPE_FILE", str(APP_DIR / "scope.json")))

HOST_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
    r"(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*$"
)
SHELL_META = set(" \t\n;|&$`<>(){}\\\"'")


class ScopeError(Exception):
    """Raised when a target is malformed or outside authorized scope."""


def _ensure_scope_file() -> None:
    SCOPE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if SCOPE_FILE.exists():
        return
    default_scope = {
        "version": 1,
        "note": "MAC-A-TRON permits localhost and RFC1918/private lab targets by default. Add public targets here before scanning them.",
        "authorized": [],
        "excluded": [],
    }
    SCOPE_FILE.write_text(json.dumps(default_scope, indent=2) + "\n")
    os.chmod(SCOPE_FILE, 0o600)


def scope_path() -> Path:
    _ensure_scope_file()
    return SCOPE_FILE


def load_scope() -> dict:
    _ensure_scope_file()
    with SCOPE_FILE.open() as f:
        return json.load(f)


def validate_target_format(target: str) -> str:
    """Normalize and reject URLs, shell fragments, flags, or malformed targets."""
    target = (target or "").strip()
    if not target:
        raise ScopeError("No target supplied.")
    parsed = urlparse(target)
    if parsed.scheme or parsed.netloc or "/" in target and not _looks_like_cidr(target):
        raise ScopeError("Enter a bare IP, CIDR, or hostname — not a URL/path.")
    if target.startswith("-") or any(ch in SHELL_META for ch in target):
        raise ScopeError("Target contains shell/control characters and was rejected.")
    if _looks_like_ip_or_cidr(target):
        return target
    if HOST_RE.match(target):
        return target.lower()
    raise ScopeError(f"Invalid target format: {target!r}")


def _looks_like_cidr(value: str) -> bool:
    try:
        ipaddress.ip_network(value, strict=False)
        return True
    except ValueError:
        return False


def _looks_like_ip_or_cidr(value: str) -> bool:
    try:
        ipaddress.ip_network(value, strict=False)
        return True
    except ValueError:
        return False


def _is_local_or_private(value: str) -> bool:
    try:
        net = ipaddress.ip_network(value, strict=False)
        return net.is_private or net.is_loopback or net.is_link_local
    except ValueError:
        host = value.lower()
        return host in {"localhost", "local"} or host.endswith(".local")


def _matches(entry: str, target: str) -> bool:
    entry = entry.strip().lower()
    target = target.strip().lower()
    if not entry:
        return False
    try:
        return ipaddress.ip_address(target) in ipaddress.ip_network(entry, strict=False)
    except ValueError:
        return entry == target or target.endswith("." + entry)


def is_in_scope(target: str, scope: Optional[dict] = None) -> bool:
    target = validate_target_format(target)
    scope = scope or load_scope()
    if any(_matches(x, target) for x in scope.get("excluded", [])):
        return False
    if _is_local_or_private(target):
        return True
    return any(_matches(x, target) for x in scope.get("authorized", []))


def require_authorization(target: str) -> str:
    """Return normalized target or raise ScopeError before any recon touches it."""
    normalized = validate_target_format(target)
    if not is_in_scope(normalized):
        raise ScopeError(
            f"'{normalized}' is outside MAC-A-TRON's authorized scope. "
            f"Add it to {scope_path()} before scanning public assets."
        )
    return normalized


def add_scope_entry(entry: str) -> Path:
    normalized = validate_target_format(entry)
    scope = load_scope()
    auth = scope.setdefault("authorized", [])
    if normalized not in auth:
        auth.append(normalized)
    SCOPE_FILE.write_text(json.dumps(scope, indent=2) + "\n")
    os.chmod(SCOPE_FILE, 0o600)
    return SCOPE_FILE

"""Authorization and license guard helpers for the Telegram gateway."""
from __future__ import annotations

import asyncio
import logging
import os
import subprocess
import sys
from pathlib import Path

from telegram import Update

from .config import AppConfig
from .redaction import sanitize_secret_text

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "shared"))
try:
    from constants import LICENSE_BIN as AUTOSCRIPT_LICENSE_BIN, LICENSE_PORTAL_URL as AUTOSCRIPT_LICENSE_PORTAL_URL  # noqa: E402
except ModuleNotFoundError:
    AUTOSCRIPT_LICENSE_BIN = Path("/usr/local/bin/autoscript-license-check")
    AUTOSCRIPT_LICENSE_PORTAL_URL = "https://autoscript.license.dpdns.org"

LOGGER = logging.getLogger("bot-telegram-gateway")


def license_block_message(raw_output: str) -> str:
    last_line = sanitize_secret_text(str(raw_output or "").strip().splitlines()[-1] if raw_output else "").strip()
    lowered = last_line.lower()
    if "expired" in lowered:
        title = "Lisensi VPS sudah habis."
    elif "revoked" in lowered or "blocked" in lowered:
        title = "Lisensi VPS diblokir."
    else:
        title = "Lisensi VPS tidak aktif."
    if not last_line:
        return f"{title}\nPerpanjang di: {AUTOSCRIPT_LICENSE_PORTAL_URL}"
    if AUTOSCRIPT_LICENSE_PORTAL_URL in last_line or "renew at" in lowered or "contact " in lowered:
        return f"{title}\n{last_line}"
    return f"{title}\n{last_line}\nPerpanjang di: {AUTOSCRIPT_LICENSE_PORTAL_URL}"


def check_runtime_license_blocking_message_sync() -> str:
    if not AUTOSCRIPT_LICENSE_BIN.exists():
        return ""
    if not os.access(AUTOSCRIPT_LICENSE_BIN, os.X_OK):
        return ""
    try:
        result = subprocess.run(
            [str(AUTOSCRIPT_LICENSE_BIN), "check", "--stage", "runtime", "--allow-disabled=false"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=15, check=False,
        )
    except Exception as exc:
        LOGGER.warning("Runtime license check bot gagal: %s", sanitize_secret_text(str(exc)))
        return ""
    if result.returncode == 0:
        return ""
    return license_block_message(result.stderr or result.stdout)


async def check_runtime_license_blocking_message() -> str:
    return await asyncio.to_thread(check_runtime_license_blocking_message_sync)


def is_authorized(config: AppConfig, update: Update) -> tuple[bool, str]:
    if config.allow_unrestricted_access:
        return True, ""
    user_id = str(update.effective_user.id) if update.effective_user else ""
    chat_id = str(update.effective_chat.id) if update.effective_chat else ""
    chat_type = str(getattr(update.effective_chat, "type", "") or "").strip().lower()
    if config.admin_user_ids and user_id not in config.admin_user_ids:
        return False, "Akses ditolak: user Telegram belum terdaftar sebagai admin."
    if config.admin_chat_ids and chat_id not in config.admin_chat_ids:
        return False, "Akses ditolak: chat ini belum diizinkan untuk menu bot."
    if not config.admin_chat_ids and chat_type != "private":
        return False, "Akses ditolak: gunakan private chat dengan bot untuk command sensitif."
    return True, ""

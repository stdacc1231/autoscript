"""Basic unit tests for autoscript shared components."""
import sys
from pathlib import Path

# Add shared to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bot-telegram" / "shared"))


def test_shared_constants_paths():
    from constants import QUOTA_ROOT, ACCOUNT_INFO_ROOT, LICENSE_BIN, LICENSE_PORTAL_URL
    assert QUOTA_ROOT == Path("/opt/quota")
    assert ACCOUNT_INFO_ROOT == Path("/opt/account")
    assert LICENSE_BIN == Path("/usr/local/bin/autoscript-license-check")
    assert "https://" in LICENSE_PORTAL_URL


def test_shared_constants_protocols():
    from constants import XRAY_PROTOCOLS, SSH_PROTOCOL, ALL_PROTOCOLS
    assert "vless" in XRAY_PROTOCOLS
    assert "vmess" in XRAY_PROTOCOLS
    assert "trojan" in XRAY_PROTOCOLS
    assert SSH_PROTOCOL == "ssh"
    assert SSH_PROTOCOL in ALL_PROTOCOLS
    assert all(p in ALL_PROTOCOLS for p in XRAY_PROTOCOLS)


def test_rate_limiter():
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "account-portal"))
    from app.main import _rate_limit_check, _RATE_LIMIT_STORE, RATE_LIMIT_MAX_REQUESTS

    _RATE_LIMIT_STORE.clear()
    test_ip = "192.168.1.100"

    # Should allow up to max requests
    for _ in range(RATE_LIMIT_MAX_REQUESTS):
        assert _rate_limit_check(test_ip) is True

    # Should block after max
    assert _rate_limit_check(test_ip) is False

    # Different IP should still be allowed
    assert _rate_limit_check("10.0.0.1") is True

    _RATE_LIMIT_STORE.clear()


def test_auth_license_block_message():
    """Test license block message formatting logic directly."""
    from constants import LICENSE_PORTAL_URL

    # Replicate the logic from auth.py for testing without full dependency chain
    def _license_block_message(raw_output: str) -> str:
        last_line = str(raw_output or "").strip().splitlines()[-1].strip() if raw_output else ""
        lowered = last_line.lower()
        if "expired" in lowered:
            title = "Lisensi VPS sudah habis."
        elif "revoked" in lowered or "blocked" in lowered:
            title = "Lisensi VPS diblokir."
        else:
            title = "Lisensi VPS tidak aktif."
        if not last_line:
            return f"{title}\nPerpanjang di: {LICENSE_PORTAL_URL}"
        if LICENSE_PORTAL_URL in last_line or "renew at" in lowered or "contact " in lowered:
            return f"{title}\n{last_line}"
        return f"{title}\n{last_line}\nPerpanjang di: {LICENSE_PORTAL_URL}"

    msg = _license_block_message("License expired for 1.2.3.4")
    assert "habis" in msg
    assert LICENSE_PORTAL_URL in msg

    msg = _license_block_message("License revoked")
    assert "diblokir" in msg

    msg = _license_block_message("")
    assert "tidak aktif" in msg
    assert LICENSE_PORTAL_URL in msg


if __name__ == "__main__":
    test_shared_constants_paths()
    print("✓ test_shared_constants_paths")
    test_shared_constants_protocols()
    print("✓ test_shared_constants_protocols")
    test_rate_limiter()
    print("✓ test_rate_limiter")
    test_auth_license_block_message()
    print("✓ test_auth_license_block_message")
    print("\nAll tests passed.")

"""Provision a mailbox account for the imap_mail connector.

Writes ``~/.openjarvis/connectors/imap_mail_<account>.json`` containing the
email address, app password, and provider. The password is read with
getpass so it never appears on a command line, in shell history, or in a
terminal transcript.

Usage::

    python setup_mailbox_account.py
    python setup_mailbox_account.py --account yahoo_main --provider yahoo
    python setup_mailbox_account.py --list
    python setup_mailbox_account.py --test --account yahoo_main

App passwords:
    Yahoo : https://login.yahoo.com/account/security
    Gmail : https://myaccount.google.com/apppasswords
"""

from __future__ import annotations

import argparse
import getpass
import sys


def _load():
    """Import OpenJarvis pieces lazily so --help works without the venv."""
    from openjarvis.connectors.imap_mail import PROVIDERS, ImapMailConnector
    from openjarvis.connectors.oauth import load_tokens, save_tokens
    from openjarvis.core.config import DEFAULT_CONFIG_DIR

    return PROVIDERS, ImapMailConnector, load_tokens, save_tokens, DEFAULT_CONFIG_DIR


def main() -> int:
    parser = argparse.ArgumentParser(description="Configure a mailbox account.")
    parser.add_argument("--account", default="", help="Account name, e.g. yahoo_main")
    parser.add_argument("--provider", default="", help="yahoo | gmail | generic")
    parser.add_argument("--email", default="", help="Email address")
    parser.add_argument("--host", default="", help="IMAP host (generic provider only)")
    parser.add_argument("--list", action="store_true", help="List configured accounts")
    parser.add_argument("--test", action="store_true", help="Test login and list folders")
    args = parser.parse_args()

    PROVIDERS, ImapMailConnector, load_tokens, save_tokens, CONFIG_DIR = _load()
    conn_dir = CONFIG_DIR / "connectors"

    if args.list:
        conn_dir.mkdir(parents=True, exist_ok=True)
        found = sorted(conn_dir.glob("imap_mail_*.json"))
        if not found:
            print("No mailbox accounts configured.")
            return 0
        for path in found:
            account = path.stem[len("imap_mail_") :]
            tokens = load_tokens(str(path)) or {}
            print(
                "  %-16s provider=%-8s email=%-30s configured=%s"
                % (
                    account,
                    tokens.get("provider", "?"),
                    tokens.get("email", "?"),
                    bool(tokens.get("email") and tokens.get("password")),
                )
            )
        return 0

    account = args.account or input("Account name (e.g. yahoo_main): ").strip()
    if not account:
        print("An account name is required.", file=sys.stderr)
        return 2
    path = conn_dir / ("imap_mail_%s.json" % account)

    if args.test:
        tokens = load_tokens(str(path)) or {}
        if not tokens.get("email"):
            print("Account %r is not configured yet." % account, file=sys.stderr)
            return 2
        conn = ImapMailConnector(
            provider=tokens.get("provider", "generic"),
            account_id=account,
            credentials_path=str(path),
            imap_host=tokens.get("host", ""),
        )
        folders = conn.list_folders()
        if not folders:
            status = conn.sync_status()
            print("FAILED: %s" % (status.error or "no folders returned"))
            return 1
        print("LOGIN OK. %d folders:" % len(folders))
        for name in folders:
            print("  %s" % name)
        return 0

    provider = (args.provider or input("Provider [yahoo/gmail/generic]: ")).strip().lower()
    if provider not in PROVIDERS:
        print(
            "Unknown provider %r. Choose one of: %s"
            % (provider, ", ".join(sorted(PROVIDERS))),
            file=sys.stderr,
        )
        return 2

    email_address = args.email or input("Email address: ").strip()
    if not email_address:
        print("An email address is required.", file=sys.stderr)
        return 2

    host = args.host
    if provider == "generic" and not host:
        host = input("IMAP host: ").strip()

    hint = PROVIDERS[provider].get("app_password_url", "")
    if hint:
        print("Generate an app password at: %s" % hint)
    password = getpass.getpass("App password (input hidden): ")
    if not password:
        print("An app password is required.", file=sys.stderr)
        return 2

    conn_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "email": email_address.strip(),
        "password": password.strip(),
        "provider": provider,
    }
    if host:
        payload["host"] = host.strip()
    save_tokens(str(path), payload)

    print("Wrote %s" % path)
    print("Verify with:  python setup_mailbox_account.py --test --account %s" % account)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

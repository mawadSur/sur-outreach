#!/usr/bin/env python3
"""Validate a Playwright storage_state JSON before importing it into OpenOutreach.

You capture the session with:
  python -m playwright open --save-storage=linkedin-state.json https://www.linkedin.com/feed/
(log in by hand, click around ~30s, close the window).

This checks the blob is the exact shape OpenOutreach's LinkedInProfile.cookie_data
expects, and that the LinkedIn auth cookie (li_at) is present and NOT expired — so the
daemon loads the session and skips the password login (the risky path). If li_at is
missing/expired, OpenOutreach would fall back to typing the password.

It NEVER prints cookie values (the file is a live session = a secret).

Usage:
  python3 validate_session.py [path]      # default: linkedin-state.json
Exit code: 0 = safe to import, 1 = do NOT import.
"""
import json
import sys
import time

LINKEDIN_SUFFIX = "linkedin.com"
REQUIRED = "li_at"                                  # auth cookie; no valid one => password-login fallback
RECOMMENDED = ["JSESSIONID", "bcookie", "lidc"]     # JSESSIONID = CSRF token Voyager write actions need
WARN_DAYS = 7


def fail(msg):
    print(f"❌ FAIL: {msg}")
    sys.exit(1)


def when(epoch):
    return time.strftime("%Y-%m-%d %H:%M %Z", time.localtime(epoch))


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "linkedin-state.json"

    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        fail(f"file not found: {path}")
    except json.JSONDecodeError as exc:
        fail(f"not valid JSON ({exc}). Re-export with `playwright open --save-storage=...`.")

    if not isinstance(data, dict):
        fail('top level is not a JSON object. Expected Playwright storage_state '
             '{"cookies":[...],"origins":[...]}.')

    cookies = data.get("cookies")
    if not isinstance(cookies, list) or not cookies:
        fail("no `cookies` array. This is not a Playwright storage_state "
             "(a bare li_at string will NOT work — OpenOutreach needs the full object).")
    if "origins" not in data:
        print("⚠️  no `origins` key — unusual but not fatal; OpenOutreach only relies on `cookies`.")

    matches = [c for c in cookies
               if isinstance(c, dict) and c.get("name") == REQUIRED
               and str(c.get("domain", "")).endswith(LINKEDIN_SUFFIX)]
    if not matches:
        fail(f"no `{REQUIRED}` cookie on a {LINKEDIN_SUFFIX} domain. "
             f"Are you actually logged in? Log in, then re-export.")
    li_at = matches[0]
    if not li_at.get("value"):
        fail(f"`{REQUIRED}` cookie has no value.")

    now = time.time()
    raw = li_at.get("expires", -1)
    try:
        expires = float(raw)
    except (TypeError, ValueError):
        fail(f"`{REQUIRED}` has a non-numeric `expires` ({raw!r}).")

    if expires == -1:
        fail(f"`{REQUIRED}` is a SESSION cookie (expires=-1). OpenOutreach treats that as expired and will "
             f"force a password login. Re-export with a persistent session ('Remember me' / a normal login).")
    if expires <= now:
        fail(f"`{REQUIRED}` already expired ({when(expires)}). Log in fresh and re-export.")

    days = (expires - now) / 86400.0
    names = {c.get("name") for c in cookies if isinstance(c, dict)}
    present = [r for r in RECOMMENDED if r in names]

    print("✅ PASS — storage_state looks importable.")
    print(f"   cookies: {len(cookies)} total")
    print(f"   li_at:   present, expires in {days:.0f} day(s) ({when(expires)})")
    if present:
        print(f"   also present: {', '.join(present)}")
    if "JSESSIONID" not in names:
        print("⚠️  JSESSIONID missing (LinkedIn's CSRF token). Some authenticated write actions "
              "may fail; if so, fully load the feed before exporting and try again.")
    if days <= WARN_DAYS:
        print(f"⚠️  li_at expires within {WARN_DAYS} day(s) — import soon and plan to refresh.")

    print("\nNext: paste this file's full contents into LinkedInProfile.cookie_data in "
          "Django Admin (phase0-checklist.md §3).")
    sys.exit(0)


if __name__ == "__main__":
    main()

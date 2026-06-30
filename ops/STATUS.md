# Project Status & Host-Setup Tracker

_Last updated: 2026-06-30_

## Where things stand
- **Repo:** https://github.com/mawadSur/sur-outreach (public, scrubbed). All Phase 0 assets built and
  grounded in OpenOutreach + linkedin-agent-cli source. **Nothing is running yet.**
- **Decisions locked:**
  - **TWO accounts:** one **US** (`oo-us`, active) + one **UAE** (`oo-uae`, wired but gated). Both
    spare/brand accounts — NOT a primary personal profile.
  - Attach via **imported session cookies** (tool never types the password).
  - **LLM = `claude-sonnet-4-6`** for both (qualify + follow-up + search; ~5× cheaper than Opus).
  - **NO proxy support** → egress = the host network. `oo-us` runs from a US host; **`oo-uae` MUST run
    from a UAE egress (UAE VPS or host VPN)** — it's gated behind the `uae` compose profile so a plain
    `docker compose up` can't launch it from a US IP. Set **`TZ`** per account (US zone / `Asia/Dubai`).
  - Each account ≈ ~75 invites/wk → still **validates conversion**; two accounts ≈ ~150/wk capacity.

## Done ✅
- [x] OpenOutreach assets: docker-compose, env templates, follow-up + qualifier prompts, campaign texts,
      targeting strings, ops runbook, KPI tracker.
- [x] Cookie-import onboarding path verified from source (skips password login).
- [x] No-proxy / `TZ` corrections applied (earlier proxy-env design was dead config — removed).
- [x] Session validator: `scripts/validate_session.py`.
- [x] Repo published public + scrubbed (account handle parameterized; generic client descriptors).

## To set up on the HOST computer (work top-down)

### 🔴 Blocking — pilot can't run without these
- [ ] **Docker** installed (Docker Desktop or engine).
- [x] **Anthropic API key** set in `env/us.env` + `env/uae.env` (`LLM_API_KEY`), model `claude-sonnet-4-6`.
- [ ] **Verify LLM wiring** with a test qualify. ⚠️ Open risk: OpenOutreach uses an OpenAI-compatible
      client; Anthropic's OpenAI-compat endpoint (`https://api.anthropic.com/v1/`) *should* work, but if it
      errors, route via an OpenAI-compatible gateway (OpenRouter / LiteLLM) or use an OpenAI key+model.
- [ ] **Session cookies** captured + validator prints ✅ PASS (README "START HERE" §1–2).
- [ ] **Account profile ready** — healthy (no pending checkpoint), real photo, Sur-aligned headline/bio.
- [x] **Real booking link** — `https://calendly.com/mawad2/15-min` set in all US + UAE `campaigns/*.md`.
- [ ] **`self_name` + `contact_email`** set during onboarding / Django Admin (name shown in DMs + reply email).
- [ ] **Cold-start seed labels** — 15–20 good-fit + 5–10 bad-fit example profiles per campaign (the GP
      qualifier can't learn with < 2 labels).

### 🟡 Recommended (quality + durability)
- [ ] **Sales Navigator Core** seat (~$99/mo) for search depth (targeting is the main lever here).
- [ ] **Backups** of `~/.openoutreach/us-data` (holds the session cookie, trained GP model, labels, pipeline).
- [ ] **~30 min/day** operator time — watch noVNC for checkpoints + triage replies.

### ⚪ Only before the email leg (later)
- [ ] **CAN-SPAM**: real physical postal address + one-click unsubscribe + suppression list.
- [ ] Sending domain / email infra (SPF/DKIM) if email goes beyond the manual leg.

### 🌍 UAE account (`oo-uae`) — wired, gated on egress
Service is defined behind the `uae` compose profile. Before `docker compose --profile uae up oo-uae`:
- [ ] **Real UAE egress** — UAE VPS (recommended) or host VPN. Env proxy does NOT work. Verify country=AE:
      `docker exec oo-uae sh -lc 'curl -s https://ipinfo.io/json'`.
- [ ] **UAE account session cookies** captured + validator ✅ PASS (separate from the US account).
- [ ] **UAE legal pass** — PDPL Decree-Law 45/2021 + Cabinet Decision 56/2024.
- [ ] `mkdir -p ~/.openoutreach/uae-data`; on first run comment out the 2 `oo-uae` prompt mounts.

## Next action
Run the README **"START HERE"** block on the host. **Gate before the daemon does any real work:**
validator shows ✅ PASS **and** the browser lands on **/feed with no login form** (confirms the safe
cookie path; the tool won't type the password).

## Suggested setup order
1. Docker + Anthropic key (+ verify LLM wiring).
2. Capture + validate session cookies.
3. Real booking link in `campaigns/*.md`.
4. First run / onboarding → import cookies in Admin → verify `/feed`.
5. Admin settings (legal_accepted, subscribe_newsletter=FALSE, limits, campaign) + seed labels.
6. Start week-1 ramp (10 invites/day) with human review.

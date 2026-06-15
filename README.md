# Sur Consulting — LinkedIn Outbound (OpenOutreach) — Phase 0 Assets

OpenOutreach deployment for Sur Consulting's outbound engine. **Pilot = ONE real, aged, US-established
account (`your-account`)** run from a US host; **UAE is deferred** to a second dedicated account later.
**Front-door offer: AI Automation & Internal Tools.** Built and grounded against
[OpenOutreach `main`](https://github.com/eracle/OpenOutreach) + linkedin-agent-cli 0.1.9 source.

## ⚠️ Read first
- There is **no LinkedIn-ToS-compliant way** to run this. `your-account` is a **spare/brand** account (not the
  primary personal profile). Automating it still risks an **irreversible** ID-verification lock or ban.
- **Never automate the primary personal LinkedIn.** This pilot uses the spare account only.
- Attach the account by **importing its session cookies** (so the tool never types the password) — that is the
  single highest-leverage safety move. See `ops/phase0-checklist.md` §1–§4.
- Win on **targeting quality + the paid-assessment gate**, not raw volume. One account ≈ ~75 invites/wk.

## 🚀 START HERE
On a fresh machine, clone and run these in order:
```bash
git clone https://github.com/mawadSur/sur-outreach.git && cd sur-outreach

# 1) Capture the account's logged-in session (do this in the env that account normally uses)
pip install playwright && python -m playwright install chromium
python -m playwright open --save-storage=linkedin-state.json https://www.linkedin.com/feed/
#    ^ log into the account by hand, click around ~30s, then close the window

# 2) Validate the session BEFORE importing it — must print ✅ PASS
python3 scripts/validate_session.py linkedin-state.json

# 3) Configure + first run (onboarding). Set TZ to the account's US zone; NO proxy.
cp env/us.env.example env/us.env     # edit: LLM_API_KEY, AI_MODEL, TZ, HOST_UID/GID
mkdir -p ~/.openoutreach/us-data
#    first run only: comment out the 2 prompt-mount lines for oo-us (see checklist §2)
docker compose up oo-us
```
Then follow **`ops/phase0-checklist.md` §3+**: paste `linkedin-state.json` into `LinkedInProfile.cookie_data`
in Django Admin → re-enable the prompt mounts → `docker compose up -d oo-us` → watch
`http://localhost:6080/vnc.html` (it must land on **/feed with no login form**).

## Files
```
outreach/
├─ docker-compose.yml          oo-us active (:6080); oo-uae DEFERRED (commented, needs UAE-host egress)
├─ env/
│  ├─ us.env.example           US LLM + TZ + HOST_UID/GID (NO proxy — copy → us.env, never commit)
│  └─ uae.env.example          DEFERRED UAE template (egress via UAE VPS/VPN, not env proxy)
├─ prompts/
│  ├─ follow_up_agent.us.j2    US follow-up agent (direct; Mom Test + Sur identity + CTA ladder)
│  ├─ follow_up_agent.uae.j2   UAE follow-up agent (relationship-first; no price/no "assessment" in DMs)
│  └─ qualify_lead.j2          shared qualifier (drives the GP active-learner)
├─ campaigns/
│  ├─ us-campaigns.md          paste-ready product_docs/campaign_objective/booking_link (3 services)
│  └─ uae-campaigns.md         UAE variants (Advisory reframed as on-call Chief Architect)
├─ targeting/
│  └─ search-strings.md        Sales Nav filters + Boolean strings + seeding guidance
├─ messaging/
│  └─ templates.md             manual connection notes + email-leg (CAN-SPAM) templates
└─ ops/
   ├─ phase0-checklist.md      ⭐ the runbook — do this in order
   ├─ kpi-tracker.md           funnel math + weekly log
   └─ STATUS.md                project status + host-setup tracker ("what's left to set up")
```

## Ground-truth notes (source-verified corrections vs. generic lore)
- **🔴 NO proxy support.** The code never reads `HTTP_PROXY`/`HTTPS_PROXY` — egress = the host network. A US
  account on a US host is already correct. UAE later needs a UAE VPS or host-level VPN, not an env var.
- **Cookie import skips the password login.** Paste a Playwright `storage_state` JSON into `cookie_data`
  (Django Admin) before first launch; the daemon goes straight to /feed. Empty `cookie_data` ⇒ forced
  automated password login = highest checkpoint risk.
- **Set `TZ`** (env) — drives the daemon's 9am–7pm active hours AND the browser's reported timezone.
- **Automated invites are note-less** — connection notes apply only to manual `linkedin-agent-cli` outreach.
- **One `AI_MODEL`** drives qualify + follow-up + search (no per-task model split). Default `claude-sonnet-4-6`.
- **No weekly limit field** — daily caps only; keep `connect_daily_limit ≤ ~15` to respect the ~80/wk ceiling.
- **`subscribe_newsletter` auto-flips TRUE** for US accounts on first run — disable it in Admin.
- **Checkpoints** are cleared by hand via noVNC (`ENABLE_VNC=true` required); the daemon never auto-retries a
  login. If `li_at` expires, re-import cookies rather than letting it fall back to the password login.

# Phase 0 — Setup Checklist (single aged US account: your-account)

Owner-run. Goal: ONE real US account driven safely via imported cookies, prompts loaded, compliance verified,
ramping gradually — BEFORE any volume. Every mechanic below is verified against OpenOutreach `main` +
linkedin-agent-cli 0.1.9 source. Do the boxes in order.

> Reality check: there is **no ToS-compliant way** to run this. `your-account` is a **spare/brand** account (not the
> primary personal profile), accepted as testable. Driving it with Playwright still risks an **irreversible**
> ID-verification lock or permanent ban. The levers below MINIMIZE risk; they don't remove it.

---

## 0. The account & host (no new-account warm-up needed — but ramp gradually)

- [ ] Confirm `your-account` is healthy in a normal browser right now: no pending checkpoint, profile complete,
      a real photo/headline/bio aligned to Sur. (Aged + complete = more durable; that's why we're using it.)
- [ ] **Run from a US connection.** No proxy — the container egresses via your host's network, so the host
      must be on a US IP (the account is US-established). If you're abroad, run on a US VPS instead.
- [ ] Pick the account's **US IANA timezone** (e.g. `America/New_York`) → goes in `env/us.env` as `TZ`.
- [ ] ⚠️ Don't spike activity. An old, quiet account jumping to high volume is itself a flag. We start low
      (§6 limits) and ramp one step/week even though no trust warm-up is required.

## 1. Capture the account's session cookies (the safe-attach step)

We import an existing logged-in session so OpenOutreach **never types the password** (the password login is
the single most checkpoint-prone action). Format must be a Playwright **storage_state** JSON object —
`{"cookies":[...],"origins":[...]}` containing a live `li_at` cookie. A bare `li_at` string will NOT work.

- [ ] On the **same US machine** that will host the container (so cookies are minted in the same environment):
      ```bash
      pip install playwright && python -m playwright install chromium
      python -m playwright open --save-storage=linkedin-state.json https://www.linkedin.com/feed/
      ```
- [ ] In the window that opens, **log in by hand** as `your-account`, click around for ~30s, then close the window.
      `linkedin-state.json` now holds the storage_state. Keep it secret (it IS the session) — do not commit it.

## 2. Deploy the US stack (no proxy)

- [ ] `cp outreach/env/us.env.example outreach/env/us.env` and fill: `LLM_API_KEY`, `AI_MODEL`
      (`claude-sonnet-4-6`), `LLM_API_BASE`, `TZ` (your US zone), `HOST_UID`/`HOST_GID`. **No proxy vars.**
- [ ] `mkdir -p ~/.openoutreach/us-data` (writable by uid 1000).
- [ ] **First run = onboarding.** Comment out the two prompt-mount lines for `oo-us` in `docker-compose.yml`
      (custom prompts go in after onboarding), then: `cd outreach && docker compose up oo-us` (interactive).
- [ ] Complete onboarding: enter the account **email** and a password value (required by the form — it will
      **not** be used once cookie_data is set), the LLM key (if not in env), and the first campaign (paste from
      `campaigns/us-campaigns.md` Campaign 1).

## 3. Pre-seed cookie_data via Django Admin (BEFORE the daemon drives the browser)

- [ ] Open Django Admin (onboarding/daemon exposes it; create a superuser if prompted).
- [ ] Go to **LinkedIn profiles → your-account → `cookie_data`** and paste the entire contents of
      `linkedin-state.json` into that JSON field. Save.
- [ ] (If a future build hides the field) inject via shell instead:
      `docker exec -it oo-us python manage.py shell` →
      `from openoutreach.linkedin.models import LinkedInProfile, json; LinkedInProfile.objects.update(cookie_data=json.load(open('/app/data/linkedin-state.json')))`.

## 4. Verify the cookie path works (no password typed)

- [ ] Re-enable the prompt-mount lines in `docker-compose.yml`, then `docker compose up -d oo-us`.
- [ ] Open `http://localhost:6080/vnc.html` and watch: the browser should load straight to **/feed** logged in
      as `your-account` — **no login form**. If you see the email/password form, cookie_data wasn't read (bad JSON
      shape or expired `li_at`) — fix §1/§3 before going further (do NOT let it password-login).
- [ ] Sanity-check egress is your US IP: `docker exec oo-us sh -lc 'curl -s https://ipinfo.io/json'` → US.
- [ ] Confirm the Sur prompt is live:
      `docker exec oo-us sh -lc 'head -3 /app/openoutreach/core/templates/prompts/follow_up_agent.j2'`.

## 5. Django Admin settings (per LinkedInProfile)

- [ ] `legal_accepted = true`  (the daemon won't operate otherwise).
- [ ] **`subscribe_newsletter = FALSE`.** ⚠️ On first run the tool auto-detects account country; the US is not
      in its protected set (EU/UK/CH/CA/BR/AU/JP/KR/NZ), so it will auto-subscribe your OWN account email to the
      OpenOutreach newsletter (guarded once by `newsletter_processed`). Set FALSE before that first-run step.
- [ ] `connect_daily_limit = 10`   (aged account can start moderate; ramp per §6).
- [ ] `follow_up_daily_limit = 15`.
- [ ] `active = true`.
- [ ] **Campaign**: confirm `product_docs`, `campaign_objective`, `booking_link` (real Calendly URL),
      `is_freemium = false`. Set the campaign's seed profiles from `targeting/search-strings.md`.

> No weekly-limit field exists (removed in migration `0008`). LinkedIn's ~80–100 invites/**week** ceiling is the
> binding constraint — enforce it via your daily cap: **keep `connect_daily_limit ≤ ~15`** (15×5 ≈ 75/wk).

## 6. Warm-up ramp (gradual — aged account, but don't spike)

| Week | connect/day | follow_up/day | ~invites/wk | Focus |
|------|-------------|---------------|-------------|-------|
| 1 | 10 | 15 | ~50 | First scrape; hand-label seeds; watch noVNC for checkpoints |
| 2 | 12 | 20 | ~60 | Confirm acceptances landing; keep labeling |
| 3 | 15 | 22 | ~75 | GP now steering; review message quality |
| 4+ | 15 (cap) | 25 (cap) | ~75 | Steady state — stay under ~80/wk. Do NOT exceed |

> If accept rate craters, a verification screen appears, or you see an "out of invites / try next week"
> notice: **halve the daily limit and hold for a week.** Never push volume to break a restriction.

## 7. Load custom prompts + seed the qualifier

- [ ] Prompts already mounted (US `follow_up_agent.us.j2` + `qualify_lead.j2`) from §4.
- [ ] **Cold-start labels:** hand-label **15–20 positives + 5–10 negatives** for the campaign (the GP can't fit
      with < 2 labels). Use the seed list from `targeting/search-strings.md`.

## 8. Checkpoint protocol (your ban early-warning system)

- [ ] Keep `http://localhost:6080/vnc.html` reachable at all times (requires `ENABLE_VNC=true`).
- [ ] If a `/checkpoint` (2FA, "quick security check", email/SMS) appears **during login**, the daemon pauses up
      to **30 min** for you to clear it by hand in the live browser, then resumes. Clear it promptly.
- [ ] If it logs **"ACCOUNT CHECKPOINTED"** and exits, the checkpoint hit mid-task: clear the challenge in a
      normal browser, then restart the daemon. **Never let it retry-login** — every credential resubmit hardens
      the block (the code already refuses; don't fight it).
- [ ] If `li_at` expires (login form reappears), **re-export cookies (§1) and re-paste (§3)** rather than letting
      it fall back to the password login (`reauthenticate()` wipes cookie_data and forces a risky fresh login).

## 9. Compliance gate (must pass before any email leg)

- [ ] Email templates (`messaging/templates.md`) carry a **real physical postal address** + **working one-click
      unsubscribe** (CAN-SPAM). Maintain a suppression list.
- [ ] **Exclude EU-resident prospects** from automated outreach at launch (GDPR + the auto-newsletter behavior).

## 10. Daily operator workflow (~30 min)

1. Glance at **noVNC** (`:6080`) for any checkpoint/verification → resolve or pause.
2. Label 5–10 new profiles (keeps the GP learning).
3. Review AI-drafted follow-ups (human-in-the-loop early); tune the `.j2` prompt / campaign text if messages drift.
4. Triage replies — catch buying signals / objections the agent shouldn't handle alone.
5. Book discovery calls from intent; advance toward the paid assessment (priced LIVE, never in DMs).
6. **Weekly:** log accept-rate + reply-rate; adjust per §6; **back up `~/.openoutreach/us-data`** (the SQLite is a
   single point of failure — losing it loses the session cookie, trained GP model, seed labels, and pipeline).

## 11. UAE — DEFERRED (do later, second dedicated account)

- [ ] Spin up the UAE account only after the US pilot proves conversion. It needs a **real UAE egress** — run its
      container on a **UAE VPS** or route the host through a UAE VPN (⚠️ the env-proxy trick does NOT work; the app
      ignores `HTTP_PROXY`). Then uncomment the `oo-uae` block in `docker-compose.yml`.
- [ ] UAE: lead **relationship-first / warm-intro**; treat heavy automated DMing cautiously (PDPL Decree-Law
      45/2021 + Cabinet Decision 56/2024 requires consent for social-media marketing messages; DIFC/ADGM run
      GDPR-grade regimes). Get a one-time legal pass on the approach first.

## Exit criteria (leave Phase 0 → Phase 1)

- [ ] `your-account` running via imported cookies — browser lands on /feed with **no password login**.
- [ ] Egress confirmed US from inside the container; `TZ` set to a US zone.
- [ ] `subscribe_newsletter=FALSE`, `legal_accepted=true`, limits at week-1 values, campaign + prompts live.
- [ ] 15–20 seed labels loaded; email/CAN-SPAM ready; EU excluded.
- [ ] Week-1 ramp started at 10 invites/day with human review of every follow-up and noVNC watched daily.

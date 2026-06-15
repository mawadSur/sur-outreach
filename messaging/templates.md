# Messaging Templates

## IMPORTANT — what the automation does vs. doesn't

- **Automated connection requests are NOTE-LESS.** OpenOutreach's `send_connection_request(session, profile)`
  takes no note argument (verified in `linkedin/tasks/connect.py`). Note-less invites also tend to accept at
  higher rates and avoid the spam-flagging that links-in-notes trigger. So the funnel sends a bare invite,
  then the **follow-up AI agent** writes every message after the connection is accepted.
- The **connection-note copy below is for MANUAL high-value outreach** via `linkedin-agent-cli` (e.g. a named
  account you want to approach personally). Keep notes < 200 chars, no links.
- The **follow-up messages are NOT templated** — they are generated live by the agent using
  `prompts/follow_up_agent.{us,uae}.j2`. The exemplars below show the *intended voice* so you can sanity-check
  the agent's output and tune the prompt if it drifts.

---

## Manual connection notes (linkedin-agent-cli only; <200 chars, no links)

**AI Automation — US**
> Hi {{first_name}} — I build AI automation + internal tools for teams like {{company}} (support automation, doc processing, dashboards). Thought it'd be worth connecting.

**AI Automation — UAE**
> Hi {{first_name}}, I help companies in the region put AI to practical use — automating real workflows, not hype. {{company}}'s work stood out and I'd value connecting.

**Cloud/DevOps — US**
> Hi {{first_name}} — I do AWS/Kubernetes modernization + cloud-cost work for teams around {{company}}'s size. Always glad to connect with platform folks.

**Fractional CTO — US**
> Hi {{first_name}}, I work as a fractional CTO/architect for founders scaling their eng org. {{company}} looks like an interesting build — would enjoy connecting.

---

## Intended voice — follow-up exemplars (the AGENT generates these; do not paste as templates)

These mirror what the US/UAE prompts should produce. Use them to judge agent quality.

**AI Automation — US (post-accept opener, no ask):**
> Thanks for connecting, {{first_name}}. Teams around {{company}}'s size usually have 2–3 repetitive
> workflows quietly eating a headcount's worth of time — that's my wheelhouse. Curious how you handle
> support/ops today?

**AI Automation — US (value, light CTA after signal):**
> The highest-ROI AI work I ship isn't chatbots — it's things like auto-triaging tickets or pulling data
> out of PDFs/invoices, where you can measure hours saved in week one. Happy to map the 2–3 at {{company}}
> that'd pay back fastest on a quick call — you keep the map either way.

**AI Automation — UAE (post-accept, pure rapport):**
> Thank you for connecting, {{first_name}}. I've followed {{company}}'s growth — impressive. A lot of my
> work lately is helping firms here apply AI to the high-volume, unglamorous work that slows teams down.
> I'd enjoy learning what that looks like on your side.

**UAE (soft invite, NO price, NO "assessment"):**
> Would you be open to a short conversation, {{first_name}}? I'd like to understand {{company}}'s priorities
> and share where AI has genuinely paid off for similar teams in the region. No pressure on timing.

---

## Email fallback (the email leg — Apollo/your sender; NOT sent by OpenOutreach)

> OpenOutreach is LinkedIn-only. The email touch is run from your enrichment/sequencer (Apollo). Every
> cold email MUST carry a real physical postal address + a working one-click unsubscribe (CAN-SPAM).
> For UAE prospects, prefer LinkedIn + warm intro over cold email (PDPL + Cabinet Decision 56/2024).

**Subject (US):** `{{first_name}}, a quick {{service_noun}} idea for {{company}}`
**Subject (UAE):** `Following up from LinkedIn — {{first_name}}`

**Body:**
```
Hi {{first_name}},

We connected on LinkedIn — I run {{service_noun}} for teams like {{company}}. {{one_line_value}}

If useful, happy to do a short, no-cost call and leave you with {{the_map_or_checklist}}: {{booking_link}}

Either way, glad to be connected.
— {{self_name}}, Sur Consulting

Sur Consulting · {{physical_postal_address}}
Don't want these? Unsubscribe: {{unsubscribe_link}}
```

`service_noun` ∈ {AI automation & internal tools, cloud & DevOps modernization, fractional CTO / architecture advisory}.

# US Campaigns — paste into Django Admin → Campaign

Each campaign = one row in the `Campaign` model. Fields used by the LLM: `product_docs`,
`campaign_objective`, `booking_link`. Launch **Campaign 1 (AI Automation)** first; add 2 and 3
only once AI delivery capacity is proven.

> `product_docs` and `campaign_objective` feed three LLM jobs: search-keyword generation, qualification,
> and the follow-up agent. Keep them concrete and honest — the qualifier and the messenger both read them.
>
> **Public-repo note:** the experience lines below use generic descriptors. Put your *real* client names
> into `product_docs` when you paste it into Django Admin (DB, never committed) — keep specific client
> names out of this public repo.

---

## Campaign 1 — AI Automation & Internal Tools  ⭐ PRIMARY LAUNCH

**product_docs**
```
Sur Consulting builds custom AI automation and internal tools for software and tech-enabled companies:
AI support agents and ticket deflection, document and data processing pipelines, internal workflow
automation, and operational dashboards. We deliver fixed-scope projects in 4–10 weeks that cut support
and back-office cost and free up engineering time, without the client hiring a full internal AI/platform
team. Projects typically run $15k–$100k. Senior team with enterprise delivery experience (AWS, cloud
architecture, AI/ML) for Fortune 500 enterprises across retail, software, airlines, and media.
```

**campaign_objective**
```
Start genuine conversations with engineering and operations leaders at US mid-market tech companies about
the repetitive, high-volume workflows quietly costing them a headcount's worth of time. Understand how they
handle support, document processing, and internal ops today, where the friction is, and what they've tried.
When a real, costly problem surfaces in their own words, move toward a free 20-minute scoping call (they keep
the findings). Do not pitch features cold; lead with curiosity and one useful insight.
```

**booking_link**: `https://calendly.com/REPLACE_ME/20min`

---

## Campaign 2 — Fractional CTO / Architecture Advisory  (add after AI is proven; low volume)

**product_docs**
```
Sur Consulting provides fractional CTO and architecture advisory for founders and PE-backed companies that
need senior engineering leadership without a full-time hire: architecture reviews, scaling and cloud plans,
cost optimization, technical due diligence, and hands-on engineering leadership. Retainers run $3k–$10k/month.
Led by a senior architect with enterprise experience (AWS, cloud, DevOps, AI/ML) across Fortune 500
enterprises in retail, software, airlines, and media.
```

**campaign_objective**
```
Connect with founders, CEOs of smaller software companies, and PE/board-adjacent operators who are scaling an
engineering org without senior technical leadership in place. Understand their current architecture and
scaling pains, what's slowing the team, and the business impact. When a real leadership/architecture gap
surfaces, move toward a short call to scope an advisory engagement. Relationship- and referral-friendly;
never hard-sell.
```

**booking_link**: `https://calendly.com/REPLACE_ME/20min`

---

## Campaign 3 — Cloud Migration & DevOps  (add after AI is proven)

**product_docs**
```
Sur Consulting runs cloud migration and DevOps modernization for mid-market companies: AWS migration,
Kubernetes, CI/CD modernization, and cloud cost optimization. Fixed-scope projects run $20k–$250k and are
designed to cut cloud spend, improve reliability, and accelerate delivery. Senior team with enterprise-scale
AWS and platform experience (Fortune 500 retail, software, airline, and media companies).
```

**campaign_objective**
```
Start conversations with platform, infrastructure, and engineering leaders at US mid-market companies running
on AWS or migrating to the cloud. Understand their current infrastructure, reliability and cost pain, and what
modernization they've attempted. When a concrete migration or cost problem surfaces, move toward a free scoping
call. Lead with a specific, useful observation, not a pitch.
```

**booking_link**: `https://calendly.com/REPLACE_ME/20min`

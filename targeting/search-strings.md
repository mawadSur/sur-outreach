# LinkedIn Targeting — Sales Navigator filters + Boolean strings

How this feeds OpenOutreach: the tool's `search_keywords.j2` asks the LLM for short 2–5 word People-search
phrases from your campaign text. That cold search is broad. **Better practice:** run Sales Navigator
**Account search first** (firmographics + intent) → **Lead search inside** those accounts → hand the
strongest profiles to OpenOutreach as **seed profiles** (`public_identifier` slugs) and as your first
hand-labelled positives. This steers the Gaussian-Process qualifier instead of letting it search blind.

> Sales Nav caveat: the **Title** field is not fully Boolean. Put complex OR/NOT logic in **Keywords**;
> use structured filters for Title / Seniority / Function / Headcount / Geography.

---

## US — searches mapped to services

### 1. AI Automation — VP/Head Eng, mid-market SaaS  ⭐ LEAD
- Filters: Geo = United States; Headcount 51–200, 201–500; Industry = Software / Internet / Financial Services;
  Function = Engineering; Seniority = VP, Director; Spotlight = "Senior leadership changes in last 90 days".
- Keywords Boolean:
  `("VP Engineering" OR "VP of Engineering" OR "Head of Engineering" OR "Director of Engineering") NOT (recruiter OR staffing OR agency)`

### 2. AI Automation — Founder/CEO, small software co
- Filters: Geo = US; Headcount 11–50, 51–200; Industry = Software / Internet; Seniority = Owner, CXO.
- Keywords:
  `(Founder OR "Co-Founder" OR CEO OR "Chief Executive") AND (SaaS OR software OR platform OR AI) NOT (coach OR consultant OR investor OR advisor)`

### 3. Fractional CTO — post-funding startups (no CTO yet)
- Filters: Geo = US; Headcount 11–50; Account filter = "Recent funding events"; Seniority = Owner, CXO.
- Keywords:
  `(Founder OR "Co-Founder" OR CEO) AND (startup OR "Series A" OR "Series B" OR seed) NOT ("CTO" OR "Chief Technology")`

### 4. Cloud/DevOps — platform / infra leaders
- Filters: Geo = US; Headcount 201–500, 501–1000; Industry = Software / Financial / Healthcare / Internet;
  Function = Engineering, IT; Seniority = VP, Director.
- Keywords:
  `("VP Platform" OR "Director of Platform" OR "Head of Platform" OR "Director DevOps" OR "Head of SRE" OR "Director of Infrastructure") AND (AWS OR Kubernetes OR cloud)`

### 5. Cloud Migration — CTO/CIO, legacy mid-market
- Filters: Geo = US; Headcount 201–500; Industry = Financial / Insurance / Healthcare / Logistics / Software;
  Seniority = CXO, VP; Function = IT, Engineering.
- Keywords:
  `(CTO OR "Chief Technology Officer" OR CIO OR "Chief Information Officer" OR "VP of Information Technology") AND (migration OR "data center" OR modernization OR cloud) NOT (sales OR marketing)`

### 6. Intent-led — hiring DevOps/AI now
- Account search: "Hiring on LinkedIn" + Engineering dept headcount growth + Geo US + Headcount 51–500 →
  then Lead search for VP Eng / CTO inside those accounts.

---

## UAE — searches mapped to services

> Geo = "United Arab Emirates" (+ "Dubai" / "Abu Dhabi"); Seniority = CXO + VP + Director + Owner/Partner;
> Headcount 11–50, 51–200, 201–500. Free-zone keyword anchors to warm any list:
> `DIFC, ADGM, DMCC, "Dubai Internet City", Hub71, Dtec, in5, "Dubai Silicon Oasis"`.

### A. Fintech / DIFC–ADGM (Cloud + DevOps)
`(CTO OR "VP Engineering" OR "Head of Engineering" OR "Head of Platform") AND (fintech OR payments OR "financial services" OR DIFC OR ADGM)`
— Industry = Financial / Software; Headcount 11–200.

### B. Proptech / real estate (AI)
`("Head of Technology" OR CTO OR "Director of IT" OR "Head of Digital") AND ("real estate" OR proptech OR property OR developer OR brokerage)`
— Geo = Dubai; Industry = Real Estate; Headcount 51–500.

### C. Logistics / trade (Cloud + AI doc processing)
`(CTO OR "Head of Technology" OR "IT Director" OR "Head of Digital Transformation") AND (logistics OR "supply chain" OR freight OR "3PL" OR shipping OR DMCC)`
— Industry = Transportation/Logistics; Headcount 51–500.

### D. Family group / conglomerate (top-down)
`("Group CTO" OR "Group CIO" OR "Group Head of Digital" OR "Chief Digital Officer" OR "Head of Digital Transformation") AND (Group OR Holding)`
— Headcount 201–500, 501–1000.

### E. Founder-led scale-ups (Advisory)
`(Founder OR "Co-Founder" OR CEO OR "Managing Director") AND (SaaS OR startup OR technology OR software OR platform)`
— Geo = Dubai / Abu Dhabi; Industry = Software; Headcount 11–50; +Keywords `"Dubai Internet City" OR Hub71 OR Dtec`.

### F. Government-adjacent / digital services
`("Head of Technology" OR CTO OR "Director of Engineering" OR "Solutions Director") AND ("digital transformation" OR "smart city" OR government OR "public sector" OR GovTech)`
— Geo = Abu Dhabi / Dubai; Headcount 51–500.

---

## Seeding OpenOutreach (cold-start)

The Gaussian-Process qualifier cannot fit with fewer than 2 labels. For EACH campaign:
1. From the searches above, hand-pick **15–20 ideal prospects** → collect their `public_identifier` (the
   `/in/<slug>/` part of the URL).
2. Add them as the campaign's seed profiles and **label them positive**.
3. Add **5–10 crisp negatives** (recruiters, agency owners, ICs, students) and label them negative.
4. Now BALD explore/exploit has signal and the `min_ready_to_connect_prob = 0.9` gate promotes only strong matches.

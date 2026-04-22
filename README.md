<p align="center">
  <a href="https://myclaw.ai">
    <img src="https://img.shields.io/badge/Created%20%26%20Maintained%20by-MyClaw.ai-2563eb?style=for-the-badge" alt="Created and maintained by MyClaw.ai">
  </a>
</p>

<h1 align="center"><b>Google Ads Master in MyClaw.ai</b></h1>

<p align="center">
  <b>A clean, reusable Google Ads AgentSkill for onboarding, KPI-safe audits, conversion diagnostics, and paused campaign creation.</b>
</p>

<p align="center">
  Part of the <a href="https://myclaw.ai"><b>MyClaw.ai ecosystem</b></a> — created and maintained by <a href="https://myclaw.ai"><b>MyClaw.ai</b></a>.
</p>

---

## What this project is

**Google Ads Master in MyClaw.ai** is an AgentSkill that gives an AI agent a professional workflow for Google Ads operations.

Instead of jumping straight into campaign changes, it forces a safer process:

1. **Onboard the account properly**
2. **Confirm the real KPI first**
3. **Analyze by campaign type, intent, and conversion action**
4. **Recommend clear actions**
5. **Create paused campaign skeletons before anything goes live**

This makes it suitable for:

- Google Ads account audits
- Purchase / lead / signup conversion diagnostics
- Search term and keyword analysis
- Low CTR investigations
- Safe campaign structure creation
- Team workflows where AI should assist without blindly changing live spend

---

## Why it exists

Most Google Ads accounts become messy for the same reasons:

- mixed conversion actions in the UI
- unclear KPI definitions
- inconsistent naming conventions
- low CTR campaigns with no structured diagnosis
- live edits made too early
- broad recommendations with no reproducible workflow

This skill solves that by turning Google Ads work into a **repeatable operating system**.

---

## Built for safe AI-assisted Google Ads work

### Key principles

- **No live credentials included**
- **No default customer ID included**
- **No default MCC ID included**
- **No default conversion action included**
- **No business-specific keywords or offers preloaded**
- **All new campaigns, ad groups, and keywords are created as `PAUSED` by default**
- **The user must provide their own Google Ads config**

That means this repository is intentionally blank where it matters.
It is designed to be installed into a new environment and filled in through onboarding.

---

## What it can do

### 1. Onboarding
Collects the account context an agent actually needs before doing useful work:

- customer ID / MCC / auth config
- business model and offer
- target markets and languages
- primary conversion action
- budget and bidding constraints
- keyword buckets, negatives, and messaging guardrails

### 2. Analysis
Helps an agent interpret performance correctly across:

- **Search**
- **PMax**
- **Demand Gen**
- **Display / Video / App**

With the right diagnostic lens:

- CTR
- CPC
- CPA
- ROAS
- Search IS
- Rank Lost IS
- Budget Lost IS
- conversion-action-specific performance

### 3. Controlled writes
Creates safe **paused** campaign skeletons from a JSON spec, so teams can review before enabling.

---

## Repository structure

```text
.
├── SKILL.md
├── scripts/
│   ├── gads_client.py
│   ├── report_campaigns.py
│   ├── purchase_keywords.py
│   └── create_search_skeleton.py
└── references/
    ├── onboarding-checklist.md
    ├── analysis-playbook.md
    ├── gaql-patterns.md
    └── campaign-build-spec.md
```

---

## Script examples

### Campaign diagnostics

```bash
python3 scripts/report_campaigns.py \
  --customer-id 1234567890 \
  --days 10 \
  --config /path/to/google_ads_config.json
```

### Primary conversion keyword analysis

```bash
python3 scripts/purchase_keywords.py \
  --customer-id 1234567890 \
  --days 10 \
  --purchase-name "Primary Conversion" \
  --config /path/to/google_ads_config.json
```

### Create paused Search campaign skeletons

```bash
python3 scripts/create_search_skeleton.py \
  --customer-id 1234567890 \
  --spec /tmp/spec.json \
  --config /path/to/google_ads_config.json \
  --dry-run
```

---

## Who this is for

This project is useful if you are:

- an operator managing Google Ads across multiple accounts
- a founder who wants AI help without unsafe account edits
- an agency standardizing audit and build workflows
- a growth team that needs structured diagnostics, not vague advice
- a MyClaw.ai ecosystem user building reusable growth capabilities

---

## Part of the MyClaw.ai ecosystem

This project is **created and maintained by <a href="https://myclaw.ai">MyClaw.ai</a>**.

It is intended to be one capability inside a broader ecosystem of agent-powered workflows for:

- growth operations
- campaign analysis
- design systems
- creative production
- automation infrastructure

If you want more projects like this, visit:

<p align="center">
  <a href="https://myclaw.ai"><b>https://myclaw.ai</b></a>
</p>

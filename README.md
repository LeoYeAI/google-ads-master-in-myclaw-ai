# Google Ads Master in MyClaw.ai

A clean, reusable AgentSkill for Google Ads operators.

This skill gives an AI agent a structured workflow for Google Ads onboarding, auditing, reporting, and safe campaign creation. It is intentionally blank by default: no account IDs, no tokens, no business-specific keywords, no preloaded offers, and no assumptions about which conversion action matters.

## What it does

- Guides new users through Google Ads onboarding
- Collects account config, business goals, conversion actions, keyword strategy, budgets, and write permissions
- Runs account and campaign performance diagnostics
- Analyzes Search, PMax, Demand Gen, and other campaign types with the right metric context
- Separates mixed Google Ads conversions from user-confirmed primary conversion actions
- Investigates low CTR using query intent, match type, Search IS, Rank Lost IS, Budget Lost IS, and ad-query fit
- Creates paused Search campaign / ad group / keyword skeletons from a JSON spec
- Verifies writes with GAQL readback

## Why it exists

Most Google Ads accounts become hard to reason about because UI conversions are mixed, campaign naming is inconsistent, and ad changes are made directly in live campaigns.

This skill forces a safer workflow:

1. Understand the account and business first
2. Confirm the real KPI before judging performance
3. Analyze by conversion action, intent, campaign type, and geography
4. Recommend clear actions
5. If writing to the account, create paused objects first and verify them

## Safety principles

- No live credentials are included
- No default customer ID is included
- No default MCC ID is included
- No default conversion action is included
- New campaigns, ad groups, and keywords are created as `PAUSED` unless the user explicitly asks otherwise
- The user must provide their own Google Ads client config

## Structure

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

## Example usage

```bash
python3 scripts/report_campaigns.py \
  --customer-id 1234567890 \
  --days 10 \
  --config /path/to/google_ads_config.json

python3 scripts/purchase_keywords.py \
  --customer-id 1234567890 \
  --days 10 \
  --purchase-name "Primary Conversion" \
  --config /path/to/google_ads_config.json

python3 scripts/create_search_skeleton.py \
  --customer-id 1234567890 \
  --spec /tmp/spec.json \
  --config /path/to/google_ads_config.json \
  --dry-run
```

## Install

Clone this folder into your agent skills directory, then ask your agent to audit or operate Google Ads. The skill will first collect the information it needs before reading or writing account data.

```bash
git clone https://github.com/LeoYeAI/google-ads-master-in-myclaw-ai.git ~/.openclaw/skills/google-ads-master-in-myclaw-ai
```

## Required setup

The user must provide a Google Ads Python client config JSON with:

- developer token
- OAuth client ID
- OAuth client secret
- refresh token
- optional login customer ID / MCC
- `use_proto_plus: true`

No credential file is shipped with this repository.

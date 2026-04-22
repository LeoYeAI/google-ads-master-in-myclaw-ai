---
name: google-ads-master-in-myclaw-ai
description: "Google Ads expert workflow for onboarding, account analysis, conversion-value diagnostics, campaign/search term/keyword/geography reports, low CTR investigations, and creating paused Search campaigns/ad groups/keywords via the google-ads Python client. For a new installation, first collect the user's account config, business goals, conversion actions, keywords, offers, budgets, and guardrails before analysis or writes."
---

# Google Ads Master

Use this skill for Google Ads onboarding, analysis, and controlled account operations.

## Core rules

- Default language: match the user; keep Google Ads terms in English: CTR, CPC, CPA, ROAS, Search IS, Rank Lost IS, Purchase.
- **Primary KPI must be user-defined during onboarding**. Do not assume Purchase, lead, signup, or any specific conversion action.
- Never trust mixed Google Ads UI conversions until the user confirms which conversion action(s) matter.
- New campaigns should default to **Maximize Conversions** unless the user chooses another bidding strategy.
- Any write operation must be explicit and safe:
  - create campaigns/ad groups/keywords **PAUSED** unless user clearly asks to enable
  - summarize IDs and status after writes
  - do not edit budgets/bids/enabled status without confirmation
- Prefer `google-ads` Python client (gRPC). REST may be incomplete for Google Ads.

## New-user onboarding first

Before analysis or account writes for a new installation, collect the required setup data in `references/onboarding-checklist.md`.

Minimum required before reads:

- Google Ads customer ID and optional MCC login customer ID
- OAuth / service auth path or confirmation that existing auth is configured
- developer token source
- reporting timezone and date range

Minimum required before performance recommendations:

- business model and product/service
- primary conversion action name/ID
- revenue/value source and ROAS/CPA target
- target countries/languages
- campaign types in use

Minimum required before writes:

- explicit permission to create/update
- daily budgets
- bidding strategy
- campaign/ad group naming convention
- landing page URLs and tracking requirements
- keyword list, match types, negatives
- ad copy claims and compliance guardrails

## Standard workflow

1. Check whether onboarding data is complete. If not, ask for the missing items from `references/onboarding-checklist.md`.
2. Clarify task type:
   - onboarding / setup
   - account/campaign performance analysis
   - conversion-action-specific keyword/search term analysis
   - low CTR diagnosis
   - campaign creation/update
3. Run the relevant script in `scripts/` when possible.
4. Interpret results using the user's confirmed business rules:
   - use their primary conversion action first
   - do not trust mixed conversion CPA alone
   - segment intent buckets based on the user's actual market and keywords
5. Give concrete actions:
   - keep / observe / reduce / pause / split / add negatives
   - include campaign/keyword names and metrics
6. For writes, verify after mutation with a GAQL readback.

## Scripts

- `scripts/gads_client.py` — shared client/config helpers.
- `scripts/report_campaigns.py` — recent campaign summary, CTR/ROAS/IS diagnostics.
- `scripts/purchase_keywords.py` — keyword-level primary-conversion report.
- `scripts/create_search_skeleton.py` — create paused Search campaigns/ad groups/keywords from a JSON spec.

Run scripts from the skill directory or pass absolute paths. Examples:

```bash
python3 <skill-dir>/scripts/report_campaigns.py --customer-id 1234567890 --days 10 --config /path/to/google_ads_config.json
python3 <skill-dir>/scripts/purchase_keywords.py --customer-id 1234567890 --days 10 --purchase-name "Primary Conversion" --config /path/to/google_ads_config.json
python3 <skill-dir>/scripts/create_search_skeleton.py --customer-id 1234567890 --spec /tmp/spec.json --config /path/to/google_ads_config.json --dry-run
```

## References

Read these only when needed:

- `references/onboarding-checklist.md` — what to collect from a new user before using the skill.
- `references/analysis-playbook.md` — generic Google Ads interpretation heuristics.
- `references/gaql-patterns.md` — GAQL query patterns and API caveats.
- `references/campaign-build-spec.md` — JSON spec format for campaign creation.

## Safety checklist before write

- Is this a read-only analysis? If yes, do not mutate.
- Did the user ask to create/update? If yes, create PAUSED by default.
- Are budgets explicit? If not, ask or use conservative defaults and keep paused.
- After write, read back:
  - campaign id/name/status/budget
  - ad group id/status
  - keyword text/match/status
- Tell the user what is created and what is still not enabled.

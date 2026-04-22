# Generic Google Ads Analysis Playbook

## Metrics hierarchy

Use the user's confirmed primary conversion action first. Common examples:

- Purchase ROAS for e-commerce / SaaS revenue
- Qualified lead CPA for lead gen
- Trial-to-paid ROAS or CAC for SaaS
- Booked call CPA for sales-led offers

Do not rely on mixed UI conversions until conversion actions are segmented.

## Campaign type caveats

- Search CTR is not comparable to PMax / Demand Gen / Display CTR.
- PMax and Demand Gen should be judged more by conversion quality, placement/audience fit, creative asset quality, and incremental value.
- Search low CTR usually means query intent, match type, ad rank, or ad-query relevance problems.

## Search diagnostics

For each Search campaign, inspect:

- CTR and CPC
- conversion-action-specific CPA/ROAS
- Search IS
- Rank Lost IS
- Budget Lost IS
- keyword match type mix
- search term drift
- ad copy relevance

Interpretation:

- High Rank Lost IS: ad rank / bid / quality issue, not mainly budget.
- High Budget Lost IS: budget cap issue; only increase budget if conversion quality is acceptable.
- High CTR + weak conversion: landing page / offer / wrong intent issue.
- Low CTR + high impressions: broad matching, weak ad-query fit, or low SERP position.

## Intent segmentation template

Customize buckets for each user. Common buckets:

- Brand exact
- Brand variants / misspellings
- Competitor
- High-intent problem/solution
- Implementation / install / setup
- Pricing / comparison
- Informational research
- Support / login / docs
- Broad generic category

## Recommendation format

For every audit, return:

1. Executive summary
2. What is working
3. What is wasting spend
4. What to split or restructure
5. What to pause/reduce/watch
6. What to test next
7. What data is missing or unreliable

## Write recommendation safety

Prefer creating paused experiments over editing live winners. Before writes, state:

- exact objects to create/change
- budget
- bidding strategy
- status
- tracking/URL assumptions
- rollback plan

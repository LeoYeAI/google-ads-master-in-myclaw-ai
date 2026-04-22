# GAQL Patterns and Caveats

## Campaign performance

```sql
SELECT
  campaign.id,
  campaign.name,
  campaign.status,
  campaign.advertising_channel_type,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.search_impression_share,
  metrics.search_rank_lost_impression_share,
  metrics.search_budget_lost_impression_share
FROM campaign
WHERE segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
```

## Search terms

```sql
SELECT
  search_term_view.search_term,
  campaign.name,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value
FROM search_term_view
WHERE segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
  AND metrics.impressions > 0
```

Caveat: `search_term_view` cannot reliably select `segments.conversion_action` together with clicks/cost/impressions. For Purchase-only decisions, use keyword-level conversion segmentation or separate reports.

## Keyword Purchase segmentation

```sql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_criterion.criterion_id,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  segments.conversion_action_name,
  metrics.conversions,
  metrics.conversions_value
FROM keyword_view
WHERE segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
  AND segments.conversion_action_name = '<USER_PRIMARY_CONVERSION_ACTION_NAME>'
```

Ask the user for the conversion action name/ID during onboarding. Then merge with a separate keyword cost query by `(campaign.id, ad_group.id, criterion_id)`.

## Campaign creation caveats

- New campaign creation requires `contains_eu_political_advertising`.
- Keep new campaigns `PAUSED` by default.
- Read back after mutation.
- Some proto fields may differ by library version; if `start_date` is unavailable, omit it and rely on PAUSED status.

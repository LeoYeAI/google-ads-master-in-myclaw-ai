# Campaign Build Spec

Use with `scripts/create_search_skeleton.py`.

## Example

```json
{
  "campaigns": [
    {
      "name": "0417-Claude-Bot-Intent",
      "daily_budget": 100,
      "ad_groups": [
        {
          "name": "Claude Bot",
          "cpc_bid": 4.0,
          "keywords": [
            {"text": "example keyword one", "match_type": "EXACT"},
            {"text": "example keyword one", "match_type": "PHRASE"},
            {"text": "example keyword two", "match_type": "EXACT"}
          ]
        }
      ]
    }
  ]
}
```

## Notes

- Campaigns are created as Search campaigns in `PAUSED` status.
- Ad groups are created in `PAUSED` status.
- Keywords are created in `PAUSED` status.
- Use this script to build safe skeletons first; add ads later after review.

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from gads_client import load_client, search


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=10)
    ap.add_argument("--customer-id", required=True)
    ap.add_argument("--login-customer-id")
    ap.add_argument("--config")
    args = ap.parse_args()

    client = load_client(config_path=args.config, login_customer_id=args.login_customer_id)
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=args.days - 1)

    query = f"""
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
    WHERE segments.date BETWEEN '{start}' AND '{end}'
      AND campaign.status != 'REMOVED'
    ORDER BY metrics.cost_micros DESC
    """

    rows = []
    for row in search(client, query, customer_id=args.customer_id):
        rows.append({
            "id": row.campaign.id,
            "name": row.campaign.name,
            "status": row.campaign.status.name,
            "channel": row.campaign.advertising_channel_type.name,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "ctr": row.metrics.ctr,
            "avg_cpc": row.metrics.average_cpc / 1e6 if row.metrics.average_cpc else 0,
            "cost": row.metrics.cost_micros / 1e6,
            "conversions": row.metrics.conversions,
            "value": row.metrics.conversions_value,
            "roas": (row.metrics.conversions_value / (row.metrics.cost_micros / 1e6)) if row.metrics.cost_micros else 0,
            "search_is": row.metrics.search_impression_share,
            "rank_lost_is": row.metrics.search_rank_lost_impression_share,
            "budget_lost_is": row.metrics.search_budget_lost_impression_share,
        })

    print(json.dumps({"start": str(start), "end": str(end), "campaigns": rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

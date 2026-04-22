#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import date, timedelta
from gads_client import load_client, search

DEFAULT_PURCHASE_NAME = None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=10)
    ap.add_argument("--customer-id", required=True)
    ap.add_argument("--login-customer-id")
    ap.add_argument("--config")
    ap.add_argument("--purchase-name", required=False)
    args = ap.parse_args()

    purchase_name = args.purchase_name or DEFAULT_PURCHASE_NAME
    if not purchase_name:
        raise ValueError("--purchase-name is required unless a default is configured")

    client = load_client(config_path=args.config, login_customer_id=args.login_customer_id)
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=args.days - 1)

    q_cost = f"""
    SELECT
      campaign.id,
      campaign.name,
      ad_group.id,
      ad_group.name,
      ad_group_criterion.criterion_id,
      ad_group_criterion.keyword.text,
      ad_group_criterion.keyword.match_type,
      metrics.impressions,
      metrics.clicks,
      metrics.cost_micros
    FROM keyword_view
    WHERE segments.date BETWEEN '{start}' AND '{end}'
      AND metrics.impressions > 0
    ORDER BY metrics.cost_micros DESC
    """
    q_purchase = f"""
    SELECT
      campaign.id,
      campaign.name,
      ad_group.id,
      ad_group.name,
      ad_group_criterion.criterion_id,
      ad_group_criterion.keyword.text,
      ad_group_criterion.keyword.match_type,
      segments.conversion_action_name,
      metrics.conversions,
      metrics.conversions_value
    FROM keyword_view
    WHERE segments.date BETWEEN '{start}' AND '{end}'
      AND segments.conversion_action_name = '{purchase_name}'
    ORDER BY metrics.conversions_value DESC
    """

    merged = {}
    for row in search(client, q_cost, customer_id=args.customer_id):
        k = (row.campaign.id, row.ad_group.id, row.ad_group_criterion.criterion_id)
        merged[k] = {
            "campaign": row.campaign.name,
            "ad_group": row.ad_group.name,
            "keyword": row.ad_group_criterion.keyword.text,
            "match_type": row.ad_group_criterion.keyword.match_type.name,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "cost": row.metrics.cost_micros / 1e6,
            "purchase": 0,
            "purchase_value": 0,
        }

    for row in search(client, q_purchase, customer_id=args.customer_id):
        k = (row.campaign.id, row.ad_group.id, row.ad_group_criterion.criterion_id)
        if k not in merged:
            merged[k] = {
                "campaign": row.campaign.name,
                "ad_group": row.ad_group.name,
                "keyword": row.ad_group_criterion.keyword.text,
                "match_type": row.ad_group_criterion.keyword.match_type.name,
                "impressions": 0,
                "clicks": 0,
                "cost": 0,
                "purchase": 0,
                "purchase_value": 0,
            }
        merged[k]["purchase"] += row.metrics.conversions
        merged[k]["purchase_value"] += row.metrics.conversions_value

    rows = []
    for row in merged.values():
        row["purchase_roas"] = row["purchase_value"] / row["cost"] if row["cost"] else 0
        row["purchase_cpa"] = row["cost"] / row["purchase"] if row["purchase"] else None
        rows.append(row)

    rows.sort(key=lambda x: x["cost"], reverse=True)
    print(json.dumps({"start": str(start), "end": str(end), "purchase_action": purchase_name, "keywords": rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

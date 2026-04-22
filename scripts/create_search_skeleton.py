#!/usr/bin/env python3
"""Create paused Search campaign skeletons from JSON.

Spec format is documented in references/campaign-build-spec.md.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from gads_client import load_client


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--customer-id", required=True)
    ap.add_argument("--login-customer-id")
    ap.add_argument("--config")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    spec = json.loads(Path(args.spec).read_text())

    if args.dry_run:
        print(json.dumps({"dry_run": True, "spec": spec}, ensure_ascii=False, indent=2))
        return

    client = load_client(config_path=args.config, login_customer_id=args.login_customer_id)
    budget_service = client.get_service("CampaignBudgetService")
    campaign_service = client.get_service("CampaignService")
    ad_group_service = client.get_service("AdGroupService")
    criterion_service = client.get_service("AdGroupCriterionService")

    created = []
    for camp in spec["campaigns"]:
        name = camp["name"]
        daily = float(camp["daily_budget"])

        b_op = client.get_type("CampaignBudgetOperation")
        b = b_op.create
        b.name = f"{name} Budget {int(time.time()*1000)}"
        b.amount_micros = int(daily * 1_000_000)
        b.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
        b.explicitly_shared = False
        budget_rn = budget_service.mutate_campaign_budgets(customer_id=args.customer_id, operations=[b_op]).results[0].resource_name

        c_op = client.get_type("CampaignOperation")
        c = c_op.create
        c.name = name
        c.status = client.enums.CampaignStatusEnum.PAUSED
        c.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
        c.campaign_budget = budget_rn
        c.manual_cpc.enhanced_cpc_enabled = False
        c.network_settings.target_google_search = True
        c.network_settings.target_search_network = True
        c.network_settings.target_content_network = False
        c.network_settings.target_partner_search_network = False
        c.contains_eu_political_advertising = client.enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
        campaign_rn = campaign_service.mutate_campaigns(customer_id=args.customer_id, operations=[c_op]).results[0].resource_name

        adgroups_created = []
        for ag in camp.get("ad_groups", []):
            ag_op = client.get_type("AdGroupOperation")
            adg = ag_op.create
            adg.name = ag["name"]
            adg.campaign = campaign_rn
            adg.status = client.enums.AdGroupStatusEnum.PAUSED
            adg.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
            adg.cpc_bid_micros = int(float(ag.get("cpc_bid", 2.0)) * 1_000_000)
            adg_rn = ad_group_service.mutate_ad_groups(customer_id=args.customer_id, operations=[ag_op]).results[0].resource_name

            kw_ops = []
            for kw in ag.get("keywords", []):
                op = client.get_type("AdGroupCriterionOperation")
                crit = op.create
                crit.ad_group = adg_rn
                crit.status = client.enums.AdGroupCriterionStatusEnum.PAUSED
                crit.keyword.text = kw["text"]
                crit.keyword.match_type = getattr(client.enums.KeywordMatchTypeEnum, kw.get("match_type", "PHRASE").upper())
                kw_ops.append(op)
            kw_results = []
            if kw_ops:
                resp = criterion_service.mutate_ad_group_criteria(customer_id=args.customer_id, operations=kw_ops)
                kw_results = [r.resource_name for r in resp.results]
            adgroups_created.append({"name": ag["name"], "resource": adg_rn, "keywords": kw_results})

        created.append({"name": name, "campaign": campaign_rn, "budget": budget_rn, "ad_groups": adgroups_created})

    print(json.dumps({"created_paused": created}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

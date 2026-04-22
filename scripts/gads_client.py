#!/usr/bin/env python3
"""Shared Google Ads client helpers for a generic installation."""
from __future__ import annotations

import json
from pathlib import Path
from google.ads.googleads.client import GoogleAdsClient

DEFAULT_CUSTOMER_ID = None
DEFAULT_LOGIN_CUSTOMER_ID = None
TOKEN_FILE = None

CONFIG = {
    "developer_token": "YOUR_DEVELOPER_TOKEN",
    "client_id": "YOUR_OAUTH_CLIENT_ID",
    "client_secret": "YOUR_OAUTH_CLIENT_SECRET",
    "use_proto_plus": True,
}


def load_client(config_path: str | None = None, login_customer_id: str | None = None) -> GoogleAdsClient:
    """Load client from a supplied JSON config.

    Pass a complete Google Ads client config JSON file via --config.
    This skill intentionally avoids shipping live account paths or secrets.
    """
    if not config_path:
        raise ValueError("config_path is required")

    cfg = json.loads(Path(config_path).read_text())
    if login_customer_id:
        cfg["login_customer_id"] = login_customer_id
    elif DEFAULT_LOGIN_CUSTOMER_ID and "login_customer_id" not in cfg:
        cfg["login_customer_id"] = DEFAULT_LOGIN_CUSTOMER_ID
    return GoogleAdsClient.load_from_dict(cfg)


def search(client: GoogleAdsClient, query: str, customer_id: str | None = None):
    service = client.get_service("GoogleAdsService")
    cid = customer_id or DEFAULT_CUSTOMER_ID
    if not cid:
        raise ValueError("customer_id is required")
    for batch in service.search_stream(customer_id=cid, query=query):
        for row in batch.results:
            yield row

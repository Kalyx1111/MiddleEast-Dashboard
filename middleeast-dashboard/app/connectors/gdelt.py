"""GDELT DOC 2.0 API - free, no key. English-source filter enforced upstream
(sourcelang:eng). Requests are PACED (GDELT asks clients not to flood it) and
a 429 is retried once after a pause; every failure reports its real HTTP
status or response type so the status panel tells you what happened."""
from __future__ import annotations
import json
import time
from .base import Item, ConnectorResult
from ..classify import classify

NAME = "gdelt"
ENDPOINT = "https://api.gdeltproject.org/api/v2/doc/doc"
PACE_SECONDS = 6.0          # spacing between queries
BACKOFF_SECONDS = 20.0      # pause before the single retry on HTTP 429

QUERIES = [
    "Iran war sourcelang:eng",
    "Iran missile strikes Gulf sourcelang:eng",
    "Strait of Hormuz shipping sourcelang:eng",
    "Israel Iran missile sourcelang:eng",
    "Hezbollah Israel Lebanon sourcelang:eng",
    "Gaza ceasefire sourcelang:eng",
    "Houthi Red Sea sourcelang:eng",
    "Bab el-Mandeb sourcelang:eng",
    "Al Udeid Qatar base sourcelang:eng",
    "Bahrain Fifth Fleet sourcelang:eng",
    "Kuwait Ali Al Salem sourcelang:eng",
    "UAE Al Dhafra sourcelang:eng",
    "Saudi Arabia Iran strikes sourcelang:eng",
    "Oman Duqm Salalah sourcelang:eng",
    "Iraq militia US bases sourcelang:eng",
    "Syria Russia Hmeimim Tartus sourcelang:eng",
    "Syria Israel strikes sourcelang:eng",
    "Iran nuclear IAEA Bushehr sourcelang:eng",
    "Natanz Fordow Isfahan sourcelang:eng",
    "Iran drone missile production sourcelang:eng",
    "Iranian navy Bandar Abbas sourcelang:eng",
    "Israel navy Haifa submarine sourcelang:eng",
    "Turkey navy Golcuk submarine sourcelang:eng",
    "Turkey defence industry Baykar ASELSAN sourcelang:eng",
    "Egypt Suez Canal sourcelang:eng",
    "Jordan Iran war sourcelang:eng",
    "Cyprus Akrotiri British bases sourcelang:eng",
    "Qatar LNG Ras Laffan sourcelang:eng",
    "Yemen Houthi attacks Israel sourcelang:eng",
    "Iran ceasefire talks Pakistan sourcelang:eng",
    "Lebanon ceasefire Israel talks sourcelang:eng",
]


def configured() -> bool:
    return True


def _get(safe_http, q):
    params = {"query": q, "mode": "ArtList", "format": "json", "timespan": "3d",
              "maxrecords": "40", "sort": "DateDesc"}
    r = safe_http.safe_get(ENDPOINT, params=params)
    if r.status_code == 429:
        time.sleep(BACKOFF_SECONDS)
        r = safe_http.safe_get(ENDPOINT, params=params)
    return r


def fetch() -> ConnectorResult:
    from .. import safe_http
    items, errors = [], []
    for i, q in enumerate(QUERIES):
        if i:
            time.sleep(PACE_SECONDS)
        try:
            r = _get(safe_http, q)
            if r.status_code != 200:
                errors.append(f"'{q.split(' sourcelang')[0]}': HTTP {r.status_code}")
                continue
            try:
                data = json.loads(r.content)
            except ValueError:
                errors.append(f"'{q.split(' sourcelang')[0]}': non-JSON response (service busy or changed)")
                continue
            for a in data.get("articles", []):
                title = (a.get("title") or "").strip()
                if not title:
                    continue
                items.append(Item(
                    category=classify(title), label=title[:90], text=title,
                    source=a.get("domain", "GDELT"), date=a.get("seendate", ""),
                    url=a.get("url"), connector=NAME,
                ).to_dict())
        except safe_http.FetchError as e:
            errors.append(f"'{q.split(' sourcelang')[0]}': blocked ({e})")
        except Exception as e:
            errors.append(f"'{q.split(' sourcelang')[0]}': {type(e).__name__}")
    if not items and errors:
        return ConnectorResult(NAME, True, False, "; ".join(errors)[:300])
    msg = f"{len(items)} items across {len(QUERIES)} topic queries"
    if errors:
        msg += f" ({len(errors)} failed: {'; '.join(errors)[:200]})"
    return ConnectorResult(NAME, True, True, msg, items)

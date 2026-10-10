"""RSS aggregator - free, no key. English-language feeds only.

Feed URLs are either confirmed from a publisher's own feed (SpaceNews returned
live items during verification), or listed in a feed directory (FeedSpot)
pending the connector's own live check. Each feed reports its own status and
fails independently. World-wide feeds keep only region-relevant headlines.
"""
from __future__ import annotations
import re
from .base import Item, ConnectorResult
from ..classify import classify

NAME = "rss"

FEEDS = [
    {"url": "https://tehrantimes.com/rss", "source": "Tehran Times (Iran)"},
    {"url": "https://en.mehrnews.com/rss", "source": "Mehr News (Iran)"},
    {"url": "https://feeds.iranherald.com/rss/1b76a2b4cf7810bd", "source": "Iran Focus"},
    {"url": "https://www.thetower.org/tag/iran-news/feed/", "source": "The Tower (Iran)"},
    {"url": "https://globalvoices.org/-/world/middle-east-north-africa/iran/feed/", "source": "Global Voices (Iran)"},
    {"url": "https://globalvoices.org/-/world/middle-east-north-africa/yemen/feed/", "source": "Global Voices (Yemen)"},
    {"url": "https://globalvoices.org/-/world/middle-east-north-africa/egypt/feed/", "source": "Global Voices (Egypt)"},
    {"url": "https://www.jpost.com/rss/rssallnews", "source": "The Jerusalem Post (all news)"},
    {"url": "https://www.jpost.com/rss/rssfeedsiran", "source": "The Jerusalem Post (Iran)"},
    {"url": "https://www.jpost.com/rss/israel-hamas-war", "source": "The Jerusalem Post (Israel-Hamas war)"},
    {"url": "https://www.haaretz.com/srv/israel-news-rss", "source": "Haaretz (Israel)"},
    {"url": "https://www.haaretz.com/srv/middle-east-news-rss", "source": "Haaretz (Middle East)"},
    {"url": "https://www.timesofisrael.com/israel-inside/feed/", "source": "The Times of Israel (Israel)"},
    {"url": "https://www.arabnews.com/taxonomy/term/2/feed", "source": "Arab News (Middle East)"},
    {"url": "https://www.aa.com.tr/en/rss/default?cat=live", "source": "Anadolu Agency (live)"},
    {"url": "https://www.aljazeera.com/xml/rss/all.xml", "source": "Al Jazeera"},
    {"url": "https://feeds.bbci.co.uk/news/world/middle_east/rss.xml", "source": "BBC News - Middle East"},
    {"url": "https://www.twz.com/category/iran/feed", "source": "The War Zone (Iran)"},
    {"url": "https://www.foreignaffairs.com/feeds/region/iran/rss.xml", "source": "Foreign Affairs (Iran)"},
    {"url": "https://eaworldview.com/topics/iran/feed/", "source": "EA WorldView (Iran)"},
    {"url": "https://www.euronews.com/rss?level=tag&name=us-iran-crisis", "source": "Euronews (US-Iran crisis)"},
    {"url": "https://breakingdefense.com/feed", "source": "Breaking Defense"},
    {"url": "https://therecord.media/feed", "source": "The Record (cyber)"},
    {"url": "https://news.usni.org/feed", "source": "USNI News (naval)"},
    {"url": "https://news.google.com/rss/search?q=Iran+war+Gulf&hl=en-US&gl=US&ceid=US:en", "source": "Google News: Iran war and the Gulf (Gulf and international press)"},
    {"url": "https://news.google.com/rss/search?q=Strait+of+Hormuz&hl=en-US&gl=US&ceid=US:en", "source": "Google News: Strait of Hormuz"},
    {"url": "https://news.google.com/rss/search?q=Hezbollah+Lebanon+Israel&hl=en-US&gl=US&ceid=US:en", "source": "Google News: Lebanon and Hezbollah"},
    {"url": "https://news.google.com/rss/search?q=Gaza+ceasefire&hl=en-US&gl=US&ceid=US:en", "source": "Google News: Gaza ceasefire"},
    {"url": "https://news.google.com/rss/search?q=Houthi+Yemen+Red+Sea&hl=en-US&gl=US&ceid=US:en", "source": "Google News: Yemen and the Red Sea"},
    {"url": "https://news.google.com/rss/search?q=Syria+Russia+bases+Tartus+Hmeimim&hl=en-US&gl=US&ceid=US:en", "source": "Google News: Syria and Russian bases"},
    {"url": "https://news.google.com/rss/search?q=Saudi+Arabia+UAE+Qatar+Iran&hl=en-US&gl=US&ceid=US:en", "source": "Google News: Saudi Arabia, UAE and Qatar"},
    {"url": "https://news.google.com/rss/search?q=Turkey+navy+submarine+defence+industry&hl=en-US&gl=US&ceid=US:en", "source": "Google News: Turkey defence"},
]

WORLD_WIDE_SOURCES = ('Tehran Times (Iran)', 'Mehr News (Iran)', 'Iran Focus', 'The Tower (Iran)', 'Global Voices (Iran)', 'Global Voices (Yemen)', 'Global Voices (Egypt)', 'The Jerusalem Post (all news)', 'The Jerusalem Post (Iran)', 'The Jerusalem Post (Israel-Hamas war)', 'Haaretz (Israel)', 'Haaretz (Middle East)', 'The Times of Israel (Israel)', 'Arab News (Middle East)', 'Anadolu Agency (live)', 'Al Jazeera', 'BBC News - Middle East', 'The War Zone (Iran)', 'Foreign Affairs (Iran)', 'EA WorldView (Iran)', 'Euronews (US-Iran crisis)', 'Breaking Defense', 'The Record (cyber)', 'USNI News (naval)')
REGION_TERMS = ["iran", "iranian", "tehran", "israel", "israeli", "gaza", "west bank", "hamas", "hezbollah", "lebanon", "beirut", "syria", "damascus", "iraq", "baghdad", "erbil", "jordan", "amman", "saudi", "riyadh", "uae", "emirates", "abu dhabi", "dubai", "qatar", "doha", "kuwait", "bahrain", "manama", "oman", "muscat", "yemen", "houthi", "sanaa", "aden", "egypt", "cairo", "suez", "sinai", "turkey", "turkish", "ankara", "istanbul", "cyprus", "nicosia", "hormuz", "bab el-mandeb", "red sea", "gulf", "persian gulf", "centcom", "fifth fleet", "al udeid", "bushehr", "natanz", "fordow", "isfahan", "haifa", "tartus", "hmeimim", "iaea", "middle east"]


def configured() -> bool:
    return True


def _looks_english(text: str) -> bool:
    if not text:
        return False
    latin = sum(1 for c in text if c.isascii() and c.isalpha())
    letters = sum(1 for c in text if c.isalpha())
    if letters == 0:
        return True
    return (latin / letters) > 0.6


def _relevant(title: str, source: str) -> bool:
    if not source.startswith(WORLD_WIDE_SOURCES):
        return True
    t = title.lower()
    return any(re.search(r'\b' + re.escape(term) + r'\b', t) for term in REGION_TERMS)


def fetch(per_feed_limit: int = 15) -> ConnectorResult:
    from .. import safe_http
    import feedparser
    all_items, errors, ok_feeds = [], [], 0
    for feed in FEEDS:
        try:
            r = safe_http.safe_get(feed["url"])
            if r.status_code != 200:
                errors.append(f"{feed['source']}: HTTP {r.status_code}")
                continue
            parsed = feedparser.parse(r.content)
            if parsed.bozo and not parsed.entries:
                errors.append(f"{feed['source']}: not a readable feed")
                continue
            ok_feeds += 1
            count = 0
            for entry in parsed.entries:
                title = getattr(entry, "title", "").strip()
                if not title or not _looks_english(title) or not _relevant(title, feed["source"]):
                    continue
                all_items.append(Item(
                    category=classify(title), label=title[:90] if len(title) > 90 else title,
                    text=title, source=feed["source"],
                    date=getattr(entry, "published", "") or getattr(entry, "updated", ""),
                    url=getattr(entry, "link", None), connector=NAME,
                ).to_dict())
                count += 1
                if count >= per_feed_limit:
                    break
        except safe_http.FetchError as e:
            errors.append(f"{feed['source']}: blocked ({e})")
        except Exception as e:
            errors.append(f"{feed['source']}: {type(e).__name__}")
    if not all_items and errors:
        return ConnectorResult(NAME, True, False, "; ".join(errors)[:300])
    msg = f"{len(all_items)} items from {ok_feeds} of {len(FEEDS)} feeds"
    if errors:
        msg += f" ({len(errors)} failed: {'; '.join(errors)[:200]})"
    return ConnectorResult(NAME, True, True, msg, all_items)

"""Routes every headline into one of the Chinese dashboard's 15 headings, applied to the Middle East.

Order matters: the most specific headings first (darkweb, cyber, hazard, armed groups, internal security, naval,
chokepoints, air, space, weapons and nuclear programmes, military operations, technology, economy, social, wellbeing),
then geopolitics as the default. Short words are whole words only, so " rat " does not match "rate", " import " does not
match "important", and " ied " does not match "died".
"""
import re

HEADINGS = ["geo", "milops", "arms", "naval", "scs", "air", "space", "tech", "cyber", "darkweb",
            "econ", "mss", "social", "wellbeing", "hazard"]

RULES = [
    ("darkweb", ["dark web", "darknet", "onion", "ransomware", "leak site", "infostealer", "stealer", "data breach",
                 "data leak", "threat intel", "threat intelligence", "initial access broker"]),
    ("cyber", ["cyber", "hacker", "hacked", "hacking", "malware", "vulnerabilit", "intrusion", "phishing", "ddos",
               "zero-day", "cyberattack", "apt33", "apt34", "apt35", "charming kitten", "wiper"]),
    ("hazard", ["earthquake", "tremor", "flood", "floods", "sandstorm", "heatwave", "heat wave", "cyclone", "storm",
                "drought", "wildfire", "locust", "cloudburst"]),
    ("milops", ["hezbollah", "houthi", "houthis", "hamas", "kataib", "popular mobilization", "pmf", "quds force",
                "jaysh al-ghadab", "islamic resistance in iraq"]),
    ("mss", ["mossad", "espionage", "spy", "spying", "sleeper cell", "informant", "intelligence service", "crackdown",
             "executed", "executions", "arrested for", "assassinat", "counterintelligence", "dissident", "interrogation"]),
    ("naval", ["navy", "naval", "submarine", "warship", "frigate", "destroyer", "corvette", "minesweeper", "fifth fleet",
               "irin", "irgc navy", "irgc-n", "shayetet", "gölcük", "golcuk", "haifa naval", "base ship", "midget submarine"]),
    ("scs", ["strait of hormuz", "hormuz", "bab el-mandeb", "bab al-mandab", "red sea", "suez", "blockade", "shipping lane",
             "tanker", "shipping", "gulf of oman", "persian gulf", "tiran", "bosporus", "dardanelles", "sea lane"]),
    ("air", ["air force", "airbase", "air base", "fighter jet", "f-35", "f-15", "f-16", "airspace", "airport", "helicopter",
             "air defense", "air defence", "interceptor", "patriot", "uav"]),
    ("space", ["satellite", "space program", "rocket launch", "orbit", "spacecraft", "space agency"]),
    ("geo", ["talks", "negotiat", "summit", "mediat", "memorandum", "diplomat"]),
    ("arms", ["nuclear", "enrichment", "enrich", "uranium", "reactor", "iaea", "centrifuge", "ballistic", "warhead",
              "munition", "ammunition", "weapons", "drone production", "shahed", "missile production", "rocket fuel",
              "bunker buster", "bunker-buster", "arms deal", "arms sale"]),
    ("milops", ["drone attack", "drone strike", "strike", "strikes", "airstrike", "attack on", "missile attack", "missiles hit", "missiles struck",
                "troops", "army", "soldier", "soldiers", "offensive", "military operation", "invasion", "clashes", "clash",
                "idf", "centcom", "pentagon", "us forces", "u.s. forces", "bases", "base struck", "killed in strike"]),
    ("tech", [" ai ", "artificial intelligence", "chips", "semiconductor", "export control", "digital", "technology"]),
    ("econ", ["oil", "crude", "lng", "gas prices", "trade", "tariff", "sanctions", "exports", "imports", "inflation",
              "economy", "economic", "energy", "brent", "budget", "investment", "fuel prices"]),
    ("social", ["protest", "protests", "human rights", "refugee", "refugees", "displaced", "civilians", "humanitarian",
                "famine", "hunger", "aid workers", "students", "women", "women's rights"]),
    ("wellbeing", ["happiness", "wellbeing", "well-being", "life expectancy", "poverty index", "human development index"]),
]

_SHORT = {"spy", "irin", "pmf", "uav", "uranium", "enrich", "shahed", "bases", "oil", "lng", "tiran", "ied", "mss"}


def _has(text: str, word: str) -> bool:
    if " " in word or "-" in word or "'" in word or "." in word or "/" in word:
        return word in text
    if word in _SHORT or (len(word) <= 4 and word.isalpha()):
        return re.search(r"\b" + re.escape(word) + r"\b", text) is not None
    return word in text


def classify(text: str) -> str:
    t = " " + (text or "").lower() + " "
    for heading, words in RULES:
        if any(_has(t, w) for w in words):
            return heading
    return "geo"

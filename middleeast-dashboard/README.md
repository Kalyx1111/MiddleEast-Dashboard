# MiddleEast Dashboard - v1

Covers the **17 states named in the brief** (Bahrain, Cyprus, Egypt, Iran, Iraq, Israel, Jordan, Kuwait, Lebanon,
Oman, Palestine, Qatar, Saudi Arabia, Syria, Turkey, United Arab Emirates, Yemen) and **100 km around them**. Nothing
outside that margin is drawn. Neighbouring territory appears only inside the margin (for example Greece, Bulgaria,
Libya, Sudan, Eritrea, Djibouti, Somalia, Afghanistan, Pakistan, Turkmenistan, Azerbaijan, Armenia and Georgia, where
they fall within 100 km). The build uses the Chinese dashboard's architecture and its 15 headings and marker categories.

## Local address

**http://127.0.0.1:8810/** (earlier builds: 8787, 8790, 8795, 8800, 8805). Edit `PORT` in `run.py` and `start.bat` to change it.

## Start (Windows)

Double-click `start.bat`. It creates the virtual environment, installs the packages, runs the self-check, starts the
server under the supervisor, and opens the page. The first pass takes a few minutes: GDELT paces its requests (6 seconds
per query, 30 queries).

## The 15 headings (the Chinese dashboard's set)

Geopolitical & Diplomatic - Military Operations & Force Posture - Strategic Arms & Nuclear Program - Naval & Maritime
Security - Gulf, Red Sea & Maritime Chokepoints - Air Force & Aviation - Space Tech & Aerospace - Critical Tech & AI
Governance - Cyber Espionage & APTs - Darkweb & Threat Intel - Economic & Trade (energy, shipping) - Internal Security &
Intelligence Operations - Social Pulse & Public Sentiment - Happiness & Wellbeing Indices - Natural Hazards &
Environmental Risks. Only the chokepoint heading's title differs from China's (the region's straits replace the South China
Sea).

Routing is rule-based (`app/classify.py`). The rules run in order: darkweb, cyber, hazards, armed groups (Hezbollah,
Houthis, Hamas, Iraqi militias) to military operations, internal security, naval, chokepoints, air, space, weapons and
nuclear programmes, diplomacy (talks, memoranda), military operations, technology, economy, social, wellbeing, and
geopolitics by default. Short words match whole words only.

## The map

- **Frame:** the 17 states plus 100 km (lon 23.65 to 64.33, lat 11.21 to 42.99), with the margin drawn as a dashed line.
- **Shaded:** the 17 states. **Outlined:** the neighbours, inside the margin only.
- **Rivers:** 41 lines from Natural Earth (the Nile, Tigris, Euphrates, Jordan and others, within the frame).
- **Towns:** 171 places with 200,000 or more people, and every capital.
- **Airports:** 749 civil airports (OurAirports, public domain) and 133 military-designated airfields, chosen by name
  ("air base", "air force" and similar). A name is a clue, not a confirmation of use: the base perimeter is not published.
- **Ports:** 53 Natural Earth port points, plus six named sites from the reporting (Mina Salman, Duqm, Salalah, Sohar,
  Bukha, Mina al Fahal).
- **Sea labels:** Persian Gulf, Gulf of Oman, Red Sea, Gulf of Aqaba, Black Sea.

**Map basis:** Natural Earth country boundaries. Disputed or contested areas are described, not settled: the Golan Heights
(Israeli-administered; Syria claims it), Gaza and the West Bank (Palestinian territories; the Gaza Health Ministry and
government media report that Israel holds more than 63% of Gaza), the Kurdistan Region of Iraq (autonomous), the islands in
the Strait of Hormuz (claimed by Iran and the UAE), the British Sovereign Base Areas of Akrotiri and Dhekelia, and the
divided island of Cyprus. Most military positions are approximate. Events reflect reports up to 10 October 2026. The map
settles no dispute.

## What is plotted, and how sure each point is

Every tooltip gives the point's source, its date and its status. **Verified** means a government, an agency or a
reputable outlet reports it; **not verified in this build** means public knowledge that this build's searches did not
confirm. Positions are approximate unless the note says otherwise.

**US forces (6).** Al Udeid (Qatar; about 10,000 US troops; hit by an Iranian missile on 3-4 March 2026), Al Dhafra
(UAE; US Air Force training hub), Ali Al Salem (Kuwait; 386th Air Expeditionary Wing), Camp Arifjan (Kuwait; CENTCOM's
forward Army headquarters), Camp Buehring (Kuwait) and Prince Sultan (Saudi Arabia). Each is listed with the reported
strikes. The Pentagon's inspector general reports that Iranian strikes damaged hundreds of buildings across US bases in
the region (CSMonitor, 29 Sep 2026). NSA Bahrain, the US Fifth Fleet headquarters, is in the navy layer.

**Navies and submarines (14).**
- Israel: Haifa Naval Base, and the Shayetet 7 submarine flotilla there (six submarines; INS Drakon arrived in late
  September 2026).
- Turkey: Gölcük Naval Base and its submarine command and shipyard (Reis-class boats S-330 and S-331 in service), Erdek
  (mine warfare) and Bartın (home port of the Preveze and Gür-class boats).
- Iran: Bandar Abbas (struck on 28 Feb, 2 Mar and 5 Mar 2026; the submarine maintenance facility was hit on 12 July 2026),
  Jask (IRIN 2nd Naval District headquarters, relocated), Konarak (IRIN 3rd Naval District), Chabahar (IRGC Navy Imam Ali
  base) and Bandar Mahshahr (IRGC Navy district headquarters).
- Russia in Syria: Tartus, under the 9 August 2026 MoU (a joint training centre; Syria takes the commercial pier).
- US: NSA Bahrain.

**Missile bases (5).** Bid Ganeh, Kashan, Esfahan South, Dezful (struck in early March 2026) and Amand near Tabriz (struck
June 2025). Impact and strike dates come from Critical Threats and JINSA, which use satellite imagery and public
statements.

**Nuclear sites (8).** Natanz, Fordow, Isfahan Nuclear Technology Center and Khondab (Arak), all struck in June 2025
(damage assessments differ). Bushehr, the country's only operating power reactor, had projectiles strike near its
premises on 18 March and 4 April 2026 (IAEA). Dimona, Barakah (UAE) and Akkuyu (Turkey) are **not verified in this build**.

**Defence industry (10).** HESA at Shahin Shahr (drones; struck 1-2 March 2026), Shiraz Electronics Industries and the
Isfahan munitions factory (struck June 2025), the Khojir missile complex (struck June 2025), ODIR (headquarters
placed at Tehran), and Masyaf in Syria (destroyed by Israeli strikes in 2024). Turkey: ASELSAN (Ankara), Roketsan (Ankara,
with new production at Kırıkkale), Baykar (Istanbul, with test firing at Çorlu) and TAI (Ankara). **Israeli, Gulf and
Egyptian defence-industry sites were not verified in this build and are not plotted.**

**Conflict zones (8).** Iran (the war from 28 February 2026); the Gulf host states (Iranian strikes on US bases and
ports); Iraq (strikes on bases hosting US forces); Israel (Iranian missile and drone strikes); southern Lebanon (ceasefires
of 16 April and 1-4 June 2026; fighting continued); Gaza (ceasefire since 10 October 2025; more than 1,478 killed since,
per the Gaza Health Ministry); Yemen (Houthi attacks on Israel since 28 March 2026; Israeli strikes in 2025); and Syria
(the 2024 Masyaf strike; the 2026 Russian bases agreement). Locations for the country-wide items are the capitals, for
orientation only.

**Chokepoints (6).** Strait of Hormuz (largely blocked since 28 February 2026; the US blockade of Iranian ports from 13
April; fighting resumed 8 July), Bab el-Mandeb (Houthi threats and attacks), the Suez Canal, the Bosporus, the Dardanelles
and the Tiran Strait (the last four are public information).

**Oil and gas terminals (3).** Ras Laffan (QatarEnergy halted LNG production after Iranian attacks, 2 March 2026).
Kharg Island and Ceyhan are **not verified in this build**.

**Not plotted, because the sources in this build did not verify them:** Israeli air bases, Israeli and Gulf defence
industry, the Egyptian and Saudi navies, Incirlik, the Iraqi bases, Jordan's Muwaffaq Salti and any Army corps or division
headquarters. RAF Akrotiri is plotted as "not verified in this build".

## News and social sources: what each can and cannot do

**Feeds (addresses printed by the directories or verified in earlier builds).**
- Iran: Tehran Times, Mehr News (verified earlier), Iran Focus, The Tower (Iran tag), Global Voices (Iran, Yemen, Egypt),
  The War Zone (Iran), Foreign Affairs (Iran) and EA WorldView (Iran).
- Israel: The Jerusalem Post (all news, Iran and the Israel-Hamas war), Haaretz (Israel and Middle East) and The Times of
  Israel (Israel section).
- Gulf and Arab: Arab News (Middle East section).
- Turkey: Anadolu Agency (live).
- Regional and wire: Al Jazeera and BBC News (Middle East), both verified earlier.
- Defence and cyber: Breaking Defense, The Record and USNI News (verified earlier); Euronews (US-Iran crisis).
- **Google News search feeds** for the Gulf and other outlets whose own feeds printed no address (Gulf News, Khaleej Times,
  The National, Middle East Eye, Daily Sabah and others). These are aggregators; the underlying outlets are not named by the feed.

**GDELT:** 30 English-language queries across the war, the chokepoints, each Gulf state, the navies and submarines,
nuclear sites, the defence industries and the ceasefires.

**X (Twitter): official API v2 recent search.** Set `X_BEARER_TOKEN`. Ten queries are in `data/x_queries.json`. Recent
search needs a paid API tier; the status panel shows X's error if your tier does not include it. Not live-tested here.

**Facebook: Meta Graph API, Page posts.** Set `FACEBOOK_PAGE_TOKEN` and list Page IDs in `data/facebook_pages.json`. Pages
you manage, or Pages that have granted Page Public Content Access. Not live-tested here.

**Instagram: Meta Business Discovery.** Business and Creator accounts you own or can access, in
`data/instagram_accounts.json`.

**Telegram: public channels.** The channel list in `data/telegram_channels.json` is the global list from earlier builds.
I could not verify any Middle East Telegram handles in this build, so none were added. Add the channels you follow.

**Dark web (Tor).** Only onion sources you verify on the outlet's own site; none are configured.

**USGS earthquakes** map events inside the frame. **Ransomware.live** is filtered to the 17 states' country codes; its
entries are group claims, not verified facts.

**Limits, stated plainly.** No route here reads private accounts, closed groups or personal profiles, and scraping those
services is against their terms, so it is not built. Conflict and casualty figures come from the sources named on each
point and are contested; the map does not adjudicate them.

## Reference items

Each is dated and carries its source: the war's start (28 February 2026); the ceasefire and MoU timeline (CRS R48887); the
Hormuz traffic figures (House of Commons Library); the strikes on US bases (France 24, Middle East Eye, Stripes); the
Pentagon inspector general's damage count (CSMonitor, 29 September 2026); the Bandar Abbas strikes (FDD, USNI) and the July
2026 submarine facility strike (CENTCOM via Maritime News); INS Drakon's arrival (Algemeiner, September 2026); the Reis-class
submarines (Wikipedia); the June 2025 nuclear strikes and the Bushehr incidents (Armscontrol.org; IAEA via ANS); HESA's
strike (Critical Threats); the Masyaf raid (Wikipedia); the Qatar LNG halt (Al Jazeera); the Oman port strikes
(Wikipedia); Kuwait airport (Stripes); the Russia-Syria MoU (Al Jazeera, Moscow Times); the Gaza and Lebanon ceasefire
timelines (AAWSAT, Al Jazeera, AP); and the Houthi attacks (Wikipedia).

## Tests

`pip install -r requirements.txt pytest`, then `python -m pytest tests/` (36 tests). The browser suites load the shipped
`dashboard.js` into a real DOM: `npm install` and `npm test`.

## Security

- Keys and tokens are encrypted with AES-256-GCM and removed from every error message.
- The server listens on 127.0.0.1 only, on port 8810.
- Strict Content-Security-Policy: no third-party scripts, fonts or trackers.
- Hostile text (headlines, posts, labels) is escaped before display; only http and https links become clickable.
- Telegram handles, Instagram usernames and Facebook Page IDs are validated before any URL is built.
- Requests can go through a proxy you choose (`PROXY_URL`); dark-web requests go through Tor only.

A dashboard cannot secure your whole PC or phone from attack, and it cannot hide your IP address from the sites it fetches
from unless you route traffic through a VPN (which can still see your traffic).

## Honest limitations

- **Most positions are approximate.** Bases and industrial sites are placed at their town or area centre; open sources do
  not publish perimeters or coordinates. Each tooltip says so.
- **Some items are not verified in this build** (marked in their tooltips and listed above). Treat them as unconfirmed.
- **The situation changes daily.** The war, the ceasefires and the strikes are current to the reports cited (10 October
  2026). Refresh the sources before relying on any event.
- **No live news was fetched in the build sandbox**, which has no internet access. Check the status panel on your machine.
- **Coverage depends on the feeds.** Gulf outlets come through Google News aggregation; Arabic- and Persian-language press,
  and Israeli Hebrew-language press, are not covered.
- **The map is not a targeting product.** It maps publicly reported locations and events for analysis.
- **Single-user, local.** It runs on your machine while it is open.

# MPOB-price-scraper
A Python automation that scrapes daily Crude Palm Oil (CPO) and Fresh Fruit
Bunch (FFB) prices from the Malaysian Palm Oil Board (MPOB) portal and
distributes them to stakeholders via WhatsApp.

## Overview

Palm oil prices published by MPOB drive daily commercial decisions — from
estate-level FFB pricing to sales contract negotiations. Previously, someone
had to manually visit the MPOB website each day, read the price, and forward
it to management and estate teams.

This project automates that entire workflow end-to-end:

1. Constructs the MPOB daily price URL for the current date
2. Fetches and parses the price table with BeautifulSoup
3. Extracts the correct CPO price from the table (position varies by day/month)
4. Formats a message with the date and price
5. Sends it to a WhatsApp group via `pywhatkit`

## Why this exists

The problem was not technically difficult — it was *routine*. A task that
takes 2 minutes and must be done every single working day, by a human, is a
task that will eventually be forgotten, delayed, or done incorrectly. The
value of this script is not in its complexity; it's in removing a recurring
manual step from someone's day, permanently.

## Note on FFB prices

The original version of this script also scraped FFB (Fresh Fruit Bunch)
prices from MPOB. Starting in 2025, MPOB added authentication to the FFB
price page, requiring a login to view it. Because automated login would
violate MPOB's terms of use, the FFB portion was removed from this script.
The CPO price page remains publicly accessible, so this script focuses on
CPO only.

## Technical details

**Scraping logic**

The MPOB daily price pages follow a predictable URL pattern:

    https://price.mpob.gov.my/dailys/mas_cpo/<DD>/<MM>/<YYYY>   (CPO)
    
The script builds these URLs from `datetime.date.today()`, fetches the pages
with `requests`, and parses the price table with BeautifulSoup. It then
locates the row corresponding to the current day of the month and extracts
the price cell.

**Delivery**

WhatsApp delivery uses `pywhatkit.sendwhatmsg_to_group()`, which opens
WhatsApp Web, types the message into the specified group, and presses Enter.
A `keyboard.press_and_release('enter')` call after the send acts as a
safety net for cases where the default delay is too short.

**Configuration**

The WhatsApp group ID is read from an environment variable
(`WHATSAPP_GROUP_ID`) rather than hardcoded, so the same script can be
deployed in different environments without exposing sensitive identifiers.


**Error handling**

Wrapped in a `try/except` so that a single failed day — a network issue,
a page change, a missing price — does not crash the scheduled run.

## What's good about this implementation

- **Idempotent URL construction** — the URL is derived from today's date,
  so the script is re-runnable at any point in the day without state.
- **No external dependencies beyond the essentials** — `requests`,
  `BeautifulSoup`, `pywhatkit`, `keyboard`. No frameworks, no API keys.
- **Zero-config delivery** — no need to manage WhatsApp API credentials;
  `pywhatkit` handles the browser automation.

## Impact

- Eliminated daily manual price lookups and forwarding. 
- Ensured consistent, same-time delivery to stakeholders every working day.
- Removed the risk of a forgotten or delayed price update on busy days.

## Tech stack

- **Python 3**
- **requests** — HTTP client
- **BeautifulSoup4** — HTML parsing
- **pywhatkit** — WhatsApp Web automation
- **keyboard** — Keypress automation for message send
- **datetime** — Date arithmetic for URL and message construction

## How to run

```bash
pip install requests beautifulsoup4 pywhatkit keyboard

python cpo_scraper.py
```
## What I'd do differently today
Written in 2022. The FFB portion was removed in 2025 when MPOB added
authentication to that page. If rebuilt today, I would use the WhatsApp
Business API instead of browser automation, and add schema validation to
the HTML parsing step.

## About

Built by Chin Kee Ming — Python developer with 30 years of financial and 
plantation accounting experience.
LinkedIn: www.linkedin.com/in/chin-kee-ming-588685148
Portfolio: https://github.com/chinkm/MPOB-price-scraper.git



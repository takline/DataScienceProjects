# Treasury Tales: An Adventure in SEC Data Exploration
Welcome to the magical world of "Treasury Tales"! This enchanting repository houses our Python Web Scraper, a delightful tool for unraveling the mysteries of 13F filings (those intriguing declarations of mutual fund holdings) from the SEC's enchanted forest, known as [EDGAR](https://www.sec.gov/edgar/searchedgar/companysearch.html). Our scraper not only seeks out these filings but also artfully crafts a .tsv file from the gleaned data, like an alchemist turning lead into gold.

## Spellbook Requirements

#### Embarking on Your Journey
- Cast the spell `pip install -r requirements.txt` (or, if you're a wizard of the `pipenv` school, use `pipenv install`) to gather all the magical ingredients.
- Summon the scraper by invoking `python scraper.py` (or, in the lands of `pipenv`, chant `pipenv run python scraper.py`).
- When the oracle speaks, respond with the 10-digit CIK number of the mutual fund you seek to unravel.

#### Potent Potions and Charms

- [Requests](https://2.python-requests.org/en/master/), a mystical Python scroll for conjuring HTTP requests.
- [lxml](https://lxml.de/), a powerful Python tome for parsing the cryptic languages of XML and HTML.
- [Beautiful Soup](https://pypi.org/project/beautifulsoup4/), a sorcerer's Python guide for extracting secrets from the depths of Web pages.
- [re](https://docs.python.org/3/library/re.html), a Python spell for weaving and interpreting the complex tapestry of regular expressions.
- [csv](https://docs.python.org/3/library/csv.html), a Python scroll for decoding and inscribing CSV and TSV scripts.

## Keeper of the Codex
- [Tyler Kline](https://github.com/takline)

## Scrolls of Wisdom
- [SEC: Oracle's Guide to Form 13F](https://www.sec.gov/divisions/investment/13ffaq.htm), a compendium of frequently asked questions and answers, shedding light on the mysteries of Form 13F.

Embark on your journey with "Treasury Tales" and uncover the hidden treasures within the SEC's vast vaults of data. Happy exploring! 🌟📜🔍
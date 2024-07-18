---
layout: post-wide
hero-bg-color: "#D22E1E"
uid: aiwebscraping
title:  "Web Scraping with AI"
worktype: "Coding"
date:   2021-07-01 12:00:00
categories: portfolio
progress: 100
---

# (Web Scraping with AI)[https://github.com/takline/TK-Projects/tree/main/Web%20Scraping%20%26%20Automation/web-scraping-with-AI]

## What's Brewing Here?

Embark on a digital treasure hunt with this code ensemble! It's your magic wand to sift through the web's labyrinth and gracefully extract nuggets of knowledge. We weave together the spells of [OpenAI Functions](https://openai.com/blog/function-calling-and-other-api-updates) and [LangChain](https://python.langchain.com/docs/get_started/introduction) to make this happen. Just sketch out your data map in `schemas.py`, pick your web destination, and let `scrape_with_playwright()` in `main.py` be your guide.

Pro Tip: Web pages are a tapestry of `<p>`, `<span>`, and `<h>` tags. Find the combination that whispers the secrets of your chosen site.

### Example Adventure

1. Craft your digital map in `provide_schema.py`. Whether it's a Pydantic class or a simple dictionary, your wish is our command:

   ```python
   class NewsPortalSchema(BaseModel):
       headline: str
       brief_summary: str
   ```

2. Set sail in `run.py` like this:

   ```python
   asyncio.run(playwright_scrape_and_analyze(
           url="https://www.bbc.com",
           tags=["span"],
           schema_pydantic=NewsPortalSchema
       ))
   ```

## Setting Up Your Magic Kit

### 1. Conjure a Python virtual environment

`python -m venv virtual-env` or `python3 -m venv virtual-env` (Mac)

`py -m venv virtual-env` (Windows 11)

### 2. Awaken your virtual environment

`.\virtual-env\Scripts\activate` (Windows)

`source virtual-env/bin/activate` (Mac)

### 3. Summon dependencies with Poetry's charm

Cast `poetry install --sync` or simply `poetry install`

### 4. Enlist Playwright in your quest

```bash
playwright install
```

### 5. Secretly store your OpenAI API key in a `.env` scroll

```text
OPENAI_API_KEY=XXXXXX
```

## How to Unleash the Magic

### Run it in your own mystical realm

```bash
python run.py
```

## Scrolls of Extra Wisdom

- Transform this into a FastAPI crystal ball to peer into your data through an API gateway.

- Tread the web with the caution of a wise wizard. Only venture where the digital ethics compass allows.

- A little bird told me this wizardry is now part of LangChain's spellbook [in this PR](https://github.com/langchain-ai/langchain/pull/8732). Peek into [the grand library here](https://python.langchain.com/docs/use_cases/web_scraping#quickstart) for more enchantments.

In this enhanced documentation, the instructions are reimagined to be more engaging and less technical, while still providing all the necessary steps to use the code effectively.
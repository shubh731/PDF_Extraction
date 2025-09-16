import os
import streamlit as st
import asyncio
import nest_asyncio
from scrapegraphai.graphs import SmartScraperGraph

nest_asyncio.apply()

if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

st.title("Flipkart Scraper with scrapegraphai + Playwright")

url = st.text_input("Enter a Flipkart URL", "https://www.flipkart.com")
prompt = st.text_input("What do you want to extract?", "Extract product names and prices")

if st.button("Scrape"):
    config = {
        "llm": {
            "model": "gpt-3.5-turbo",
            "api_key": os.getenv("OPENAI_API_KEY"),
        },
        "loader": {
            "type": "chromium",
            "timeout": 30,
        }
    }
    graph = SmartScraperGraph(prompt=prompt, source=url, config=config)

    try:
        result = graph.run()
        st.json(result)
    except Exception as e:
        st.error(f"Scraping failed: {e}")

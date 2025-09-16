# Import the required libraries
import streamlit as st
from scrapegraphai.graphs import SmartScraperGraph

# Set up the Streamlit app
st.title("Web Scrapping AI Agent 🕵️‍♂️")
st.caption("This app allows you to scrape a website using Llama 3.2")

# Set up the configuration for the SmartScraperGraph
graph_config = {
    "llm": {
        "provider": "ollama",
        "model": "llama2",  # ✅ Correct model name as per `ollama run llama2`
        "base_url": "http://localhost:11434",
        "format": "json",  # ✅ Required for Ollama responses to parse properly
        "temperature": 0,
    },
    "loader": {
        "type": "chromium",  # ✅ Use Playwright for JS-heavy pages
        "timeout": 30,
    },
    "verbose": True,
}

# Get the URL of the website to scrape
url = st.text_input("Enter the URL of the website you want to scrape")
# Get the user prompt
user_prompt = st.text_input("What you want the AI agent to scrape from the website?")

# Create a SmartScraperGraph object
smart_scraper_graph = SmartScraperGraph(
    prompt=user_prompt,
    source=url,
    config=graph_config
)
# Scrape the website
if st.button("Scrape"):
    result = smart_scraper_graph.run()
    st.write(result)
import os
import requests
from bs4 import BeautifulSoup
import pdfplumber
from urllib.parse import urljoin, unquote

# --- CONFIG ---
BASE_URL = "https://www.nrcgrapes.in/MONTHLY-WEATHER%20BASED%20GRAPE%20ADVISORY.htm"
SAVE_DIR = "data/pdfs"
os.makedirs(SAVE_DIR, exist_ok=True)

# --- SCRAPER TOOL ---
def scrape_pdf_links(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    pdf_links = []

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.lower().endswith(".pdf"):
            full_url = urljoin(base_url, href)
            pdf_links.append(full_url)

    return pdf_links

# --- DOWNLOADER TOOL ---
def download_pdfs(pdf_links, save_dir):
    for url in pdf_links:
        raw_filename = os.path.basename(url)
        filename = os.path.join(save_dir, unquote(raw_filename))

        if not os.path.exists(filename):
            print(f"⬇️ Downloading: {url}")
            try:
                r = requests.get(url)
                r.raise_for_status()
                with open(filename, "wb") as f:
                    f.write(r.content)
            except Exception as e:
                print(f"❌ Failed to download {url}: {e}")
        else:
            print(f"✅ Already downloaded: {filename}")

# --- PDF TEXT EXTRACTION TOOL ---
def extract_text_from_pdf(pdf_path):
    full_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"
    except Exception as e:
        print(f"❌ Could not read {pdf_path}: {e}")
    return full_text.strip()

# --- AGENT FLOW ---
def grape_advisory_agent():
    print("🔍 Scraping PDF links...")
    pdf_links = scrape_pdf_links(BASE_URL)
    print(f"🔗 Found {len(pdf_links)} PDFs.")

    print("⬇️ Downloading PDFs...")
    download_pdfs(pdf_links, SAVE_DIR)

    # print("📄 Extracting text from each PDF...")
    # for file in os.listdir(SAVE_DIR):
    #     if file.lower().endswith(".pdf"):
    #         path = os.path.join(SAVE_DIR, file)
    #         text = extract_text_from_pdf(path)
    #         print(f"\n📘 {file}")
    #         # print("------------------------------------------------------")
    #         # print(text[:1000] + "...")  # Print first 1000 characters only
    #         # print("------------------------------------------------------")

# --- RUN ---
if __name__ == "__main__":
    grape_advisory_agent()

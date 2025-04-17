import requests
from bs4 import BeautifulSoup
import re

def extract_doi_from_url(url):
    doi_regex = r"10\.\d{4,9}/[-._;()/:A-Z0-9]+"
    match = re.search(doi_regex, url, re.IGNORECASE)
    return match.group(0) if match else None

def search_scholar_fast(query, num_results=10):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:117.0) Gecko/20100101 Firefox/117.0"
    }

    base_url = "https://scholar.google.com/scholar"
    params = {"q": query, "hl": "en", "num": num_results}  # ← Получить до 10 за раз

    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code != 200:
        print("Blocked or error. Try again later.")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.select(".gs_ri")

    for i, result in enumerate(results):
        title_tag = result.select_one(".gs_rt a")
        title = title_tag.text if title_tag else result.select_one(".gs_rt").text
        url = title_tag["href"] if title_tag else "No link"
        doi = extract_doi_from_url(url) if url.startswith("http") else None

        authors_year = result.select_one(".gs_a")
        snippet = result.select_one(".gs_rs")

        print(f"\n{i+1}. {title}")
        print(f"   Link: {url}")
        if authors_year:
            print(f"   Authors/Year: {authors_year.text}")
        if snippet:
            print(f"   Snippet: {snippet.text.strip()}")
        if doi:
            print(f"   DOI: {doi}")

# 🔍 Пример
search_scholar_fast("quantum computing", num_results=10)

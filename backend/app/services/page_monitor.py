import hashlib
import requests
from bs4 import BeautifulSoup


def fetch_page_text(url: str) -> str:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    cleaned_text = " ".join(text.split())

    return cleaned_text


def generate_content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def check_page(url: str):
    text = fetch_page_text(url)
    content_hash = generate_content_hash(text)

    return {
        "url": url,
        "content_length": len(text),
        "content_hash": content_hash
    }
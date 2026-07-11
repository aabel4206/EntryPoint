import hashlib

import requests
from bs4 import BeautifulSoup


def fetch_page_text(url: str) -> str:
    response = requests.get(
        url,
        timeout=15,
        headers={
            "User-Agent": (
                "EntryPoint student research monitoring prototype"
            )
        },
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(
        ["script", "style", "nav", "footer", "header", "noscript"]
    ):
        tag.decompose()

    text = soup.get_text(separator=" ")
    return " ".join(text.split())


def generate_content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def check_page(url: str) -> dict:
    text = fetch_page_text(url)

    return {
        "url": url,
        "content_length": len(text),
        "content_hash": generate_content_hash(text),
        "content_text": text,
    }
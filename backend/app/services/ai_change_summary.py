import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "gemma3:1b"
MAX_TEXT_LENGTH = 8_000


def summarize_page_change(
    page_title: str,
    old_text: str,
    new_text: str,
) -> str:
    old_excerpt = old_text[:MAX_TEXT_LENGTH]
    new_excerpt = new_text[:MAX_TEXT_LENGTH]

    prompt = f"""
You summarize meaningful changes in university onboarding webpages.

Page title: {page_title}

OLD PAGE TEXT:
{old_excerpt}

NEW PAGE TEXT:
{new_excerpt}

Write a concise student-facing summary.

Requirements:
- Use no more than 3 short sentences.
- State only changes supported by the supplied text.
- Focus on routes, schedules, deadlines, closures, locations,
  fees, requirements, or procedures.
- Ignore formatting and wording changes that do not change meaning.
- Do not invent information.
- If no meaningful change is clear, respond exactly:
  The page changed, but no clear student-relevant change was identified.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                },
            },
            timeout=120,
        )
        response.raise_for_status()

        data = response.json()
        summary = data.get("response", "").strip()

        if not summary:
            return "The page changed, but no AI summary was generated."

        return summary

    except requests.RequestException:
        return (
            f"{page_title} changed, but the local AI summary "
            "service was unavailable."
        )
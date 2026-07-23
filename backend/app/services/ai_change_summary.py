import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "gemma3:1b"
MAX_TEXT_LENGTH = 8_000
OLLAMA_TIMEOUT_SECONDS = 120


def summarize_page_change(
    page_title: str,
    old_text: str,
    new_text: str,
) -> str:
    """
    Use the locally hosted Ollama model to create a short factual summary
    of meaningful changes between two versions of a university webpage.

    Personal advice is intentionally excluded here. Personalization is
    handled separately by the notification system.
    """

    old_excerpt = old_text[:MAX_TEXT_LENGTH]
    new_excerpt = new_text[:MAX_TEXT_LENGTH]

    prompt = f"""
You analyze changes to university information webpages.

PAGE TITLE:
{page_title}

PREVIOUS PAGE CONTENT:
{old_excerpt}

UPDATED PAGE CONTENT:
{new_excerpt}

Write a concise factual summary of the meaningful changes between the
previous page content and the updated page content.

Requirements:
- Use between 1 and 3 short sentences.
- State only changes that are directly supported by the supplied text.
- Focus on schedules, routes, service hours, deadlines, closures,
  locations, fees, eligibility rules, requirements, availability,
  documents, or procedures.
- Include important dates, times, prices, locations, or route names
  when they appear in the supplied text.
- Ignore formatting, navigation, and wording changes that do not alter
  the meaning.
- Do not speculate about how the change might affect a student.
- Do not provide recommendations or personal advice.
- Do not mention being an AI or language model.
- Do not add headings, bullet points, introductions, or conclusions.
- If no meaningful student-relevant change can be identified, respond
  with exactly this sentence:
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
            timeout=OLLAMA_TIMEOUT_SECONDS,
        )

        response.raise_for_status()

        data = response.json()
        summary = data.get("response", "").strip()

        if not summary:
            return (
                "The page changed, but no AI summary was generated."
            )

        return summary

    except requests.Timeout:
        return (
            f"{page_title} changed, but the local AI summary service "
            "timed out."
        )

    except requests.ConnectionError:
        return (
            f"{page_title} changed, but the local AI summary service "
            "could not be reached."
        )

    except requests.HTTPError:
        return (
            f"{page_title} changed, but the local AI summary service "
            "returned an error."
        )

    except requests.RequestException:
        return (
            f"{page_title} changed, but the local AI summary service "
            "was unavailable."
        )

    except ValueError:
        return (
            f"{page_title} changed, but the local AI summary service "
            "returned an invalid response."
        )
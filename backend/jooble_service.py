import os

import requests
from dotenv import load_dotenv


load_dotenv()


JOOBLE_API_KEY = os.getenv("JOOBLE_API_KEY")
JOOBLE_API_URL = f"https://cz.jooble.org/api/{JOOBLE_API_KEY}"


def is_relevant_job(
    title: str,
    description: str,
    position: str,
) -> bool:
    """
    Určí, zda je nabídka relevantní pro hledanou pozici.
    Posuzuje název i popis nabídky.
    """

    title_lower = (title or "").lower().strip()
    description_lower = (description or "").lower().strip()
    position_lower = (position or "").lower().strip()

    text = f"{title_lower} {description_lower}"

    # Prázdné hledání = všechno
    if not position_lower:
        return True

    # =================================================
    # PYTHON DEVELOPER
    # =================================================

    if "python developer" in position_lower:

        # Nabídky, které jsou jasně zaměřené
        # na jinou technologii nebo obor.
        excluded_terms = [
            "c#",
            ".net",
            "c++",
            "cnc",
            "oděv",
            "oděvní",
            "konstruktér",
            "konstrukční",
            "strojní",
            "mechanik",
            "elektromechanik",
        ]

        if any(
            term in title_lower
            for term in excluded_terms
        ):
            return False

        # Python přímo v nabídce = silný signál.
        if "python" in text:
            return True

        # Obecná softwarová pozice může být relevantní,
        # pokud je z popisu jasné, že jde o vývoj software.
        software_terms = [
            "software",
            "backend",
            "frontend",
            "web aplikac",
            "webov",
            "informační systém",
            "informačních systém",
            "api",
            "databáz",
            "programování",
            "programovac",
            "vývoj aplikac",
            "vývoj software",
        ]

        programming_terms = [
            "programátor",
            "programmer",
            "developer",
            "vývojář",
            "kodér",
            "kódování",
        ]

        has_software_context = any(
            term in text
            for term in software_terms
        )

        has_programming_context = any(
            term in text
            for term in programming_terms
        )

        return (
            has_software_context
            and has_programming_context
        )

    # =================================================
    # BACKEND DEVELOPER
    # =================================================

    if "backend developer" in position_lower:

        excluded_terms = [
            "cnc",
            "oděv",
            "konstruktér",
            "strojní",
            "mechanik",
        ]

        if any(
            term in title_lower
            for term in excluded_terms
        ):
            return False

        backend_terms = [
            "backend",
            "back-end",
            "server",
            "api",
            "databáz",
            "database",
        ]

        developer_terms = [
            "developer",
            "programátor",
            "programmer",
            "vývojář",
            "software",
        ]

        return (
            any(term in text for term in backend_terms)
            and any(term in text for term in developer_terms)
        )

    # =================================================
    # FRONTEND DEVELOPER
    # =================================================

    if "frontend developer" in position_lower:

        frontend_terms = [
            "frontend",
            "front-end",
            "html",
            "css",
            "javascript",
            "web",
            "ui",
            "ux",
        ]

        developer_terms = [
            "developer",
            "programátor",
            "programmer",
            "vývojář",
            "kodér",
        ]

        return (
            any(term in text for term in frontend_terms)
            and any(term in text for term in developer_terms)
        )

    # =================================================
    # OBECNÝ DEVELOPER
    # =================================================

    if "developer" in position_lower:

        excluded_terms = [
            "cnc",
            "oděv",
            "oděvní",
            "konstruktér",
            "strojní",
            "mechanik",
        ]

        if any(
            term in title_lower
            for term in excluded_terms
        ):
            return False

        developer_terms = [
            "developer",
            "software developer",
            "software engineer",
            "vývojář softwaru",
            "programátor",
            "programmer",
            "vývojář",
        ]

        return any(
            term in text
            for term in developer_terms
        )

    # =================================================
    # OBECNÝ PROGRAMÁTOR
    # =================================================

    if "programátor" in position_lower:

        excluded_terms = [
            "cnc",
            "soustruh",
            "obráběc",
            "strojní",
            "výrob",
        ]

        if any(
            term in title_lower
            for term in excluded_terms
        ):
            return False

        programming_terms = [
            "programátor",
            "programmer",
            "developer",
            "vývojář",
            "software",
            "programování",
        ]

        return any(
            term in text
            for term in programming_terms
        )

    # =================================================
    # OSTATNÍ POZICE
    # =================================================

    return position_lower in text


def search_jooble(
    position: str,
    location: str = "",
):
    """
    Vyhledá pracovní nabídky přes Jooble API
    a odstraní nerelevantní výsledky.
    """

    if not JOOBLE_API_KEY:
        raise RuntimeError(
            "JOOBLE_API_KEY není nastavený v .env"
        )

    payload = {
        "keywords": position,
        "location": location,
        "page": 1,
    }

    response = requests.post(
        JOOBLE_API_URL,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    jobs = data.get("jobs", [])

    results = []

    for job in jobs:

        title = job.get("title", "")

        if not is_relevant_job(
            title,
            job.get("snippet", ""),
            position,
        ):
            continue

        results.append(
            {
                "title": title,
                "company": job.get(
                    "company",
                    "",
                ),
                "location": job.get(
                    "location",
                    "",
                ),
                "salary": job.get(
                    "salary",
                    "",
                ),
                "url": job.get(
                    "link",
                    "",
                ),
                "source": "Jooble",
                "source_id": job.get(
                    "id",
                    "",
                ),
                "description": job.get(
                    "snippet",
                    "",
                ),
            }
        )

    return results
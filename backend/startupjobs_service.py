import os

import requests
from dotenv import load_dotenv


load_dotenv()


STARTUPJOBS_API_KEY = os.getenv("STARTUPJOBS_API_KEY")

STARTUPJOBS_API_URL = "https://api.startup.jobs/v1/jobs"


def search_startupjobs(
    position: str,
    location: str = "",
):
    """
    Vyhledá pracovní nabídky přes Startup Jobs API.
    """

    if not STARTUPJOBS_API_KEY:
        raise RuntimeError(
            "STARTUPJOBS_API_KEY není nastavený v .env"
        )

    headers = {
        "Authorization": f"Bearer {STARTUPJOBS_API_KEY}",
        "Accept": "application/json",
    }

    params = {
        "country": "CZ",
        "limit": 50,
    }

    if position:
        params["q"] = position

    response = requests.get(
        STARTUPJOBS_API_URL,
        headers=headers,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    jobs = data.get("data", [])

    results = []

    for job in jobs:
        location_data = job.get("location") or {}

        city = location_data.get("city", "")
        state = location_data.get("state", "")
        country = location_data.get("country", "")

        location_parts = []

        if city:
            location_parts.append(city)

        if state and state != city:
            location_parts.append(state)

        if country and country != "Czech Republic":
            location_parts.append(country)

        location_text = ", ".join(location_parts)

        company_data = job.get("company") or {}

        company_name = company_data.get(
            "name",
            "",
        )

        salary_data = job.get("salary")

        if salary_data is None:
            salary = ""
        elif isinstance(salary_data, dict):
            salary = str(salary_data)
        else:
            salary = str(salary_data)

        results.append(
            {
                "title": job.get(
                    "title",
                    "",
                ),
                "company": company_name,
                "location": location_text,
                "salary": salary,
                "url": job.get(
                    "url",
                    "",
                ),
                "source": "StartupJobs",
                "source_id": job.get(
                    "id",
                    "",
                ),
                "description": job.get(
                    "description_html",
                    "",
                ),
                "published_at": job.get(
                    "published_at",
                    "",
                ),
                "employment_type": job.get(
                    "employment_type",
                    "",
                ),
                "workplace_type": job.get(
                    "workplace_type",
                    "",
                ),
            }
        )

    if location:
        location_lower = location.lower().strip()

        filtered_results = []

        for job in results:
            job_location = (
                job.get("location") or ""
            ).lower()

            if location_lower in job_location:
                filtered_results.append(job)

        results = filtered_results

    unique_results = []
    seen = set()

    for job in results:
        source_id = job.get("source_id")

        if source_id:
            key = str(source_id)
        else:
            title = (
                job.get("title") or ""
            ).strip().lower()

            company = (
                job.get("company") or ""
            ).strip().lower()

            key = (
                title,
                company,
            )

        if key in seen:
            continue

        seen.add(key)
        unique_results.append(job)

    return unique_results
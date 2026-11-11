from backend.mpsv_service import load_mpsv_data
from backend.jooble_service import search_jooble
from backend.startupjobs_service import search_startupjobs


def get_location(job):
    """
    Získá lokalitu pracovní nabídky z dat MPSV.
    """

    location_data = job.get("mistoVykonuPrace") or {}

    # 1. Přímý text lokality
    address_text = location_data.get("adresaText")

    if address_text:
        return str(address_text)

    # 2. Pracoviště
    pracoviste = location_data.get("pracoviste") or []

    locations = []

    for workplace in pracoviste:

        workplace = workplace or {}

        # Název pracoviště
        name = workplace.get("nazev")

        if name:
            locations.append(str(name))

        address = workplace.get("adresa") or {}

        # Dodatek adresy
        dodatek = address.get("dodatekAdresy")

        if dodatek:
            locations.append(str(dodatek))

        # Část obce
        cast_obce = address.get("nazevCastiObce")

        if cast_obce:
            locations.append(str(cast_obce))

        # Obec
        obec = address.get("obec") or {}

        # Zlínský kraj
        kraj = address.get("kraj") or {}

        if kraj.get("id") == "Kraj/141":
            locations.append("Zlínský kraj")

        # Praha
        if obec.get("id") == "Obec/554782":
            locations.append("Praha")

    # Odstranění duplicit při zachování pořadí
    unique_locations = []

    for location in locations:

        if location not in unique_locations:
            unique_locations.append(location)

    return ", ".join(unique_locations)


def search_mpsv_jobs(
    position: str,
    location: str = "",
    skills: str = "",
):
    """
    Vyhledá pracovní nabídky z MPSV.
    Vyhledávání bere v úvahu název pozice i popis nabídky.
    """

    data = load_mpsv_data()

    jobs = data.get("polozky", [])

    position_lower = position.lower().strip()
    location_lower = location.lower().strip()

    # Varianty názvů technických pozic.
# Pozor: obecné "programátor" nepoužíváme
# u softwarových pozic, protože by do výsledků
# dostávalo CNC programátory.
    position_aliases = {
    "python developer": [
        "python",
        "python developer",
        "python programátor",
        "python programmer",
        "backend developer",
        "backend programátor",
        "software developer",
        "software engineer",
        "full-stack developer",
        "full stack developer",
    ],

    "backend developer": [
        "backend developer",
        "backend programátor",
        "backend",
        "software developer",
        "software engineer",
        "python",
        "api developer",
        "full-stack developer",
        "full stack developer",
    ],

    "frontend developer": [
        "frontend developer",
        "frontend",
        "web developer",
        "webový vývojář",
        "javascript developer",
        "software developer",
        "full-stack developer",
        "full stack developer",
    ],

    "software developer": [
        "software developer",
        "software engineer",
        "developer",
        "vývojář software",
        "vývojář",
        "full-stack developer",
        "full stack developer",
    ],

    "developer": [
        "developer",
        "vývojář",
        "software developer",
        "software engineer",
        "full-stack developer",
        "full stack developer",
    ],

    "programátor": [
        "programátor",
        "programmer",
        "software developer",
        "software engineer",
        "vývojář software",
        "vývojář",
    ],
    }
    search_terms = [position_lower]

    for key, aliases in position_aliases.items():

        if key in position_lower:

            for alias in aliases:

                if alias not in search_terms:
                    search_terms.append(alias)

    results = []

    for job in jobs:

        profession = job.get("pozadovanaProfese", {})
        title = profession.get("cs", "")

        if not title:
            continue

        title_lower = title.lower()

        description = (
            (job.get("upresnujiciInformace") or {}).get("cs", "")
        )

        description_lower = description.lower()

        # =====================================
        # POZICE
        # =====================================

        if not position_lower:
            title_match = True
        else:
            # U konkrétních IT pozic chceme hledat hlavně
            # v názvu pozice. Popis používáme pouze jako
            # doplňkový signál.
            title_match = any(
                term in title_lower
                for term in search_terms
            )

            # Python Developer musí být skutečně technická
            # vývojářská pozice.
        if "python developer" in position_lower:
                technical_terms = [
                    "python",
                    "developer",
                    "software",
                    "backend",
                    "frontend",
                    "full-stack",
                    "full stack",
                    "web",
                    "programátor",
                    "vývojář software",
                ]

                title_match = (
                    title_match
                    and any(
                        term in title_lower
                        for term in technical_terms
                    )
                )

        # =====================================
        # DOVEDNOSTI
        # =====================================

        skills_match = True

        if skills.strip():

            requested_skills = [
                skill.strip().lower()
                for skill in skills.split(",")
                if skill.strip()
            ]

            skills_match = any(
                skill in description_lower
                or skill in title_lower
                for skill in requested_skills
            )

        # =====================================
        # LOKALITA
        # =====================================

        location_text = get_location(job)

        location_match = (
            not location_lower
            or location_lower in location_text.lower()
        )

        # =====================================
        # VÝSLEDEK
        # =====================================

        if title_match and location_match and skills_match:

            salary_from = job.get("mesicniMzdaOd")
            salary_to = job.get("mesicniMzdaDo")

            if salary_from and salary_to:

                salary = (
                    f"{salary_from:,}–{salary_to:,} Kč"
                    .replace(",", " ")
                )

            elif salary_from:

                salary = (
                    f"od {salary_from:,} Kč"
                    .replace(",", " ")
                )

            elif salary_to:

                salary = (
                    f"do {salary_to:,} Kč"
                    .replace(",", " ")
                )

            else:

                salary = ""

            results.append(
                {
                    "title": title,
                    "company": job.get(
                        "nazevZamestnavatele",
                        "Neuvedeno",
                    ),
                    "location": location_text,
                    "salary": salary,
                    "url": "",
                    "source": "MPSV",
                    "source_id": job.get("id"),
                    "description": description,
                }
            )

    return results


def search_jobs(
    position: str,
    location: str = "",
    skills: str = "",
):
    """
    Vyhledá pracovní nabídky ze všech aktuálně
    připojených zdrojů.
    """

    results = []

    # =====================================
    # MPSV
    # =====================================

    try:

        mpsv_jobs = search_mpsv_jobs(
            position=position,
            location=location,
            skills=skills,
        )

        results.extend(mpsv_jobs)

    except Exception as error:

        print(
            f"⚠️ MPSV vyhledávání selhalo: {error}"
        )

    # =====================================
    # JOOBLE
    # =====================================

    try:
        jooble_jobs = search_jooble(
            position=position,
            location=location,
        )
        results.extend(jooble_jobs)
    except Exception as error:
        print(
            f"⚠️ Jooble vyhledávání selhalo: {error}"
        )
        
    # =====================================    
    # STARTUP JOBS
    # =====================================
    
    try:
        startupjobs = search_startupjobs(
            position=position,
            location=location,
        )
        results.extend(startupjobs)
    except Exception as error:
        print(
            f"⚠️ Startup Jobs vyhledávání selhalo: {error}"
        )

        # =================================================
    # SPOLEČNÝ FILTR RELEVANCE
    # =================================================

    position_lower = (position or "").strip().lower()

    def is_relevant_result(job):
        title = (
            job.get("title") or ""
        ).strip().lower()

        description = (
            job.get("description") or ""
        ).strip().lower()

        text = f"{title} {description}"

        if not position_lower:
            return True

        # ---------------------------------------------
        # PYTHON DEVELOPER
        # ---------------------------------------------

        if "python developer" in position_lower:

            # Python musí být skutečně uvedený
            # v názvu nebo popisu nabídky.
            if "python" not in text:
                return False

            # Očividně nesouvisející technologie/profese.
            excluded_terms = [
                "java developer",
                "javascript developer",
                "angular developer",
                "react developer",
                ".net developer",
                "c# developer",
                "c++ developer",
                "php developer",
                "sap developer",
                "android developer",
                "business developer",
                "salesforce developer",
                "abap developer",
                "cnc",
                "soustruh",
                "obráběc",
                "strojní",
                "mechanik",
                "elektromechanik",
                "oděv",
                "oděvní",
                "konstruktér",
                "konstrukční",
            ]

            if any(
                term in title
                for term in excluded_terms
            ):
                return False

            # Python + vývojářská/software kontext.
            developer_terms = [
                "developer",
                "programmer",
                "programátor",
                "vývojář",
                "software engineer",
                "software developer",
                "software",
                "backend",
                "back-end",
                "full-stack",
                "full stack",
                "api",
                "programování",
                "vývoj software",
            ]

            return any(
                term in text
                for term in developer_terms
            )
            
        # ---------------------------------------------
        # BACKEND DEVELOPER
        # ---------------------------------------------

        if "backend developer" in position_lower:

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
                any(
                    term in text
                    for term in backend_terms
                )
                and any(
                    term in text
                    for term in developer_terms
                )
            )

        # ---------------------------------------------
        # FRONTEND DEVELOPER
        # ---------------------------------------------

        if "frontend developer" in position_lower:

            frontend_terms = [
                "frontend",
                "front-end",
                "html",
                "css",
                "javascript",
                "javascript developer",
                "web developer",
                "webový vývojář",
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
                any(
                    term in text
                    for term in frontend_terms
                )
                and any(
                    term in text
                    for term in developer_terms
                )
            )

        # ---------------------------------------------
        # SOFTWARE DEVELOPER
        # ---------------------------------------------

        if "software developer" in position_lower:

            software_terms = [
                "software",
                "software developer",
                "software engineer",
                "vývoj software",
                "vývojář software",
                "programátor",
                "programmer",
                "developer",
                "vývojář",
            ]

            return any(
                term in text
                for term in software_terms
            )

        # ---------------------------------------------
        # OBECNÝ DEVELOPER
        # ---------------------------------------------

        if "developer" in position_lower:

            developer_terms = [
                "developer",
                "software developer",
                "software engineer",
                "programátor",
                "programmer",
                "vývojář",
                "vývoj software",
            ]

            excluded_terms = [
                "cnc",
                "soustruh",
                "obráběc",
                "strojní",
                "mechanik",
                "oděv",
                "oděvní",
                "konstruktér",
                "konstrukční",
            ]

            if any(
                term in title
                for term in excluded_terms
            ):
                return False

            return any(
                term in text
                for term in developer_terms
            )

        # ---------------------------------------------
        # PROGRAMÁTOR
        # ---------------------------------------------

        if "programátor" in position_lower:

            programming_terms = [
                "programátor",
                "programmer",
                "developer",
                "vývojář",
                "software",
                "programování",
            ]

            excluded_terms = [
                "cnc",
                "soustruh",
                "obráběc",
                "strojní",
                "výrob",
            ]

            if any(
                term in title
                for term in excluded_terms
            ):
                return False

            return any(
                term in text
                for term in programming_terms
            )

        # ---------------------------------------------
        # OSTATNÍ POZICE
        # ---------------------------------------------

        return position_lower in text

    # =================================================
    # FILTRACE RELEVANTNÍCH VÝSLEDKŮ
    # =================================================

    filtered_results = []

    for job in results:

        if is_relevant_result(job):
            filtered_results.append(job)

    # =================================================
    # ODSTRANĚNÍ DUPLICIT
    # =================================================

    unique_results = []
    seen = set()

    for job in filtered_results:

        title = (
            job.get("title") or ""
        ).strip().lower()

        company = (
            job.get("company") or ""
        ).strip().lower()

        location_text = (
            job.get("location") or ""
        ).strip().lower()

        key = (
            title,
            company,
            location_text,
        )

        if key in seen:
            continue

        seen.add(key)
        unique_results.append(job)

    return unique_results
def calculate_job_match(job: dict, skills: str = ""):
    """
    Jednoduché vyhodnocení shody pracovní nabídky
    s dovednostmi uživatele.
    """

    user_skills = [
        skill.strip().lower()
        for skill in skills.split(",")
        if skill.strip()
    ]

    description = job.get("description", "").lower()
    title = job.get("title", "").lower()

    matched_skills = []
    missing_skills = []

    for skill in user_skills:
        if skill in description or skill in title:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    if user_skills:
        score = round(
            len(matched_skills) / len(user_skills) * 100
        )
    else:
        score = None

    if score is None:
        recommendation = "Pro vyhodnocení shody zadej své dovednosti."
        level = "Shodu nelze vyhodnotit"
    elif score >= 80:
        recommendation = "Doporučuji reagovat."
        level = "Vysoká shoda"
    elif score >= 50:
        recommendation = "Nabídku stojí za to zvážit."
        level = "Střední shoda"
    else:
        recommendation = "Nabídka má nízkou shodu s tvými dovednostmi."
        level = "Nízká shoda"

    if matched_skills and missing_skills:
        match_explanation = (
            f"Nabídka odpovídá tvým dovednostem: "
            f"{', '.join(matched_skills)}. "
            f"Chybí ti: {', '.join(missing_skills)}."
        )
    elif matched_skills:
        match_explanation = (
            f"Nabídka dobře odpovídá tvým dovednostem: "
            f"{', '.join(matched_skills)}."
        )
    elif missing_skills:
        match_explanation = (
            f"Nabídka neobsahuje shodu s tvými zadanými dovednostmi. "
            f"Chybí: {', '.join(missing_skills)}."
        )
    else:
        match_explanation = (
            "Nebyly zadány žádné dovednosti pro porovnání."
        )

    return {
        "match_score": score,
        "match_level": level,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendation": recommendation,
        "match_explanation": match_explanation,
    }
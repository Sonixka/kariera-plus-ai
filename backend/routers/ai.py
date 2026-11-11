from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.job_search import search_jobs
from backend.services.job_matcher import calculate_job_match


router = APIRouter()


class AISearchRequest(BaseModel):
    position: str
    location: str = ""
    skills: str = ""
    workType: str = ""


class AIJobAnalysisRequest(BaseModel):
    title: str
    company: str
    location: str
    salary: str = ""
    url: str = ""
    contact: str = ""
    note: str = ""


@router.post("/ai/search")
async def ai_search(request: AISearchRequest):

    jobs = search_jobs(
        position=request.position,
        location=request.location,
        skills=request.skills,
    )

    for job in jobs:
        match = calculate_job_match(
            job,
            request.skills
        )

        job.update(match)

    return {
        "message": f"Nalezeno nabídek: {len(jobs)}",
        "search": {
            "position": request.position,
            "location": request.location,
            "skills": request.skills,
            "workType": request.workType,
        },
        "jobs": jobs,
    }


@router.post("/ai/analyze-job")
async def analyze_job(request: AIJobAnalysisRequest):

    prompt = f"""
Analyzuj tuto pracovní nabídku a odpověz česky.

Název pozice: {request.title}
Firma: {request.company}
Lokalita: {request.location}
Plat: {request.salary}
Kontakt: {request.contact}
Poznámka: {request.note}

Vytvoř praktickou analýzu pracovní nabídky.

Odpověď MUSÍ mít přesně tuto strukturu:

🎯 VHODNOST NABÍDKY
Napiš krátké hodnocení, pro koho je nabídka vhodná a proč.

🛠️ POŽADOVANÉ DOVEDNOSTI A TECHNOLOGIE
Uveď pouze dovednosti, technologie, programovací jazyky, frameworky nebo nástroje, které jsou skutečně uvedené v nabídce.
Pokud nejsou uvedeny, napiš: Nejsou uvedeny.

💡 CO BUDE UCHAZEČ PRAVDĚPODOBNĚ POTŘEBOVAT UMĚT
Popiš, co může být pro práci potřeba.
Jasně rozliš mezi tím, co je v nabídce uvedeno, a tím, co pouze rozumně předpokládáš.

⚠️ NA CO SI DÁT POZOR
Uveď chybějící nebo nejasné informace a případné věci, které by si měl uchazeč ověřit.

💰 INFORMACE O PLATU
Uveď pouze informace o platu, které jsou v nabídce skutečně uvedené.
Pokud plat uveden není, napiš: Plat není uveden.

⭐ CELKOVÉ DOPORUČENÍ
Napiš krátké a praktické doporučení, zda má smysl se o nabídku dále zajímat a co případně ověřit.

DŮLEŽITÁ PRAVIDLA:
- Odpovídej pouze česky.
- Nevymýšlej si informace, které nejsou v nabídce.
- Pokud informace chybí, výslovně napiš, že není uvedena.
- Buď stručný, konkrétní a praktický.
- Nepoužívej Markdown.
- Nepoužívej hvězdičky (*) pro odrážky.
"""

    from backend.services.ai_service import ask_ai

    result = ask_ai(prompt)

    return {
        "title": request.title,
        "company": request.company,
        "analysis": result,
    }
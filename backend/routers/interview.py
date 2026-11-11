from datetime import datetime
import json
import time

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from backend.database.database import get_connection
from backend.services.ai_service import ask_ai
from backend.utils.security import decode_access_token


router = APIRouter(
    prefix="/interview",
    tags=["AI Interview"],
)


class InterviewRequest(BaseModel):
    position: str
    company: str = ""
    interview_type: str


@router.post("/prepare")
async def prepare_interview(data: InterviewRequest):

    if data.interview_type == "preparation":
        prompt = f"""
Jsi zkušený personalista a kariérní kouč.

Připrav uchazeče na pracovní pohovor.

Pracovní pozice:
{data.position}

Firma:
{data.company if data.company else "Firma nebyla uvedena."}

Vytvoř seznam 10 realistických otázek, které může uchazeč na pohovoru dostat.

Otázky rozděl do těchto oblastí:
1. Představení uchazeče
2. Motivace
3. Zkušenosti a dovednosti
4. Technické nebo odborné znalosti
5. Chování a řešení problémů
6. Závěrečné otázky

Ke každé otázce napiš také krátkou radu, na co by měl uchazeč ve své odpovědi myslet.

Odpověď napiš v Markdown formátu.
Nepoužívej horizontální oddělovače typu "---".
"""

        start_time = time.perf_counter()
        ai_response = ask_ai(prompt)
        elapsed_time = time.perf_counter() - start_time

        print(f"⏱️ GEMINI POHOVOR: {elapsed_time:.2f} s")

        return {
            "message": "Otázky byly vytvořeny.",
            "position": data.position,
            "company": data.company,
            "interview_type": data.interview_type,
            "result": ai_response,
        }

    return {
        "message": "Simulovaný pohovor zatím není aktivní.",
        "position": data.position,
        "company": data.company,
        "interview_type": data.interview_type,
    }


class InterviewSimulationRequest(BaseModel):
    position: str
    company: str = ""


@router.post("/simulation/start")
async def start_simulation(data: InterviewSimulationRequest):

    prompt = f"""
Jsi zkušený personalista a vedeš pracovní pohovor.

Pracovní pozice:
{data.position}

Firma:
{data.company if data.company else "Firma nebyla uvedena."}

Zahaj simulovaný pracovní pohovor.

Polož uchazeči PRVNÍ realistickou otázku.
Otázka musí odpovídat pracovní pozici.

Nepřidávej hodnocení.
Nepřidávej vysvětlení.
Nepokládej více otázek najednou.

Vrať pouze samotnou otázku personalisty.
"""

    start_time = time.perf_counter()

    ai_response = ask_ai(prompt)

    elapsed_time = time.perf_counter() - start_time

    print(f"⏱️ SIMULACE START: {elapsed_time:.2f} s")

    return {
        "position": data.position,
        "company": data.company,
        "question": ai_response,
    }


class InterviewSimulationAnswerRequest(BaseModel):
    position: str
    company: str = ""
    question: str
    answer: str
    conversation: list[dict] = []


@router.post("/simulation/answer")
async def simulation_answer(data: InterviewSimulationAnswerRequest):

    history_text = ""

    for item in data.conversation:
        history_text += f"""
Otázka:
{item.get("question", "")}

Odpověď uchazeče:
{item.get("answer", "")}
"""

    prompt = f"""
Jsi zkušený personalista a vedeš simulovaný pracovní pohovor.

Pracovní pozice:
{data.position}

Firma:
{data.company if data.company else "Firma nebyla uvedena."}

Předchozí průběh pohovoru:
{history_text if history_text else "Toto je první otázka."}

Aktuální otázka:
{data.question}

Aktuální odpověď uchazeče:
{data.answer}

Na základě pracovní pozice, předchozího průběhu a aktuální odpovědi
pokračuj v simulovaném pohovoru.

Polož právě JEDNU další otázku.

Otázka může navazovat přímo na odpověď uchazeče.
Pokud odpověď odhalila zajímavou zkušenost, můžeš se na ni doptat.
Pokud je odpověď slabá nebo neúplná, můžeš ji vhodně rozvinout.
Otázka musí být realistická pro skutečný pracovní pohovor.

Nepřidávej hodnocení.
Nepřidávej vysvětlení.
Nepokládej více otázek najednou.

Vrať pouze samotnou otázku personalisty.
"""

    start_time = time.perf_counter()

    ai_response = ask_ai(prompt)

    elapsed_time = time.perf_counter() - start_time

    print(f"⏱️ SIMULACE DALŠÍ OTÁZKA: {elapsed_time:.2f} s")

    return {
        "next_question": ai_response,
    }


class InterviewEvaluationRequest(BaseModel):
    position: str
    company: str = ""
    conversation: list[dict] = []


@router.post("/simulation/evaluate")
async def evaluate_simulation(
    data: InterviewEvaluationRequest,
    authorization: str | None = Header(default=None),
):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Uživatel není přihlášen.",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Neplatný formát přístupového tokenu.",
        )

    token = authorization.replace("Bearer ", "", 1).strip()

    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except (ValueError, KeyError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Neplatný nebo prošlý přístupový token.",
        )

    conversation_text = ""

    for index, item in enumerate(data.conversation, start=1):
        conversation_text += f"""
OTÁZKA {index}:
{item.get("question", "")}

ODPOVĚĎ UCHAZEČE:
{item.get("answer", "")}

"""

    prompt = f"""
Jsi zkušený personalista a kariérní kouč.

Vyhodnoť celý simulovaný pracovní pohovor uchazeče.

Pracovní pozice:
{data.position}

Firma:
{data.company if data.company else "Firma nebyla uvedena."}

PRŮBĚH POHOVORU:
{conversation_text}

Vyhodnoť uchazeče podle těchto oblastí:

1. Obsah odpovědí
2. Relevance odpovědí
3. Odborné znalosti
4. Komunikace
5. Sebejistota
6. Profesionalita

Vytvoř celkové hodnocení od 0 do 100.

Dále uveď:

- 3 až 5 silných stránek uchazeče
- 3 až 5 oblastí ke zlepšení
- konkrétní doporučení, jak odpovědi zlepšit
- příklady odpovědí, které by bylo vhodné formulovat lépe

Buď objektivní a konkrétní.
Hodnocení založ pouze na skutečných odpovědích uchazeče.
Nevymýšlej si zkušenosti nebo znalosti, které uchazeč neuvedl.

Odpověď vrať VÝHRADNĚ jako validní JSON podle této struktury:

{{
  "score": 0,
  "content": 0,
  "relevance": 0,
  "expertise": 0,
  "communication": 0,
  "confidence": 0,
  "professionalism": 0,
  "strengths": [
    "..."
  ],
  "weaknesses": [
    "..."
  ],
  "recommendations": [
    "..."
  ],
  "better_answers": [
    {{
      "question": "...",
      "original_answer": "...",
      "better_answer": "..."
    }}
  ]
}}

Všechna skóre musí být čísla od 0 do 100.
Nevkládej Markdown.
Nevkládej ```json.
Vrať pouze JSON.
"""

    start_time = time.perf_counter()

    ai_response = ask_ai(prompt)
    elapsed_time = time.perf_counter() - start_time

    print(f"⏱️ VYHODNOCENÍ POHOVORU: {elapsed_time:.2f} s")
    print("========== VÝSLEDEK VYHODNOCENÍ ==========")
    print(ai_response)
    print("===========================================")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO interview_results (
            user_id,
            position,
            company,
            conversation,
            result,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            data.position,
            data.company,
            json.dumps(data.conversation, ensure_ascii=False),
            ai_response,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    conn.commit()
    conn.close()

    return {
        "result": ai_response,
    }


@router.get("/simulation/results")
async def get_simulation_results(
    authorization: str | None = Header(default=None),
):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Uživatel není přihlášen.",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Neplatný formát přístupového tokenu.",
        )

    token = authorization.replace("Bearer ", "", 1).strip()

    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except (ValueError, KeyError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Neplatný nebo prošlý přístupový token.",
        )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            position,
            company,
            conversation,
            result,
            created_at
        FROM interview_results
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,),
    )

    rows = cursor.fetchall()
    conn.close()

    results = []

    for row in rows:
        try:
            conversation = json.loads(row[3])
        except (json.JSONDecodeError, TypeError):
            conversation = []

        try:
            result = json.loads(row[4])
        except (json.JSONDecodeError, TypeError):
            result = row[4]

        results.append(
            {
                "id": row[0],
                "position": row[1],
                "company": row[2],
                "conversation": conversation,
                "result": result,
                "created_at": row[5],
            }
        )

    return {
        "results": results,
    }
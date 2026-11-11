from datetime import datetime
from pathlib import Path
from tempfile import mkstemp

from fastapi import APIRouter, File, Header, HTTPException, UploadFile

from backend.cv_parser import extract_text
from backend.database.database import get_connection
from backend.services.ai_service import ask_ai
from backend.utils.security import decode_access_token

router = APIRouter()

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@router.post("/cv/upload")
async def upload_cv(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Soubor nebyl vybrán.",
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Povolené jsou pouze soubory PDF a DOCX.",
        )

    file_descriptor, temporary_path = mkstemp(suffix=extension)
    file_path = Path(temporary_path)

    try:
        with open(file_descriptor, "wb", closefd=True) as temporary_file:
            while chunk := await file.read(1024 * 1024):
                temporary_file.write(chunk)

        try:
            text = extract_text(file_path)
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"Životopis se nepodařilo přečíst: {error}",
            )
    finally:
        file_path.unlink(missing_ok=True)

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Z životopisu se nepodařilo získat žádný text.",
        )

    return {
        "message": "Životopis byl úspěšně nahrán.",
        "filename": file.filename,
        "text_length": len(text),
    }


@router.post("/cv/analyze")
async def analyze_cv(
    file: UploadFile = File(...),
    authorization: str | None = Header(default=None),
):
    print("DEBUG Authorization přijat:", authorization is not None)
    print(
        "DEBUG Authorization začíná Bearer:",
        authorization.startswith("Bearer ") if authorization else False,
    )

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

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Soubor nebyl vybrán.",
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Povolené jsou pouze soubory PDF a DOCX.",
        )

    file_descriptor, temporary_path = mkstemp(suffix=extension)
    file_path = Path(temporary_path)

    try:
        with open(file_descriptor, "wb", closefd=True) as temporary_file:
            while chunk := await file.read(1024 * 1024):
                temporary_file.write(chunk)

        try:
            text = extract_text(file_path)
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"Životopis se nepodařilo přečíst: {error}",
            )
    finally:
        file_path.unlink(missing_ok=True)

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Z životopisu se nepodařilo získat žádný text.",
        )

    filename = file.filename

    prompt = f"""
Jsi profesionální AI kariérní poradce a expert na nábor zaměstnanců.

Analyzuj následující životopis kandidáta a vytvoř praktickou, konkrétní a profesionální analýzu v češtině.

DŮLEŽITÁ PRAVIDLA:

- Vycházej pouze z informací uvedených v životopisu.
- Nevymýšlej si pracovní zkušenosti, vzdělání, technologie ani jiné skutečnosti.
- Pokud nějaká důležitá informace v životopisu chybí, výslovně to uveď.
- Buď konkrétní a užitečný.
- Nepiš zbytečně obecné fráze.
- Zachovej profesionální, ale srozumitelný tón.
- Výsledek strukturovaně rozděl podle níže uvedených částí.
- Odpověď napiš v Markdown formátu.
- Nepoužívej horizontální oddělovače typu "---".

Použij přesně tuto strukturu:

# 🎯 Celkové hodnocení

Krátce zhodnoť, jak dobře je životopis připravený pro hledání zaměstnání.

Uveď také orientační hodnocení od 0 do 100 %.

# 💼 Pracovní zkušenosti

Shrň nejdůležitější pracovní zkušenosti kandidáta.

U každé zkušenosti vysvětli, jak může být relevantní pro budoucí zaměstnání.

# 🛠️ Dovednosti

Rozděl dovednosti na:

- technické dovednosti,
- odborné dovednosti,
- měkké dovednosti.

Uváděj pouze dovednosti, které lze skutečně doložit z životopisu.

# 💪 Silné stránky

Uveď největší přednosti kandidáta z pohledu zaměstnavatele.

# ⚠️ Co v životopisu chybí

Uveď důležité informace, které by bylo vhodné doplnit.

Například konkrétní projekty, technologie, výsledky práce, vzdělání, certifikace nebo odkazy na portfolio — ale pouze pokud jejich absence skutečně vyplývá z obsahu životopisu.

# 📈 Co doporučuješ zlepšit

Uveď konkrétní doporučení, jak životopis zlepšit.

Doporučení musí být praktická a použitelná.

# 🎯 Vhodné pracovní pozice

Navrhni konkrétní typy pracovních pozic, které odpovídají zkušenostem a dovednostem kandidáta.

U každé pozice krátce vysvětli proč.

# ⭐ Doporučení AI

Na závěr napiš krátké a konkrétní doporučení kandidátovi, co by měl udělat jako další krok při hledání zaměstnání.

ŽIVOTOPIS KANDIDÁTA:

{text}
"""

    print("⏱️ START AI ANALÝZY")

    ai_started_at = datetime.now()

    try:
        ai_result = ask_ai(prompt)
    except Exception as error:
        print("❌ AI ANALÝZA SELHALA:", error)
        raise HTTPException(
            status_code=500,
            detail=f"AI analýza se nepodařila: {error}",
        )

    ai_finished_at = datetime.now()
    ai_duration = ai_finished_at - ai_started_at

    print("⏱️ KONEC AI ANALÝZY")
    print("⏱️ DOBA AI ANALÝZY:", ai_duration)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO cv_profiles (
            user_id,
            filename,
            text,
            ai_analysis,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            filename,
            text,
            ai_result,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    conn.commit()
    conn.close()

    return {
        "message": "Životopis byl úspěšně analyzován.",
        "filename": filename,
        "text_length": len(text),
        "text": text,
        "ai_analysis": ai_result,
    }


@router.get("/cv/latest")
async def get_latest_cv_analysis(
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
            filename,
            text,
            ai_analysis,
            created_at
        FROM cv_profiles
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (user_id,),
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {
            "result": None,
        }

    return {
        "result": {
            "id": row[0],
            "filename": row[1],
            "text": row[2],
            "ai_analysis": row[3],
            "created_at": row[4],
        }
    }
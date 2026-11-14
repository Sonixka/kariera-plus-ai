# Kariéra+ AI

Kariéra+ AI je portfolio webová aplikace pro přehledné řízení hledání práce. Spojuje osobní správu pracovních nabídek, vyhledávání pozic, analýzu životopisu a přípravu na pracovní pohovor v jednom rozhraní.

Aplikace je zaměřená na české uchazeče o zaměstnání: při vyhledávání využívá data MPSV a API služeb Jooble a StartupJobs. Odpovědi nástrojů umělé inteligence jsou generovány v češtině.

## Funkce

- Registrace a přihlášení uživatelů pomocí JWT autentizace.
- Přidávání, úprava, mazání a změna stavu vlastních pracovních nabídek.
- Vyhledávání pracovních nabídek podle pozice a lokality napříč MPSV, Jooble a StartupJobs.
- Porovnání pracovních nabídek se zadanými dovednostmi a zobrazení míry shody.
- AI analýza vybrané pracovní nabídky pomocí Google Gemini.
- Nahrání životopisu ve formátu PDF nebo DOCX, extrakce textu a uložení AI analýzy pro přihlášeného uživatele.
- Příprava na pohovor, vícekroková simulace pohovoru a uložení závěrečného hodnocení.

## Použité technologie

- **Backend:** Python, FastAPI, Pydantic a Uvicorn
- **Databáze:** SQLite
- **Umělá inteligence:** Google Gemini prostřednictvím Google Gen AI SDK
- **Frontend:** HTML, CSS a čistý JavaScript
- **Zpracování dokumentů:** pdfplumber a python-docx
- **Autentizace:** JWT, passlib a bcrypt

## Struktura projektu

- `backend/` obsahuje aplikaci FastAPI.
  - `routers/` definuje endpointy pro autentizaci, pracovní nabídky, analýzu životopisu, AI funkce a pohovory.
  - `services/` obsahuje logiku pro AI, autentizaci, vyhledávání a porovnávání pracovních nabídek.
  - `models/` obsahuje datové modely Pydantic.
  - `database/database.py` vytváří a aktualizuje lokální databázovou strukturu SQLite.
  - `utils/` obsahuje pomocné funkce pro JWT autentizaci a zabezpečení.
- `frontend/` obsahuje statické stránky aplikace, styly a JavaScript spuštěný v prohlížeči.
- `requirements.txt` obsahuje seznam Python balíčků projektu.

## Spuštění projektu

## Požadavky

- Python 3.13 nebo novější.
- API klíče pro Google Gemini, Jooble a StartupJobs.

### 1. Naklonování repozitáře

```bash
git clone https://github.com/Sonixka/kariera-plus-ai.git
cd kariera-plus-ai
```

### 2. Vytvoření a aktivace virtuálního prostředí

Ve Windows PowerShellu spusť:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Instalace závislostí

V hlavní složce projektu spusť:

```powershell
python -m pip install -r requirements.txt
```

### 4. Nastavení proměnných prostředí

V hlavní složce projektu vytvoř soubor `.env`:

```env
GEMINI_API_KEY=tvuj_gemini_api_klic
SECRET_KEY=nahodny_tajny_klic_o_delce_alespon_32_znaku
JOOBLE_API_KEY=tvuj_jooble_api_klic
STARTUPJOBS_API_KEY=tvuj_startupjobs_api_klic
```

`GEMINI_API_KEY` a `SECRET_KEY` jsou potřebné pro spuštění API. `JOOBLE_API_KEY` a `STARTUPJOBS_API_KEY` umožňují načítání výsledků z těchto zdrojů; vyhledávání v datech MPSV funguje samostatně.

**Bezpečnost:** Soubor `.env` obsahuje citlivé údaje, je vyloučený ze správy verzí a nikdy nesmí být nahrán do veřejného repozitáře.

### 5. Spuštění backendu

V hlavní složce projektu spusť:

```powershell
python -m uvicorn backend.main:app --reload
```

API poběží na adrese [http://127.0.0.1:8000](http://127.0.0.1:8000). Interaktivní dokumentace FastAPI je dostupná na [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Při prvním spuštění aplikace vytvoří soubor `jobs.db` v hlavní složce projektu a inicializuje potřebné tabulky.

### 6. Spuštění frontendu

V druhém terminálu, opět v hlavní složce projektu, spusť:

```powershell
python -m http.server 5500 --directory frontend
```

V prohlížeči otevři [http://localhost:5500](http://localhost:5500). Backend musí během používání frontendu zůstat spuštěný; frontend aktuálně používá API na adrese `http://127.0.0.1:8000`.

## Přehled API

Backend nabízí endpointy pro registraci a přihlášení, správu a vyhledávání pracovních nabídek, nahrávání a analýzu životopisů, AI analýzu nabídek a přípravu, simulaci a ukládání výsledků pohovorů. Přesné formáty požadavků a odpovědí jsou při spuštěném backendu dostupné v dokumentaci `/docs`.

## Poznámky

- Databáze, nahrané životopisy a lokální konfigurační soubory jsou záměrně ignorovány Gitem.
- Vyhledávání pracovních nabídek využívá externí služby; výsledky závisejí na jejich dostupnosti a platných API klíčích.
- Projekt je průběžně rozvíjen jako portfolio aplikace.

## Autor

Sonixka — [GitHub profil](https://github.com/Sonixka)

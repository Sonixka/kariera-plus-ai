# Kariéra+ AI

**AI-powered job search assistant built for the Czech job market.**

Kariéra+ AI je webová aplikace, která pomáhá uchazečům o zaměstnání organizovat hledání práce na jednom místě. Kombinuje správu pracovních nabídek, vyhledávání volných pozic, analýzu životopisu a přípravu na pracovní pohovor s využitím umělé inteligence.

Aplikace je zaměřena na český pracovní trh. Při vyhledávání využívá data MPSV a služby Jooble a StartupJobs. AI funkce využívají Google Gemini a komunikují v češtině.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/JavaScript-Frontend-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript" />
  <img src="https://img.shields.io/badge/Google-Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white" alt="Google Gemini" />
</p>

---

## ✨ Hlavní funkce

### 👤 Uživatelský účet
- Registrace a přihlášení uživatelů.
- Zabezpečení pomocí JWT autentizace.
- Oddělená správa pracovních nabídek jednotlivých uživatelů.

### 💼 Správa pracovních nabídek
- Přidávání, úprava a mazání pracovních nabídek.
- Evidence průběhu hledání zaměstnání.
- Změna stavu nabídky podle průběhu výběrového řízení.

### 🔎 Vyhledávání zaměstnání
- Vyhledávání podle pracovní pozice a lokality.
- Propojení se zdroji MPSV, Jooble a StartupJobs.
- Porovnávání pracovních nabídek se zadanými dovednostmi.
- Výpočet a zobrazení míry shody s pracovní pozicí.

### 🤖 AI analýza
- Analýza pracovních nabídek pomocí Google Gemini.
- Nahrávání životopisů ve formátu PDF a DOCX.
- Extrakce textu z dokumentů.
- AI vyhodnocení životopisu a uložení výsledků pro přihlášeného uživatele.

### 🎯 Příprava na pracovní pohovor
- Příprava na pracovní pohovor.
- Vícekroková simulace pohovoru.
- Vyhodnocení odpovědí a uložení závěrečného hodnocení.

---

## 🛠️ Použité technologie

| Oblast | Technologie |
|---|---|
| Programovací jazyk | Python |
| Backend | FastAPI, Uvicorn |
| Datové modely | Pydantic |
| Databáze | SQLite |
| Umělá inteligence | Google Gemini, Google Gen AI SDK |
| Frontend | HTML5, CSS3, JavaScript |
| Autentizace | JWT, Passlib, bcrypt |
| Zpracování PDF | pdfplumber |
| Zpracování DOCX | python-docx |
| Vývojové prostředí | Visual Studio Code |
| Správa verzí | Git, GitHub |

---

## 📁 Struktura projektu

```text
kariera-plus-ai/
│
├── backend/
│   ├── database/
│   ├── models/
│   ├── routers/
│   ├── services/
│   ├── uploads/
│   ├── utils/
│   └── main.py
│
├── frontend/
│   ├── ai_analysis.html
│   ├── cv-builder.html
│   ├── cv.html
│   ├── index.html
│   ├── interview.html
│   ├── login.html
│   ├── registre.html
│   └── style.css
│
├── tests/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

### Backend

- `routers/` – API endpointy pro autentizaci, pracovní nabídky, životopisy, AI funkce a pohovory.
- `services/` – aplikační logika, AI služby, autentizace, vyhledávání a porovnávání pracovních nabídek.
- `models/` – datové modely a validace pomocí Pydantic.
- `database/` – připojení k databázi a správa struktury SQLite.
- `utils/` – pomocné funkce pro JWT autentizaci a zabezpečení.
- `uploads/` – soubory nahrané do aplikace.
- `main.py` – hlavní vstupní bod aplikace FastAPI.

### Frontend

Uživatelské rozhraní tvořené HTML stránkami, CSS styly a JavaScriptem.

---

## 🚀 Spuštění projektu

### Požadavky

- Python 3.13 nebo novější
- pip
- Git

### 1. Naklonování repozitáře

```bash
git clone https://github.com/Sonixka/kariera-plus-ai.git
```

### 2. Otevření složky projektu

```bash
cd kariera-plus-ai
```

### 3. Vytvoření virtuálního prostředí

```bash
python -m venv .venv
```

### 4. Aktivace virtuálního prostředí

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Instalace závislostí

```bash
pip install -r requirements.txt
```

### 6. Konfigurace prostředí

V kořenové složce projektu vytvoř soubor `.env` a nastav potřebné API klíče a konfigurační hodnoty podle používaných služeb.

Pro AI funkce je potřeba platný přístup ke Google Gemini API.

**Důležité:** Soubor `.env` s tajnými klíči nikdy neukládej do veřejného GitHub repozitáře.

### 7. Spuštění aplikace

```bash
python -m uvicorn backend.main:app --reload
```

Po spuštění je aplikace dostupná na:

```text
http://127.0.0.1:8000
```

Dokumentace API:

```text
http://127.0.0.1:8000/docs
```

---

## 🎯 Cíl projektu

Cílem Kariéra+ AI je vytvořit praktický nástroj, který usnadní hledání zaměstnání a pomůže uchazečům lépe se připravit na pracovní příležitosti.

Projekt vzniká jako vlastní vývojářský projekt se zaměřením na Python, vývoj webových aplikací, práci s API, databázemi a integraci umělé inteligence.

---

<p align="center">
  <b>Built with Python, curiosity and AI. ✨</b>
</p>

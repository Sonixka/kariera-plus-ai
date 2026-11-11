import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY nebyl nalezen v souboru .env")

client = genai.Client(api_key=GEMINI_API_KEY)

GEMINI_MODEL = "gemini-3.5-flash-lite"


def ask_ai(prompt: str) -> str:
    max_retries = 3
    last_error: Exception | None = None

    for attempt in range(max_retries):
        try:
            start_time = time.perf_counter()

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
                ),
            )

            elapsed_time = time.perf_counter() - start_time
            print(f"⏱️ GEMINI POKUS {attempt + 1}: {elapsed_time:.2f} s")

            if response.text is None:
                raise RuntimeError("Gemini nevrátil textovou odpověď.")

            return response.text
        except Exception as error:
            last_error = error

            if "503" in str(error) and attempt < max_retries - 1:
                print(
                    f"⚠️ Google API je dočasně přetížené (503). "
                    f"Zkouším znovu za 2 s ({attempt + 1}/{max_retries})..."
                )
                time.sleep(2)
                continue

            print("❌ CHYBA GEMINI API:", error)
            raise RuntimeError(f"Gemini API selhalo: {error}") from error

    if last_error is not None:
        raise RuntimeError(f"Gemini API selhalo po opakovaných pokusech: {last_error}")

    raise RuntimeError("Gemini API selhalo po opakovaných pokusech.")
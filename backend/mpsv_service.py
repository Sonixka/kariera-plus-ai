import json
import os
import urllib.request
import requests


MPSV_URL = "https://data.mpsv.cz/od/soubory/volna-mista/volna-mista.json"

DATA_DIR = "backend/data"
DATA_FILE = os.path.join(DATA_DIR, "mpsv_jobs.json")


def download_mpsv_data():
    os.makedirs(DATA_DIR, exist_ok=True)

    print("Stahuji data z MPSV...")

    response = requests.get(
        MPSV_URL,
        timeout=120,
    )

    response.raise_for_status()

    with open(DATA_FILE, "wb") as file:
        file.write(response.content)

    print("Data MPSV byla uložena.")

    return DATA_FILE


def load_mpsv_data():
    if not os.path.exists(DATA_FILE):
        download_mpsv_data()

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


if __name__ == "__main__":
    file_path = download_mpsv_data()

    print("Soubor byl uložen zde:")
    print(file_path)
import urllib.request
import urllib.error

URL = "https://data.mpsv.cz/od/soubory/volna-mista/volna-mista.json"

try:
    with urllib.request.urlopen(URL, timeout=30) as response:
        content = response.read()
        text = content.decode("utf-8", errors="replace")
        status = response.getcode()
except urllib.error.URLError as e:
    print("HTTP error:", e)
else:
    print("HTTP status:", status)
    print("Velikost odpovědi:", len(content), "bytů")
    print("Prvních 1000 znaků:")
    print(text[:1000])
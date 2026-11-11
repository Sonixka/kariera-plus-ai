from pathlib import Path

from backend.cv_parser import extract_text


file_path = Path("backend/uploads/cv_sona_parizkova.pdf")

text = extract_text(file_path)

print("\n========== ZAČÁTEK TEXTU CV ==========\n")
print(text)
print("\n=========== KONEC TEXTU CV ===========\n")
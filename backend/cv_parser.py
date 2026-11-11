from pathlib import Path
import pdfplumber  # type: ignore[reportMissingImports]
from docx import Document  # type: ignore[reportMissingImports]


def extract_text_from_pdf(file_path: Path) -> str:
    """
    Extrakce textu z PDF pomocí pdfplumber.
    Funguje na většinu moderních PDF, včetně těch exportovaných z Wordu.
    """
    text = []

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
    except Exception as error:
        raise RuntimeError(f"Chyba při čtení PDF: {error}")

    return "\n".join(text).strip()


def extract_text_from_docx(file_path: Path) -> str:
    """
    Extrakce textu z DOCX včetně tabulek.
    """
    try:
        document = Document(str(file_path))
    except Exception as error:
        raise RuntimeError(f"Chyba při čtení DOCX: {error}")

    text = []

    # Odstavce
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text.strip())

    # Tabulky
    for table in document.tables:
        for row in table.rows:
            row_text = " ".join(
                cell.text.strip()
                for cell in row.cells
                if cell.text.strip()
            )
            if row_text:
                text.append(row_text)

    return "\n".join(text).strip()


def extract_text(file_path: Path) -> str:
    """
    Hlavní funkce pro extrakci textu podle typu souboru.
    """
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if extension == ".docx":
        return extract_text_from_docx(file_path)

    raise ValueError("Nepodporovaný formát souboru. Povolené jsou PDF a DOCX.")

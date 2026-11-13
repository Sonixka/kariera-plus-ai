
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from docx import Document

from backend.cv_parser import extract_text


class TestCVParser(unittest.TestCase):

    def test_extract_text_from_docx(self):
        """Ověří extrakci textu z DOCX včetně tabulek."""

        file_path = Path("test_cv_parser_sample.docx")

        document = Document()
        document.add_paragraph("Testovací životopis")
        table = document.add_table(rows=1, cols=2)
        table.cell(0, 0).text = "Python"
        table.cell(0, 1).text = "FastAPI"
        document.save(str(file_path))

        try:
            result = extract_text(file_path)

            self.assertIn("Testovací životopis", result)
            self.assertIn("Python", result)
            self.assertIn("FastAPI", result)

        finally:
            file_path.unlink(missing_ok=True)

    @patch("backend.cv_parser.pdfplumber.open")
    def test_extract_text_from_pdf(self, mock_pdf_open):
        """Ověří extrakci textu z PDF."""

        page_one = MagicMock()
        page_one.extract_text.return_value = "První stránka životopisu"

        page_two = MagicMock()
        page_two.extract_text.return_value = "Druhá stránka životopisu"

        mock_pdf_open.return_value.__enter__.return_value.pages = [
            page_one,
            page_two,
        ]

        result = extract_text(Path("test.pdf"))

        self.assertIn("První stránka životopisu", result)
        self.assertIn("Druhá stránka životopisu", result)

    def test_unsupported_file_format(self):
        """Ověří odmítnutí nepodporovaného formátu."""

        with self.assertRaises(ValueError):
            extract_text(Path("test.txt"))


if __name__ == "__main__":
    unittest.main()

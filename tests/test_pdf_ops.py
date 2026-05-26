import tempfile
import unittest
from pathlib import Path

import fitz

from doclira_lite.pdf_ops import add_basic_watermark, delete_page, merge_pdfs, rotate_page, split_pdf


def create_pdf(path, page_count=2):
    document = fitz.open()
    for number in range(page_count):
        page = document.new_page()
        page.insert_text((72, 92), f"Sample page {number + 1}", fontsize=18)
    document.save(path)
    document.close()


class PdfOperationsTest(unittest.TestCase):
    def test_merge_and_split(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            first = folder / "first.pdf"
            second = folder / "second.pdf"
            merged = folder / "merged.pdf"
            create_pdf(first, 2)
            create_pdf(second, 1)
            merge_pdfs([first, second], merged)
            with fitz.open(merged) as document:
                self.assertEqual(document.page_count, 3)
            outputs = split_pdf(merged, folder / "split")
            self.assertEqual(len(outputs), 3)

    def test_page_changes_and_watermark(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            source = folder / "source.pdf"
            rotated = folder / "rotated.pdf"
            deleted = folder / "deleted.pdf"
            marked = folder / "marked.pdf"
            create_pdf(source, 2)
            rotate_page(source, rotated, 0)
            with fitz.open(rotated) as document:
                self.assertEqual(document[0].rotation, 90)
            delete_page(source, deleted, 1)
            with fitz.open(deleted) as document:
                self.assertEqual(document.page_count, 1)
            add_basic_watermark(source, marked, "CONFIDENTIAL")
            with fitz.open(marked) as document:
                self.assertIn("CONFIDENTIAL", document[0].get_text())


if __name__ == "__main__":
    unittest.main()

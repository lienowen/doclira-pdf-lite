from pathlib import Path

import fitz


def merge_pdfs(paths, output_path):
    source_paths = [Path(path) for path in paths]
    if len(source_paths) < 2:
        raise ValueError("Select at least two PDF files to merge.")
    target = fitz.open()
    try:
        for path in source_paths:
            with fitz.open(path) as source:
                target.insert_pdf(source)
        target.save(output_path)
    finally:
        target.close()


def split_pdf(source_path, output_dir):
    source_path = Path(source_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    with fitz.open(source_path) as source:
        for number in range(source.page_count):
            target = fitz.open()
            try:
                target.insert_pdf(source, from_page=number, to_page=number)
                output = output_dir / f"{source_path.stem}_page_{number + 1:03d}.pdf"
                target.save(output)
                outputs.append(output)
            finally:
                target.close()
    return outputs


def rotate_page(source_path, output_path, page_number, degrees=90):
    with fitz.open(source_path) as document:
        page = document[page_number]
        page.set_rotation((page.rotation + degrees) % 360)
        document.save(output_path)


def delete_page(source_path, output_path, page_number):
    with fitz.open(source_path) as document:
        if document.page_count <= 1:
            raise ValueError("A PDF must keep at least one page.")
        document.delete_page(page_number)
        document.save(output_path)


def add_basic_watermark(source_path, output_path, watermark_text, opacity=0.22):
    text = watermark_text.strip()
    if not text:
        raise ValueError("Enter watermark text first.")
    if any(ord(character) > 127 for character in text):
        raise ValueError("Lite watermark text currently supports Latin characters only.")
    with fitz.open(source_path) as document:
        for page in document:
            rect = page.rect
            baseline = fitz.Point(rect.x0 + 36, rect.y1 - 36)
            page.insert_text(
                baseline,
                text,
                fontsize=17,
                fontname="helv",
                color=(0.06, 0.42, 0.38),
                fill_opacity=max(0.08, min(float(opacity), 0.8)),
                overlay=True,
            )
        document.save(output_path)


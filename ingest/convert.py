from pathlib import Path
from docling.document_converter import DocumentConverter

PDF_DIR = Path("original-pdfs")
OUTPUT_DIR = Path("knowledge-base")

OUTPUT_DIR.mkdir(exist_ok=True)

converter = DocumentConverter()

for pdf_file in PDF_DIR.glob("*.pdf"):
    print(f"Converting: {pdf_file.name}")

    result = converter.convert(pdf_file)

    markdown = result.document.export_to_markdown()

    output_file = OUTPUT_DIR / f"{pdf_file.stem}.md"
    output_file.write_text(markdown, encoding="utf-8")

    print(f"Saved: {output_file}")

print("Conversion complete!")
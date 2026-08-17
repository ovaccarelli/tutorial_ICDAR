"""Transform all PDF files in the data directory into markdown files with the same name."""

from pathlib import Path

from pdfminer.high_level import extract_text

HERE = Path(__file__).parent
DATA_DIR = HERE.parent.parent / "data"

if __name__ == "__main__":
    pdf_files = list(DATA_DIR.glob("*.pdf"))
    for pdf_file in pdf_files:
        pdfminer_md_file = pdf_file.with_suffix(".md")
        pdfminer_text = extract_text(pdf_file)
        pdfminer_md_file.write_text(pdfminer_text)
        print(f"Saved markdown file: {pdfminer_md_file.name}")

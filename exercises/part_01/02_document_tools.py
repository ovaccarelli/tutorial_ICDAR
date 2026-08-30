"""Document Tools Exercise

In this exercise, we explore how to extract text from different document formats.

1. List all available documents in the configured document directory.
2. Extract text from a Markdown file using pathlib.
3. Extract text from a PDF document using pdfminer.
4. Extract text from an image file using RapidOCR.

For each extraction, measure and print how long the operation takes.

"""

import time
from pathlib import Path

from pdfminer.high_level import extract_text
from rapidocr import RapidOCR

from tutorial_ICDAR.utils.console_utils import (
    INFO_STYLE,
    console,
    print_result,
    print_step,
)

# Define file paths and constants
HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent.parent / "data"
MY_DOCUMENTS = DATA_DIR / "my_documents"

#################################################################
# STEP 1 - List all available documents in the directory
#################################################################

print_step("STEP 1 - List all available documents in the directory")

# List all files in the MY_DOCUMENTS directory to see what documents are available for preprocessing.
available_documents = sorted(
    path.name
    for path in MY_DOCUMENTS.iterdir()
    if path.is_file() and not path.name.startswith(".")
)
console.print("Available documents:", style=INFO_STYLE)
print_result(available_documents)

#################################################################
# STEP 2 - Extract text from a Markdown file
#################################################################

print_step("STEP 2 - Extract text from a Markdown file")

markdown_path = MY_DOCUMENTS / "Flight_Ticket.md"

# EXERCISE - Read the Markdown file as UTF-8 text
start_time = time.time()
doc_markdown = ...(encoding="utf-8")
end_time = time.time()

console.print(f"Using file: {markdown_path.name}", style=INFO_STYLE)
console.print(f"Markdown extracted {len(doc_markdown)} characters", style=INFO_STYLE)
console.print(f"Extraction time: {end_time - start_time:.4f} seconds", style=INFO_STYLE)
console.print("Preview of first 500 characters:", style=INFO_STYLE)
print_result(doc_markdown[:500])

#################################################################
# STEP 3 - Extract PDF text
#################################################################

print_step("STEP 3 - Extract PDF text")

pdf_path = MY_DOCUMENTS / "HAL_9000_Expense_Reimbursement_Policy.pdf"

# EXERCISE - Extract the PDF text using pdfminer
start_time = time.time()
doc_pdfminer = ...
end_time = time.time()

console.print(f"Using file: {pdf_path.name}", style=INFO_STYLE)
console.print(f"pdfminer extracted {len(doc_pdfminer)} characters", style=INFO_STYLE)
console.print(f"Extraction time: {end_time - start_time:.4f} seconds", style=INFO_STYLE)
console.print("Preview of first 500 characters:", style=INFO_STYLE)
print_result(doc_pdfminer[:500])

#################################################################
# STEP 4 - Extract text from image file
#################################################################

print_step("STEP 4 - Extract text from an image file")

image_path = MY_DOCUMENTS / "Restaurant_Invoice.png"

# EXERCISE - Create the RapidOCR engine and extract the image text
engine = ...(params={"Global.log_level": "warning"})

start_time = time.time()
result = engine(str(image_path))
doc_ocr = "\n".join(result.txts or [])
end_time = time.time()

console.print(f"Using file: {image_path.name}", style=INFO_STYLE)
console.print(f"RapidOCR extracted {len(doc_ocr)} characters", style=INFO_STYLE)
console.print(f"Extraction time: {end_time - start_time:.4f} seconds", style=INFO_STYLE)
console.print("Preview of first 500 characters:", style=INFO_STYLE)
print_result(doc_ocr[:500])

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

# Define file paths and constants
HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent.parent / "data"
MY_DOCUMENTS = DATA_DIR / "my_documents"

#################################################################
# STEP 1 - List all available documents in the directory
#################################################################

print("\n----------- STEP 1: LIST DOCUMENTS -----------")

# List all files in the MY_DOCUMENTS directory to see what documents are available for preprocessing.
available_documents = sorted(
    path.name
    for path in MY_DOCUMENTS.iterdir()
    if path.is_file() and not path.name.startswith(".")
)
print(f"Available documents: {available_documents}")

#################################################################
# STEP 2 - Extract text from a Markdown file
#################################################################

print("\n----------- STEP 2: MARKDOWN EXTRACTION -----------")

markdown_path = MY_DOCUMENTS / "Flight_Ticket.md"

# EXERCISE - Read the Markdown file as UTF-8 text
start_time = time.time()
doc_markdown = ...(encoding="utf-8")
end_time = time.time()

print(f"Using file: {markdown_path.name}")
print(f"Markdown extracted {len(doc_markdown)} characters")
print(f"Extraction time: {end_time - start_time:.4f} seconds")
print(f"Preview of first 500 characters:\n{doc_markdown[:500]}")

#################################################################
# STEP 3 - Extract PDF text
#################################################################

print("\n----------- STEP 3: PDF EXTRACTION -----------")

pdf_path = MY_DOCUMENTS / "HAL_9000_Expense_Reimbursement_Policy.pdf"

# EXERCISE - Extract the PDF text using pdfminer
start_time = time.time()
doc_pdfminer = ...
end_time = time.time()

print(f"Using file: {pdf_path.name}")
print(f"pdfminer extracted {len(doc_pdfminer)} characters")
print(f"Extraction time: {end_time - start_time:.4f} seconds")
print(f"Preview of first 500 characters:\n{doc_pdfminer[:500]}")

#################################################################
# STEP 4 - Extract text from image file
#################################################################

print("\n----------- STEP 4: IMAGE OCR -----------")

image_path = MY_DOCUMENTS / "Restaurant_Invoice.png"

# EXERCISE - Create the RapidOCR engine and extract the image text
engine = ...

start_time = time.time()
result = engine(str(image_path))
doc_ocr = "\n".join(result.txts or [])
end_time = time.time()

print(f"Using file: {image_path.name}")
print(f"RapidOCR extracted {len(doc_ocr)} characters")
print(f"Extraction time: {end_time - start_time:.4f} seconds")
print(f"Preview of first 500 characters:\n{doc_ocr[:500]}")

"""Solution for the Document Tools Exercise.

This solution mirrors exercises/part_01/02_document_tools.py and fills every
exercise placeholder.

"""

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

# List all files in the MY_DOCUMENTS directory to see what documents are available for preprocessing.
available_documents = sorted(
    path.name
    for path in MY_DOCUMENTS.iterdir()
    if path.is_file() and not path.name.startswith(".")
)
print(f"Available documents: {available_documents}")

#################################################################
# STEP 2 - Extract PDF text
#################################################################

pdf_path = MY_DOCUMENTS / "HAL_9000_Expense_Reimbursement_Policy.pdf"

# SOLUTION - Extract the text from the PDF using pdfminer
doc_pdfminer = extract_text(str(pdf_path))

print(f"Using file: {pdf_path.name}")
print(f"pdfminer extracted {len(doc_pdfminer)} characters")
print(f"Preview of first 500 characters:\n{doc_pdfminer[:500]}")

#################################################################
# STEP 3 - Extract text from image file
#################################################################

image_path = MY_DOCUMENTS / "Restaurant_Invoice.png"

# SOLUTION - Extract the text from the image using RapidOCR
engine = RapidOCR()

result = engine(str(image_path))
doc_ocr = "\n".join(result.txts or [])

print(f"Using file: {image_path.name}")
print(f"RapidOCR extracted {len(doc_ocr)} characters")
print(f"Preview of first 500 characters:\n{doc_ocr[:500]}")

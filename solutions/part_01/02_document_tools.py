"""Solution for the Document Tools Exercise.

This solution mirrors exercises/part_01/02_document_tools.py and fills every
exercise placeholder.

"""

import time
from pathlib import Path

from loguru import logger
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
logger.info(f"Available documents: {available_documents}")

#################################################################
# STEP 2 - Extract text from a Markdown file
#################################################################

markdown_path = MY_DOCUMENTS / "Flight_Ticket.md"

# SOLUTION - Measure how long it takes to read the Markdown file as UTF-8 text
start_time = time.time()
doc_markdown = markdown_path.read_text(encoding="utf-8")
end_time = time.time()

logger.info(f"Using file: {markdown_path.name}")
logger.info(f"Markdown extracted {len(doc_markdown)} characters")
logger.info(f"Extraction time: {end_time - start_time:.4f} seconds")
logger.info(f"Preview of first 500 characters:\n{doc_markdown[:500]}")

#################################################################
# STEP 3 - Extract PDF text
#################################################################

pdf_path = MY_DOCUMENTS / "HAL_9000_Expense_Reimbursement_Policy.pdf"

# SOLUTION - Measure how long it takes to extract the PDF text using pdfminer
start_time = time.time()
doc_pdfminer = extract_text(str(pdf_path))
end_time = time.time()

logger.info(f"Using file: {pdf_path.name}")
logger.info(f"pdfminer extracted {len(doc_pdfminer)} characters")
logger.info(f"Extraction time: {end_time - start_time:.4f} seconds")
logger.info(f"Preview of first 500 characters:\n{doc_pdfminer[:500]}")

#################################################################
# STEP 4 - Extract text from image file
#################################################################

image_path = MY_DOCUMENTS / "Restaurant_Invoice.png"

# SOLUTION - Measure how long RapidOCR takes to extract the image text
engine = RapidOCR()

start_time = time.time()
result = engine(str(image_path))
doc_ocr = "\n".join(result.txts or [])
end_time = time.time()

logger.info(f"Using file: {image_path.name}")
logger.info(f"RapidOCR extracted {len(doc_ocr)} characters")
logger.info(f"Extraction time: {end_time - start_time:.4f} seconds")
logger.info(f"Preview of first 500 characters:\n{doc_ocr[:500]}")

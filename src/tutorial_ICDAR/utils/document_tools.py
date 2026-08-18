"""Document handling and text extraction tools for a Pydantic AI agent."""

from pathlib import Path
from typing import Literal

from loguru import logger
from rapidocr import RapidOCR

HERE = Path(__file__).parent
DATA_DIR = HERE.parent.parent.parent / "data"
DOCUMENT_DIR = DATA_DIR / "my_documents"


DocumentType = Literal["text", "image", "unknown"]


def list_my_available_documents() -> list[str]:
    """List available workshop documents.
    Returns:
        A list of document filenames available in the document directory.
    """
    return sorted(
        path.name
        for path in DOCUMENT_DIR.iterdir()
        if path.is_file() and not path.name.startswith(".")
    )


def extract_text_from_md_or_txt_file(file_path: str) -> str:
    """Fast, best-effort plain-text extraction for Markdown or text files.

    Args:
        file_path: The filename or path of the document to extract text from.

    Returns:
        The extracted plain text content of the document.
    """
    path = DOCUMENT_DIR / file_path
    logger.info(f"Extracting plain text from {path.name}")
    return path.read_text(encoding="utf-8")


def extract_text_from_image_file(file_path: str) -> str:
    """OCR extraction for image files with uv-managed RapidOCR.

    Args:
        file_path: The filename or path of the image to extract text from.

    Returns:
        The extracted text content of the image.
    """
    path = DOCUMENT_DIR / file_path

    logger.info(f"Extracting image text with RapidOCR from {path.name}")
    ocr = RapidOCR()
    result = ocr(path)
    return "\n".join(result.txts) if result else "Image text could not be extracted."

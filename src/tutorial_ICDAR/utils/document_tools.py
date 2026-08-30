"""Document handling and text extraction tools for a Pydantic AI agent."""

from pathlib import Path

from loguru import logger
from pdfminer.high_level import extract_text
from pydantic_ai import ModelRetry
from rapidocr import RapidOCR

HERE = Path(__file__).parent
DATA_DIR = HERE.parent.parent.parent / "data"
DOCUMENT_DIR = DATA_DIR / "my_documents"


TEXT_EXTENSIONS = {".md", ".txt"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


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
    """Extract text only from Markdown (.md) or plain-text (.txt) files.

    Args:
        file_path: The filename or path of the document to extract text from.

    Returns:
        The extracted plain text content of the document.
    """
    path = DOCUMENT_DIR / file_path

    if not path.is_file():
        raise ModelRetry(
            f"Document '{file_path}' was not found. "
            "Call list_my_available_documents and choose an existing filename."
        )

    if path.suffix.lower() not in TEXT_EXTENSIONS:
        if path.suffix.lower() == ".pdf":
            raise ModelRetry(
                f"'{path.name}' is a PDF, so it cannot be read with the Markdown/text tool. "
                "If the user is asking about the HAL 9000 policy, use the RAG search tool "
                "instead. Otherwise, use the PDF extraction tool."
            )
        raise ModelRetry(
            f"'{path.name}' is not a Markdown or text file. "
            "Use the image extraction tool for .png, .jpg, .jpeg, or .webp files."
        )

    logger.info(f"Extracting plain text from {path.name}")
    return path.read_text(encoding="utf-8")


def extract_text_from_image_file(file_path: str) -> str:
    """Extract text only from image files using uv-managed RapidOCR.

    Args:
        file_path: The filename or path of the image to extract text from.

    Returns:
        The extracted text content of the image.
    """
    path = DOCUMENT_DIR / file_path

    if not path.is_file():
        raise ModelRetry(
            f"Document '{file_path}' was not found. "
            "Call list_my_available_documents and choose an existing filename."
        )

    if path.suffix.lower() not in IMAGE_EXTENSIONS:
        if path.suffix.lower() == ".pdf":
            raise ModelRetry(
                f"'{path.name}' is a PDF, not an image supported by this OCR tool. "
                "Use the PDF extraction tool instead."
            )
        raise ModelRetry(
            f"'{path.name}' is not a supported image. "
            "Use the Markdown/text extraction tool for .md or .txt files."
        )

    logger.info(f"Extracting image text with RapidOCR from {path.name}")
    ocr = RapidOCR(params={"Global.log_level": "warning"})
    result = ocr(path)
    return "\n".join(result.txts) if result else "Image text could not be extracted."


def extract_text_from_pdf_file(file_path: str) -> str:
    """Extract text only from PDF files using pdfminer.

    Args:
        file_path: The filename or path of the PDF document to extract text from.

    Returns:
        The extracted text content of the PDF document.
    """
    path = DOCUMENT_DIR / file_path

    if not path.is_file():
        raise ModelRetry(
            f"Document '{file_path}' was not found. "
            "Call list_my_available_documents and choose an existing filename."
        )

    if path.suffix.lower() != ".pdf":
        raise ModelRetry(
            f"'{path.name}' is not a PDF file. Use the Markdown/text extraction "
            "tool for .md or .txt files, or the image extraction tool for images."
        )

    logger.info(f"Extracting PDF text with pdfminer from {path.name}")
    return extract_text(str(path))

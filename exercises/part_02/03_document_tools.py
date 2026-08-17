"""Document handling and text extraction tools for a Pydantic AI agent."""

from pathlib import Path

from loguru import logger
from rapidocr import RapidOCR

HERE = Path(__file__).parent
DATA_DIR = HERE.parent.parent / "data"
DOCUMENT_DIR = DATA_DIR / "my_documents"


def list_my_available_documents() -> list[str]:
    """List available workshop documents.
    Returns:
        A list of document filenames available in the document directory.
    """
    return sorted(path.name for path in DOCUMENT_DIR.iterdir() if path.is_file())


def resolve_document_path(file_path: str) -> Path:
    """Resolve document names relative to the configured document folder.

    Names that are not absolute paths will be resolved relative to the document directory.

    Args:
        file_path: The filename or path of the document to resolve.

    Returns:
        A Path object representing the resolved absolute path to the document.
    """
    document_root = DOCUMENT_DIR.resolve()
    path = Path(file_path).expanduser()
    if not path.is_absolute():
        path = document_root / path

    path = path.resolve()

    return path


def extract_text_from_md_or_txt_file(file_path: str) -> str:
    """Fast, best-effort plain-text extraction for Markdown or text files.

    Args:
        file_path: The filename or path of the document to extract text from.

    Returns:
        The extracted plain text content of the document.
    """
    path = resolve_document_path(file_path)
    logger.info(f"Extracting plain text from {path.name}")
    return path.read_text(encoding="utf-8")


def extract_text_from_image_file(file_path: str) -> str:
    """OCR extraction for image files with uv-managed RapidOCR.

    Args:
        file_path: The filename or path of the image to extract text from.

    Returns:
        The extracted text content of the image.
    """
    path = resolve_document_path(file_path)

    logger.info(f"Extracting image text with RapidOCR from {path.name}")
    ocr = RapidOCR()
    result = ocr(path)

    return " /n".join(result.txts) if result else "Image text could not be extracted."


if __name__ == "__main__":
    # EXERCISE 0 - Act as an agent and use the correct tools to solve the exercises.

    # EXERCISE 1 - List and print the available documents
    print(...)

    # EXERCISE 2 - Extract and print text from a Markdown or text file
    print(...)

    # EXERCISE 3 - Extract and print text from an image file using OCR
    print(...)

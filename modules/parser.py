

import pdfplumber
import os


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts raw text from a PDF file page by page.

    Args:
        file_path: Path to PDF file
    Returns:
        Extracted text as string
    """
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text.strip()


def extract_text_from_txt(file_path: str) -> str:
    """
    Extracts text from a plain text file.

    Args:
        file_path: Path to TXT file
    Returns:
        File content as string
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def parse_resume(file_path: str) -> str:
    """
    Main parser — detects file type and extracts text.
    Supports PDF and TXT files.

    Args:
        file_path: Path to resume file
    Returns:
        Extracted text as string
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif extension == ".txt":
        return extract_text_from_txt(file_path)

    else:
        raise ValueError(f"Unsupported file type: {extension}")


def parse_resume_from_upload(uploaded_file) -> str:
    """
    Parses resume from Streamlit uploaded file object.
    Used in the Streamlit UI.

    Args:
        uploaded_file: Streamlit UploadedFile object
    Returns:
        Extracted text as string
    """
    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text.strip()
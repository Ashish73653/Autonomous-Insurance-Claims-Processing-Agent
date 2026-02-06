import os
import pdfplumber
import re
from models import ClaimData

def read_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file using pdfplumber.
    Returns full document text as a single string.
    """
    try:
        text_pages = []

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_pages.append(page_text)

        text = "\n".join(text_pages)

        # 🔹 CLEANING STEP
        text = text.replace("\r", "")
        text = "\n".join(line.strip() for line in text.splitlines())

        return text

    except Exception as e:
        raise RuntimeError(f"Error reading PDF file: {e}")



def read_txt(file_path: str) -> str:
    """
    Extract text from a plain text file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        # 🔹 CLEANING STEP
        text = text.replace("\r", "")
        text = "\n".join(line.strip() for line in text.splitlines())

        return text

    except Exception as e:
        raise RuntimeError(f"Error reading TXT file: {e}")



def extract_text(file_path: str) -> str:
    """
    Detect file type and extract raw text accordingly.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".pdf":
        return read_pdf(file_path)

    elif file_extension == ".txt":
        return read_txt(file_path)

    else:
        raise ValueError("Unsupported file format. Only PDF and TXT are allowed.")

def extract_fields(text: str) -> dict:
    """
    Extract structured claim data from raw text.
    """

    claim = ClaimData()

    # Normalize spacing (keep it reasonable)
    text = text.replace("\n", " ")

    # ---------------------------
    # POLICY NUMBER
    # ---------------------------
    policy_match = re.search(
        r"POLICY NUMBER\s*[:\-]?\s*([A-Z0-9\-]{6,})",
        text,
        re.IGNORECASE
    )
    if policy_match:
        claim.policy_number = policy_match.group(1)

    # ---------------------------
    # DATE OF LOSS
    # ---------------------------
    date_match = re.search(
        r"DATE OF LOSS\s*[:\-]?\s*(\d{1,2}/\d{1,2}/\d{4})",
        text,
        re.IGNORECASE
    )
    if date_match:
        claim.date_of_loss = date_match.group(1)

    # ---------------------------
    # TIME OF LOSS
    # ---------------------------
    time_match = re.search(
        r"TIME OF LOSS\s*[:\-]?\s*(AM|PM)",
        text,
        re.IGNORECASE
    )
    if time_match:
        claim.time_of_loss = time_match.group(1)

    # ---------------------------
    # ESTIMATED DAMAGE
    # ---------------------------
    damage_match = re.search(
        r"ESTIMATE AMOUNT\s*[:\-]?\s*\$?([\d,]+)",
        text,
        re.IGNORECASE
    )
    if damage_match:
        claim.estimated_damage = damage_match.group(1).replace(",", "")

    # ---------------------------
    # DESCRIPTION
    # ---------------------------
    description_match = re.search(
        r"DESCRIPTION OF ACCIDENT\s*[:\-]?\s*(.*)",
        text,
        re.IGNORECASE
    )
    if description_match:
        claim.description = description_match.group(1).strip()

    # ---------------------------
    # CLAIM TYPE
    # ---------------------------
    lower_text = text.lower()

    if "injury" in lower_text:
        claim.claim_type = "injury"
    elif "vehicle" in lower_text:
        claim.claim_type = "vehicle"
    else:
        claim.claim_type = "property"

    return claim.__dict__

from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file.
    Args:
        pdf_file: A file-like object containing the PDF data.
    Returns:
        A string containing all the extracted text.
    """
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

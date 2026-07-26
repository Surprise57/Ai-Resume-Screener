import docx
import PyPDF2


def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file object."""
    text = ""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text


def extract_text_from_docx(docx_file):
    """Extracts text from a DOCX file object."""
    text = ""
    try:
        doc = docx.Document(docx_file)
        for para in doc.paragraphs:
            if para.text:
                text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text


def extract_resume_text(uploaded_file):
    """Main parser function that determines file type and extracts text."""
    if uploaded_file is None:
        return ""

    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type == "pdf":
        return extract_text_from_pdf(uploaded_file)
    elif file_type == "docx":
        return extract_text_from_docx(uploaded_file)
    else:
        return ""
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from each page of the PDF (assumed to be slides).
    Returns a list of strings, one per slide.
    """
    slides = []
    doc = fitz.open(pdf_path)

    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            slides.append(text)
        else:
            slides.append(f"[Slide {i+1}] No text found.")

    return slides

from pypdf import PdfReader

def extract_text_from_pdf(uploaded_file):
    # If the teacher didn't upload a file, return nothing
    if uploaded_file is None:
        return ""
    
    # Read the PDF and extract text from every page
    reader = PdfReader(uploaded_file)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text() + "\n"
        
    return extracted_text

import glob
from PyPDF2 import PdfReader


def extract_pdf_text(pdf_path):
    """
    Extracts text from a given PDF file.
    :param pdf_path: Path to the PDF file
    :return: Extracted text as a string
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""

def load_and_extract_texts_from_pdfs(data_folder):
    """
    Loads and extracts text from all PDF files in the specified folder.
    :param data_folder: Folder containing PDF files
    :return: List of extracted texts from the PDFs
    """
    texts = []
    # pdf_files = glob.glob(f"{data_folder}/*.pdf")

    # if not pdf_files:
    #     print(f"No PDF files found in folder: {data_folder}")
    #     return texts

    try:
        text = extract_pdf_text(data_folder)
        if text:
            texts.append(text)
        else:
            print(f"Warning: Empty or unreadable text in {data_folder}")
    except Exception as e:
        print(f"Error processing {data_folder}: {e}")
    print(f"Extracted text from {len(texts)} PDFs")
    return texts







# def load_and_extract_texts_from_pdfs(data_folder):
#     """
#     Loads and extracts text from all PDF files in the specified folder.
#     :param data_folder: Folder containing PDF files
#     :return: List of extracted texts from the PDFs
#     """
#     texts = []
#     pdf_files = glob.glob(f"{data_folder}/*.pdf")

#     if not pdf_files:
#         print(f"No PDF files found in folder: {data_folder}")
#         return texts

#     for pdf_file in pdf_files:
#         try:
#             text = extract_pdf_text(pdf_file)
#             if text:
#                 texts.append(text)
#             else:
#                 print(f"Warning: Empty or unreadable text in {pdf_file}")
#         except Exception as e:
#             print(f"Error processing {pdf_file}: {e}")
#     print(f"Extracted text from {len(texts)} PDFs")
#     return texts


def detect_subject(texts):
    """
    Detects the subject of the text based on keywords.
    :param text: Extracted text from the PDF
    :return: Subject as a string (e.g., 'Math', 'English', 'Science', 'General')
    """
    if not texts:
        return "Unknown"
    
    for text in texts:
        # Basic keyword matching for subject detection
        text_lower = text.lower()
        if "math" in text_lower or "calculus" in text_lower or "geometry" in text_lower:
            return "Math"
        elif "grammar" in text_lower or "literature" in text_lower:
            return "English"
        elif "science" in text_lower or "biology" in text_lower:
            return "Science"
        else:
            return "General"


# Example usage
if __name__ == "__main__":
    data_folder = "files"  # Specify the folder containing your PDFs
    extracted_texts = load_and_extract_texts_from_pdfs(data_folder)
    for text in extracted_texts:
        subject = detect_subject(text)
        print(f"Detected subject: {subject}")

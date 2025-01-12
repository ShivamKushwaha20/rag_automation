import os
import time
from modules.text_extraction import load_and_extract_texts_from_pdfs, detect_subject
from modules.chunking import split_text_into_chunks
from modules.retrieval import retrieve_relevant_chunks
from modules.mcq_generation import generate_mcqs
from modules.json_format import format_mcqs_to_json
from modules.token_management import calculate_token_size

DATA_FOLDER = "files"
OUTPUT_FOLDER = "results"
MAX_TOKENS = 6000
MCQ_TARGET = 100
TIME_LIMIT = 30  # seconds


def process_single_pdf(pdf_path, query_template, output_folder):
    start_time = time.time()
    mcqs = []
    context_history = []


    # Load and extract text
    pdf_text = load_and_extract_texts_from_pdfs(pdf_path)
    subject = detect_subject(pdf_text)  # Determine subject of the PDF
    print(f"Detected subject: {subject}")

    # Prepare query based on the subject
    query = query_template.format(subject=subject)

    # Chunk the text and initialize the loop
    chunks = split_text_into_chunks(pdf_text)
    relevant_chunks = retrieve_relevant_chunks(chunks, query)

    while len(mcqs) < MCQ_TARGET and time.time() - start_time < TIME_LIMIT:
        response = generate_mcqs(relevant_chunks, query, context_history)
        new_mcqs = format_mcqs_to_json(response, subject, len(mcqs) + 1)
        mcqs.extend(new_mcqs)

        if len(mcqs) >= MCQ_TARGET:
            break

    # Save results
    output_path = os.path.join(
        output_folder, os.path.basename(pdf_path).replace(".pdf", "_mcqs.json")
    )
    os.makedirs(output_folder, exist_ok=True)
    with open(output_path, "w") as f:
        import json

        json.dump(mcqs[:MCQ_TARGET], f, indent=4)

    print(f"MCQs saved to: {output_path}")


def process_all_pdfs(data_folder, output_folder):
    pdf_files = [
        os.path.join(data_folder, f)
        for f in os.listdir(data_folder)
        if f.endswith(".pdf")
    ]
    query_template = "Generate MCQs on the subject '{subject}' with options and answers in JSON format."

    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file}")
        process_single_pdf(pdf_file, query_template, output_folder)


if __name__ == "__main__":
    process_all_pdfs(DATA_FOLDER, OUTPUT_FOLDER)

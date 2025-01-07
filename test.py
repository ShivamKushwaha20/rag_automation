import os
from groq import Groq
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import glob
from collections import deque


# current folder path
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "files", "hemh1an.pdf")


API_KEY = os.getenv("GROQ_API")  # retriving api key from .env
print("The api key is : ", API_KEY)

BASE_URL = "https://api.groq.com/openai/v1"
# adding api key
client = Groq(api_key=API_KEY)


# function to extract pdf file
def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


# function to extract files from folder


def load_and_extract_texts_from_pdfs(data_folder="files"):
    texts = []
    folder_and_file_path = glob.glob(os.path.join(data_folder, "*.pdf"))
    for files_path in folder_and_file_path:
        try:
            text = extract_pdf_text(files_path)
            texts.append({"text": text, "file_path": files_path})
        except Exception as e:
            print(f"Error processing {files_path}: {e} ")
    return texts


# function to split the text into chunks
def split_text_into_chunks(text, chunk_size=256):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append({"text": text[i : i + chunk_size]})
    return chunks


# Advanced ranking and retrieval with TF-IDF and cosine similarity:


def retrieve_relevent_chunks(texts, query, top_k=5):
    corpus = [query] + [text["text"] for text in texts]
    vectorizer = TfidfVectorizer().fit_transform(corpus)
    vectors = vectorizer.toarray()
    cosine_matrix = cosine_similarity(vectors)
    similarity_scores = cosine_matrix[0][1:]  # exclude query itself
    ranked_indices = np.argsort(similarity_scores)[-top_k:]
    relevent_texts = [texts[idx] for idx in ranked_indices]
    return relevent_texts


def calculate_token_size(text):
    return len(text.split())


# function to generate a response based on verifed chunks


def generate_response(
    chunks, query, context_history=None, model="llama-3.3-70b-versatile"
):
    context = " ".join([chunk["text"] for chunk in chunks])
    if context_history:
        context = " ".join(context_history) + " " + context

    # Calculate token size
    query_token_size = calculate_token_size(query)
    context_token_size = calculate_token_size(context)
    total_token_size = query_token_size + context_token_size

    if total_token_size > 6000:
        print(
            f"Total tokens ({total_token_size}) exceed limit (6000). Reducing input size."
        )
        # Reduce context size
        while calculate_token_size(context) + query_token_size > 6000:
            # Trim 100 characters
            context = context[: context.rfind(" ", 0, len(context) - 100)]

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"context: {
                context} Query: {query}",
                }
            ],
            model=model,
            stream=False,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Error generating response."


# maintaining conversational context


def maintain_converstonal_context(response, context_history, max_context_length=10):
    if len(context_history) >= max_context_length:
        context_history.popleft()
    context_history.append(response)
    return context_history


# multi-step Rag Function:
def rag_pipline(data_folder, query, context_history, max_tokens=6000):
    texts = load_and_extract_texts_from_pdfs(data_folder)
    if not texts:
        print("No texts extracted from PDFs. Exiting pipeline.")
        return "No relevant texts found."
    print(f"Loaded and extracted texts from {len(texts)} PDFs")

    relevant_texts = retrieve_relevent_chunks(texts, query)
    print(f"Relevant Texts: {[text['file_path'] for text in relevant_texts]}")

    chunks = []
    for text in relevant_texts:
        chunks.extend(split_text_into_chunks(text["text"]))

    # Dynamically reduce chunks if total token size exceeds limit
    total_token_size = calculate_token_size(
        " ".join([chunk["text"] for chunk in chunks])
    ) + calculate_token_size(query)
    while total_token_size > max_tokens:
        chunks.pop()  # Remove the last chunk
        total_token_size = calculate_token_size(
            " ".join([chunk["text"] for chunk in chunks])
        ) + calculate_token_size(query)

    response = generate_response(chunks, query, context_history)
    return response


# interactive command line interface :
# to allow  user to input queries and receive response


def interactive_cli(data_folder="files/"):
    data_folder = os.path.abspath(data_folder)
    if not os.path.exists(data_folder):
        print(f"The folder {data_folder} doesn't exists")
        return
    if not glob.glob(os.path.join(data_folder, "*.pdf")):
        print(f"No pdf files found in this folder : {data_folder}")
        return

    context_history = deque()
    print("Welcome to the RAG-powered conversational assistant! Type /bye to exit")

    while True:
        user_input = input(">> user: ")
        os.system("clear")
        if user_input.lower() == "/bye":
            print("Goodbye!")
            break

        print(f">> user: {user_input}")
        response = rag_pipline(data_folder, user_input, context_history)
        context_history = maintain_converstonal_context(response, context_history)
        print(f">> groq: {response}")


if __name__ == "__main__":
    interactive_cli()

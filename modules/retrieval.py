from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def retrieve_relevant_chunks(texts, query, top_k=5):
    """
    Retrieves the most relevant text chunks based on cosine similarity.
    :param texts: List of dictionaries with 'text' and 'file_path'
    :param query: The user query
    :param top_k: Number of top relevant chunks to retrieve
    :return: List of top_k relevant text dictionaries
    """
    # Ensure all texts are strings
    corpus = [query] + [" ".join(text["text"]) if isinstance(text["text"], list) else text["text"] for text in texts]

    try:
        vectorizer = TfidfVectorizer().fit_transform(corpus)
        vectors = vectorizer.toarray()
        cosine_matrix = cosine_similarity(vectors)
        similarity_scores = cosine_matrix[0][1:]  # Exclude query itself
        ranked_indices = np.argsort(similarity_scores)[-top_k:]
        relevant_texts = [texts[idx] for idx in ranked_indices]
        return relevant_texts
    except Exception as e:
        print(f"Error during retrieval: {e}")
        return []

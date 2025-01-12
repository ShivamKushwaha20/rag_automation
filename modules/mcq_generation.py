from groq import Groq
import os

API_KEY = os.getenv("GROQ_API")
client = Groq(api_key=API_KEY)

def generate_mcqs(chunks, query, context_history, model="llama-3.3-70b-versatile"):
    """
    Generate MCQs from given text chunks using the Groq API.
    :param chunks: List of text chunks.
    :param query: Query for generating MCQs.
    :param context_history: Context history for conversational relevance.
    :param model: Language model to use for generation.
    :return: List of generated MCQs in the required format.
    """
    # Ensure all chunks are strings
    context = " ".join(
        [" ".join(chunk["text"]) if isinstance(chunk["text"], list) else chunk["text"]
         for chunk in chunks[:10]]  # Limit context size
    )

    # Add conversational context if available
    if context_history:
        context = " ".join(context_history) + " " + context

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Context: {context}\nQuery: Generate MCQs based on the context.",
                }
            ],
            model=model,
            stream=False,
        )

        # Parse and return response as JSON
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating MCQs: {e}")
        return []

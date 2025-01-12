def split_text_into_chunks(text, chunk_size=256):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append({"text": text[i: i + chunk_size]})
    return chunks

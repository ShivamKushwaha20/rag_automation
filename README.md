# RAG-Based MCQ Generation Model

This project implements a Retrieval-Augmented Generation (RAG) pipeline to extract text from PDFs, identify their subjects, and generate multiple-choice questions (MCQs) in JSON format. The model uses PDF text extraction, subject detection, chunking, and an API for question generation. It is modularized for clarity and extensibility.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Detailed Workflow](#detailed-workflow)
- [Limitations and Considerations](#limitations-and-considerations)
- [Contributing](#contributing)

---

## Features

- Extract text from multiple PDFs in a specified folder.
- Detect subject matter (e.g., Math, English, Science).
- Split text into manageable chunks.
- Generate MCQs from text using a conversational AI model.
- Output MCQs in a structured JSON format.
- Modularized code for easy understanding and extension.

---

## Installation

### Prerequisites

- Python 3.8+
- A virtual environment (optional but recommended)
- Libraries: Install the required packages listed in `requirements.txt`
- API key for Groq or the conversational AI tool being used

### Steps

1. Clone or download the zip repository:
    

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Add your API key to the environment variables by creating a `.env` file:
    ```bash
    echo "GROQ_API=<your_api_key>" > .env
    ```

5. Ensure the `files` folder contains the PDFs to process:
    ```bash
    mkdir files
    # Add your PDFs to the `files` directory
    ```

6. Create an `results` folder for generated MCQs:
    ```bash
    mkdir results 
    ```

---

## Usage

### Running the Pipeline

Run the main script to process PDFs and generate MCQs:

```bash
python main.py
```

The script will:
1. Extract text from PDFs in the `files` folder.
2. Detect the subject of each PDF.
3. Generate 100 MCQs for each PDF and save them in the `output` folder in JSON format.

### Example Output

Each JSON file will have the following structure for MCQs:

```json
{
  "question": "Which of the following words can be used as an adjective, adverb, pronoun or verb, depending on the context?",
  "options": [
    "Word",
    "Sentence",
    "Phrase",
    "Text"
  ],
  "answer": [1],
  "metadata": {
    "class": "Class_4",
    "subject": "English",
    "topic": "Grammar_Basics",
    "id": 1,
    "type": "objective",
    "difficulty": "high"
  }
}
```

---

## Folder Structure

```
rag-mcq-generator/
├── files/                   # Folder containing input PDFs
├── output/                  # Folder for generated JSON files
├── modules/                 # Modularized code
│   ├── __init__.py          # Makes `modules` a package
│   ├── text_extraction.py   # Functions for text extraction and subject detection
│   ├── retrieval.py         # Functions for chunk retrieval and similarity ranking
│   ├── mcq_generation.py    # Functions for generating MCQs
|   ├── chunking.py
|   ├── token_managemet.py
|   ├── context_managemet.py
|   ├── json_format.py
├── main.py                  # Main script for running the pipeline
├── requirements.txt         # Python dependencies
├── .env                     # API key (excluded from version control)
├── README.md                # Documentation
```

---

## Detailed Workflow

1. **Text Extraction**:
   - Extract text from PDFs using `PyPDF2`.
   - Store extracted text for further processing.

2. **Subject Detection**:
   - Detect the subject of each PDF using keyword matching.

3. **Chunking**:
   - Split extracted text into manageable chunks (e.g., 256 characters each).

4. **Question Generation**:
   - Send chunks to the Groq API for generating MCQs based on the detected subject.
   - Format responses into the desired JSON structure.

5. **Output**:
   - Save the generated MCQs in the `output` folder as JSON files.

---

## Limitations and Considerations

- **Token Limit**: The model has a token limit of 6000, so text context is truncated dynamically.
- **Subject Detection**: The subject detection is keyword-based and may require enhancement for complex texts.
- **Time Constraint**: A 30-second interval is enforced for generating 100 MCQs per PDF to prevent API overload.
- **PDF Content**: Ensure PDFs contain readable, text-based content (not scanned images).

---


import json


def format_mcqs_to_json(response, subject, start_id):
    mcqs = []
    try:
        for idx, question_data in enumerate(response.split("\n\n")):
            parts = question_data.split("\n")
            if len(parts) < 2:
                continue
            question = parts[0].strip()
            options = [opt.strip() for opt in parts[1:]]
            mcqs.append(
                {
                    "question": question,
                    "options": options,
                    "answer": [1],  # Placeholder for correct answer
                    "metadata": {
                        "class": "Class_4",
                        "subject": subject,
                        "topic": "Auto-Generated",
                        "id": start_id + idx,
                        "type": "objective",
                        "difficulty": "medium",
                    },
                }
            )
    except Exception as e:
        print(f"Error formatting MCQs: {e}")
    return mcqs

import google.generativeai as genai
import json
import re

# =========================
# CONFIG (DO NOT HARD CODE IN PRODUCTION)
# =========================
API_KEY = "YOUR_NEW_API_KEY_HERE"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


# =========================
# SAFE JSON CLEANER
# =========================
def extract_json(text: str):
    """
    Extract valid JSON from Gemini response safely.
    Handles ```json blocks and extra text.
    """

    text = text.strip()

    # Remove markdown code blocks
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    text = text.strip()

    # Try direct parsing
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Fallback: extract JSON array using regex
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    raise ValueError("Gemini returned invalid JSON")


# =========================
# MAIN FUNCTION
# =========================
def generate_questions(subject, difficulty, count):
    prompt = f"""
You are an expert quiz generator for students.

Generate {count} multiple-choice questions.

Subject: {subject}
Difficulty: {difficulty}

Rules:
- Return ONLY valid JSON
- No explanation
- No markdown
- No extra text

Format:
[
  {{
    "question": "Question text",
    "option_a": "Option A",
    "option_b": "Option B",
    "option_c": "Option C",
    "option_d": "Option D",
    "answer": "Correct Answer"
  }}
]
"""

    response = model.generate_content(prompt)

    if not response or not response.text:
        raise ValueError("Empty response from Gemini")

    return extract_json(response.text)
import json
import re
import os
from dotenv import load_dotenv
from google import genai

# -----------------------------
# Load API Key
# -----------------------------
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# -----------------------------
# Difficulty Calculator
# -----------------------------
def calculate_difficulty(steps, tools):

    if len(steps) <= 3 and len(tools) <= 2:
        return "Beginner"

    elif len(steps) <= 6:
        return "Intermediate"

    else:
        return "Advanced"


# -----------------------------
# Extract JSON
# -----------------------------
def extract_json(text):

    text = text.strip()

    # Remove markdown if Gemini returns it
    text = text.replace("```json", "")
    text = text.replace("```", "")

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("Gemini did not return valid JSON.")

    return json.loads(match.group())


# -----------------------------
# Generate Complete Project
# -----------------------------
def generate_project_details(idea, materials):

    prompt = f"""
You are an expert in DIY recycling and sustainability.

Detected Materials:
{materials}

Selected Project:
{idea}

Generate ALL the following.

Return ONLY valid JSON.

{{
  "title": "",
  "steps": [
    ""
  ],
  "tools": [
    ""
  ],
  "eco_score": 0,
  "co2_saved": 0,
  "estimated_cost": 0,
  "selling_price": 0,
  "profit": 0,
  "marketplace": "",
  "reason": ""
}}

Do not write explanations.
Do not use markdown.
Only JSON.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    project = extract_json(response.text)

    project["difficulty"] = calculate_difficulty(
        project["steps"],
        project["tools"]
    )

    return project


# -----------------------------
# Testing
# -----------------------------
if __name__ == "__main__":

    result = generate_project_details(
        "Paper Basket",
        ["paper"]
    )

    print(json.dumps(result, indent=4))
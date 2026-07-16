import json
import re
import os
from dotenv import load_dotenv
from google import genai

# -------------------------
# Load API Key
# -------------------------

load_dotenv()

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE")
)

# -------------------------
# Analyze Project
# -------------------------

def analyze_project(materials, project, difficulty, steps):

    prompt = f"""
You are an environmental sustainability expert.

Materials:
{materials}

Project:
{project}

Difficulty:
{difficulty}

Steps:
{steps}

Estimate and return ONLY valid JSON.

{
    "title": "",
    "steps": [],
    "tools": [],
    "difficulty": "",
    "eco_score": 0,
    "co2_saved": 0,
    "estimated_cost": 0,
    "selling_price": 0,
    "profit": 0,
    "marketplace": "",
    "reason": "",
    "project_score": 0
}
Do not use markdown.
Only return JSON.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    response_text = response.text.strip()

    response_text = response_text.replace("```json", "")
    response_text = response_text.replace("```", "")

    match = re.search(r"\{.*\}", response_text, re.DOTALL)

    if not match:
        raise ValueError("Gemini did not return valid JSON.")

    json_text = match.group()

    return json.loads(json_text)
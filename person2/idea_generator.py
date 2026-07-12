from dotenv import load_dotenv
import os
from google import genai
import random
import time
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# -----------------------------------
# MATERIAL KNOWLEDGE BASE
# -----------------------------------

material_properties = {

    "plastic": [
        "waterproof",
        "lightweight",
        "container",
        "durable"
    ],

    "plastic bottle": [
        "waterproof",
        "lightweight",
        "container",
        "durable"
    ],

    "cardboard": [
        "foldable",
        "structural",
        "lightweight"
    ],

    "rope": [
        "flexible",
        "hanging",
        "binding"
    ],

    "glass": [
        "decorative",
        "fragile",
        "container"
    ],

    "glass bottle": [
        "decorative",
        "fragile",
        "container"
    ],

    "metal": [
        "metallic",
        "strong",
        "heat-resistant"
    ],

    "tin can": [
        "metallic",
        "strong",
        "heat-resistant"
    ],

    "paper": [
        "foldable",
        "lightweight",
        "craftable"
    ],

    "wood": [
        "strong",
        "structural",
        "durable"
    ]
}

# -----------------------------------
# IDEA DATABASE
# -----------------------------------

idea_database = {

    "waterproof": [
        "Self-watering planter",
        "Mini water storage",
        "Outdoor plant holder"
    ],

    "foldable": [
        "Desk organizer",
        "Storage box",
        "Drawer divider"
    ],

    "hanging": [
        "Hanging planter",
        "Wall organizer",
        "Bird feeder"
    ],

    "decorative": [
        "Decorative lamp",
        "Flower vase",
        "LED bottle light"
    ],

    "metallic": [
        "Pen stand",
        "Candle holder",
        "Kitchen holder"
    ],

    "craftable": [
        "Paper flowers",
        "Greeting cards",
        "Paper decorations"
    ],

    "structural": [
        "Shelf organizer",
        "Book stand",
        "Phone holder"
    ]
}

# -----------------------------------
# RULE-BASED IDEA GENERATOR
# -----------------------------------

def generate_dynamic_ideas(materials):

    generated_ideas = set()

    for material in materials:

        material = material.lower()

        if material in material_properties:

            properties = material_properties[material]

            for prop in properties:

                if prop in idea_database:

                    ideas = idea_database[prop]

                    random_ideas = random.sample(
                        ideas,
                        min(2, len(ideas))
                    )

                    generated_ideas.update(random_ideas)

    return list(generated_ideas)

# -----------------------------------
# SAFE GEMINI RESPONSE FUNCTION
# -----------------------------------

def safe_generate(prompt):

    response = None

    for i in range(3):

        try:

            print(f"\nTrying Gemini Request {i+1}...\n")

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            print(f"\nRetry {i+1} failed:\n")
            print(e)

            print("\nWaiting 10 seconds...\n")

            time.sleep(10)

    return None

# -----------------------------------
# GEMINI AI IDEA GENERATOR
# -----------------------------------

def generate_ai_ideas(materials):

    prompt = f"""
    You are a creative recycling assistant.

    Generate 5 creative reuse project ideas
    using these waste materials:

    {materials}

    Return ONLY comma separated idea names.

    Example:
    Bottle Planter, Desk Organizer, Bird Feeder
    """

    result = safe_generate(prompt)

    if result is None:

        return [
            "Bottle Planter",
            "Desk Organizer",
            "Bird Feeder"
        ]

    

    ai_ideas = result.split(",")

    return [
        idea.strip()
        for idea in ai_ideas
    ]

# -----------------------------------
# HYBRID IDEA GENERATOR
# -----------------------------------

def generate_ideas(materials):

    # RULE-BASED IDEAS
    rule_ideas = generate_dynamic_ideas(materials)

    # GEMINI AI IDEAS
    ai_ideas = generate_ai_ideas(materials)

    # COMBINE BOTH
    final_ideas = list(
        set(rule_ideas + ai_ideas)
    )

    result = {
        "materials": materials,
        "generated_ideas": final_ideas
    }

    return result

# -----------------------------------
# TESTING
# -----------------------------------

if __name__ == "__main__":

    materials = [
        "plastic",
        "paper"
    ]

    result = generate_ideas(materials)

    
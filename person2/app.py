from fastapi import FastAPI
import random

from idea_generator import generate_ideas
from step_generator import generate_project_details

# -----------------------------------
# CREATE FASTAPI APP
# -----------------------------------

app = FastAPI()

# -----------------------------------
# MAIN API
# -----------------------------------
@app.get("/generate")

def generate():

    try:

        materials = [
            "paper",
            "cardboard"
        ]

        ideas_result = generate_ideas(materials)

        selected_idea = random.choice(
            ideas_result["generated_ideas"]
        )

        project_details = generate_project_details(
            selected_idea,
            materials
        )

        final_output = {

            "materials": materials,

            "generated_ideas":
                ideas_result["generated_ideas"],

            "selected_project":
                project_details
        }

        return final_output

    except Exception as e:

        return {
            "ERROR": str(e)
        }
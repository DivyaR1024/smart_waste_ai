
print("started")

import json
import random

print("import running")

from person1.predict import predict_img
from person2.idea_generator import generate_ideas
from person2.step_generator import generate_project_details

print("imported")
print("RUNNING DETECTION")

# -----------------------------------
# DETECT MATERIAL FROM IMAGE
# -----------------------------------

image_path = r"D:\Div project\waste-into-useful-things\person1\test_images\glass1.jpg"

material = predict_img(image_path)

materials = [material]

print("\nDETECTED MATERIALS:\n")
print(materials)

# -----------------------------------
# GENERATE IDEAS
# -----------------------------------

ideas_result = generate_ideas(materials)

# Safety check
if len(ideas_result["generated_ideas"]) == 0:
    print("No ideas generated!")
    exit()

# -----------------------------------
# SELECT RANDOM IDEA
# -----------------------------------

selected_idea = random.choice(
    ideas_result["generated_ideas"]
)

# -----------------------------------
# GENERATE PROJECT DETAILS
# -----------------------------------

project_details = generate_project_details(
    selected_idea,
    materials
)


print("\nPROJECT DETAILS:")
print(project_details)




# -----------------------------------
# FINAL OUTPUT
# -----------------------------------

final_output = {
    "materials": materials,
    "generated_ideas": ideas_result["generated_ideas"],
    "selected_project": project_details
}

# -----------------------------------
# PRINT FINAL JSON
# -----------------------------------

print("\nFINAL OUTPUT:\n")

print(
    json.dumps(
        final_output,
        indent=4
    )
)
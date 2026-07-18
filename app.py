from flask import Flask, render_template, request
import os
import random

from person1.predict import predict_img
from person2.idea_generator import generate_ideas
from person2.step_generator import generate_project_details

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    print("Analyze route called")

    if "image" not in request.files:
        return "No image uploaded"

    image = request.files["image"]

    if image.filename == "":
        return "No image selected"

    image_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
    image.save(image_path)

    print("Image Saved")

    # Detect Material
    material = predict_img(image_path)
    materials = [material]

    print("Detected:", material)

    # Generate Ideas
    ideas_result = generate_ideas(materials)

    print("Ideas Generated")

    # Random Idea
    selected_idea = random.choice(
        ideas_result["generated_ideas"]
    )

    print("Selected Idea:", selected_idea)

    # Gemini Project Details
    project = generate_project_details(
        selected_idea,
        materials
    )

    print("Project Generated")

    return render_template(
        "result.html",
        image=image.filename,
        materials=materials,
        ideas=ideas_result["generated_ideas"],
        project=project
    )


if __name__ == "__main__":
    app.run(debug=True)
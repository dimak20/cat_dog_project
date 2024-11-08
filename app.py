import os

import keras
from flask import Flask, request, render_template

from classifier import classify

app = Flask(__name__)
STATIC_FOLDER = "static"
UPLOAD_FOLDER = "static/uploads/"

BACKGROUND_IMAGE = "static/background/cat_dog_background.png"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

cnn_model = keras.models.load_model(STATIC_FOLDER + "/models/" + "cat_dog.keras")


@app.route("/")
def home():
    return render_template("index.html", background_image=BACKGROUND_IMAGE)


@app.post("/classify")
def upload_file():
    if "image" not in request.files:
        return "No file part", 400

    file = request.files["image"]

    if file.filename == "":
        return "No selected file", 400

    if file:
        upload_image_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(upload_image_path)

        label, prob = classify(cnn_model, upload_image_path)
        prob = round(prob * 100, 2)

        return render_template(
            "index.html", label=label, prob=prob, background_image=BACKGROUND_IMAGE
        )

    return "Error", 500


if __name__ == "__main__":
    app.run(debug=True)

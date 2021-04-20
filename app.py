import logging
import requests

from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import FileField
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = "secretkey"


class MyForm(FlaskForm):
    image = FileField('image')


@app.route("/", methods=["GET", "POST"])
def index():
    form = MyForm()
    if form.validate_on_submit() and request.method == 'POST':
        f = request.files['image']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        print(form.image.data)
    return render_template("index.html", form=form)


@app.route("/submit", methods=["GET", "POST"])
def post_image():

    if request.method == "POST":
        file = request.files["image"]
        img_bytes = file.read()

        r = requests.post("http://127.0.0.1:5000/predict",
                          files={"file": img_bytes})

        r.raise_for_status()

        return render_template("response.html")


if __name__ == '__main__':
    app.run(debug=True)

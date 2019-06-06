from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
import os


app = Flask(__name__)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    os.path.join(basedir, "app.sqlite")

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Image(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(1000), primary_key=True)

    def __init__(self, image_url):
        self.image_url = image_url


class ImagesSchema(ma.Schema):
    class Meta:
        fields = ("id", "image_url")


image_schema = ImagesSchema()
images_schema = ImagesSchema(many=True)


@app.route("/images", methods=["GET"])
def get_images():
    all_images = Image.query.all()
    result = images_schema.dump(all_images)
    return jsonify(result.data)


@app.route("/add-image", methods=["POST"])
def add_image():
    image_url = request.json["image_url"]

    record = Image(image_url)

    db.session.add(record)
    db.session.commit()

    image = Image.query.get(record.id)
    return image_schema.jsonify(image)


@app.route("/image/<id>", methods=["PUT"])
def update_image(id):
    image = Image.query.get(id)

    new_image_url = request.json["image_url"]

    image.image_url = new_image_url

    db.session.commit()
    return image_schema.jsonify(image)


@app.route("/image/<id>", methods=["DELETE"])
def delete_image(id):
    record = Image.query.get(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify("Record deleted")


if __name__ == "__main__":
    app.debug = True
    app.run()

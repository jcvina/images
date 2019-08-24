from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_marshmallow import Marshmallow
from PIL import Image
import os
import imagehash
from io import BytesIO
from werkzeug.exceptions import BadRequestKeyError

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init database
db = SQLAlchemy(app)

# Init marshmallow
ma = Marshmallow(app)


# ImageHandler Class/Model
class Images(db.Model):
    id_image = db.Column(db.String, primary_key=True)
    image_name = db.Column(db.String, unique=False)
    image = db.Column(db.LargeBinary, unique=True)

    def __init__(self, id_image, image_name, image):
        self.id_image = id_image
        self.image_name = image_name
        self.image = image


# ImageHandler Schema
class ImagesSchema(ma.Schema):
    class Meta:
        fields = ('id_image', 'image_name', 'image')


# Init Schema
image_schema = ImagesSchema()


# Upload Image
@app.route('/images', methods=['POST'])
def upload_image():
    try:
        image = request.files['image']
    except BadRequestKeyError as e:
        code = 400
        msg = 'Please upload a valid file.'
        return jsonify(msg), code

    if validate_image(image):
        img = Image.open(image)
        id_image = str(imagehash.phash(img))
        image_name = os.path.splitext(image.filename)[0] + '.jpg'
        with BytesIO() as i:
            img.save(i, format='JPEG')
            value = i.getvalue()
        new_image = Images(id_image=id_image, image_name=image_name, image=value)
        image.close()

        db.session.add(new_image)
        try:
            db.session.commit()
        except IntegrityError as e:
            res = {"new": False, "url": "/images/" + id_image}
            return jsonify(res)

        res = {"new": True, "url": "/images/" + id_image}
        return jsonify(res)

    else:
        code = 400
        msg = 'Invalid file format, please upload an image (jpg or png).'
        return jsonify(msg), code


# Validate if image is JPG and less than 25 megabytes
def validate_image(file):
    old_file_position = file.tell()
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(old_file_position, os.SEEK_SET)

    if size <= 26214400:
        code = 400
        msg = 'The file is too big. Maximum size = 25 megabytes.'
        return jsonify(msg), code

    try:
        img = Image.open(file)
        if img.format == 'PNG':
            img = convert_to_jpeg(img)
        return img.format == 'JPEG'
    except IOError:
        return False


# If image is PNG -> convert to JPG
def convert_to_jpeg(img):
    with BytesIO() as i:
        img.save(i, format='JPEG')
        return Image.open(i)


# Run server
if __name__ == '__main__':
    app.run(debug=True)
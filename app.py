from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from PIL import Image
import os
import imagehash

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
    image = db.Column(db.LargeBinary, unique=True)

    def __init__(self, id_image, image):
        self.id_image = id_image
        self.image = image


# ImageHandler Schema
class ImagesSchema(ma.Schema):
    class Meta:
        fields = ('id_image', 'image')


# Init Schema
image_schema = ImagesSchema()


# Upload Image
@app.route('/images', methods=['POST'])
def upload_image():

    image = request.files['image']
    image_to_upload = image.read()
    id_image = str(imagehash.phash(Image.open(image)))
    image.close()
    new_image = Images(id_image=id_image, image=image_to_upload)

    db.session.add(new_image)
    db.session.commit()

    return 'Uploaded image'


# Run server
if __name__ == '__main__':
    app.run(debug=True)
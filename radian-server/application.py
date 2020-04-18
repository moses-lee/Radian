import os
import base64
from flask import Flask, jsonify, request
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import sys
from flask_cors import CORS


def get_prediction(img_data):
   img = base64.b64decode(img_data)
   img = cv2.imdecode(np.frombuffer(img, np.uint8), -1)
   img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_NEAREST)
   img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
   img = np.expand_dims(img, axis=0)
   model = load_model('model.h5', compile=False)
   return model.predict(img)


app = Flask(__name__)
CORS(app)
@app.route('/')
def get_home():
    return "Welcome to Radian's Server!"


@app.route('/diagnose', methods=['GET'])
def get_image():
   image = request.args.get('image')
   image = str(image)
   image = image.replace(" ", "+")
   pred = get_prediction(str(image))
   print(pred, file=sys.stderr)
   res = pred[0][0] < pred[0][1]
#    [non-Covid, Covid]
   return jsonify({'has_covid': str(res)})


if __name__ == '__main__':
    # app.debug = True
    app.run()

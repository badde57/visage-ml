#!/usr/bin/env python

import os
import json
from deepface.commons import functions
from deepface.basemodels import Facenet512
import tensorflow as tf

gpus = tf.config.list_physical_devices('GPU')
for gpu in gpus:
    try:
        tf.config.set_logical_device_configuration(gpu, [tf.config.LogicalDeviceConfiguration(memory_limit=800)] * 12)
    except RuntimeError as e:
        # Virtual devices must be set before GPUs have been initialized
        print(e)
logical_gpus = tf.config.list_logical_devices('GPU')
print(len(gpus), "Physical GPU,", len(logical_gpus), "Logical GPUs")

print("Loading model")
# load the face model
model = Facenet512.loadModel()
input_shape_x, input_shape_y = functions.find_input_shape(model)


def process_image(image):
    name, _ = os.path.splitext(image)
    file = name + ".vector"
    if os.path.exists(file):
        return

    print("looking at image", file)

    try:
        img = functions.preprocess_face(
            img=image,
            target_size=(input_shape_x, input_shape_y),
            enforce_detection=False,
            detector_backend="retinaface",
            align=True,
        )
        
        img = functions.normalize_input(img, normalization="Facenet2018")

        face = model.predict(img)[0].tolist()
    except Exception as e:
        print(e)
        return

    if face:
        with open(file, "w") as e:
            json.dump(face, e)


print("starting scanning for images")

total = 0
for root, dirs, files in os.walk("/images"):
    for file in files:
        if file.endswith((".jpg", ".jpeg", ".png", "webp")):
            process_image(os.path.join(root, file))
            total += 1

print("done scanning for images", total)

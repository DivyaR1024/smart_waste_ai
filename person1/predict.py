import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

# Load model
model = tf.keras.models.load_model("person1/garbage_model1.h5")

# Class names
class_names = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

# Material mapping
material_map = {
    "cardboard": "paper",
    "paper": "paper",
    "plastic": "plastic",
    "glass": "glass",
    "metal": "metal",
    "trash": "trash"
}

def predict_img(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array, verbose=0)
    index = np.argmax(prediction)

    detected_class = class_names[index]

    
    return material_map[detected_class]


if __name__ == "__main__":
    img_path = "person1/test_images/trash11.jpg"
    material = predict_img(img_path)

    print("Material:", material)
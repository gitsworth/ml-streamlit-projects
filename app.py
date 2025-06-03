import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

st.title("Image Classifier using MobileNetV2")

# Load pre-trained MobileNetV2 model + weights
model = tf.keras.applications.MobileNetV2(weights="imagenet")

# Function to preprocess the uploaded image
def preprocess_image(image):
    image = image.resize((224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Preprocess and predict
    input_tensor = preprocess_image(image)
    preds = model.predict(input_tensor)
    decoded_preds = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)[0]

    st.write("### Predictions:")
    for i, (imagenetID, label, prob) in enumerate(decoded_preds):
        st.write(f"{i+1}. {label}: {prob*100:.2f}%")

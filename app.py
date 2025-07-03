import numpy as np
from PIL import Image
import tensorflow as tf
import json
from huggingface_hub import hf_hub_download
import streamlit as st

 
# Load model 
model_path = hf_hub_download(
    repo_id="nkdrago/food_classification_model",   
    filename="food_classification_model.keras",              
)

model = tf.keras.models.load_model(model_path)

with open("class_names.json", "r") as file:
    class_names = json.load(file)

# App title
st.title("🍽️ Food Classifier")

# Upload image
uploaded_file = st.file_uploader("Upload a food image", type=["jpg", "png", "jpeg"])
if uploaded_file:
    
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)




    # Preprocess image
    img = image.resize((224, 224)) 
    img_array = np.array(img)
 
    img_array = img_array.astype(np.float32)

    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    preds = model.predict(img_array)[0]
    top_indices = preds.argsort()[-3:][::-1]
    
    st.subheader("🍴 Top Predictions:")
    for i in top_indices:
        st.write(f"**{class_names[i]}** — {preds[i]*100:.2f}%")
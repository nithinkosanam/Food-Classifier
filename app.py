import numpy as np
from PIL import Image as PILImage
import tensorflow as tf
import json
from huggingface_hub import hf_hub_download
import streamlit as st

img_size = (224, 224)

# Functions
def preprocess(file):
    image = PILImage.open(file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    img = image.resize((224, 224)) 
    img_array = np.array(img)
 
    img_array = img_array.astype(np.float32)

    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict(img_array):
    preds = model.predict(img_array)[0]
    top_indices = preds.argsort()[-3:][::-1]

    return preds, top_indices

def read_json(path):
    with open("class_names.json", "r") as file:
        class_names = json.load(file)

    return class_names

def load_model(repo_id, filename):
    model_path = hf_hub_download(repo_id, filename,)
    model = tf.keras.models.load_model(model_path)

    return model

# Load model 
model = load_model("nkdrago/food_classification_model", "food_classification_model.keras")

# Read class names json file
class_names = read_json("class_names.json")   

# App title
st.title("🍽️ Food Classifier")

# Upload image
uploaded_file = st.file_uploader("Upload a food image", type=["jpg", "png", "jpeg"])

# Sidebar with model classes
st.sidebar.title("🍱 Model Classes (50)")

auto_scroll_html = f"""
<style>
@keyframes scroll {{
  0% {{ transform: translateY(0%); }}
  100% {{ transform: translateY(-100%); }}
}}

.scroll-container {{
  height: 300px;
  overflow: hidden;
  position: relative;
}}

.scroll-content {{
  display: inline-block;
  animation: scroll 20s linear infinite;
}}

.scroll-content:hover {{
  animation-play-state: paused;
}}

.scroll-content ul {{
  list-style: none;
  padding-left: 0;
  margin: 0;
}}

.scroll-content li {{
  font-size: 16px;
  padding: 4px 0;
  color: #white;
}}
</style>

<div class="scroll-container">
  <div class="scroll-content">
    <ul>
      {''.join(f"<li>{cls}</li>" for cls in class_names)}
    </ul>
  </div>
</div>
"""

st.sidebar.markdown(auto_scroll_html, unsafe_allow_html=True)

if uploaded_file:
    # Preprocess image and predict
    img_array = preprocess(uploaded_file)
    with st.spinner("Predicting..."):
        preds, top_indices = predict(img_array)


    st.subheader("🍴 Top Predictions:")
    for i in top_indices:
        st.write(f"**{class_names[i]}** — {preds[i]*100:.2f}%")
    

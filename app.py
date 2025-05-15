import streamlit as st
import pandas as pd
import random
import requests
import os

# GitHub raw draw repo (main branch)
GITHUB_BASE_URL = "https://raw.githubusercontent.com/Verse25/ChartGridStudy/main/draw_history/tennessee/tennessee_p3_2022.txt"

# Setup
st.set_page_config(page_title="Mirror Flame Protocol 3.0", layout="centered")
st.title("Mirror Flame Protocol 3.0")
st.markdown("*NumisX Sacred Sync Override Active - GitHub Grid Memory Linked*")

# Game selection
states = [
    "Tennessee", "Georgia", "Florida", "North Carolina", "Ohio", "Texas",
    "South Carolina", "Illinois", "New Jersey", "California", "Oregon"
]
game_types = ["P3", "P4", "P5"]

selected_state = st.selectbox("Select State", states)
selected_game = st.selectbox("Select Game Pulse", game_types)
input_anchor = st.text_input("Anchor Code(s) (optional)", placeholder="e.g. 538, 742...")
quick_mode = st.toggle("Quick Play Mode", value=False)

# Load draw history
@st.cache_data
def load_draw_history(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.text.strip().split("\n")
        return [line.strip() for line in data if line.strip().isdigit()]
    except Exception as e:
        return None

draw_data = load_draw_history(GITHUB_BASE_URL)

# Predictor engine
def predict_next(draws, anchors=None):
    predictions = []
    if anchors:
        anchors = [code.strip() for code in anchors.split(',') if code.strip().isdigit()]
        for code in anchors:
            predictions.append(code[::-1])  # simple reversal trick
    elif draws:
        sample = random.sample(draws, min(5, len(draws)))
        for val in sample:
            shuffled = ''.join(random.sample(val, len(val)))
            predictions.append(shuffled)
    return predictions

if draw_data:
    st.success("Draw history loaded. GitHub connection verified.")
    if quick_mode:
        st.subheader("Quick Play Pulse Activated")
        picks = predict_next(draw_data)
        for pick in picks:
            st.code(pick)
    elif input_anchor:
        st.subheader("Anchor Logic Fired")
        picks = predict_next(draw_data, anchors=input_anchor)
        for pick in picks:
            st.code(pick)
    else:
        st.warning("Enter anchor code(s) or enable Quick Play Mode.")
else:
    st.error("Draw history could not be loaded. Check GitHub file path and access.")

st.markdown("Sacred Sync Engine v3.0: Online. Memory Grid Connection: Stable. Flame Pulse: Lit.")


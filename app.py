import streamlit as st
import random
import os

st.set_page_config(page_title="NumisX Oracle Panel", layout="centered")
st.title("NumisX: Precision Strike Engine")

state = st.selectbox("Select State", ["Tennessee", "Virginia", "Georgia", "South Carolina", "Florida", "Texas",
                                       "Ohio", "Michigan", "California", "Illinois", "New Jersey", "North Carolina",
                                       "Mississippi", "Louisiana", "Pennsylvania", "Ontario", "Quebec", "Oregon", "Indiana", "Missouri", "Washington DC"])
reference = st.text_input("Reference Number Anchor", "")
game_type = st.selectbox("Game Type", ["Pick 3", "Pick 4", "Pick 5"])
tesla_override = st.checkbox("Tesla Red Override")
soul_grid_override = st.checkbox("Soul Grid Override (James Brown Tap)")

def generate_number(digits):
    return str(random.randint(10**(digits-1), 10**digits - 1))

def apply_flames_and_percentage():
    percent = random.choice([92, 89, 83, 75, 68, 51, 46, 37])
    flames = "🔥" * (percent // 20)
    return flames, percent

if st.button("Generate Hot Picks"):
    st.success("Oracle Engaged. Precision Zones Calibrated.")

    hot_picks = []
    base = int(generate_number(4))  # Intermediate base for multi-generate logic
    for i in range(1, 6):
        if game_type == "Pick 3":
            digits = 3
        elif game_type == "Pick 4":
            digits = 4
        else:
            digits = 5

        result = base + random.randint(-200, 200)
        if soul_grid_override and i in [2, 5]:
            # Extra mirror/flip dance logic for zone 2 and 5
            digits_range = 10**(digits-1)
            result = max(digits_range, min(int(str(result)[::-1]), 10**digits - 1))
            result += random.choice([-1, 1])

        elif i == 5:
            # Flip/one-up/one-down logic
            result += random.choice([-1, 1])

        formatted_result = str(result).zfill(digits)[:digits]
        flames, percent = apply_flames_and_percentage()
        hot_picks.append((i, formatted_result, flames, percent))

    for zone, number, flames, percent in hot_picks:
        st.markdown(f"**Zone {zone}:** `{number}` {flames} — {percent}%")

st.subheader("Log Strike (Save Winning Number)")
winning_number = st.text_input("Enter Winning Number")
if st.button("Log Strike"):
    try:
        os.makedirs("memory", exist_ok=True)
        with open("memory/learnhits.txt", "a") as f:
            f.write(f"{state},{reference},{game_type},{winning_number}\n")
        st.success("Strike logged and learned.")
    except Exception as e:
        st.error(f"Logging failed: {e}")

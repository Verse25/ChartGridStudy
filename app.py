import streamlit as st
import random
import os

# UI Setup
st.title("Codex Oracle Panel")
state = st.selectbox("Target State", [
    "Tennessee", "Georgia", "Florida", "Ohio", "North Carolina", "Texas",
    "South Carolina", "Illinois", "New Jersey", "California", "Pennsylvania",
    "Missouri", "Michigan", "Louisiana", "Washington DC", "Ontario",
    "Mississippi", "Indiana", "Virginia", "Quebec", "Oregon"
])
reference = st.text_input("Reference Anchor", "")
game_type = st.selectbox("Target Type", ["Pick 3", "Pick 4", "Pick 5"])
tesla = st.checkbox("Tesla Red Mode (Override)")
soul = st.checkbox("Soul Grid Override (James Brown Tap)")
if st.button("Generate Hot Picks"):
    st.success("Oracle Activated. Strike Zone Primed.")

    def generate_number(length):
        lower = 10**(length-1)
        upper = (10**length) - 1
        return random.randint(lower, upper)

    def get_flame(percent):
        if percent >= 90:
            return "🔥🔥🔥🔥🔥"
        elif percent >= 75:
            return "🔥🔥🔥🔥"
        elif percent >= 60:
            return "🔥🔥🔥"
        elif percent >= 45:
            return "🔥🔥"
        else:
            return "🔥"

    length = 3 if game_type == "Pick 3" else 4 if game_type == "Pick 4" else 5
    base = generate_number(length)
    picks = []

    for i in range(5):
        offset = random.randint(-50, 50)
        val = base + offset
        if val < 10**(length-1):
            val = 10**(length-1)
        if val > (10**length)-1:
            val = (10**length)-1
        percent = random.choice([75, 68, 51, 37, 46, 83, 92, 89])
        flames = get_flame(percent)
        if i in [1, 4] and soul:
            # Apply James Brown Tap on Zones 2 and 5
            flipped = str(val)[::-1]
            val = int(flipped)
        picks.append((i+1, val, flames, percent))

    for zone in picks:
        st.markdown(f"**Zone {zone[0]}:** {zone[1]} {zone[2]} — {zone[3]}%")

# Strike Log Section
st.subheader("Strike Log")
winning_number = st.text_input("Enter Winning Number")
if st.button("Log Strike"):
    try:
        os.makedirs("memory", exist_ok=True)
        with open("memory/learnhits.txt", "a") as f:
            f.write(f"{state},{reference},{game_type},{winning_number}\n")
        st.success("Strike logged successfully.")
    except Exception as e:
        st.error(f"Logging failed: {e}")

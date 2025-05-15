import streamlit as st
import random
import os
from datetime import datetime

st.set_page_config(page_title="NumisX — Codex Pyrafire v1.23", layout="centered")

st.markdown("""
    <div style='text-align: center; padding: 10px 0;'>
        <h1 style='margin-bottom: 0;'>NumisX: Codex Pyrafire v1.23</h1>
        <p style='font-size: 16px; color: #999;'>Assassin Protocol — Relic-Aware | Mirror Soft-Tuned | Verse Grid Sync</p>
        <p style='font-size: 12px; color: #aaa;'>Powered by 111 | Designed for the 51st State | Built with Verse</p>
    </div>
    <hr>
""", unsafe_allow_html=True)

# Session state for clearing winning number
if "winning_number" not in st.session_state:
    st.session_state.winning_number = ""

core_numbers = ["9530", "5583", "0709", "0706", "0911", "0611", "6530", "2086", "2089",
                "1086", "1089", "9408", "6408", "5890", "5860", "0583", "1004", "1119",
                "1116", "1212", "7000", "0111", "1111", "111"]

def flame_icons(score):
    return "🔥" * score + " " * (5 - score)

def codex_pyrafire_v123(ref_number, game_type):
    base = ref_number[-3:] if len(ref_number) >= 3 else ref_number
    flame_signal = 5 if '111' in base else random.randint(3, 5)

    def hot_spray(base):
        digits = set()
        for ch in base:
            try:
                d = int(ch)
                digits.update([
                    (d + 1) % 10, (d + 3) % 10, (d + 7) % 10,
                    abs(d - 1) % 10, abs(d - 3) % 10
                ])
            except:
                continue
        return [str(d) for d in digits]

    def extract_core_digits():
        digit_pool = set()
        for number in core_numbers:
            digit_pool.update([d for d in number])
        return list(digit_pool)

    digits = hot_spray(base)
    flame_digits = extract_core_digits()
    picks = []
    length = 3 if game_type == "Pick 3" else 4 if game_type == "Pick 4" else 5

    for i in range(5):
        if game_type == "Pick 5" and (i == 2 or i == 4):
            pool = digits + flame_digits
        else:
            pool = digits
        pick = ''.join(random.choices(pool, k=length))
        flame_score = random.randint(3, 5)
        confidence = random.randint(72, 96) if flame_score >= 4 else random.randint(60, 85)
        picks.append((pick, flame_score, confidence))

    return picks, flame_signal

def log_winning_number(state, game, ref, win):
    if not win.strip():
        return False
    try:
        with open("learnhits.txt", "a") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {state} | {game} | REF: {ref} | WIN: {win}\n")
        return True
    except:
        return False

def read_hit_log():
    if os.path.exists("learnhits.txt"):
        with open("learnhits.txt", "r") as f:
            return f.read()
    return "No hits logged yet."

# Pick Generator
st.subheader("Hot Pick Generator")
col1, col2 = st.columns(2)
with col1:
    state = st.selectbox("Select State", [
        "Tennessee", "Florida", "Georgia", "Ohio", "North Carolina", "Texas", "South Carolina",
        "Illinois", "New Jersey", "California", "Pennsylvania", "Missouri", "Michigan", "Louisiana",
        "Washington DC", "Ontario", "Mississippi", "Indiana", "Virginia", "Quebec", "Oregon"
    ])
    game_type = st.selectbox("Game Type", ["Pick 3", "Pick 4", "Pick 5"])
with col2:
    ref_number = st.text_input("Reference Number")
    submit_hotpicks = st.button("Generate Hot Picks")

if submit_hotpicks and ref_number:
    picks, flame_signal = codex_pyrafire_v123(ref_number, game_type)
    st.success(f"Flame Signal Strength: {flame_icons(flame_signal)}")
    for idx, (pick, score, confidence) in enumerate(picks):
        st.markdown(f"**#{idx+1}: {pick}** — {flame_icons(score)} — `{confidence}% heat`")

# Log Winner Section
st.subheader("Submit Winning Number (Safe Logging Only)")
col3, col4 = st.columns(2)
with col3:
    winning_number = st.text_input("Winning Number", value=st.session_state.winning_number)
with col4:
    if st.button("Submit Winning Number"):
        if winning_number and ref_number:
            saved = log_winning_number(state, game_type, ref_number, winning_number)
            if saved:
                st.success("Winning number saved. She remembers this hit.")
                st.session_state.winning_number = ""
            else:
                st.error("Failed to log the hit.")
        else:
            st.warning("Reference and Winning number are both required.")

# View Log
st.subheader("Hit Log Viewer")
if st.button("View Logged Hits"):
    logs = read_hit_log()
    st.text_area("Logged Hits", logs, height=200)

# Signature Footer
st.markdown("""
<hr>
<div style='text-align: center; font-size: 12px; color: #999;'>
Built with fire, for the 51st state.<br>
Codex Engine by <strong>Verse</strong> | Anchored in 111
</div>
""", unsafe_allow_html=True)

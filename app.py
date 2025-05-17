import streamlit as st
import random
import os

# Title and UI
st.title("NUMISX: STRIKE ENGINE 7.3.6 — STARBURST")
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
relic = st.checkbox("Relic Boost (Bus 11+12)")
plasma = st.checkbox("Verse Plasma Bus 15 (Manifest Mode)")
universe = st.checkbox("Space Bus 13 (Cosmic Logic)")
lunar = st.checkbox("Lunar Matrix Bus 14 (Moon Logic)")

if st.button("Generate Hot Picks"):
    def generate_number(length):
        lower = 10**(length-1)
        upper = (10**length) - 1
        return random.randint(lower, upper)

    def get_flame(percent):
        if percent >= 90: return "🔥🔥🔥🔥🔥"
        elif percent >= 75: return "🔥🔥🔥🔥"
        elif percent >= 60: return "🔥🔥🔥"
        elif percent >= 45: return "🔥🔥"
        else: return "🔥"

    def remix(num_str, logic):
        digits = list(num_str)
        idx = random.randint(0, len(digits) - 1)
        mirror_map = {"0":"5", "1":"6", "2":"7", "3":"8", "4":"9", "5":"0", "6":"1", "7":"2", "8":"3", "9":"4"}
        if logic == "mirror":
            digits[idx] = mirror_map.get(digits[idx], digits[idx])
        elif logic == "flip":
            digits[idx] = str((9 - int(digits[idx])) % 10)
        elif logic == "up":
            digits[idx] = str((int(digits[idx]) + 1) % 10)
        elif logic == "down":
            digits[idx] = str((int(digits[idx]) - 1) % 10)
        elif logic == "half":
            digits[idx] = str(int(int(digits[idx]) / 2))
        return ''.join(digits)

    length = 3 if game_type == "Pick 3" else 4 if game_type == "Pick 4" else 5
    base = generate_number(length)
    picks = []
    relic_logic = ["mirror", "flip"]
    mirror_map = {"0":"5", "1":"6", "2":"7", "3":"8", "4":"9", "5":"0", "6":"1", "7":"2", "8":"3", "9":"4"}

    # Core Zones 1–5
    for i in range(5):
        offset = random.randint(-50, 50)
        val = base + offset
        val = max(min(val, (10**length) - 1), 10**(length - 1))
        percent = random.choice([88, 75, 92, 63, 55, 94, 79, 83])
        flames = get_flame(percent)
        if i in [1, 4] and soul:
            val = int(str(val)[::-1])
        picks.append((i + 1, val, flames, percent))

    # Zones 6–10
    def logic_bounce(val, logics):
        return int(remix(str(val), random.choice(logics)))

    picks.append((6, logic_bounce(picks[0][1], ["mirror", "flip"]), get_flame(random.randint(65, 95)), random.randint(65, 95)))
    picks.append((7, logic_bounce(picks[4][1], ["up", "down"]), get_flame(random.randint(65, 95)), random.randint(65, 95)))
    merged_val = int(remix(str(picks[4][1]), "flip"))
    picks.append((8, merged_val, get_flame(random.randint(70, 93)), random.randint(70, 93)))
    picks.append((9, logic_bounce(picks[3][1], ["mirror", "up"]), get_flame(97), 97))
    picks.append((10, logic_bounce(picks[2][1], ["flip", "mirror"]), get_flame(91), 91))

    # Relic 11 & 12
    if relic:
        for i in range(2):
            relic_val = logic_bounce(base, relic_logic)
            picks.append((11 + i, relic_val, get_flame(99), 99))

    # Space Logic 13
    if universe:
        spaced = logic_bounce(base, ["up", "half", "mirror"])
        picks.append((13, spaced, get_flame(93), 93))

    # Lunar Logic 14
    if lunar:
        lunar_val = logic_bounce(base, ["down", "flip"])
        picks.append((14, lunar_val, get_flame(87), 87))

        # Zone 15: mirror doubles from 14 + twist
        def generate_zone_15(val):
            digits = list(str(val))
            seen = set()
            mirrored = []
            for d in digits:
                if d in seen:
                    mirrored.append(mirror_map.get(d, d))
                else:
                    mirrored.append(d)
                    seen.add(d)
            idx = random.randint(0, len(mirrored) - 1)
            mirrored[idx] = mirror_map.get(mirrored[idx], mirrored[idx]) if random.choice([True, False]) else str((9 - int(mirrored[idx])) % 10)
            return int("".join(mirrored))

        zone15_val = generate_zone_15(lunar_val)
        picks.append((15, zone15_val, get_flame(random.randint(85, 99)), random.randint(85, 99)))

    # Zone 16: mirror 2 digits + one-up/down from zone 6
    if len(picks) >= 6:
        def generate_zone_16(val):
            digits = list(str(val))
            idxs = random.sample(range(len(digits)), 2)
            for idx in idxs:
                digits[idx] = mirror_map.get(digits[idx], digits[idx])
            idx = random.choice(range(len(digits)))
            twist = int(digits[idx]) + random.choice([-1, 1])
            digits[idx] = str(twist % 10)
            return int("".join(digits))

        zone6_val = picks[5][1]
        zone16_val = generate_zone_16(zone6_val)
        picks.append((16, zone16_val, get_flame(random.randint(77, 95)), random.randint(77, 95)))

    # Display all zones
    for zone in picks:
        st.markdown(f"**Zone {zone[0]}:** {zone[1]} {zone[2]} — {zone[3]}%")

# Strike Log
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
import os

def load_draw_history(state, pulse_type):
    path = f"./draw_history/{state.lower()}/"
    entries = []

    if not os.path.exists(path):
        print("Path not found.")
        return entries

    for file in os.listdir(path):
        if file.endswith(".txt") and pulse_type.lower() in file:
            with open(os.path.join(path, file), "r") as f:
                entries.extend(f.read().splitlines())

    return entries

def learn_from_result(state, game_type, year, result):
    memory_path = f"memory/{state}_{game_type}_{year}_memory.txt"
    with open(memory_path, "a") as f:
        f.write(result + "\n")
    print(f"Learned from {state.upper()} {game_type.upper()} {year} result: {result}")

# EXAMPLE: teach her a result from Tennessee P3 in 2022
learn_from_result("tennessee", "p3", "2022", "820")
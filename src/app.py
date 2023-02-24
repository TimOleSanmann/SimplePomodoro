import time
import os
import sys
import json
import math
import platform
import random
from tqdm import tqdm
from pathlib import Path
if platform.system().lower().startswith('win'):
    from win11toast import toast

config_path = os.path.join(Path.home(), ".config/simplepomodoro")
config_path_full = os.path.join(config_path, "config.json")


def pomodoro_timer(config, duration, command):
    end_time = time.time() + duration * 60
    is_interupted = False
    with tqdm(total=duration, leave=False, colour=config[command]["bar_colour"], bar_format="{l_bar}{bar} {n_fmt}/{total_fmt} min") as pbar:
        i = 0
        time_spent = 0
        while time.time() < end_time:
            try:
                i += 1
                if i == 15:
                    pbar.update(0.25)
                    time_spent += 0.25
                    i = 0
                time.sleep(1)
            except KeyboardInterrupt:
                pbar.close()
                is_interupted = True
                break

    if command == "work":
        publish_suggested_break(calc_duration(config, time_spent))

    phrase = config[command]["phrases"][random.randint(0, int(len(config[command]["phrases"])-1))]["text"]
    if platform.system().lower().startswith("win") and not is_interupted:
        toast(phrase, duration="short", buttons=['Ok'])
    elif platform.system().lower().startswith("dar") and not is_interupted:
        os.system(f"osascript -e 'display notification \042{phrase}\042 with title \042Pomodoro Timer\042 sound name \042\042'")

def edit_config_file(config):
    if config["editor"]:
        os.system(f"{config['editor']} {config_path_full}")
    else:
        print(f"No editor was defined. Please find the config file at '{config_path_full}' and insert an editor.")

def create_config_file():
    default_editor = ""
    if platform.system().lower().startswith("win"):
        default_editor = "notepad"
    elif platform.system().lower().startswith("dar"):
        default_editor = "open -e"

    config = {
        "work": {"duration": 50, "bar_colour": "green", "phrases": [{"text": "Work phase ended"},{"text": "Work is done"}]},
        "break": {"duration": 10, "bar_colour": "red", "phrases": [{"text": "Back to work"},{"text": "Break is done"}]},
        "editor": default_editor
    }

    Path(config_path).mkdir(parents=True, exist_ok=True)

    with open(config_path_full, "w") as f:
        json.dump(config, f, indent=4)

def calc_duration(config, duration):
    break_per_work = config["break"]["duration"] / config["work"]["duration"]
    return math.floor(break_per_work * (duration))

def publish_suggested_break(duration):
    print(f"You deserved a {duration} minutes break")

def start_meeting(config):
    duration = 0
    print(f"The meeting has started. Listen close, sit straight and leave if you're not required anymore.")
    print(f"Press Ctrl-C to End the Meeting.", end="\n\n")
    while True:
        try:
            print(f"The Meeting now lasts {math.floor(duration / 60)} minutes.", end="\r")
            time.sleep(1)
            duration += 1
        except KeyboardInterrupt:
            publish_suggested_break(calc_duration(config, duration /60))
            sys.exit(0)

if __name__ == "__main__":
    command = sys.argv[1]

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python pomodoro.py [work/break/config/meet] [duration (optional)]")
        sys.exit(1)
    
    if not os.path.exists(config_path):
        create_config_file()

    with open(config_path_full, "r") as f:
        config = json.load(f)

    if command not in ["work", "break", "config", "meet"]:
        print("Error: Invalid parameter. Use either 'work', 'break', or 'config'.")
        sys.exit(1)

    if command == "config":
        edit_config_file(config)
        sys.exit(0)

    if command == "meet" and len(sys.argv) == 3:
        duration = int(sys.argv[2])
        publish_suggested_break(calc_duration(config, duration))
        sys.exit(0)
    elif command == "meet":
        start_meeting(config)
        sys.exit(0)
    
    if len(sys.argv) == 3:
        duration = int(sys.argv[2])
    else:
        duration = config[command]["duration"]
    pomodoro_timer(config, duration, command)

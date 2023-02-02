import time
import os
import sys
import json
import math
import platform
from tqdm import tqdm
from pathlib import Path
if platform.system().lower().startswith('win'):
    from win11toast import toast

config_path = os.path.join(Path.home(), ".simplepomodoro")
config_path_full = os.path.join(config_path, "config.json")


def pomodoro_timer(duration):
    end_time = time.time() + duration * 60
    with tqdm(total=duration * 60) as pbar:
        while time.time() < end_time:
            try:
                time.sleep(1)
                pbar.update(1)
            except KeyboardInterrupt:
                sys.exit(0)

    if platform.system().lower().startswith("win"):
        toast("Pomodoro timer finished.")
    elif platform.system().lower().startswith("dar"):
        os.system("osascript -e 'display notification \"Pomodoro timer finished.\" with title \"Pomodoro Timer\" sound name \"\"'")

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
        "work": {"duration": 50},
        "break": {"duration": 10},
        "editor": default_editor
    }

    Path(config_path).mkdir(parents=True, exist_ok=True)

    with open(config_path_full, "w") as f:
        json.dump(config, f, indent=4)
    print("Created default configuration file at 'config.json'.")

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
            break_per_work = config["break"]["duration"] / config["work"]["duration"]
            print(f"The Meeting duration was {math.floor(duration / 60)} minutes.")
            print(f"You deserved a {math.floor(break_per_work * (duration/60))} minute break")

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

    if command == "meet":
        start_meeting(config)
        sys.exit(0)
    
    if len(sys.argv) == 3:
        duration = int(sys.argv[2])
    else:
        duration = config[command]["duration"]
    pomodoro_timer(duration)

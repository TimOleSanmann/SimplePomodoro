import time
import os
import sys
import json
import math
import progressbar
from win11toast import toast

def pomodoro_timer(duration):
    widgets = [
        progressbar.Percentage(),
        " ", progressbar.Bar(),
        " ", progressbar.ETA(),
    ]
    bar = progressbar.ProgressBar(maxval=duration * 60, widgets=widgets)
    bar.start()
    end_time = time.time() + duration * 60
    while time.time() < end_time:
        bar.update(math.floor(time.time() - (end_time - duration * 60)))
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(0)
    if os.name == "nt":
        toast("Pomodoro timer finished.")
    else:
        os.system("osascript -e 'display notification \"Pomodoro timer finished.\" with title \"Pomodoro Timer\" sound name \"\"'")

def open_config_file(config):
    if os.name == "nt":
        os.system(f"{config['editor']['windows']} config.json")
    else:
        os.system(f"{config['editor']['macos']} config.json")

def create_config_file():
    config = {
        "work": {"duration": 50},
        "break": {"duration": 10},
        "editor":{
            "windows": "notepad",
            "macos": "open -e"
        }
    }

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    print("Created default configuration file at 'config.json'.")

if __name__ == "__main__":
    command = sys.argv[1]

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python pomodoro.py [work/break/config] [duration (optional)]")
        sys.exit(1)
    
    if not os.path.exists("config.json"):
        create_config_file()

    with open("config.json", "r") as f:
        config = json.load(f)

    if command not in ["work", "break", "config"]:
        print("Error: Invalid parameter. Use either 'work', 'break', or 'config'.")
        sys.exit(1)

    if command == "config":
        open_config_file(config)
        sys.exit(0)
    
    if len(sys.argv) == 3:
        duration = int(sys.argv[2])
    else:
        duration = config[command]["duration"]
    pomodoro_timer(duration)

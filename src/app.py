import time
import os
import sys
import json
import math
import progressbar

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
        os.system("msg * Pomodoro timer finished.")
    else:
        os.system("osascript -e 'display notification \"Pomodoro timer finished.\" with title \"Pomodoro Timer\" sound name \"\"'")

def open_config_file():
    if os.name == "nt":
        os.system("start notepad config.json")
    else:
        os.system("open -e config.json")

def create_config_file():
    config = {
        "work": {"duration": 50},
        "break": {"duration": 10}
    }
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    print("Created default configuration file at 'config.json'.")
    open_config_file()

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python pomodoro.py [work/break/config] [duration (optional)]")
        sys.exit(1)
        
    command = sys.argv[1]
    if command == "config":
        if os.path.exists("config.json"):
            open_config_file()
        else:
            create_config_file()
        sys.exit(0)
    
    if not os.path.exists("config.json"):
        create_config_file()
        sys.exit(0)
        
    with open("config.json", "r") as f:
        config = json.load(f)
    if command not in config:
        print("Error: Invalid parameter. Use either 'work', 'break', or 'config'.")
        sys.exit(1)
        
    if len(sys.argv) == 3:
        duration = int(sys.argv[2])
    else:
        duration = config[command]["duration"]
    pomodoro_timer(duration)


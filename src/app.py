import time
import os
import sys
import json
import math
import platform
import random
import click
from tqdm import tqdm
from pathlib import Path
if platform.system().lower().startswith('win'):
    from win11toast import toast

class global_config:
    def __init__(self):
        self.config_path = os.path.join(Path.home(), ".config/simplepomodoro", "config.json")
        if not os.path.isfile(self.config_path):
            self.create_config_file()
        with open(self.config_path) as f:
            config = json.load(f)
        self.work_duration = config["work"]["duration"]
        self.break_duration = config["break"]["duration"]
        self.work_bar_colour = config["work"]["bar_colour"]
        self.break_bar_colour = config["break"]["bar_colour"]
        self.editor = config["editor"]

    def create_config_file(self):
        default_editor = ""
        if platform.system().lower().startswith("win"):
            default_editor = "notepad"
        elif platform.system().lower().startswith("dar"):
            default_editor = "open -e"

        config = {
            "work": {"duration": 50, "bar_colour": "green"},
            "break": {"duration": 10, "bar_colour": "red"},
            "editor": default_editor
        }

        Path(os.path.dirname(self.config_path)).mkdir(parents=True, exist_ok=True)

        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=4)

@click.group()
def sp():
    pass

@sp.command()
@click.argument("time", required=False)
def work(time):
    duration = gc.work_duration
    if time:
        duration = time

    start_timer(int(duration), gc.work_bar_colour)

@sp.command(name="break")
@click.argument("time", required=False)
def rest(time):
    duration = gc.break_duration
    if time:
        duration = time

    start_timer(int(duration), gc.break_bar_colour)


@sp.command()
def config():
    os.system(f"{gc.editor} {gc.config_path}")

def start_timer(duration, bar_colour):
    end_time = time.time() + float(duration) * 60
    is_interupted = False
    with tqdm(total=duration, leave=False, colour=bar_colour, bar_format="{l_bar}{bar} {n_fmt}/{total_fmt} min") as pbar:
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

    if click.get_current_context().info_name == "work":
        phrase = "Work phase is done"
    elif click.get_current_context().info_name == "break":
        phrase = "Break phase is done"
    else:
        phrase = ""

    if platform.system().lower().startswith("win") and not is_interupted:
        toast(phrase, duration="short", buttons=['Ok'])
    elif platform.system().lower().startswith("dar") and not is_interupted:
        os.system(f"osascript -e 'display notification \042{phrase}\042 with title \042Pomodoro Timer\042 sound name \042\042'")    

    if click.get_current_context().info_name == "work":
        publish_suggested_break(calc_duration(time_spent))

def calc_duration(duration):
    break_per_work = gc.break_duration / gc.work_duration
    return math.floor(break_per_work * (duration))

def publish_suggested_break(duration):
    print(f"You deserved a {duration} minutes break")

if __name__ == "__main__":
    gc = global_config()
    sp()

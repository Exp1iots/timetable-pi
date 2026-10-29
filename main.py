import json
from datetime import datetime
from zoneinfo import ZoneInfo
from html import escape
import shutil
from pathlib import Path
from cairosvg import svg2png # must be installed
# import epaper # waveshare-epaper must be installed
from PIL import Image

# Variables
timezone = "Australia/Sydney"
display_to_screen = True
cleanup = True

# Load all json files
with open("timetable.json", mode="r", encoding="utf-8") as read_file:
    timetable = json.load(read_file)

with open("line_assignments.json", mode="r", encoding="utf-8") as read_file:
    line_assignments = json.load(read_file)

with open("weeks.json", mode="r", encoding="utf-8") as read_file:
    weeks = json.load(read_file)

def edit_svg(file_name, text_to_replace, text_to_replace_with):
    # Source - https://stackoverflow.com/a/67695756
    # Posted by KRM
    # Retrieved 2026-10-29, License - CC BY-SA 4.0
    # Modified by Exp1iots

    # copy file to another location to avoid writing over original
    if Path(f"tmp/{file_name}").exists(): # check if the tmp file already exists - not checking this results in the tmp file being overwritten by the default on every edit
        pass
    else:
        shutil.copy(f"source/defaults/{file_name}", f"tmp/{file_name}")

    #read input file
    fin = open(f"tmp/{file_name}", "rt")

    #read file contents to string
    data = fin.read()

    if "&" in text_to_replace_with:
        text_to_replace_with = escape(text_to_replace_with, quote=False)

    #replace all occurrences of the required string
    data = data.replace(text_to_replace, text_to_replace_with)

    #close the input file
    fin.close()

    #open the input file in write mode
    fin = open(f"tmp/{file_name}", "wt")

    #overrite the input file with the resulting data
    fin.write(data)

    #close the file
    fin.close()

def convert_svg_to_png(svg_path, output_path):
    # Source - https://stackoverflow.com/a/13320450
    # Posted by JWL, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-10-29, License - CC BY-SA 3.0
    # Modified by Exp1iots

    svg2png(url=svg_path,write_to=output_path)

    if cleanup: Path.unlink(svg_path) # remove svg after use

user_person = input("Person (lower case): ")

today = datetime.now(ZoneInfo(timezone))
day_of_week = today.weekday()
week_of_year = today.isocalendar().week
days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday"]

def main(week):
    day = timetable[f"week_{week}"][days_of_week[day_of_week]]

    def run_edit_svg(svg_name):
        for period, line in day.items(): # assigns the key and value pair of "period: line_num" in timetable.json to python variables
            edit_svg(svg_name, f"period_{period}_line", f"Line {str(line)}") # must do line first as doing class first results in f"period_{period}_line" becoming f"period_{line_assignments[str(line)][user_person]}_line"
            edit_svg(svg_name, f"period_{period}", line_assignments[str(line)][user_person])
        png_name = Path(svg_name).stem + ".png"
        convert_svg_to_png(f"tmp/{svg_name}", f"bitmaps/{png_name}")

        if display_to_screen:
            edp = epaper.epaper('epd2in13_V4').EPD()

            edp.Clear()

            try:
                edp.init()

                # Fit the picture to the panel and convert to 1-bit monochrome
                image = Image.open("bitmaps/full_without_period_0.png").convert("RGB")
                image = image.convert("1")

                edp.display(edp.getbuffer(image))

            finally:
                edp.sleep()

        if cleanup: Path.unlink(f"bitmaps/{png_name}") # remove png after use

    if "period_0" in day: # check if their is a period 0
        if day_of_week == 1: # check if it's tuesday
            run_edit_svg("tuesday_with_period_0.svg")
        elif day_of_week != 1: # check if it's not tuesday
            run_edit_svg("full_with_period_0.svg")
    elif "period_0" not in day: # check if there isn't a period 0
        if day_of_week == 1: # check if it's tuesday
            run_edit_svg("tuesday_without_period_0.svg")
        elif day_of_week != 1: # check if it's not tuesday
            run_edit_svg("full_without_period_0.svg")

if week_of_year in weeks["week_a"]:
    main("a")
elif week_of_year in weeks["week_b"]:
    main("b")
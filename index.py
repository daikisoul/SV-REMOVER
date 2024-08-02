import os
import re
import pygetwindow as gw

def find_osu_window_title():
    windows = gw.getWindowsWithTitle('')
    for window in windows:
        if window.title.lower().startswith('osu!'):
            return window.title
    return None

def extract_beatmap_name(title):
    cleaned_title = title.strip()
    match = re.search(r'\[([^]]+)]', cleaned_title)
    if match:
        return match.group(1)
    return None

def find_osu_file_path(beatmap_name, songs_directory):
    for root, dirs, files in os.walk(songs_directory):
        for file in files:
            if file.endswith('.osu') and beatmap_name in file:
                return os.path.join(root, file)
    return None

def edit_osu_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except IOError as e:
        print(f"Error reading file: {e}")
        return

    metadata_section = False
    timing_points_section = False
    first_timing_point = False
    new_lines = []

    for line in lines:
        if line.strip() == '[Metadata]':
            metadata_section = True
            new_lines.append(line)
            continue
        elif line.strip() == '[TimingPoints]':
            timing_points_section = True
            first_timing_point = True
            new_lines.append(line)
            continue
        elif line.startswith('['):
            metadata_section = False
            timing_points_section = False
            new_lines.append(line)
            continue

        if metadata_section and line.startswith('Version:'):
            line = 'Version: sv deleted\n'

        if timing_points_section:
            if first_timing_point:
                new_lines.append(line)
                first_timing_point = False
            # Skip all other lines in the [TimingPoints] section
        else:
            new_lines.append(line)

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(new_lines)
    except IOError as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    osu_title = find_osu_window_title()
    if osu_title:
        beatmap_name = extract_beatmap_name(osu_title)
        if beatmap_name:
            # Use os.path.expanduser to correctly handle user directories
            songs_directory = os.path.expanduser(r'~\AppData\Local\osu!\Songs')
            osu_file_path = find_osu_file_path(beatmap_name, songs_directory)
            if osu_file_path:
                edit_osu_file(osu_file_path)
                print("File modified successfully.")
            else:
                print("No matching .osu file found.")
        else:
            print("Beatmap name not found in the title.")
    else:
        print("osu! window not found.")

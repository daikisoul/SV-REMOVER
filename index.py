import os
import re
import pygetwindow as gw

def find_osu_window_title():
    # Get a list of all open windows
    windows = gw.getWindowsWithTitle('')
    for window in windows:
        if window.title.lower().startswith('osu!'):
            return window.title
    return None

def extract_beatmap_name(title):
    # Clean the title by removing extra whitespace and special characters if needed
    cleaned_title = title.strip()
    # Use a regular expression to extract the beatmap name enclosed in brackets
    match = re.search(r'\[([^]]+)]', cleaned_title)
    if match:
        return match.group(1)
    return None

def find_osu_file_path(beatmap_name, songs_directory):
    # Iterate over directories in the Songs folder
    for root, dirs, files in os.walk(songs_directory):
        for file in files:
            if file.endswith('.osu'):
                if beatmap_name in file:
                    return os.path.join(root, file)
    return None

def edit_osu_file(file_path):
    # Read the content of the .osu file with UTF-8 encoding
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the [HitObjects] and [Metadata] sections and modify the lines
    hit_objects_section = False
    metadata_section = False
    new_lines = []

    for line in lines:
        if line.strip() == '[HitObjects]':
            hit_objects_section = True
            new_lines.append(line)
            continue
        elif line.strip() == '[Metadata]':
            hit_objects_section = False
            metadata_section = True
            new_lines.append(line)
            continue
        elif line.startswith('[') and (hit_objects_section or metadata_section):
            hit_objects_section = False
            metadata_section = False
            new_lines.append(line)
            continue

        if hit_objects_section:
            # Replace the specific hit object format
            line = re.sub(r'128,\d+,\d+:\d+:\d+:\d+:\d+', '1,0,0:0:0:0:', line)

        if metadata_section and line.startswith('Version:'):
            # Update the Version: field
            line = 'Version: ln deleted\n'  # Change this to the desired version

        new_lines.append(line)

    # Write the modified content back to the file with UTF-8 encoding
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

if __name__ == "__main__":
    osu_title = find_osu_window_title()
    if osu_title:
        print(f"Found osu! window title: {osu_title}")
        beatmap_name = extract_beatmap_name(osu_title)
        if beatmap_name:
            print(f"Beatmap name: {beatmap_name}")

            # Set the path to your Songs directory
            songs_directory = r'C:\Users\daiki\AppData\Local\osu!\Songs'
            osu_file_path = find_osu_file_path(beatmap_name, songs_directory)
            if osu_file_path:
                print(f"Found .osu file at: {osu_file_path}")
                edit_osu_file(osu_file_path)
                print("Modified [HitObjects] section and updated [Metadata] Version in the .osu file.")
            else:
                print("No matching .osu file found.")
        else:
            print("Beatmap name not found in the title.")
    else:
        print("osu! window not found.")

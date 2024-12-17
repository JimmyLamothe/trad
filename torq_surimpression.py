#!/usr/bin/env python

"""
Convertit un XML Adobe Premier en TXT avec Time Codes et identification de personnages.
Génère aussi un TXT avec les personnages et leur temps total
"""

from analysis import get_input_file, get_tc_info, get_title_dicts
from analysis import combine_titles, add_duration, get_character_timing

print('Ne pas oublier de vérifier que le TC est bon avant de travailler sur le document Word.\n')

input_file = get_input_file()
tc_info = get_tc_info()
tc = tc_info['tc']
hour = tc_info['hour']
subtitle_list = get_title_dicts(input_file, tc, hour)
combined_list = combine_titles(subtitle_list)
add_duration(combined_list)
character_timing = get_character_timing(combined_list)

output_characters = input_file.parent / f"{input_file.stem}_characters.txt"
output_titles = input_file.parent / f"{input_file.stem}_titles.txt"

with open(output_characters, 'w') as output_file:
    for name, duration_frames in character_timing:
        total_seconds = max(duration_frames // tc, 1)
        minutes, seconds = divmod(total_seconds, 60)  # Get minutes and remaining seconds
        if minutes > 0:
            output_file.write(f"{name} - {minutes} min {seconds} sec\n")
        else:
            output_file.write(f"{name} - {seconds} sec\n")

with open(output_titles, 'w') as output_file:
    for title in combined_list:
        if title['ST']:  #Add identifier to name if it's a subtitle
            title['name'] += ' (sous-titres)'

        # Convert frame numbers to timecode in HH:MM:SS,ms format
        start_seconds = title['start'] // tc
        end_seconds = title['end'] // tc
        duration_seconds = max(title['duration'] // tc, 1)

        start_time = f"{hour}:{(start_seconds % 3600) // 60:02}:{start_seconds % 60:02},{(title['start'] % tc) * (1000 // tc):03}"
        end_time = f"{hour}:{(end_seconds % 3600) // 60:02}:{end_seconds % 60:02},{(title['end'] % tc) * (1000 // tc):03}"

        # Format duration as "X sec" or "X min Y sec"
        minutes, seconds = divmod(duration_seconds, 60)
        duration_str = f"{minutes} min {seconds} sec" if minutes > 0 else f"{seconds} sec"

        # Write the formatted text to the file
        output_file.write(f"{start_time} --> {end_time} - {duration_str}\n")
        output_file.write(f"{title['name']}\n")
        output_file.write(f"{title['text']}\n\n")

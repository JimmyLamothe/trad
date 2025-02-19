#!/usr/bin/env python

"""
Convertit un XML Adobe Premier en TXT avec Time Codes et identification de personnages.
Génère aussi un TXT avec les personnages et leur temps total
"""

from analysis import get_input_files, get_full_tc_info, get_title_dicts
from analysis import combine_titles, add_duration, get_character_timing
from get_tc import get_tc

print('Ne pas oublier de vérifier que le TC est bon avant de travailler sur le document Word.\n')

input_file = get_input_files(single_file=True)
tc_info = get_full_tc_info(tc_out='ignore')
tc_in = tc_info['tc_in']
start_hour = tc_info['start_hour']
subtitle_list = get_title_dicts(input_file)
combined_list = combine_titles(subtitle_list)
add_duration(combined_list)
character_timing = get_character_timing(combined_list)

output_characters = input_file.parent / f"{input_file.stem}_characters.txt"
output_titles = input_file.parent / f"{input_file.stem}_titles.txt"

with open(output_characters, 'w') as output_file:
    for name, duration_frames in character_timing:
        total_seconds = max(duration_frames // tc_in, 1)
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
        start_time = get_tc(
            title['start'],
            tc_in=tc_in,
            tc_out='SRT',
            start_hour=start_hour,
            coefficient=False
        )
        end_time = get_tc(
            title['end'],
            tc_in=tc_in,
            tc_out='SRT',
            start_hour=start_hour,
            coefficient=False
        )
        # Format duration as "X sec" or "X min Y sec"
        duration_seconds = max(title['duration'] // tc_in, 1)
        minutes, seconds = divmod(duration_seconds, 60)
        duration_str = f"{minutes} min {seconds} sec" if minutes > 0 else f"{seconds} sec"
        # Write the formatted text to the file
        output_file.write(f"{start_time} --> {end_time} - {duration_str}\n")
        output_file.write(f"{title['name']}\n")
        output_file.write(f"{title['text']}\n\n")

            
"""
with open(output_titles, 'w') as output_file:
    for title in combined_list:
        if title['ST']:  #Add identifier to name if it's a subtitle
            title['name'] += ' (sous-titres)'

        # Convert frame numbers to timecode in HH:MM:SS,ms format
        start_seconds = title['start'] // tc_in
        end_seconds = title['end'] // tc_in
        duration_seconds = max(title['duration'] // tc_in, 1)

        start_time = f"{start_hour}:{(start_seconds % 3600) // 60:02}:{start_seconds % 60:02},{(title['start'] % tc_in) * (1000 // tc_in):03}"
        end_time = f"{start_hour}:{(end_seconds % 3600) // 60:02}:{end_seconds % 60:02},{(title['end'] % tc_in) * (1000 // tc_in):03}"

        # Format duration as "X sec" or "X min Y sec"
        minutes, seconds = divmod(duration_seconds, 60)
        duration_str = f"{minutes} min {seconds} sec" if minutes > 0 else f"{seconds} sec"

        # Write the formatted text to the file
        output_file.write(f"{start_time} --> {end_time} - {duration_str}\n")
        output_file.write(f"{title['name']}\n")
        output_file.write(f"{title['text']}\n\n")
"""

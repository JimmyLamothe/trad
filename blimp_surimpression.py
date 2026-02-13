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
tc_info = get_full_tc_info(tc_out='23,976')
tc_in = tc_info['tc_in']
tc_out = '23,976'
print('fix stupid tc_out bug someday, too tired')
start_hour = tc_info['start_hour']
subtitle_list = get_title_dicts(input_file, add_number=True)
combined_list = combine_titles(subtitle_list)
add_duration(combined_list)
character_timing = get_character_timing(combined_list, fps=tc_in, TORQ=False)

output_characters = input_file.parent / f"{input_file.stem}_characters.txt"
output_titles = input_file.parent / f"{input_file.stem}_titles.txt"

with open(output_characters, 'w') as output_file:
    for name, seconds in character_timing:
        minutes, seconds = divmod(seconds, 60)  # Get minutes and remaining seconds
        if minutes > 0:
            output_file.write(f"{name} - {minutes} min {seconds} sec\n")
        else:
            output_file.write(f"{name} - {seconds} sec\n")

with open(output_titles, 'w') as output_file:
    for title in combined_list:
        # Convert frame numbers to timecode in HH:MM:SS,ms format
        start_time = get_tc(
            title['start'],
            tc_in=tc_in,
            tc_out=tc_out,
            start_hour=start_hour,
            coefficient=False
        )
        end_time = get_tc(
            title['end'],
            tc_in=tc_in,
            tc_out=tc_out,
            start_hour=start_hour,
            coefficient=False
        )
        duration_seconds = max(title['duration'] // tc_in, 1)
        # Write the formatted text to the file
        if duration_seconds < 0:
            tc_string = f"{start_time}"
        else:
            tc_string = f"{start_time} à {end_time};"
        output_file.write(tc_string)
        output_file.write(f"{title['number']};")
        output_file.write(f"{title['name']};")
        output_file.write(f"{title['text']}\n")

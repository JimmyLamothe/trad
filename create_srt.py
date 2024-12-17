#!/usr/bin/env python

"""
Convertit un XML Adobe Premier en fichier de sous-titres SRT
"""

from analysis import get_input_file, get_full_tc_info, get_title_dicts
from get_tc import get_tc

input_file = get_input_file()
tc_info = get_full_tc_info(tc_out='ignore', start_hour='ignore')
tc_in = tc_info['tc_in']
title_list = get_title_dicts(input_file, surimpression=False)
subtitle_list = [title for title in title_list if title.get('ST', False)]
output_srt = input_file.parent / f"{input_file.stem}.srt"

with open(output_srt, 'w') as output_file:
    for index, title in enumerate(subtitle_list, start=1):
        # Convert frame numbers to timecode in HH:MM:SS,ms format
        start_time = get_tc(title['start'], tc_in=tc_in, tc_out='SRT', start_hour=0)
        end_time = get_tc(title['end'], tc_in=tc_in, tc_out='SRT', start_hour=0)

        # Write in SRT format
        output_file.write(f"{index}\n")  # Title number
        output_file.write(f"{start_time} --> {end_time}\n")  # Timecodes
        output_file.write(f"{title['text']}\n")  # Title text
        output_file.write("\n")  # Line break

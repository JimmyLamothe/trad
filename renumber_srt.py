#!/usr/bin/env python3

"""
Corrige la numérotation d'un SRT lorsqu'on a rajouté ou enlevé un titre.

"""

import sys

input_filename = sys.argv[1]

output_filename = input_filename[:-4] + '_new.srt'

with open(input_filename, 'r') as input_file:
    with open(output_filename, 'w') as output_file:
        line_count = 0
        title_number = 1
        for line in input_file:
            if line == '\n':
                line_count = 0
                title_number += 1
                output_file.write(line)
            elif line_count == 0:
                output_file.write(str(title_number))
                output_file.write('\n')
                line_count += 1
            else:
                line_count += 1
                output_file.write(line)
                
                                  

"""
    srt_output.write(str(count))
    srt_output.write('\n')
    srt_output.write(tc_in)
    srt_output.write(' --> ')
    srt_output.write(tc_out)
    srt_output.write('\n')
    srt_output.write(clip[2])
    srt_output.write('\n')
    srt_output.write('\n')
"""

#!/usr/bin/env python3

"""
Convertit un XML FCP7 en .srt.

Prend deux arguments: input/NOMDUXML - TC
"""

from lxml import etree
import sys
import tc_calc

input_file = sys.argv[1]

tc = "0"

try:
    tc = int(sys.argv[2])
except IndexError:
    print("Don't forget to enter Time Code (24 or 30)")
    sys.exit(0)

skip_empty = True

try:
    if sys.argv[3] == 'False':
        skip_empty = False
    else:
        print('Invalid argument')
        sys.exit(0)
except IndexError:
    pass

filename_srt = input_file[:-4] + '.srt'

tree = etree.parse(input_file)
root = tree.getroot()
sequence = root.find('sequence')
media = sequence.find('media')
video = media.find('video')
def get_track_list(video_or_audio):
    return(video_or_audio.findall('track'))

track_list = get_track_list(video)
v1 = track_list[0]
clip_list = v1.findall('clipitem')
with open(filename_srt, 'w') as srt_output:
    title_list = []
    for clip in clip_list:
        start = int(clip.find('start').text)
        end = int(clip.find('end').text)
        filter_list = clip.findall('filter')
        value = ""
        line = 1
        for filter in filter_list:
            if line > 1:
                value += '\n'
            effect = filter.find('effect')
            if effect.find('name').text == None:
                print('Title failed - No value')
                continue
            else:
                value += effect.find('name').text
                line += 1
            if skip_empty:
                if value[0] == '\r':
                    print('empty first')
                    value = value[1:]
        title_list.append((start, end, value))
    sorted_clip_list = sorted(title_list, key = lambda clip: clip[0])

    count = 0
    for clip in sorted_clip_list:
        if value[0] == '\r':
            print('still empty first')
        count += 1
        duration = clip[1] - clip[0]
        tc_in_base = tc_calc.tc_calc(clip[0], hour = 10, tc = tc)
        tc_in_start = tc_in_base[0:8]
        tc_in_frames = tc_in_base[9:]
        tc_in_milliseconds_base = float(tc_in_frames) / tc
        tc_in_milliseconds = "{0:.3f}".format(tc_in_milliseconds_base)[2:5]
        tc_in = tc_in_start + ',' + tc_in_milliseconds
        tc_out_base = tc_calc.tc_calc(clip[1], hour = 10, tc = tc)
        tc_out_start = tc_out_base[0:8]
        tc_out_frames = tc_out_base[9:]
        tc_out_milliseconds_base = float(tc_out_frames) / tc
        tc_out_milliseconds = "{0:.3f}".format(tc_out_milliseconds_base)[2:5]
        tc_out = tc_out_start + ',' + tc_out_milliseconds
        srt_output.write(str(count))
        srt_output.write('\n')
        srt_output.write(tc_in)
        srt_output.write(' --> ')
        srt_output.write(tc_out)
        srt_output.write('\n')
        srt_output.write(clip[2])
        srt_output.write('\n')
        srt_output.write('\n')

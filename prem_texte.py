#!/usr/bin/env python3

"""
Convertit un XML FCP7 en .txt.

Prend un arguement: input/NOMDUXML
"""

from lxml import etree
import sys

input_file = sys.argv[1]

filename_txt = input_file[:-4] + '.txt'

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
with open(filename_txt, 'w') as txt_output:
    title_list = []
    for clip in clip_list:
        filter_list = clip.findall('filter')
        value = ""
        for filter in filter_list:
            effect = filter.find('effect')
            if effect.find('name').text == None:
                print('Title skipped - No value')
                continue
            else:
                value += effect.find('name').text
            if value[0] == '\r':
                print('deleting empty first')
                value = value[1:]
            value = value.replace('\n', ' ')
            value = value.replace('\r', ' ')
        title_list.append(value + ' ')

    count = 0
    for title in title_list:
        title = title.replace('\n',' ')
        title = title.replace('\r',' ')
        title = title.replace('.','. ')
        title = title.replace('?','? ')
        title = title.replace('!','! ')
        title = title.replace('  ',' ')
        txt_output.write(title)
        count += 1

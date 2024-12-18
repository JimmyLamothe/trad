#!/usr/bin/env python3

"""
Compte le nombre de lignes dans un XML FCP7 sorti par Premiere et écrit un fichier texte

Prend un argument: input/NOMDUXML
"""

from lxml import etree
import sys
import tc_calc

input_file = sys.argv[1]

filename_txt = input_file[:-4] + '_count.txt'

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

try:
    v2 = track_list[1]
    clip_list_v2 = v2.findall('clipitem')
    clip_list = clip_list + clip_list_v2

except Exception:
    pass

with open(filename_txt, 'w') as txt_output:
    title_list = []
    for clip in clip_list:
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
        title_list.append(value)
    line_list = []
    for text in title_list:
        letter_count = 0
        if text == None:
            print('pass')
            continue
        line = ""
        for letter in text:
            if letter in ['\n','\r','\n\r','\r\n']:
                line += letter
                letter_count +=1
                line_list.append(line)
                line = ""
            else:
                line += letter
                letter_count += 1
        if line:
            line_list.append(line)
        letter_count = 0

    count = 0
    short_line_list = [line for line in line_list if len(line) > 1]
    for line in short_line_list:
        if line:
            print(len(line))
            print(line)
        else:
            print('EMPTY')
    print(short_line_list)
    def strip_carriage_return(text):
        print('\n' in text)
        print('\r' in text)
        text = text.strip('\n')
        text = text.strip('\r')
        print('\n' in text)
        print('\r' in text)
        return text
    for line in short_line_list:
        print(count)
        print(line)
        line = strip_carriage_return(line)
        count += 1
        num_line = str(count) + ': ' + line 
        txt_output.write(num_line)
        txt_output.write('\n')

print(count)

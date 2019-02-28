#!/usr/bin/env python3

"""
Prints the text  of titles in a FCP7 XML file.

Usage: python3 linecount_fcp_xml.py input/XMLNAME

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

title_list = v1.findall('generatoritem')

with open(filename_txt, 'w') as txt_output:
    final_title_list = []
    for title in title_list:
        effect = title.find('effect')
        parameter = effect.find('parameter')
        value = parameter.find('value').text
        if value == None:
            try:
                parameter = effect[6]
                value = parameter.find('value').text
            except Exception:
                print('Title failed')
                continue
        text = ""
        count = 0
        for letter in value:
            if letter in ['\n','\r','\n\r','\r\n']:
                text += " "
                text += letter
                count +=1
            else:
                text += letter
                count += 1
        final_title_list.append(text)
        count = 0
    for title in final_title_list:
        txt_output.write(title)
        txt_output.write('\n')

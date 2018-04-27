"""
Counts the number of title lines in a FCP7 XML file.

Usage: python3 trad_count.py input/XMLNAME output/TXTNAME

"""
from lxml import etree
import sys

filename = sys.argv[2]

input = sys.argv[1]

filename_txt = filename + '_count.txt'

tree = etree.parse(input)

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
    line_list = []
    for title in title_list:
        effect = title.find('effect')
        parameter = effect.find('parameter')
        value = parameter.find('value')
        text = value.text
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
        count += 1
        num_line = str(count) + ': ' + line 
        txt_output.write(num_line)
        txt_output.write('\n')

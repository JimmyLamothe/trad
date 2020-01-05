#!/usr/bin/env python3

"""
Convertit un XML FCP7 en .txt pour Antidote.
Fait une pause après la conversion.
Ensuite, reconvertit le .txt corrigé en XML.

Prend un argument: input/NOMDUXML.
"""


from lxml import etree
import sys
import tc_calc

input_xml = sys.argv[1]

filename = input_xml[:-4]

filename_xml = filename + '_new.xml'

tc = 30

text_only = True 

filename_txt = filename + '.txt'

tree = etree.parse(input_xml)

root = tree.getroot()

sequence = root.find('sequence')

media = sequence.find('media')

video = media.find('video')

def get_track_list(video_or_audio):
    return(video_or_audio.findall('track'))

track_list = get_track_list(video)
    
v1 = track_list[0]

clip_list = v1.findall('generatoritem')

with open(filename_txt, 'w') as txt_output:
    title_list = []
    for title in clip_list:
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
        title_list.append(value)    
    for title in title_list:
        txt_output.write("*** " +title)
        txt_output.write('\n')

test = input("Press ENTER after antidote correction to create final XML")

with open(filename_txt, 'r') as txt_input:
    txt_input_string = txt_input.read()
    print(txt_input_string)
    title_list = txt_input_string.split(sep="*** ")
    print(len(title_list))
    print(title_list)
    title_list = title_list[1:]
    for number, clip in enumerate(clip_list):
        print(number)
        print(clip)
        effect = clip.find('effect')
        parameter = effect.find('parameter')
        value = parameter.find('value').text
        if value == None:
            try:
                parameter = effect[6]
                value = parameter.find('value').text
            except Exception:
                print('Title failed')
                continue
        try:
            value = title_list[number].replace('\n', 'BRK_LN')
            print(value)
            parameter.find('value').text = value
        except Exception:
            print('Title failed')
            print(clip)
            sys.exit(0)

tree.write(filename_xml, encoding = 'UTF-8', xml_declaration = True)


# correcting bad line break formatting
filedata = None
with open(filename_xml, 'r') as file :
  filedata = file.read()

filedata = filedata.replace('BRK_LN', '&#13;')

with open(filename_xml, 'w') as file:
  file.write(filedata)

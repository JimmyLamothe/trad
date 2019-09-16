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

try:
    output_xml = sys.argv[2] #input/REF/REF_ECHO_24 or 30
except Exception:
    answer = input('24 or 30?')
    if answer == '24':
        output_xml = 'input/REF/REF_ECHO_24.xml'
    elif answer == '30':
        output_xml = 'input/REF/REF_ECHO_30.xml'

filename = input_xml[:-4]

filename_xml = filename + '_new.xml'

tc = 30

text_only = True 

filename_txt = filename + '.txt'

tree = etree.parse(input_xml)
output_tree = etree.parse(output_xml)

def xml_print(xml, pretty=True):
    print(etree.tostring(xml, pretty_print=pretty))
    sys.exit(0)

root = tree.getroot()
output_root = output_tree.getroot()

sequence = root.find('sequence')
output_sequence = output_root.find('sequence')

media = sequence.find('media')
output_media = output_sequence.find('media')
                    
video = media.find('video')
output_video = output_media.find('video')

def get_track_list(video_or_audio):
    return(video_or_audio.findall('track'))

track_list = get_track_list(video)
output_track_list = get_track_list(output_video)

v1 = track_list[0]
output_v1 = output_track_list[0]

clip_list = v1.findall('clipitem')
output_clip_list = output_v1.findall('generatoritem')

with open(filename_txt, 'w') as txt_output:
    title_list = []
    for number, clip in enumerate(clip_list):
        filter_list = clip.findall('filter')
        value = ""
        line = 1
        for filter in filter_list:
            if line > 1:
                value += '\n'
            effect = filter.find('effect')
            if effect.find('name').text == None:
                print('Title ' + str(number) + ' failed - No value')
                continue
            else:
                value += effect.find('name').text
                line += 1

        print('Title ' + str(number) + ': ')
        print(value.replace('\r','\n'))
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
    input('Continue?')
    title_list = title_list[1:]
    print(output_clip_list)
    for number, clip in enumerate(output_clip_list): # Remove extra items from XML REF
        if number >= len(title_list) or number >= len(clip_list):
            output_v1.remove(clip)
            continue
            break
        print(number)
        print(clip)
        effect = clip.find('effect')
        parameter = effect.find('parameter')
        value = parameter.find('value').text
        source = clip_list[number]
        start = source.find('start').text
        end = source.find('end').text
        clip.find('start').text = start
        clip.find('end').text = end
        for loop_parameter in effect.findall('parameter'):
            if loop_parameter.find('parameterid').text == 'fontsize':
                loop_parameter.find('value').text = '32' #Value for ECHO - change if necessary
                print('changed font size')
            if loop_parameter.find('parameterid').text == 'origin':
                origin_value = loop_parameter.find('value')
                origin_value.find('vert').text = '0.410000' #Value for ECHO - change if necessary
                print('changed title origin')
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
            print(parameter.find('value'))
        except Exception:
            print('Title failed')
            print(clip)

#Change name
output_sequence.find('name').text = 'REF_' + filename[6:]

output_tree.write(filename_xml, encoding = 'UTF-8', xml_declaration = True)

# correcting bad line break formatting
filedata = None
with open(filename_xml, 'r') as file :
  filedata = file.read()

filedata = filedata.replace('BRK_LN', '&#13;')

with open(filename_xml, 'w') as file:
  file.write(filedata)

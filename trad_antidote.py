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

v1 = root[0][8][0][1]

v2 = root[0][8][0][2]

v1_content = [clip for clip in v1]

clips_v1 = v1_content[:-2]

with open(filename_txt, 'w') as txt_output:
    title_list = []
    for clip in clips_v1:
        try:
            value = clip[14][5][2].text
        except IndexError:
            value = clip[13][5][2].text
        if value == None:
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
    for clip in enumerate(clips_v1):
        print(clip[0])
        print(clip[1])
        try:
            clip[1][14][5][2].text = title_list[clip[0]].replace('\n', 'BRK_LN')
        except IndexError:
            clip[1][13][5][2].text = title_list[clip[0]].replace('\n', 'BRK_LN')

tree.write(filename_xml, encoding = 'UTF-8', xml_declaration = True)


# correcting bad line break formatting
filedata = None
with open(filename_xml, 'r') as file :
  filedata = file.read()

filedata = filedata.replace('BRK_LN', '&#13;')

with open(filename_xml, 'w') as file:
  file.write(filedata)

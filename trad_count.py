"""
Counts the number of title lines in a FCP7 XML file.

Usage: python3 linecount_fcp_xml.py input/XMLNAME output/TXTNAME

"""
import xml.etree.ElementTree as etree
import sys
import tc_calc

filename = sys.argv[2]

input = sys.argv[1]

filename_txt = filename + '_count.txt'

tree = etree.parse(input)

root = tree.getroot()

v1 = root[0][8][0][1]

#v2 = root[0][8][0][2]

v1_content = [clip for clip in v1]

clips_v1 = v1_content[:-2]

with open(filename_txt, 'w') as txt_output:
    title_list = []
    count = 0
    for clip in clips_v1:
        count += 1
        try:
            value = clip[14][5][2].text
        except IndexError:
            value = clip[13][5][2].text
        text = str(count) + ": "
        letter_count = 0
        if value == None:
            continue
        for letter in value:
            if letter in ['\n','\r','\n\r','\r\n']:
                if letter_count is 0:
                    letter_count +=1
                else:
                    text += letter
                    letter_count +=1
                    count += 1
                    text += str(count) + ": "
            else:
                text += letter
                letter_count += 1
        title_list.append(text)    
        letter_count = 0
    for title in title_list:
        txt_output.write(title)
        txt_output.write('\n')

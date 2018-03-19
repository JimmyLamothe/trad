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
    line_list = []
    for clip in clips_v1:
        try:
            value = clip[14][5][2].text
        except IndexError:
            value = clip[13][5][2].text
        letter_count = 0
        if value == None:
            continue
        line = ""
        for letter in value:
            if letter in ['\n','\r','\n\r','\r\n']:
                line += letter
                letter_count +=1
                line_list.append(line)
                line = ""
            else:
                line += letter
                letter_count += 1
        letter_count = 0

    count = 0
    for line in line_list:
        if len(line) > 1:
            count += 1
            num_line = str(count) + ': ' + line 
            txt_output.write(num_line)
            txt_output.write('\n')
        else:
            print(len(line))
            print(len(line) > 1)



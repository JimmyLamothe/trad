"""
Convertit un XML FCP7 en .txt convertible en tableau dans Word avec Time Codes
et identifications de personnages. Prend deux pistes vidéo.

Modifier le nom du personnage de la V1 dans le programme directement.

Prend trois arguments: input/NOMDUXML -  output/NOMDUTXT - TC
"""

import xml.etree.ElementTree as etree
import sys
import tc_calc

print('Ne pas oublier de vérifier que le TC est bon avant de travailler sur le document Word.\n')

filename = sys.argv[2]

input_file = sys.argv[1]

intervenants = True

tc = "0"

try:
    tc = int(sys.argv[3])
except IndexError:
    print("Don't forget to enter Time Code (24 or 30)")
    sys.exit(0)
"""
if(len(sys.argv) == 5):
    with open(sys.argv[4], 'r') as liste_intervenants:
        for intervenant in liste_intervenants:
            intervenants.append(intervenant)

text_only = False
if(len(sys.argv) > 3):
    if(sys.argv[3] == "text_only"):
        text_only = True
    elif(int(sys.argv[3]) > 0):
        tc = int(sys.argv[3])
"""
final = False

filename_txt = filename + '.txt'

tree = etree.parse(input_file)

root = tree.getroot()

v1 = root[0][8][0][1]

v2 = root[0][8][0][2]

v1_content = [clip for clip in v1]

clips_v1 = v1_content[:-2]

if(intervenants):
    v2_content = [clip for clip in v2]
    clips_v2 = v2_content[:-2]




if(intervenants):
    with open(filename_txt, 'w') as txt_output:
        clip_list = []
        name = input("Entrez le nom du personnage principal\n")
        number = "ST-1"
        for clip in clips_v1:
            start = int(clip[5].text)
            end = int(clip[6].text)
            try:
                value = clip[14][5][2].text
            except IndexError:
                value = clip[13][5][2].text
            text = ""
            previous_letter = ""
            letter_count = 0
            for letter in value:
                if letter in ['\n','\r','\n\r','\r\n']:
                    if letter_count == 0:
                        pass
                    else:
                        text += " "
                elif letter == "-" and letter_count in [0,1,2]:
                    pass
                elif previous_letter == "-" and letter_count in [1,2,3]:
                    pass
                else:
                    text += letter
                previous_letter = letter
                letter_count += 1
            clip_list.append((start, end, number, name, text))
        name = "Nom"
        number = "1"
        for clip in clips_v2:
            start = int(clip[5].text)
            end = int(clip[6].text)
            value = clip[14][5][2].text
            text = ""
            previous_letter = ""
            letter_count = 0
            for letter in value:
                if letter in ['\n','\r','\n\r','\r\n']:
                    if letter_count == 0:
                        pass
                    else: 
                        text += " "
                elif letter == "-" and letter_count in [0,1,2]:
                    pass
                elif previous_letter == "-" and letter_count in [1,2,3]:
                    pass
                else:
                    text += letter
                previous_letter = letter
                letter_count += 1
            clip_list.append((start, end, number, name, text))
        sorted_clip_list = sorted(clip_list, key = lambda clip: clip[0])
        #short_clip_list serves to combine subtitles when the same person is talking for a long time.
        short_clip_list = []
        current_start = 0
        current_end = 0
        current_number = "0"
        current_name = ""
        current_text = ""
        for clip in sorted_clip_list:
            if clip[0] -  current_end > 60 or clip[3] != current_name:
                short_clip_list.append((current_start, current_end, current_number,
                                        current_name, current_text))
                current_start = clip[0]
                current_text=""
            current_end = clip[1]
            current_number = clip[2]
            current_name = clip[3]
            if current_text:
                current_text += " "
            current_text += clip[4]
        #To catch last title
        if current_text:
            short_clip_list.append((current_start, current_end, current_number,
                                        current_name, current_text))
        for clip in sorted_clip_list:
            duration = clip[1] - clip[0]
            tc_in = tc_calc.tc_calc(clip[0], hour = 10, tc = tc)
            tc_out = tc_calc.tc_calc(clip[1], hour = 10, tc = tc)
            txt_output.write(tc_in)
            txt_output.write(';')
            txt_output.write(clip[2])
            txt_output.write(';')
            txt_output.write(clip[3])
            txt_output.write(';')
            if value[0] in ['\n','\r','\r\n']:
                txt_output.write(clip[4])
                txt_output.write('\n')
            else:
                txt_output.write(clip[4])
                txt_output.write('\n')

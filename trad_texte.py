"""
Convertit un XML FCP7 en .txt convertible en .txt pour Antidote.

Toujours utiliser text_only pour avoir uniquement le texte. Utiliser
parse_fcp_xml_doublage.py pour obtenir le tableau final pour Océan.

Prend trois arguments: input/NOMDUXML output/NOMDUTXT text_only.
"""


import xml.etree.ElementTree as etree
import sys
import tc_calc

filename = sys.argv[2]

input = sys.argv[1]

intervenants = []

tc = 30

if(len(sys.argv) == 5):
    with open(sys.argv[4], 'r') as liste_intervenants:
        for intervenant in liste_intervenants:
            intervenants.append(intervenant)

text_only = True #Changed default to text_only - modify loop below to change behavior
"""
if(len(sys.argv) > 3):
    if(sys.argv[3] == "text_only"):
        text_only = True
    elif(int(sys.argv[3]) > 0):
        tc = int(sys.argv[3])
"""

final = False

filename_txt = filename + '.txt'

tree = etree.parse(input)

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
        for clip in clips_v1:
            start = int(clip[5].text)
            end = int(clip[6].text)
            value = clip[14][5][2].text
            name = "nom"
            number = "1"
            text = ""
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
        for clip in clips_v2:
            start = int(clip[5].text)
            end = int(clip[6].text)
            value = clip[14][5][2].text
            name = "Jean-Luc"
            number = "St-1"
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
            
        for clip in short_clip_list[1:]:
            duration = clip[1] - clip[0]
            tc_in = tc_calc.tc_calc(clip[0], hour = 10)
            tc_out = tc_calc.tc_calc(clip[1], hour = 10)
            if duration < 150:
                txt_output.write(tc_in)
            else:
                txt_output.write(tc_in + " À " + tc_out)
            txt_output.write(';')
            txt_output.write(clip[2])
            txt_output.write(';')
            txt_output.write(clip[3])
            txt_output.write(';')
            if value[0] in ['\n','\r','\r\n']:
                txt_output.write(clip[4][1:])
                txt_output.write('\n')
            else:
                txt_output.write(clip[4])
                txt_output.write('\n')

elif (text_only):
    with open(filename_txt, 'w') as txt_output:
        title_list = []
        for clip in clips_v1:
            try:
                value = clip[14][5][2].text
            except IndexError:
                value = clip[13][5][2].text
            text = ""
            count = 0
            if value == None:
                continue
            for letter in value:
                if letter in ['\n','\r','\n\r','\r\n']:
                    text += " "
                    text += letter
                    count +=1
                else:
                    text += letter
                    count += 1
            title_list.append(text)    
            count = 0
        for title in title_list:
            txt_output.write(title)
            txt_output.write('\n')

else:
    with open(filename_txt, 'w') as txt_output:
        clip_list = []
        for clip in clips_v1:
            start = int(clip[5].text)
            end = int(clip[6].text)
            try:
                value = clip[14][5][2].text
            except IndexError:
                value = clip[13][5][2].text
            text = ""
            count = 0
            for letter in value:
                if letter in ['\n','\r','\n\r','\r\n']:
                    if count == 0:
                        count += 1
                    else:
                        text += " "
                        text += letter
                        count +=1
                else:
                    text += letter
                    count += 1
            clip_list.append((start, end, text))    
            count = 0
        for clip in clip_list:
            duration = clip[1] - clip[0]
            tc_in = tc_calc.tc_calc(clip[0], hour = 10, tc = tc)
            tc_out = tc_calc.tc_calc(clip[1], hour = 10, tc = tc)
            txt_output.write(tc_in + " - " + tc_out)
            txt_output.write(';')
            txt_output.write(clip[2])
            txt_output.write('\n')

# Append ; before every second line.
    temp_output = []
    with open(filename_txt, 'r') as test_output:
        for line in test_output:
            temp_output.append(line)
        
    with open(filename + '_temp.txt', 'w') as test_output:
        for line in temp_output:
            if line[0] not in ['0','1']:
                test_output.write(';')
            test_output.write(line)










                
"""
else:
    with open(filename_final, 'w') as final_output:
        with open(filename_txt, 'r') as input:
            lines = input.readlines()
            part1 = ""
            part2 = ""
            titre = ""
            start = ""
            dernier_end = ""
            premier_start = ""
            end = ""
            num_intervenant = ""
            dernier_num_intervenant = ""
            intervenant = ""
            def_num_intervenant = False;
            def_intervenant = False;
            narrateur = False;
            write = False;
            linecount = 0
            count = 0
            diff_tc = 0
            for line in lines:
                if line[4] != ';':
                    part2 = line[:-1] + " "
                    titre += part2
                else:
                    start = line[0:4]
                    end = line[5:9]
                    if not premier_start:
                        premier_start = start
                    if dernier_end:
                        diff_tc = int(start) - int(dernier_end)
                    if diff_tc > 90:
                        write = True
                        premier_start = ""
                    dernier_end = end
                    num_intervenant = line[10]
                    if int(num_intervenant):
                        write = True
                        if num_intervenant == "9":
                            narrateur = True;
                            count = 15
                        else:
                            narrateur = False;
                            dernier_num_intervenant = num_intervenant
                            count = 12
                            intervenant = ""
                            for letter in line[12:]:
                                if letter != ';':
                                    intervenant += letter
                                    count += 1
                                else:
                                    count += 1
                                    break
                    else:
                        count = 17
                    for letter in line[count:]:
                        if letter in ['\n','\r','\n\r','\r\n']:
                            part1 += " "
                        else:
                            part1 += letter
                    titre += part1
                    if write:
                        final_output.write("LINE - " + str(linecount))
                        final_output.write('\n')
                        final_output.write("START: " + start)
                        final_output.write('\n')
                        final_output.write("PREMIER_START: " + premier_start)
                        final_output.write('\n')
                        final_output.write("END: "+ end)
                        final_output.write('\n')
                        final_output.write("DERNIER_END: " + dernier_end)
                        final_output.write('\n')
                        final_output.write("DIFF_TC: " + str(diff_tc))
                        final_output.write('\n')                
                        final_output.write("NUM_INTERVENANT: " + num_intervenant)
                        final_output.write('\n')
                        final_output.write("DERNIER_NUM: " + dernier_num_intervenant)
                        final_output.write('\n')
                        final_output.write("INTERVENANT: " + intervenant)
                        final_output.write('\n')
                        final_output.write("TITRE: " + titre)
                        final_output.write('\n')
                        final_output.write("PART1: " + part1)
                        final_output.write('\n')
                        final_output.write("PART2: " + part2)
                        final_output.write('\n')
                        final_output.write("NARRATEUR: " + str(narrateur))
                        final_output.write('\n')
                        final_output.write("WRITE: " + str(write))
                        final_output.write('\n')
                        final_output.write('OUTPUT STARTS:')
                        final_output.write('\n')
                        final_output.write(premier_start)
                        final_output.write(';')
                        final_output.write(end)
                        final_output.write(';')
                        if narrateur:
                            final_output.write('ST')
                            final_output.write(';')
                        else:
                            final_output.write(dernier_num_intervenant)
                            final_output.write(';')
                        if narrateur:
                            final_output.write('Jean-Luc')
                            final_output.write(';')
                        else:
                            write = False;
                            final_output.write(intervenant)
                            final_output.write(';')
                        titre_count = 0
                        for letter in titre:
                            if letter == " ":
                                if titre_count > 40:
                                    final_output.write('\n')
                                    titre_count = 0
                                else:
                                    final_output.write(' ')
                            else:
                                final_output.write(letter)
                                titre_count += 1
                        final_output.write('\n')
                        part1 = ""
                        part2 = ""
                        titre = ""
                    else:
                        final_output.write("LINE - " + str(linecount))
                        final_output.write('\n')
                        final_output.write("START: " + start)
                        final_output.write('\n')
                        final_output.write("PREMIER_START: " + premier_start)
                        final_output.write('\n')
                        final_output.write("END: "+ end)
                        final_output.write('\n')
                        final_output.write("DERNIER_END: " + dernier_end)
                        final_output.write('\n')
                        final_output.write("DIFF_TC: " + str(diff_tc))
                        final_output.write('\n')                
                        final_output.write("NUM_INTERVENANT: " + num_intervenant)
                        final_output.write('\n')
                        final_output.write("DERNIER_NUM: " + dernier_num_intervenant)
                        final_output.write('\n')
                        final_output.write("INTERVENANT: " + intervenant)
                        final_output.write('\n')
                        final_output.write("TITRE: " + titre)
                        final_output.write('\n')
                        final_output.write("PART1: " + part1)
                        final_output.write('\n')
                        final_output.write("PART2: " + part2)
                        final_output.write('\n')
                        final_output.write("NARRATEUR: " + str(narrateur))
                        final_output.write('\n')
                        final_output.write("WRITE: " + str(write))
                        final_output.write('\n')
                        final_output.write('OUTPUT STARTS:')
                        final_output.write('\n')
                        part1 = ""
                        part2 = ""
                linecount +=1                    
"""
                

"""
with open(filename_txt, 'w') as txt_output:
    for clip in clips_v1:
        start = clip[5].text
        end = clip[6].text
        value = clip[14][5][2].text
        txt_output.write(start)
        txt_output.write('\n')
        txt_output.write(end)
        txt_output.write('\n')
        if value[0] in ['\n','\r','\r\n']:
            txt_output.write(value[1:])
        else:
            txt_output.write(value)
        txt_output.write('\n')

with open(filename_csv, 'w') as csv_output:
    for clip in clips_v1:
        start = clip[5].text
        end = clip[6].text
        value = clip[14][5][2].text
        csv_output.write('"')
        csv_output.write(start)
        csv_output.write('"')
        csv_output.write(';')
        csv_output.write('"')
        csv_output.write(end)
        csv_output.write('"')
        csv_output.write(';')
        if value[0] in ['\n','\r','\r\n']:
            csv_output.write('"')
            csv_output.write(value[1:])
            csv_output.write('"')
        else:
            csv_output.write('"')
            csv_output.write(value)
            csv_output.write('"')
        csv_output.write('\n')

with open(filename_start, 'w') as start_output:
    start_output.write('start')
    start_output.write('\n')
    for clip in clips_v1:
        start = clip[5].text
        start_output.write(start)
        start_output.write('\n')

with open(filename_end, 'w') as end_output:
    end_output.write('end')
    end_output.write('\n')
    for clip in clips_v1:
        end = clip[6].text
        end_output.write(end)
        end_output.write('\n')

with open(filename_value, 'w') as value_output:
    value_output.write('value')
    value_output.write('\n')
    for clip in clips_v1:
        value = clip[14][5][2].text
        if value[0] in ['\n','\r','\r\n']:
            value = value[1:]
        for letter in value:
            if letter in ['\n','\r','\r\n']:
                value_output.write(' ')
            else:
                value_output.write(letter)
        value_output.write('\n')
"""

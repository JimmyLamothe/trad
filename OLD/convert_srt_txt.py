import sys

input_file = sys.argv[1]

output_file = input_file[:-4] + '.txt'

with open(input_file, 'r') as input_srt:
    with open(output_file, 'w') as output_txt:
        count = 0
        for line in input_srt:
            count += 1
            if count in [1,2]:
                pass
            elif len(line) < 2:
                count = 0
                pass
            else:
                output_txt.write(line)

from os import wait

PATTERN_LENGTH = 96
#PATTERN_LENGTH = 72

def main():
    path = 'test.s'
    prefix = 'not_yet_calculated'
    input_lines = open(path).readlines()
    output_lines = []

    current_time = 0
    in_track = False

    for line in input_lines:

        if in_track == False and 'voicegroup' in line:
            prefix = line.strip().split()[1][0:-5]

        if line.startswith('@'):
            output_lines.append(line)
            # comment
            continue

        wait_time = 0

        if line.strip().startswith('.byte'):
            # interesting data
            first_component = line.strip().split('\t')[1]
            if first_component.startswith('W'):
                wait_time = int(first_component[1:])
                print(current_time)
            elif first_component == 'PATT':
                wait_time+= PATTERN_LENGTH

        if line.startswith(prefix + '_'):
            
            if line.count('_') != prefix.count('_') + 1:
                output_lines.append(line)
                continue
            # Next track label
            current_time = 0
            in_track = True
            output_lines.append(line)
            continue

        if line.startswith(prefix + ':'):
            in_track = False # Start of header

        if in_track and line.strip() != '':
            output_lines.append(str(current_time).rjust(5) + ' ' + line)
        else:
            output_lines.append(line)
        current_time += wait_time

    open('test.anno.s', 'w').writelines(output_lines)

if __name__ == '__main__':
    main()
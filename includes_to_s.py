from common import TMC_FOLDER
from os import path
import re
import os
import io
FOLDER = "data"
PREFIX = "data_"
# CURRENT = '080CC6FC.s' # TODO
CURRENT = '080D1C70.s'
SECTION = ".rodata"
ASM_FILE = path.join(TMC_FOLDER, FOLDER, PREFIX+CURRENT)
CODE_ASM_FILE_START = f'''	.include "asm/macros.inc"

	.include "constants/constants.inc"

	.syntax unified

	.text

'''
ASM_FILE_START = f'''	.include "asm/macros.inc"
	.include "constants/constants.inc"

	.section .rodata
    .align 2

'''

linker_info = []


def write_file(path, output):
    if path is None:
        raise Exception('Cannot write to file None')
    print(f'Write {len(output)} lines to {path}')
    with io.open(path, 'w', newline='\n') as file:
        file.writelines(output)


def convert_to_s(path):
    print(f'Converting {path}')
    lines = []
    with open(path, 'r') as file:
        lines = file.readlines()

    lines.insert(0, ASM_FILE_START)

    new_path = path.replace('.inc', '.s')
    with io.open(new_path, 'w', newline='\n') as file:
        file.writelines(lines)
    os.remove(path)
    add_linker_info(new_path)


def add_linker_info(path):
    global linker_info
    o_path = path[len(TMC_FOLDER)+1:-2].replace("\\", "/") + '.o'
    linker_info.append(f'        {o_path}({SECTION});')


def main():
    asm_code = []
    with open(ASM_FILE, 'r') as file:
        asm_code = file.readlines()

    current_output = []
    current_file = ASM_FILE
    in_code = True

    for line in asm_code:
        if '.include' in line:
            if '"asm/macros.inc"' in line or '"constants/constants.inc' in line:
                current_output.append(line)
                continue

            if in_code:
                if current_file is None:
                    raise Exception(
                        'Current file is still none for lines:\n'+''.join(current_output))
                add_linker_info(current_file)
                in_code = False
            matches = re.search('\.include \"(.*)\"', line)
            if not matches:
                raise Exception(f'.include in line "{line}" not understood')
            convert_to_s(path.join(TMC_FOLDER, matches.groups(1)[0]))
        else:
            if not in_code:
                if line == '\n':  # There are empty lines between multiple .includes
                    continue

                # Previous file ended
                write_file(current_file, current_output)
                current_file = None
                current_output = [ASM_FILE_START]
                #print('NEW FILE')
                in_code = True

            if current_file is None:  # Current file has no name yet, name it after the first
                if '@' in line:
                    arr = line.split('@')
                    if arr[0].strip().endswith(':'):
                        # print(arr)
                        current_file = path.join(TMC_FOLDER,
                                                 FOLDER, PREFIX + arr[1].strip().upper().replace('0X', '')+'.s')
            current_output.append(line)

    if in_code:
        add_linker_info(current_file)
        # Write rest TODO check not empty
        write_file(current_file, current_output)
#    print(asm_code)

    print('Fix in linker.ld:')
    print('\n'.join(linker_info))


if __name__ == '__main__':
    main()

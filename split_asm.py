# Split asm .s file into non_matching .inc files and output corresponding c file with ASM_FUNC macros
from posix import POSIX_FADV_NOREUSE
import sys
from typing import List
from common import TMC_FOLDER
import os
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Func:
    name: str
    lines: List[str]

def parse_file(filepath: str) -> List[Func]:

    result = []

    with open(filepath, 'r') as f:
        current_function = None
        current_lines = []

        for line in f:
            if 'thumb_func_start' in line:
                if current_function is not None:
                    result.append(Func(current_function, current_lines))
                    current_lines = []
            
                current_function = line.split()[1]
            elif current_function is not None and line.strip() != '':
                current_lines.append(line)

        if current_function is not None:
            result.append(Func(current_function, current_lines))
    return result

def main():
    if len(sys.argv) != 2:
        print('usage: split_asm.py ASM_FILE_NAME')
        return
    
    filepath = os.path.join(TMC_FOLDER, sys.argv[1])
    if not os.path.isfile(filepath):
        print(f'Could not find file: {filepath}')
        return

    filename = os.path.split(filepath)[1]
    foldername = filename[:-2]
    non_matching_folder = os.path.join('asm', 'non_matching', foldername)
    non_matching_path = os.path.join(TMC_FOLDER, non_matching_folder)

    funcs = parse_file(filepath)

    print('Found functions:')
    for func in funcs:
        print(f'{func.name}: {len(func.lines)} lines')

    print(f'File: {filepath}')
    print(f'Output folder: {non_matching_path}')

    while True:
        print('Execute? y/n')
        input_line = input()
        if input_line == 'n':
            return
        if input_line == 'y':
            break
        print(f'Unknown input: {input_line}')


    Path(non_matching_path).mkdir(parents=True, exist_ok=True)

    print('\n\n#include "entity.h"\n')
    for func in funcs:
        funcpath = os.path.join(non_matching_folder, func.name+'.inc')
        with open(os.path.join(TMC_FOLDER, funcpath), 'w') as f:
            f.write('\t.syntax unified\n')
            f.writelines(func.lines)
            f.write('\t.syntax divided\n')

        print(f'ASM_FUNC("{funcpath}", void {func.name}(Entity* this))\n')


if __name__ == '__main__':
    main()

import os
from mass_rename import rename_all
from common import TMC_FOLDER
import pyperclip

def to_file(name: str) -> str:
    return name[0].lower() + name[1:]

def to_constant(name: str) -> str:
    result = ''
    index = 0
    last_char_digit = False
    for char in name:
        if index > 0 and (char.isupper() or (not last_char_digit and char.isdigit())):
            result += '_' + char
        else:
            result += char.upper()
        index += 1
        last_char_digit = char.isdigit()
    return result

def to_docs(name: str) -> str:
    result = ''
    index = 0
    last_char_digit = False
    for char in name:
        if index > 0 and (char.isupper()):
            result += ' ' + char
        else:
            result += char
        index += 1
        last_char_digit = char.isdigit()
    return result

def rename_file(old_path: str, new_path: str):
    if os.path.exists(old_path):
        os.rename(old_path, new_path)

while True:
    print('Old name: ', end='')
    old_name = input()
    print('New name: ', end='')
    new_name = input()

    if len(new_name) == 0:
        continue

    new_file = to_file(new_name)
    new_constant = to_constant(new_name)
    if len(old_name) > 0:
        old_file = to_file(old_name)
        old_constant = to_constant(old_name)
        print('Really rename? y/n')
        answer = input()
        if answer.strip() == 'y':
            renames = [
                (old_name, new_name),
                (old_file, new_file),
                (old_constant, new_constant)
            ]
            rename_all(renames)
            rename_file(f'{TMC_FOLDER}/src/object/{old_file}.c', f'{TMC_FOLDER}/src/object/{new_file}.c')
            rename_file(f'{TMC_FOLDER}/data/animations/object/{old_file}.s', f'{TMC_FOLDER}/data/animations/object/{new_file}.s')
            rename_file(f'{TMC_FOLDER}/data/const/object/{old_file}.s', f'{TMC_FOLDER}/data/const/object/{new_file}.s')
            rename_file(f'{TMC_FOLDER}/asm/non_matching/{old_file}', f'{TMC_FOLDER}/asm/non_matching/{new_file}')

    header = f'''/**
 * @file {new_file}.c
 * @ingroup Objects
 *
 * @brief {to_docs(new_name)} object
 */'''
    pyperclip.copy(header)
    print('Pasted header to clipboard.')
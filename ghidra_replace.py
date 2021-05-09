import os
import pyperclip
from dataclasses import dataclass
import re
import subprocess
from common import TMC_FOLDER

@dataclass
class Replacement:
    source: str
    replacement: str
    dotall: bool

replacements: list[Replacement] = []


def add_replacement(source: str, replacement: str) -> None:
    global replacements
    replacements.append(Replacement(source, replacement, False))

def add_dotall_replacement(source: str, replacement: str) -> None:
    global replacements
    replacements.append(Replacement(source, replacement, True))


def clang_format(input: str) -> None:

    # Format input
    TMP_FILE = 'tmp/ghidra_code.c'
    FORMAT_FILE = 'tmp/.clang-format'

    with open(TMP_FILE, 'w') as f:
        f.write(input)

    if not os.path.isfile(FORMAT_FILE):
        # Need to copy the .clang-format file due to https://stackoverflow.com/a/46374122
        subprocess.call(['cp', os.path.join(TMC_FOLDER, '.clang-format'), FORMAT_FILE])

    subprocess.call(['clang-format', '--style=file', '-i', TMP_FILE])

    with open(TMP_FILE, 'r') as f:
        input = f.read()
    return input

# Use https://regex101.com/ to build the regular expressions

# Data types
add_replacement(r'byte', 'u8')
add_replacement(r'char', 'u8')
add_replacement(r'ushort', 'u16')
add_replacement(r'short', 's16')
add_replacement(r'uint', 'u32')
add_replacement(r'int([ _\)])', r's32\1')
add_replacement(r'undefined2', 'u16')
add_replacement(r'undefined4', 'u32')

# Word
add_replacement(r'\(int\)\*\(short \*\)\(\(int\)&(\S*) \+ 2\)', r'\1.HALF.HI')
add_replacement(r'\*\([u,s]16\*\)\&this->(\S*)', r'this->\1.HALF.LO')
add_replacement(r'(?:\(s32\))?\* ?\([s,u]16\* ?\)\(\(s32\) ?& ?this->(\S*) \+ 2\)', r'this->\1.HALF.HI')
add_replacement(r'\._2_2_', r'.HALF.HI')

# Half Word
add_replacement(r'\*\(u8\*\)&this->(\S*)', r'this->\1.HALF.LO')
add_replacement(r'\(u8\*\)\(\(s32\)&(\S*) \+ 1\)', r'\1.HALF.HI')
add_replacement(r'\(s32\)\(u32\)\(u16\)([\w\->]*)', r'\1.HWORD')
add_replacement(r'\(s32\)\(u32\) \* \(u16\*\)&([\w\->]*)', r'\1.HALF.LO')

# Formatting issues
add_replacement(r'\)\n\n{', ') {')

# Remove the last empty return
add_replacement(r'    return;\n}', r'}')

# Insert notes that these are probably macros
add_dotall_replacement(r'(- .* >> 4 & 0x3fU \|.* >> 4 & 0x3fU.*<< 6[^\n]*)', r'\1 // TODO look at TILE macro')

# 
add_replacement(r'gPlayerState\.flags ', 'gPlayerState.flags.all ')
add_replacement(r'this->frames ', 'this->frames.all ')

# Weird structs and unions
add_replacement(r'this->spriteSettings = this->spriteSettings & 0xfc \| 2;', r'this->spriteSettings.b.draw = 2;')
add_replacement(r'this->spriteSettings = this->spriteSettings & 0xfc \| 1;', r'this->spriteSettings.b.draw = 1;')


add_replacement(r'\((\w*)\*\)0x0', r'NULL')
add_replacement(r'__divsi3\(([^,]*), ([^\)]*)\)', r'\1 / \2')
add_replacement(r'__modsi3\(([^,]*), ([^\)]*)\)', r'\1 % \2')



"""
TODO
 (-uVar1 | uVar1) >> 0x1f;  <- BOOLCAST(uVar1)
"""

input = pyperclip.paste()
input = clang_format(input)

# Do replacements
for replacement in replacements:
    flags = re.MULTILINE
    if replacement.dotall:
        flags |= re.DOTALL
    input = re.sub(replacement.source, replacement.replacement, input, flags=flags)

# input = clang_format(input)
pyperclip.copy(input)
print(input)

print('DONE')
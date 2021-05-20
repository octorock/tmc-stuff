import re
from typing import Optional
import lzstring
import prison
from urllib.parse import quote_plus
import sys
import os
from common import TMC_FOLDER
import pyperclip

CEXPLORE_URL='http://cexplore.henny022.de/#'

def rison_quote(text: str) -> str:
    return quote_plus(text).replace('%2C', ',').replace('%3A', ':').replace('%40', '@').replace('%24', '$').replace('%2F', '/').replace('%20', '+')

def risonify(data) -> str:
    return rison_quote(prison.dumps(data)[1:-1])

def generate_cexplore_url(src: str, asm: str) -> str:
    # Base state url
    state = 'OYLghAFBqd5QCxAYwPYBMCmBRdBLAF1QCcAaPECAM1QDsCBlZAQwBtMQBGAZlICsupVs1qgA+hOSkAzpnbICeOpUy10AYVSsArgFtaIAEwAGUqvQAZPLUwA5PQCNMxEADZSAB1TTCS2pp19I1MvH0U6Kxt7XScXd1l5cNoGAmZiAgC9AxMZOUwFPxS0gki7R2c3GVT0zKCc6WqS6zKYitcAShlUbWJkDgByAFJDbmtkHSwAamHDVUUCAE8AOgQZweMAQWHR2nHtKZmqbV2k6RW1ze2xicxpw0MPYQXnc/v1rZHr/duZ6WRiPAeAivQzvd4AenBkw26HQk3UkzQUwQzlu/U6rBA/QArP1SAZ+sY8agsQjpN1ej8Rpw8QQsUTOhAkGhdB48OwyBQICy2RyQARdMgxMxgA5kFIqOyCM5pJQHPS8Q5rGkFliaaQWbo5gB5WisVWEvFYXQiYDsBWkfDEfKKABumFlhrMAA98tppWq8dZpZinaw8A5iCrNFhPaQCADdJ7OjR6Ew2BxOAAWfiCYSiEASMRSf0OWWQTqoIF+R14hI2vwqNS1AycMxqUrRWKCUK+Og1lveNu0RvlFx18sFOhFGpaLKCQdJEdNKJ9ieNDsDxq91r9zrknp9LgYrG4/EWkn9AVCkVi5CTCC4QgkO7cOvw1Cs9nOW+cdrw2kK9qdADWIG4xhLJwrjcNwAAchggUmADsJjYtiQhYkmeJRpwximASRKkIeZYgKYdKGoyMBQMRTIgPgVBUOQlCxowLDmpwdasAgspMSxFFUIsHgcKYxAsUYpB8dIHFcTxO44nimHEliAAieCUZMx7CqK4qTLa0iIswBCfoRnQoswWAuBAv4gEm3BLDB3BmcYrjQQAnA5xhgUxSEoSA0HQUs3DQQBrhgWZkHQWhYH7k6OEyHh4ZfqQcCwEg3QEB47rUdyj68hUdaYPgRD9qQtHxgxdYAO5Bh40aIRJoVYYe2ycJMRWEAgimCspZ46QyemYAZFTGRVyGkFG9xLK4kF2Xe2K2dwhhgXZhgplJ2FYrh+FfiZSbYksM1JjwjHbR5SbGAhvrcJJB5LVFhExaRzIYDg2UkCl+X0YmvACIYQimiAzDSLIMT6rkiSVhA5gdoYCHmCuzZ1q2SSgwhMN+JDGUAxWw4LmOdQIZOhTLs0TbIw0xRw1UxRI2uXSbgMAAC0KwpM32/Q4+qIrdkwota6IVXuC2HhsP2YH9CyTBulK3oY7Wc2RPLPpylDS3yHgLCwBB5VKMpyhaSq0CqYaajqeoGlhxqmuaTpWhW9qOlhmCusg7oDOq3pyBauZBsQCwhgMWERngUb9DSMZ0HRCZcCmb0fRmDMC0zCxCAG+a9UWpzndjyjA9WGO1vWlh43O0NdrDmedmEiO56uE55EOyTo4EWep9XpNl1DJOjrX86N7O5dvhTlJGOJ3Nnf0ysXleOVi6QD5PhyYvvnzjP6hL36kH+IxLHZSZzWBI0jNih3bX1p1hSnkUER1FXi1V0n9IvnT2sQPjKEmQA'

    state = lzstring.LZString().decompressFromBase64(state)
    data = prison.loads('(' + state + ')')


    # Insert our code in the editors
    data['g'][0]['g'][0]['g'][0]['i']['source'] = src
    data['g'][0]['g'][2]['g'][0]['i']['source'] = asm

    state = risonify(data)
    state = {
        'z': lzstring.LZString().compressToBase64(state)
    }
    url = (CEXPLORE_URL+risonify(state))
    return url


def find_inc_file(name: str) -> Optional[str]:
    filename = name + '.inc'
    search_path = os.path.join(TMC_FOLDER, 'asm', 'non_matching')
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)        
    return None

def find_source_file(name: str) -> Optional [str]:
    # Get the source file from tmc.map
    with open(os.path.join(TMC_FOLDER, 'tmc.map'), 'r') as f:
        current_file = None
        for line in f:
            if line.startswith(' .text'):
                current_file = line.split()[3]
            elif line.strip().endswith(name):
                return current_file[0:-2] + '.c'
        return None

def extract_nonmatching_section(inc_path: str, src_file: str) -> Optional[str]:
    with open(src_file, 'r') as f:

        data = []
        headers = []

        in_headers = True
        # match headers
        for line in f:
            if in_headers:
                if '{' in line and not 'struct' in line:
                    in_headers = False
                elif 'NONMATCH' in line or 'ASM_FUNC' in line:
                    in_headers = False
                else:
                    headers.append(line)

            data.append(line)

        # match nonmatching section
        match = re.search(r'NONMATCH\(\"'+inc_path+r'\", ?(.*?)\) ?{(.*?)END_NONMATCH', ''.join(data), re.MULTILINE | re.DOTALL)
        if match:
            return ''.join(headers) + '// end of existing headers\n\n' + match.group(1) + ' {'+ match.group(2)

        match = re.search(r'ASM_FUNC\(\"'+inc_path+r'\", ?(.*?)\)', ''.join(data), re.MULTILINE)
        if match:
            return ''.join(headers) + '// end of existing headers\n\n' + match.group(1) + ') {\n\n}'
    return None

def prepare_asm(inc_file: str, name: str) -> str:
    lines = []
    with open(inc_file, 'r') as f:
        for line in f:
            l = line.strip()
            if l == '' and len(lines) == 0: # ignore empty lines at the beginning
                continue
            if l != '.text' and l != '.syntax unified' and l !='.syntax divided':
                lines.append(line)
    return 'thumb_func_start ' + name + '\n' + (''.join(lines))

def main():
    if len(sys.argv) != 2:
        print('usage: cexport_to_cexplore.py NON_MATCHING_FUN_NAME')
        return
    
    name = sys.argv[1]
    # Find the .inc file for the non matching function
    inc_file = find_inc_file(name)
    if inc_file is None:
        print(f'No {name}.inc found in asm/non_matching folder.')
        return

    src_file = find_source_file(name)
    if src_file is None:
        print(f'Source file for {name} not found in tmc.map.')
        return
    src_file = os.path.join(TMC_FOLDER, src_file)

    if not os.path.isfile(src_file):
        print(f'{src_file} is not a file.')
        return
    
    inc_path = inc_file.replace(TMC_FOLDER + '/', '')

    src = extract_nonmatching_section(inc_path, src_file)
    if src is None:
        print(f'No NONMATCH or ASM_FUNC section found for {inc_path} in {src_file}')
        return

    asm = prepare_asm(inc_file, name)    

    url = generate_cexplore_url(src, asm)
    pyperclip.copy(url)
    print('Copied url to cexplore to clipboard.')

if __name__ == '__main__':
    main()
from common import TMC_FOLDER
import os
import re
from dataclasses import dataclass
import pyperclip
import sys

@dataclass
class Function:
    name: str
    file: str
    line: str

functions = {}

for (root, dirs, files) in os.walk(os.path.join(TMC_FOLDER, 'include')):
    for file in files:
        filepath = os.path.join(root, file)
        print('> ' + filepath)
        with open(filepath) as f:
            for line in f:
                match = re.search('(\w+) (\w*)\(.*\);', line)
                if match is not None:
                    name = match.group(2)
                    functions[name] = Function(name, file, line.strip())
                else:
                    match = re.search('(\w+) (\w*);', line)
                    if match is not None:
                        name = match.group(2)
                        functions[name] = Function(name, file, line.strip())
print(f'{len(functions)} functions found.')

for line in sys.stdin:
    from_clipboard = False
    if line == '\n':
        from_clipboard = True
        line = pyperclip.paste()

    name = line.strip()
    print(f'Searching for {name}')
    if name in functions:
        function = functions[name]
        print(f'Found in {function.file}:')
        print(function.line)
        pyperclip.copy(f'#include "{function.file}"')
    else:
        print('Not found.')
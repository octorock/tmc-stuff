import sys
from colors import Color
from search_symbol import parse_rom_structure, get_structure
import pyperclip

STRUCT_FILE = 'tmp/structure.txt'


# TODO build with symbol granularity as well 
# structure = []

# # parse rom structure
# with open(STRUCT_FILE, 'r') as file:
#     for line in file:
#         arr = line.split(' ')
        
#         structure.append({
#             'start': int(arr[0], 16),
#             'file': arr[1],
#             'section': arr[2].strip(),
#             'in_ptrs': [],
#             'out_ptrs': []
#         })


# # append final structure to avoid need to test for end
# structure.append({
#     'start': 0x08ffffff,
#     'file': 'none',
#     'section': 'none',
#     'in_ptrs': [],
#     'out_ptrs': []
# })

# def get_structure(addr): # TODO could certainly be optimized
#     i = 0
#     while addr >= structure[i+1]['start']:
#         i += 1
#     return structure[i]


# Structure in symbol granularity
structure = parse_rom_structure()

def main():
    print('Enter hex addr of location: ', end='')
    sys.stdout.flush()
    for line in sys.stdin:
        from_clipboard = False
        if line == '\n':
            from_clipboard = True
            line = pyperclip.paste()
        try:
            addr = int(line, 16)
            struct = get_structure(structure, addr)
            print(f'Located {Color.Green}{hex(addr)}{Color.Off}')
            print(f'In symbol: {Color.Purple}{struct["symbol"]}{Color.Off}')
            print(f'In file: {Color.Blue}{struct["file"]} {Color.Off}') # {Color.IBlack}({struct["section"]})
            print(f'With offset: {Color.Yellow}{hex(addr-struct["start"])}{Color.Off}')

            if from_clipboard:
                # Copy filename without .o extension to be easily able to find the file
                pyperclip.copy(struct['file'][:-2])
        except:
            print(f'{Color.Red}Not a valid hex number.{Color.Off}', file=sys.stderr)
        print()
        print('Enter hex addr of location: ', end='')
        sys.stdout.flush()

if __name__ == '__main__':
    main()
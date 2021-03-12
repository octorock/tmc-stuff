import sys
from colors import Color

STRUCT_FILE = 'tmp/structure.txt'


structure = []

# parse rom structure
with open(STRUCT_FILE, 'r') as file:
    for line in file:
        arr = line.split(' ')
        
        structure.append({
            'start': int(arr[0], 16),
            'file': arr[1],
            'section': arr[2].strip(),
            'in_ptrs': [],
            'out_ptrs': []
        })


# append final structure to avoid need to test for end
structure.append({
    'start': 0x08ffffff,
    'file': 'none',
    'section': 'none',
    'in_ptrs': [],
    'out_ptrs': []
})

def get_structure(addr): # TODO could certainly be optimized
    i = 0
    while addr >= structure[i+1]['start']:
        i += 1
    return structure[i]


def main():
    print('Enter hex addr of location:')
    for line in sys.stdin:
        try:
            addr = int(line, 16)
            struct = get_structure(addr)
            print(f'Located {Color.Green}{hex(addr)}{Color.Off}')
            print(f'In file: {Color.Blue}{struct["file"]} {Color.IBlack}({struct["section"]}){Color.Off}')
            print(f'With offset: {Color.Yellow}{hex(addr-struct["start"])}{Color.Off}')
        except:
            print(f'{Color.Red}Not a valid hex number.{Color.Off}', file=sys.stderr)

if __name__ == '__main__':
    main()
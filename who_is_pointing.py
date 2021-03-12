from os import readlink


PTRS_FILE = 'tmp/rom_ptrs_at_locs.txt'
STRUCT_FILE = 'tmp/structure.txt'


structure = []

# parse rom structure
with open(STRUCT_FILE, 'r') as file:
    for line in file:
        arr = line.split(' ')
        
        structure.append({
            'start': int(arr[0], 16),
            'file': arr[1],
            'section': arr[2],
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

current_structure = 0
current_pointers = 0
with open(PTRS_FILE, 'r') as file:
    for line in file:
        arr = line.split('@')
        ptr = int(arr[0],16)
        location = int(arr[1],16)
        while location >= structure[current_structure+1]['start']:
            # print summary
            #print(f'{structure[current_structure]["file"]}: {current_pointers}')
            current_structure += 1
            #current_pointers = 0

        # Outgoing pointer
        structure[current_structure]['out_ptrs'].append(line)

        # Incoming pointer
        get_structure(ptr)['in_ptrs'].append(line)

        #current_pointers += 1

#for file in structure:
#    print(f'{file["file"]}: in({len(file["in_ptrs"])}) out({len(file["out_ptrs"])})')

import json
with open('tmp/pointers.json', 'w') as file:
    json.dump(structure, file)

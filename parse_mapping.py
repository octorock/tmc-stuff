# Parses the mapping from the tmc.map file into an format easier to use for strings:
# <function_name>:<src_file>:location


from os import path
from common import TMC_FOLDER

MAP_FILE_PATH = path.join(TMC_FOLDER, 'tmc.map')

with open(MAP_FILE_PATH, 'r') as map_file:

    # ignore header
    line = map_file.readline()
    while not line.startswith('rom'):
        line = map_file.readline()
    line = map_file.readline()
    while not line.startswith('rom'): # The second line starting with 'rom' is the one we need
        line = map_file.readline()

    # Parse declarations
    current_file = 'UNKNOWN'
    for line in map_file:
        if line.startswith(' .'):
            # ignore this definition of filename
            continue
        elif line.startswith('  '):
            parts = line.split()
            if len(parts) == 2 and parts[1] !='': # it is actually a symbol
                # print(parts[1])
                # print(parts)
                # For bash script TODO adapt the bash script to work with the python versions
                #print(f'{parts[1]}:{current_file}')
                # For python scripts
                print(f'{parts[1]} {current_file} {hex(int(parts[0],16))}')
        elif not line.startswith(' *'):
            # this defines the name
            current_file = line.split('(')[0].strip()


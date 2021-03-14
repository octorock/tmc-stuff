SYMBOLS_FILE = 'tmp/symbols.txt'




def parse_rom_structure():
    structure = []
    # parse rom structure
    with open(SYMBOLS_FILE, 'r') as file:
        for line in file:
            arr = line.split(' ')
            
            structure.append({
                'start': int(arr[2], 16),
                'file': arr[1],
                'symbol': arr[0],
                'in_ptrs': [],
                'out_ptrs': []
            })


    # append final structure to avoid need to test for end
    structure.append({
        'start': 0x08ffffff,
        'file': 'none',
        'symbol': 'none',
        'in_ptrs': [],
        'out_ptrs': []
    })
    return structure



def get_structure(structure, addr): # TODO could certainly be optimized
    #i = 0
    #while addr >= structure[i+1]['start']:
        #i += 1
    #return structure[i]
    return binary_search_iterative(structure, addr)


def binary_search_iterative(array, element): # TODO can this be optimized by earlier detecting that it lies between this and the next one?
    mid = 0
    start = 0
    end = len(array)
    step = 0

    while (start <= end):
        #print("Subarray in step {}: {}".format(step, str(array[start:end+1])))
        step = step+1
        mid = (start + end) // 2

        if element == array[mid]['start']:
            return array[mid]

        if element < array[mid]['start']:
            end = mid - 1
        else:
            start = mid + 1
    return array[end]

#print(get_structure(parse_rom_structure(), 0x0806d8ff))
#print(binary_search_iterative(parse_rom_structure(), 0x0806d8ff))
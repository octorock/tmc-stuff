from common import TMC_FOLDER

ROM_START = 0x08000000
ROM_PREFIX = 0x08
ROM_END = 0x08de7d88 
RAM_PREFIX = 0x03
RAM_END = 0x03007ffa

FILE_PREFIX = 'rom'
PREFIX = ROM_PREFIX
END = ROM_END
def read_baserom():
    # read baserom data
    with open(f'{TMC_FOLDER}/baserom.gba', 'rb') as baserom:
        return bytearray(baserom.read())

def main():

    baserom_data = read_baserom()
    print(len(baserom_data))

    possible_pointers = []

    for i in range(1, len(baserom_data)-3, 2): # TODO is it actually necessary to advance by 2?

        if baserom_data[i] == PREFIX: # rom addr first byte is 0x08

            val = int.from_bytes(baserom_data[i-3:i+1], 'little')
            
            if val < END:
                possible_pointers.append(
                    {'loc': i-3, 'ptr': val}
                )

            

        if i % 16384 == 1:
            print(f'{hex(i)} ptrs: {len(possible_pointers)}')
#    print(possible_pointers)

    with open(f'tmp/{FILE_PREFIX}_ptrs.txt', 'w') as f:
        for ptr in possible_pointers:
            f.write(hex(ptr['ptr'])+'\n')

    with open(f'tmp/{FILE_PREFIX}_ptrs_at_locs.txt', 'w') as f:
        for ptr in possible_pointers:
            f.write(hex(ptr['ptr'])+'@'+hex(ROM_START+ptr['loc'])+'\n')
if __name__ == '__main__':
    main()

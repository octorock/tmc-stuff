from common import read_baserom, bytes_to_u32


ENUM_STARTS = [
    0x812aaec,
    0x812b20c,
    0x812c600,
    0x812e60c,
    0x812f4a4,
    0x812fa3c,
    0x812feac,
    0x8130378,
    0x8130e0c,
    0x81316ac
]

ROM_START = 0x8000000

def read_str(rom, addr):
    res = ''
    while rom[addr] != 0:
        res += chr(rom[addr])
        addr += 1
    return res

def read_enum(baserom_data, ptr):
    while True:
        entry = bytes_to_u32(baserom_data[ptr:ptr+4])
        if entry < ROM_START or entry-ROM_START > len(baserom_data):
            break
        print('  ' + read_str(baserom_data, entry-ROM_START))
        ptr += 4

def main():
    baserom_data = read_baserom()


    for enum in ENUM_STARTS:
        print(f'enum {hex(enum)}:')
        read_enum(baserom_data, enum-ROM_START)
        print()





if __name__ == '__main__':
    main()
from typing import List
from common import TMC_FOLDER
from utils import read_baserom
import subprocess
import os
from search_symbol import parse_rom_structure, get_structure

ROM_START = 0x8000000
rom = read_baserom()
structure = parse_rom_structure()

#start = 0x13AE14
#length = 0x1c8c74-start#0x00005F9 + 0x0002406 + 0x0000643 + 0x0000168
#end = start+length

def convert_4bpp_to_png(path_in: str, path_out:str, options: List[str]) -> None:
    subprocess.call([os.path.join(TMC_FOLDER, 'tools', 'gbagfx', 'gbagfx'), path_in, path_out] + options)

def decompress(path_in: str, path_out: str) -> None:
    subprocess.call([os.path.join(TMC_FOLDER, 'tools', 'gbagfx', 'gbagfx'), path_in, path_out])

def extract_graphic():
    start=0x1FF1B4
    end=0x2474d4

    struct = get_structure(structure, start + ROM_START)
    print(struct)

    data = rom[start:end]

    with open('/tmp/test.4bpp', 'wb') as file:
        file.write(data)

    convert_4bpp_to_png('/tmp/test.4bpp', '/tmp/test.png', ['-mwidth', '2'])

def extract_tileset():
    base = 0x324AE4

    # tileset_tiles 0x3D0, 0x6000000, 0x4000, 1
    #               start,            size

    ts=0x258190, 0x6000000, 0x4000, 1
    

    #start=0x324EB4
    #end=0x327B08
    #start=0x327B08
    #end=0x32A0F8
    start=base+ts[0]
    end=base+ts[0]+ts[2]+1
    print(hex(start), hex(end))

    data=rom[start:end]
    with open('/tmp/test.4bpp.lz', 'wb') as file:
        file.write(data)

    decompress('/tmp/test.4bpp.lz', '/tmp/test.4bpp')
    convert_4bpp_to_png('/tmp/test.4bpp', '/tmp/test.png', ['-mwidth', '32'])


if __name__ == '__main__':
    extract_tileset()
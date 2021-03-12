TMC_FOLDER='../github'

def read_baserom():
    # read baserom data
    with open(f'{TMC_FOLDER}/baserom.gba', 'rb') as baserom:
        return bytearray(baserom.read())

def bytes_to_u32(bytes):
    return int.from_bytes(bytes, 'little')
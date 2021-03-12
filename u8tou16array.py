import struct
array = [0x01, 0x04, 0x67, 0x08]

barray = bytes(array)

count = len(barray)//2
integers = struct.unpack('H'*count, barray)

def u16_to_hex(value):
    return '0x' + (struct.pack('>H', value).hex())

result = [u16_to_hex(x) for x in integers]

print('{ ' + ', '.join(result) + '}')

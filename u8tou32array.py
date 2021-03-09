array = (
     0x00, 0x00, 0x08, 0x08
)

print(array)

def bytes_to_u32(bytes):
    return int.from_bytes(bytes, 'little')

def u32_to_hex(value):
    return '0x' + (int.to_bytes(value, 4, 'big').hex())

result = [u32_to_hex(bytes_to_u32(array[x:x+4])) for x in range(0,len(array),4)]

print('{ ' + ', '.join(result)  + '}');
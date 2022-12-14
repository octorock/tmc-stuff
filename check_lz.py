import sys

def error(message):
    print(f'\033[91m{message}\033[0m')
    sys.exit(1)

def decompress_files():
    if len(sys.argv) != 2:
        error('usage: check_lz.py file.lz')

    src = None
    with open(sys.argv[1], 'rb') as file:
        src = file.read()

    files = []
    compressed_size = len(src)
    print(f'File size: {compressed_size}')
    src_pos = 0
    while True:

        if src[src_pos] != 0x10:
            error(f'First byte is not 0x10, but {hex(src[src_pos])}. Not lz compressed.')

        decompressed_size = src[src_pos + 1] | (src[src_pos + 2] << 8) | (src[src_pos + 3] << 16)

        src_pos += 4
        print(f'Found decompressed size: {decompressed_size}')

        dest = bytearray(decompressed_size)

        dest_pos = 0

        end_of_decompressed_file = False

        while not end_of_decompressed_file:
            if src_pos >= compressed_size:
                error('Reached end of file.')

            flags = src[src_pos]
            src_pos += 1

            #print(f'flags: {bin(flags)}')
            for i in range(0,8):
                #print(i)
                if flags & 0x80:
                    if src_pos + 1 >= compressed_size:
                        error('Reached end of file.')

                    block_size = (src[src_pos] >> 4) + 3
                    block_distance = (((src[src_pos] & 0xf) << 8) | src[src_pos + 1]) + 1

                    src_pos += 2

                    block_pos = dest_pos - block_distance

                    if dest_pos + block_size > decompressed_size:
                        block_size = decompressed_size - dest_pos
                        print('Destination buffer overflow.')

                    if block_pos < 0:
                        error(f'Negative block_pos: {block_pos}')

                    for j in range(0, block_size):
                        dest[dest_pos] = dest[block_pos + j]
                        dest_pos += 1
                else:
                    if src_pos >= compressed_size:
                        error('Reached end of file.')
                    if dest_pos >= decompressed_size:
                        error('Destination buffer overflow.')
                    dest[dest_pos] = src[src_pos]
                    dest_pos += 1
                    src_pos += 1

                if dest_pos == decompressed_size:
                    files.append(dest)
                    print(f'{src_pos} / {compressed_size}')
                    remainder = 4 - (src_pos % 4)
                    if remainder != 4:
                        for i in range(0, remainder):
                            if src[src_pos + i]:
                                error(f'Padding byte is not 0, but {src[src_pos + i]}.')
                        print(f'Padding bytes: {remainder}')
                        src_pos += remainder
                    if src_pos < compressed_size:
                        print('Found another file?')
                        end_of_decompressed_file = True
                        break
                    print('Finished')
                    return files

                flags <<= 1

def main():
    files = decompress_files()
    print(f'\033[92;1mFound {len(files)} files with lengths:\033[0m')
    for i, file in enumerate(files):
        length = len(file)
        print(f'- {length} ({hex(length)})')
        with open(f'/tmp/decompressed_{i}.bin', 'wb') as f:
            f.write(file)
        print(f'/tmp/decompressed_{i}.bin')
        highest_second_byte = 0
        hsb_loc = 0
        for i in range(1, length, 2):
            if file[i] > highest_second_byte:
                highest_second_byte = file[i]
                hsb_loc = i
        print(highest_second_byte, hex(hsb_loc))
        print(file[:2])

if __name__ == '__main__':
    main()
from colors import Color

MIN_CONSECUTIVE_PTRS = 20

with open('tmp/rom_ptrs_at_locs.txt') as file:
    ptrs = []
    last = 0
    for line in file:
        arr = line.split('@')
        addr = int(arr[1], 16)
        if addr - last > 4:
            # Not consecutive anymore
            if len(ptrs) >= MIN_CONSECUTIVE_PTRS:
                print(f'{Color.Green}prev: {len(ptrs)}{Color.Off}')
                print(f'starting at: {ptrs[0].split("@")[1]}')
                #print(''.join(ptrs))
            ptrs = []
        ptrs.append(line)
        last = addr

    if len(ptrs) >= MIN_CONSECUTIVE_PTRS:
        print(f'end: {len(ptrs)}')
        print(ptrs)


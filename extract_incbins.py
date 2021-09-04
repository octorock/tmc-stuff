from common import TMC_FOLDER
import os
import re
from dataclasses import dataclass
import csv

@dataclass
class Incbin:
    path:str=''
    baserom:str=''
    start:int=0
    size:int=0
    variant:str=''
    label:str=''

def main() -> None:

    incbins = []

    for (root, dirs, files) in os.walk(os.path.join(TMC_FOLDER, 'data')):
        for file in files:
            if file.endswith('.s'):
                filepath = os.path.join(root, file)
                parse_file(filepath, file[0:-2], incbins)

    # Some asm files include incbins as well
    parse_file(os.path.join(TMC_FOLDER, 'asm', 'code_080011C4.s'), 'code_080011C4', incbins)
    parse_file(os.path.join(TMC_FOLDER, 'asm', 'code_080043E8.s'), 'code_080043E8', incbins)
    parse_file(os.path.join(TMC_FOLDER, 'asm', 'code_08016984.s'), 'code_08016984', incbins)


    with open('incbins.csv', 'w') as csv_file:
        wr = csv.writer(csv_file, delimiter=',')
        for incbin in incbins:
            wr.writerow([incbin.path, incbin.baserom, hex(incbin.start), hex(incbin.size), incbin.variant, incbin.label])

def parse_file(filepath: str, name: str, incbins:list[Incbin]) -> None:
    output_lines = []

    all_variants = ['USA', 'EU', 'JP', 'DEMO']

    current_variants = all_variants.copy()
    remaining_variants = all_variants.copy()
    label = ''
    count = 0
    layers = 0
    stack = []
    label_stack = []
    with open(filepath, 'r') as file:
        for line in file:
            match = re.search('\.incbin \"(\S*)\", (\w*), (\w*)', line)
            if match!= None:
                variant = '_'.join(current_variants)
                print(match.groups(), variant, label, count, name)

                bin_file = os.path.join('assets', name, label + (('_' + str(count)) if count>0 else '') + (('_' + variant) if current_variants != all_variants else '') + '.bin')
                print(bin_file)

                incbins.append(Incbin(bin_file, match.group(1), int(match.group(2), 16), int(match.group(3), 16), variant, label))
                output_lines.append(f'\t.incbin \"{bin_file}\"\n')
                #output_lines.append(line)

                count += 1
                # Need to increase the counter on the label stack as well if we are still in the same label
                if len(label_stack) > 0 and label == label_stack[-1][0]:
                    label_stack[-1] = (label_stack[-1][0], label_stack[-1][1]+1)
            else:
                # Handle ifdefs
                match = re.search('\.ifdef (\w*)', line)
                if match is not None:
                    #output_lines.append(';'.join(current_variants))
                    stack.append((current_variants.copy(), remaining_variants.copy()))
                    label_stack.append((label, count))

                    # This variant is only used for the current.
                    variant = match.group(1)
                    remaining_variants = current_variants.copy()
                    current_variants = [variant]
                    print(remaining_variants, variant)
                    if variant in remaining_variants:
                        remaining_variants.remove(variant)
                    else:
                        # TODO this ifdef is never true, remove it
                        output_lines.append('.ifdef false ;')
                        current_variants = []
                    layers += 1
                match = re.search('\.ifndef (\w*)', line)
                if match is not None:
                    stack.append((current_variants.copy(), remaining_variants.copy()))
                    label_stack.append((label, count))
                    # The other remaining variants are used
                    variant = match.group(1)
                    if variant in current_variants:
                        current_variants.remove(variant)
                    remaining_variants = [variant]
                    layers += 1
                if '.else' in line:
                    # Now remaining variants can be used
                    current_variants = remaining_variants.copy()

                    # Possibly need to reset labels that only exist in if branch
                    (prev_label, prev_count) = label_stack.pop()
                    if prev_label != label:
                        count = prev_count
                    label = prev_label
                    # But also need to store labels if after endif we need to reset labels that only exist in else branch
                    label_stack.append((label, count))

                if '.endif' in line:
                    layers -= 1
                    (current_variants, remaining_variants) = stack.pop()
                    (prev_label, prev_count) = label_stack.pop()
                    if prev_label != label:
                        count = prev_count
                    label = prev_label
                    #output_lines.append('layer ' + str(layers) + ' ')
                    #output_lines.append('-'.join(current_variants) + " " + '_'.join(remaining_variants))
                    if layers == 0:
                        # Reset variants
                        # TODO this should have already been the last thing on the stack?
                        remaining_variants = all_variants.copy()
                        current_variants = all_variants.copy()

                if '::' in line:
                    label = line.split('::')[0]
                    count = 0


                output_lines.append(line)

    with open(filepath, 'w') as file:
        file.writelines(output_lines)


def read_mapping(variant:str):
    mapping = {}
    with open(os.path.join(TMC_FOLDER, 'tmc' + variant + '.map'), 'r') as map_file:
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
                    mapping[parts[1]] = int(parts[0],16)
            elif not line.startswith(' *'):
                # this defines the name
                current_file = line.split('(')[0].strip()        
    return mapping


def build_assets_list(maps, roms, target_variant):
    with open('incbins.csv', 'r') as file:
        with open(os.path.join(TMC_FOLDER, 'assets_' + target_variant+'.csv'), 'w') as outfile:
            for line in file:
                parts =  line.split(',')
                path = parts[0]
                baserom = parts[1]
                start = int(parts[2], 16)
                size = int(parts[3], 16)
                variants = parts[4].split('_')
                label = parts[5].strip()
                if target_variant not in variants:
                    # This incbin is not used by the target variant
                    continue
                
                print(path)
                print(label)


                offset = 0
                # Calculate the offset to the stored baserom start
                baserom_variant = get_variant(baserom)
                if target_variant != baserom_variant:
                    offset = maps[target_variant][label]-maps[baserom_variant][label]

                    # Check that the included parts work
                    if not check_offset(roms, baserom_variant, target_variant, start, size, offset):
                        # Test a shift up to 0x20 
                        found_offset = False
                        for i in range(1, 0x60): # 0x60 needed for gUnk_080EBB34
                            if check_offset(roms, baserom_variant, target_variant, start, size, offset + i):
                                offset += i
                                found_offset = True
                                break
                            # Also check before
                            if check_offset(roms, baserom_variant, target_variant, start, size, offset - i):
                                offset -= i
                                found_offset = True
                                break

                        if not found_offset:
                            raise Exception('Found no correct offset.')

                print(offset)
                outfile.write(path + ',' + hex(start + offset) + ',' + hex(size) + ',\n')
            
def check_offset(roms, baserom_variant, target_variant, start, size, offset):
    check_size = min(size, 0x20) # only check 0x20 bytes
    for i in range(0, check_size):
        if roms[baserom_variant][start+i] != roms[target_variant][start+offset+i]:
            #print(f'Offset {offset} is wrong between {baserom_variant} and {target_variant} at {start} + {i}: {roms[baserom_variant][start+i]} != {roms[target_variant][start+offset+i]}')
            return False
    return True

def get_variant(baserom):
    map = {
        'baserom.gba': 'USA',
        'baserom_eu.gba': 'EU',
        'baserom_jp.gba': 'JP',
        'baserom_demo.gba': 'DEMO'
    }
    return map[baserom]

def read_rom(variant):
    map = {
        'USA': 'baserom.gba',
        'EU': 'baserom_eu.gba',
        'JP': 'baserom_jp.gba',
        'DEMO': 'baserom_demo.gba'
    }
    with open(os.path.join(TMC_FOLDER, map[variant]), 'rb') as file:
        baserom = bytearray(file.read())
    return baserom

def build_for_other_variants():
    maps = {}
    maps['USA'] = read_mapping('')
    maps['EU'] = read_mapping('_eu')
    maps['JP'] = read_mapping('_jp')
    maps['DEMO'] = read_mapping('_demo')
    roms = {}
    roms['USA'] = read_rom('USA')
    roms['EU'] = read_rom('EU')
    roms['JP'] = read_rom('JP')
    roms['DEMO'] = read_rom('DEMO')

    build_assets_list(maps, roms, 'USA')
    build_assets_list(maps, roms, 'EU')
    build_assets_list(maps, roms, 'JP')
    build_assets_list(maps, roms, 'DEMO')


if __name__ == '__main__':
    main()
    build_for_other_variants()


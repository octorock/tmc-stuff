from common import TMC_FOLDER
import os
import re
from dataclasses import dataclass
import csv
import yaml
import parser

@dataclass
class Incbin:
    path:str=''
    baserom:str=''
    start:int=0
    size:int=0
    variant:str=''
    label:str=''

def extract_all_incbins() -> None:

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

    all_variants = ['USA', 'EU', 'JP', 'DEMO_USA', 'DEMO_JP']

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
                variant = '-'.join(current_variants)
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
                variants = parts[4].split('-')
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
        'baserom_demo.gba': 'DEMO_USA',
        'baserom_demo_jp.gba': 'DEMO_JP',
    }
    return map[baserom]

def read_rom(variant):
    map = {
        'USA': 'baserom.gba',
        'EU': 'baserom_eu.gba',
        'JP': 'baserom_jp.gba',
        'DEMO_USA': 'baserom_demo.gba',
        'DEMO_JP': 'baserom_demo_jp.gba',
    }
    with open(os.path.join(TMC_FOLDER, map[variant]), 'rb') as file:
        baserom = bytearray(file.read())
    return baserom

def build_for_other_variants():
    maps = {}
    maps['USA'] = read_mapping('')
    maps['EU'] = read_mapping('_eu')
    maps['JP'] = read_mapping('_jp')
    maps['DEMO_USA'] = read_mapping('_demo_usa')
    maps['DEMO_JP'] = read_mapping('_demo_jp')
    roms = {}
    roms['USA'] = read_rom('USA')
    roms['EU'] = read_rom('EU')
    roms['JP'] = read_rom('JP')
    roms['DEMO_USA'] = read_rom('DEMO_USA')
    roms['DEMO_JP'] = read_rom('DEMO_JP')

    build_assets_list(maps, roms, 'USA')
    build_assets_list(maps, roms, 'EU')
    build_assets_list(maps, roms, 'JP')
    build_assets_list(maps, roms, 'DEMO_USA')
    build_assets_list(maps, roms, 'DEMO_JP')



# Allow to parse expressions instead of just hex numbers to be able to quickly adapt offsets for different versions
def parse_hex(text):
    code = parser.expr(text).compile()
    return eval(code)

@dataclass
class Asset:
    path: str
    mode: str
    start: int
    size: int

def read_asset_file(variant):
    assets = {}
    with open(os.path.join(TMC_FOLDER, f'assets_{variant}.csv'), 'r') as file:
        for line in file:
            (path,start,size,mode) = line.split(',')
            mode = mode.strip()
            start = parse_hex(start)
            size = parse_hex(size)
            assets[path] = Asset(path, mode, start, size)
    return assets


# Are all values in the array the same
def all_same(arr):
    return len(set(iter(arr.values()))) <= 1

def merge_asset_files():

    all_variants = ['USA', 'JP', 'EU', 'DEMO_USA', 'DEMO_JP']
    assets = {}
    index = {}
    current_offsets = {}
    for variant in all_variants:
        assets[variant] = read_asset_file(variant)
        index[variant] = 0
        current_offsets[variant] = 0

    output = []

    incbins = []

    with open('incbins.csv', 'r') as file:
        for line in file:
            parts =  line.split(',')
            path = parts[0]
            baserom = parts[1]
            start = int(parts[2], 16)
            size = int(parts[3], 16)
            variants = parts[4].split('-')
            label = parts[5].strip()
            incbins.append((path, start, variants))
            if variants[0] == '':
                print('An asset without variants found:')
                print(path, start, variants)
                print('This incbin is never compiled and can be deleted?')
                return

    # Sort incbins. The files themselves are already sorted, so we just need to sort the files in the global scope
    files = {}
    for incbin in incbins:
        file = incbin[0].split('/')[1]
        if file == 'tilesets':
            file = 'data_08132B30' # Quick hack because the three test tilesets were moved from their original path

        variants = incbin[2]
        print(variants)
        if not file in files:
            files[file] = {'incbins': []}
        files[file]['incbins'].append(incbin)
        if 'start' not in files[file] and 'USA' in variants:
            files[file]['start'] = incbin[1]

    # manually place starts for files not in USA
    files['strings']['start'] = 0x8C0FE0 # after data_08132B30
    files['demoScreen']['start'] = 0x127280 # after playerItem15

    arr = []

    for key in files:
        if not 'start' in files[key]:
            print(key)
            raise Exception()
        arr.append((key, files[key]['start']))

    arr = sorted(arr, key=lambda i:i[1])

    # Insert the incbins now sorted
    incbins = []

    for (a,b) in arr:
        for incbin in files[a]['incbins']:
            incbins.append(incbin)

    

    for (path, start, variants) in incbins:
        data = {
            'path': path,
        }
        if len(variants) != len(all_variants): # Omit variants if all of them use this
            data['variants'] = variants


        # For now show all starts and sizes
        starts = {}
        sizes = {}
        for variant in variants:
            print(variant, variants)
            if path in assets[variant]:
                asset = assets[variant][path]
                starts[variant] = asset.start
                sizes[variant] = asset.size
                if asset.mode != '':
                    data['type'] = asset.mode
            else:
                raise Exception()

        if 'USA' in variants: # We have a base to reference, can use relative offsets
            changed_offsets = []
            for variant in variants:
                if variant == 'USA':
                    continue
                offset = starts[variant] - starts['USA']
                if offset != current_offsets[variant]:
                    current_offsets[variant] = offset
                    changed_offsets.append((variant, offset))
            if len(changed_offsets) != 0:
                offsets = {}
                for (variant, offset) in changed_offsets:
                    offsets[variant] = offset
                output.append({
                    'offsets': offsets
                })
            data['start'] = starts['USA']
        else:
            # Need the starts for all variants
            data['starts'] = starts

        if all_same(sizes):
            data['size'] = sizes[variants[0]]

        else:
            data['sizes'] = sizes


        output.append(data)


    # Represent all integers as hex numbers
    # https://stackoverflow.com/a/42504639
    def hexint_presenter(dumper, data):
        return dumper.represent_int(hex(data))
    yaml.add_representer(int, hexint_presenter)

    with open(os.path.join(TMC_FOLDER, 'assets.yaml'), 'w') as file:
        yaml.dump(output, file, sort_keys=False)


    # with open('tmp/test.yaml') as file:
    #     data = yaml.safe_load(file)
    #     print(data)


if __name__ == '__main__':
    extract_all_incbins()
    build_for_other_variants()
    merge_asset_files()

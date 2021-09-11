from common import TMC_FOLDER
import os
import re
from dataclasses import dataclass
import csv
import yaml
import parser

@dataclass
class Incbin:
    baserom:str=''
    start:int=0
    size:int=0
    comment:str=''

def deduplicate_incbins() -> None:
    incbins = []


    #parse_file(os.path.join(TMC_FOLDER, 'asm', 'code_080043E8.s'), 'code_080043E8', incbins)
    #return



    for (root, dirs, files) in os.walk(os.path.join(TMC_FOLDER, 'data')):
        for file in files:
            if file.endswith('.s'):
                filepath = os.path.join(root, file)
                parse_file(filepath, file[0:-2], incbins)

    # Some asm files include incbins as well
    parse_file(os.path.join(TMC_FOLDER, 'asm', 'code_080011C4.s'), 'code_080011C4', incbins)
    parse_file(os.path.join(TMC_FOLDER, 'asm', 'code_080043E8.s'), 'code_080043E8', incbins)
    parse_file(os.path.join(TMC_FOLDER, 'asm', 'code_08016984.s'), 'code_08016984', incbins)



def parse_file(filepath: str, name: str, incbins:list[Incbin]) -> None:
    output_lines = []

    with open(filepath, 'r') as file:
        for line in file:
            match = re.search('\.incbin \"(\S*)\", (\w*), (\w*)(.*)', line)
            if match!= None:
                print(match.groups(), name)

                ##bin_file = os.path.join('assets', name, label + (('_' + str(count)) if count>0 else '') + (('_' + variant) if current_variants != all_variants else '') + '.bin')
                #print(bin_file)

                # Store the incbin instead of printing it to merge them
                incbins.append(Incbin(match.group(1), int(match.group(2), 16), int(match.group(3), 16), (match.group(4)).rstrip()))

            else:
                # Print out the incbins
                if len(incbins) > 0:
                    print(f'{len(incbins)} incbins.')
                    incbin = incbins[0]

                    # Merge other incbins
                    for i in range(1, len(incbins)):
                        other = incbins[i]
                        if other.baserom != incbin.baserom:
                            raise Exception(f'baserom {other.baserom} != {incbin.baserom}')
                        if incbin.start + incbin.size != other.start:
                            print(f'Not consecutive: {incbin.start + incbin.size} != {other.start}')
                            output_lines.append(f'\t.incbin "{incbin.baserom}", {"{0:#08x}".format(incbin.start).upper().replace("0X", "0x")}, {"{0:#09x}".format(incbin.size).upper().replace("0X", "0x")}{incbin.comment}\n')
                            incbin = other
                            continue
                        incbin.size += other.size

                    incbins.clear()
                    out = f'\t.incbin "{incbin.baserom}", {"{0:#08x}".format(incbin.start).upper().replace("0X", "0x")}, {"{0:#09x}".format(incbin.size).upper().replace("0X", "0x")}{incbin.comment}\n'
                    print(out)
                    output_lines.append(out)

                output_lines.append(line)

        # Print out the incbins
        if len(incbins) > 0:
            print(f'{len(incbins)} incbins.')
            incbin = incbins[0]

            # Merge other incbins
            for i in range(1, len(incbins)):
                other = incbins[i]
                if other.baserom != incbin.baserom:
                    raise Exception(f'baserom {other.baserom} != {incbin.baserom}')
                if incbin.start + incbin.size != other.start:
                    print(f'Not consecutive: {incbin.start + incbin.size} != {other.start}')
                    output_lines.append(f'\t.incbin "{incbin.baserom}", {"{0:#08x}".format(incbin.start).upper().replace("0X", "0x")}, {"{0:#09x}".format(incbin.size).upper().replace("0X", "0x")}{incbin.comment}\n')
                    incbin = other
                    continue
                incbin.size += other.size

            incbins.clear()
            out = f'\t.incbin "{incbin.baserom}", {"{0:#08x}".format(incbin.start).upper().replace("0X", "0x")}, {"{0:#09x}".format(incbin.size).upper().replace("0X", "0x")}{incbin.comment}\n'
            print(out)
            output_lines.append(out)

    with open(filepath, 'w') as file:
        file.writelines(output_lines)


if __name__ == '__main__':
    deduplicate_incbins()
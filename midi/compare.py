import sys


start = int(sys.argv[1], 16)

values = {
    'W00': 0x80,
    'W01': 0x81,
    'W02': 0x82,
    'W03': 0x83,
    'W04': 0x84,
    'W05': 0x85,
    'W06': 0x86,
    'W07': 0x87,
    'W08': 0x88,
    'W09': 0x89,
    'W10': 0x8A,
    'W11': 0x8B,
    'W12': 0x8C,
    'W13': 0x8D,
    'W14': 0x8E,
    'W15': 0x8F,
    'W16': 0x90,
    'W17': 0x91,
    'W18': 0x92,
    'W19': 0x93,
    'W20': 0x94,
    'W21': 0x95,
    'W22': 0x96,
    'W23': 0x97,
    'W24': 0x98,
    'W28': 0x99,
    'W30': 0x9A,
    'W32': 0x9B,
    'W36': 0x9C,
    'W40': 0x9D,
    'W42': 0x9E,
    'W44': 0x9F,
    'W48': 0xA0,
    'W52': 0xA1,
    'W54': 0xA2,
    'W56': 0xA3,
    'W60': 0xA4,
    'W64': 0xA5,
    'W66': 0xA6,
    'W68': 0xA7,
    'W72': 0xA8,
    'W76': 0xA9,
    'W78': 0xAA,
    'W80': 0xAB,
    'W84': 0xAC,
    'W88': 0xAD,
    'W90': 0xAE,
    'W92': 0xAF,
    'W96': 0xB0,
    'FINE': 0xb1,
    'GOTO': 0xb2,
    'PATT': 0xb3,
    'PEND': 0xb4,
    'TEMPO': 0xbb,
    'KEYSH': 0xbc,
    'VOICE': 0xbd,
    'VOL': 0xbe,
    'PAN': 0xbf,
    'BEND': 0xc0,
    'BENDR': 0xc1,
    'MOD': 0xc4,
    'MODT': 0xc5,
    'TUNE': 0xc8,  
    'XCMD': 0xcd,
    'xIECV': 0x08,
    'XIECL': 0x09,

    'EOT': 0xce,
    'TIE': 0xcf,

    'N01': 0xD0,
    'N02': 0xD1,
    'N03': 0xD2,
    'N04': 0xD3,
    'N05': 0xD4,
    'N06': 0xD5,
    'N07': 0xD6,
    'N08': 0xD7,
    'N09': 0xD8,
    'N10': 0xD9,
    'N11': 0xDA,
    'N12': 0xDB,
    'N13': 0xDC,
    'N14': 0xDD,
    'N15': 0xDE,
    'N16': 0xDF,
    'N17': 0xE0,
    'N18': 0xE1,
    'N19': 0xE2,
    'N20': 0xE3,
    'N21': 0xE4,
    'N22': 0xE5,
    'N23': 0xE6,
    'N24': 0xE7,
    'N28': 0xE8,
    'N30': 0xE9,
    'N32': 0xEA,
    'N36': 0xEB,
    'N40': 0xEC,
    'N42': 0xED,
    'N44': 0xEE,
    'N48': 0xEF,
    'N52': 0xF0,
    'N54': 0xF1,
    'N56': 0xF2,
    'N60': 0xF3,
    'N64': 0xF4,
    'N66': 0xF5,
    'N68': 0xF6,
    'N72': 0xF7,
    'N76': 0xF8,
    'N78': 0xF9,
    'N80': 0xFA,
    'N84': 0xFB,
    'N88': 0xFC,
    'N90': 0xFD,
    'N92': 0xFE,
    'N96': 0xFF,

    # Notes
	'CnM2': 0,
	'CsM2': 1,
	'DnM2': 2,
	'DsM2': 3,
	'EnM2': 4,
	'FnM2': 5,
	'FsM2': 6,
	'GnM2': 7,
	'GsM2': 8,
	'AnM2': 9,
	'AsM2': 10,
	'BnM2': 11,
	'CnM1': 12,
	'CsM1': 13,
	'DnM1': 14,
	'DsM1': 15,
	'EnM1': 16,
	'FnM1': 17,
	'FsM1': 18,
	'GnM1': 19,
	'GsM1': 20,
	'AnM1': 21,
	'AsM1': 22,
	'BnM1': 23,
	'Cn0': 24,
	'Cs0': 25,
	'Dn0': 26,
	'Ds0': 27,
	'En0': 28,
	'Fn0': 29,
	'Fs0': 30,
	'Gn0': 31,
	'Gs0': 32,
	'An0': 33,
	'As0': 34,
	'Bn0': 35,
	'Cn1': 36,
	'Cs1': 37,
	'Dn1': 38,
	'Ds1': 39,
	'En1': 40,
	'Fn1': 41,
	'Fs1': 42,
	'Gn1': 43,
	'Gs1': 44,
	'An1': 45,
	'As1': 46,
	'Bn1': 47,
	'Cn2': 48,
	'Cs2': 49,
	'Dn2': 50,
	'Ds2': 51,
	'En2': 52,
	'Fn2': 53,
	'Fs2': 54,
	'Gn2': 55,
	'Gs2': 56,
	'An2': 57,
	'As2': 58,
	'Bn2': 59,
	'Cn3': 60,
	'Cs3': 61,
	'Dn3': 62,
	'Ds3': 63,
	'En3': 64,
	'Fn3': 65,
	'Fs3': 66,
	'Gn3': 67,
	'Gs3': 68,
	'An3': 69,
	'As3': 70,
	'Bn3': 71,
	'Cn4': 72,
	'Cs4': 73,
	'Dn4': 74,
	'Ds4': 75,
	'En4': 76,
	'Fn4': 77,
	'Fs4': 78,
	'Gn4': 79,
	'Gs4': 80,
	'An4': 81,
	'As4': 82,
	'Bn4': 83,
	'Cn5': 84,
	'Cs5': 85,
	'Dn5': 86,
	'Ds5': 87,
	'En5': 88,
	'Fn5': 89,
	'Fs5': 90,
	'Gn5': 91,
	'Gs5': 92,
	'An5': 93,
	'As5': 94,
	'Bn5': 95,
	'Cn6': 96,
	'Cs6': 97,
	'Dn6': 98,
	'Ds6': 99,
	'En6': 100,
	'Fn6': 101,
	'Fs6': 102,
	'Gn6': 103,
	'Gs6': 104,
	'An6': 105,
	'As6': 106,
	'Bn6': 107,
	'Cn7': 108,
	'Cs7': 109,
	'Dn7': 110,
	'Ds7': 111,
	'En7': 112,
	'Fn7': 113,
	'Fs7': 114,
	'Gn7': 115,
	'Gs7': 116,
	'An7': 117,
	'As7': 118,
	'Bn7': 119,
	'Cn8': 120,
	'Cs8': 121,
	'Dn8': 122,
	'Ds8': 123,
	'En8': 124,
	'Fn8': 125,
	'Fs8': 126,
	'Gn8': 127,

    # Gate time parameter
    'gtp1': 1,
    'gtp2': 2,
    'gtp3': 3,

    # TMP
    'test_key+0': 0
}

rom = None
with open(sys.argv[2], 'rb') as baserom:
    rom = bytearray(baserom.read())

# Find start address of first track
def bytes_to_u32(bytes):
    return int.from_bytes(bytes, 'little')

track1_start = bytes_to_u32(rom[start+8: start+12])-0x8000000
print(hex(track1_start))

cursor = track1_start

labels = {}

with open('test.anno.s') as file:
    lines = file.readlines()

    for i in range(0, len(lines)):
        line = lines[i]
        if ':' in line:
            labels[line.split(':')[0].strip()] = cursor
        if 'NumTrks' in line: # Start of header
            break
        if '.byte' in line:
            (before, after) = line.split('.byte')
            time = before.strip()
            args = after.split(',')
            for arg in args:
                arg = arg.strip()
                orig_arg = arg
                if '*test_tbs/2' in arg:
                    arg = int(arg.replace('*test_tbs/2', ''))//2
                elif '*test_mvl/mxv' in arg:
                    arg = int(arg.replace('*test_mvl/mxv', '')) 
                elif 'c_v+' in arg:
                    arg = int(arg.replace('c_v', '')) + 0x40
                elif 'c_v-' in arg:
                    arg = int(arg.replace('c_v', '')) + 0x40
                elif arg.startswith('v'):
                    arg = int(arg[1:])
                if type(arg) != int:

                    if arg.isnumeric():
                        arg = int(arg)
                    else:
                        if arg not in values:
                            print(line)
                            raise Exception(f'Undefined byte {arg}')
                        arg = values[arg]
                #print(line)
                #print(arg)

                if rom[cursor] != arg:
                    print(f'address: {hex(cursor)}')
                    print(f'line: {line}')
                    raise Exception(f'expected: {hex(rom[cursor])} actual: {hex(arg)} ({orig_arg})')
                if orig_arg == 'GOTO' or orig_arg == 'PATT':
                    
                    expected = bytes_to_u32(rom[cursor+1:cursor+4])
                    target_label = lines[i+1].split('.word')[1].strip()
                    actual = labels[target_label]
                    if expected != actual:
                        print(f'address: {hex(cursor)}')
                        print(f'line: {line} {lines[i+1]}')
                        raise Exception(f'Pointer mismatch. expected: {hex(expected)} actual: {hex(actual)} ({orig_arg})')

                    #actual = 
                    cursor += 5
                else:
                    cursor += 1
print('Songs seem equal.')
import sys
from colors import Color
import pyperclip

# Convert a list of pointers in Ghidra by pressing p
# Then select all of them and copy. Insert into this script and press Ctrl+D
# The asm code is then copied to the clipboard.
def main():
    while True:
        print(f'{Color.Blue}Copy pointers from Ghidra into clipboard, then press Enter: {Color.Off}')

        input()

        code = []
        input_lines = pyperclip.paste().split('\n')
        # Read until Ctrl+D
        for line in input_lines:


            arr = line.split()
            if len(arr) >= 7:
                addr = arr[6]
                if 'sub_' in addr and addr.endswith('+1'): # The +1 for function pointers is not necessary
                    addr = addr[:-2]

                if not 'Point(*)' in addr:
                    code.append(f'\t.4byte {addr}')

        if len(code) == 0:
            print(f'{Color.Red}No Ghidra pointers found in clipboard: {Color.Off}')
            print('\n'.join(input_lines))
            continue
        print('\n'.join(code))
        pyperclip.copy('\n'.join(code))
        print(f'{Color.Green}Copied to clipboard.{Color.Off}')
        # print(Color.Green + str(arr) + Color.Off)

if __name__ == '__main__':
    main()
import sys
from colors import Color

# Convert a list of pointers in Ghidra by pressing p
# Then select all of them and copy. Insert into this script and press Ctrl+D

# To directly copy to clipboard run python ghidra_ptr_list_to_asm.py | xclip -selection clipboard
def main():
    for line in sys.stdin.readlines():
        
        arr = line.split()
        if len(arr) >= 7:
            print(f'.4byte {arr[6]}')
        # print(Color.Green + str(arr) + Color.Off)

if __name__ == '__main__':
    main()
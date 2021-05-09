# tmc stuff

### Script Disassembler
The python scripts used to first extract the scripts from the rom and create asm macros for them can be found in [script_disassembler](script_disassembler).

### Array Conversion
[Convert u8 array to u16 array](u8tou16array.py)  
[Convert u8 array to u32 array](u8tou32array.py)

### Find out where scripts belong to
Finds the files that the functions are defined in that are referenced by `Call` commands in scripts: [sort_scripts.sh](sort_scripts.sh)

### Colorize Output of Build
Colors stderr orange or red, depending on if a line contains `error`. Prints stdout in gray, except for final `tmc: OK` message: [make.sh](make.sh)

### Compiler Explorer
Fork of [cexplore](https://github.com/SBird1337/cexplore) that uses the tmc repo and small filters for the assembly to make it easier to see if the code and assembly match: [octorock/cexplore](https://github.com/octorock/cexplore)

### Ghidra
Some notes on the use of Ghidra: [ghidra.md](ghidra.md)
| Script | Function
|---|---|
| [ghidra_replace.py](ghidra_replace.py) | Improve Ghidra decompiler output |
| [export_to_cexplore.py](export_to_cexplore.py) | Export NONMATCH function to cexplore |

### Finding Pointers
Some scripts to find things in the rom that might point to other things.
| Script | Function |
|---|---|
|[list_filestructure.sh](list_filestructure.sh)|Reads the structure of the rom from the `.map` |file and stores it in `tmp/structure.txt`  |
| python parse_mapping.py > tmp/symbols.txt | needed for python scripts |
|[get_location.py](get_location.py) | Enter a hex address and this script tells you in which file it is defined |
|[find_pointers.py](find_pointers.py) | Searches for everything that looks like a pointer |  
|[consecutive_pointers.py](consecutive_pointers.py) | Searches in the list of possible pointers for multiple consecutive pointers |

### Enums
Reads those mysterious enum like looking things after `gUnk_0812AAE8`: [read_enums.py](read_enums.py)

### Annotating rodata
Annotates files in the data folder with the files the label was referenced from: [annotate_rodata.sh](annotate_rodata.sh)

### Commit When OK
[wip_commit.sh](wip_commit.sh)  
Creates a "WIP" commit. Then runs make and if it returns `OK`, it changes the commit with all changed files. Will repeat this process when <kbd>Enter</kbd> is pressed. This way the last `OK` version is always available in the latest commit.
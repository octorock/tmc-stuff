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
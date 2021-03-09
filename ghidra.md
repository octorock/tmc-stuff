# Notes on Ghidra

Ghidra loader: https://github.com/SiD3W4y/GhidraGBA

## Changes needed to load the includes into Ghidra as source
Replace `types.h`
```c
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef unsigned long long u64;
typedef signed char s8;
typedef signed short s16;
typedef signed int s32;
typedef signed long long s64;
```

Remove `extern` in line 88 of `screen.h`
```c
struct OAMCommand {
    u16 x;
    u16 y;
    u16 _4;
    u16 _6;
    u16 _8;
} extern gOamCmd;
```
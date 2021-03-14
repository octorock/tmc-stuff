#!/bin/bash

# Color output
# https://serverfault.com/a/59279

# ignore case while string contains
# https://unix.stackexchange.com/a/132485

TMC_FOLDER="../github"

cd $TMC_FOLDER
shopt -s nocasematch

make -j$(nproc) DINFO=0 2> >(while read line; do 
# stderr
if [[ $line =~ "error" ]]; then
    echo -e "\e[01;31m$line\e[0m" >&2;
else
    echo -e "\e[33m$line\e[0m" >&2;
fi
done) 1> >(while read line; do 
# stdout
if [[ $line == "tmc.gba: FAILED" ]]; then
    echo -e "tmc.gba: \e[01;31mFAILED\e[0m" >&1;
elif [[ $line == "tmc.gba: OK" ]]; then
    echo -e "tmc.gba: \e[01;32mOK\e[0m" >&1;
else
    echo -e "\e[90m$line\e[0;0m" >&1;
fi
done)

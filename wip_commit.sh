#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source $DIR/common.py
cd $DIR/$TMC_FOLDER
git commit -m "WIP" --allow-empty

while true;
do
    $DIR/make.sh && git add . && git commit --amend --allow-empty -m "WIP" | head -n 3
    read
done


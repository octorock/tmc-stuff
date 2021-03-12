#!/bin/bash

# !!! THIS SCRIPT CHANGES THE FILES BY ADDING ANNOTATIONS !!!

# Annotates all files in the data folder
# For each gUnk_ label it adds a comment with the places where this label is referenced

source common.py
cd $TMC_FOLDER

function split_file {
    FILE_PATH="$1"
    while IFS= read -r LINE
    do
        UNK="$(echo $LINE | grep ^gUnk.*@)"
        if [ "$?" -eq 0 ]
        then
            # A line containing a gUnk
            IFS=$'@' read -a PARTS <<<"$LINE" # split at @ https://stackoverflow.com/a/15988793
            ADDR=$(echo ${PARTS[1]} | xargs)  # trim whitespace https://stackoverflow.com/a/12973694

            # search for usages in asm/ and src/
            USAGES="$(grep $ADDR -r asm/ src/ | grep -v $FILE_PATH)" # except in this file itself (in case it resides in asm/)
            if [ "$?" -eq 0 ]
            then
                # this gUnk is referenced
                FILES=`echo "$USAGES" | cut -d : -f 1` # extract the file part
                UNIQUE_FILES=`echo "$FILES" | sort | uniq` # deduplicate file names
                COMMENT=`echo "$UNIQUE_FILES" | tr '\n' ',' | sed 's/,$//'| sed 's/,/, /g'` # join with comma, remove trailing comma, add spaces after commas
                echo "$(echo $LINE | tr -d '\n') @ $COMMENT"
            else
                # gUnk was never referenced
                echo $LINE
            fi
        else
            # Line without gUnk
            echo $LINE
        fi
    done < $FILE_PATH
}

# Files in data/
FILE_PATHS="$(find data -name '*.s')"

# Files in asm/ that still contain .incbin "baserom.gba"
#FILE_PATHS="$(grep baserom asm/* -R | cut -d : -f 1 | sort | uniq)"

export IFS=$'\n'
for FILE in $FILE_PATHS
do
    echo "Annotating $FILE..."
    split_file $FILE > $FILE.anno.s
    mv $FILE.anno.s $FILE
done

echo "done" 
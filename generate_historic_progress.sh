#!/bin/bash

FIRST_CALCROM_COMMIT='9bbfe9592511d6cb6c33ab06af370eaf69e9ab6c'

# Text Colors https://stackoverflow.com/a/28938235
Color_Off='\033[0m'
Cyan='\033[0;36m'  
BIRed='\033[1;91m'
BIGreen='\033[1;92m'

cd tmp_tmc
git reset --hard master
#COMMITS=`git rev-list $FIRST_CALCROM_COMMIT..HEAD | tac`
# Get all pull request merge commits
COMMITS=`git log --merges --oneline | grep "pull req" | cut -d " " -f 1 | tac`


i=0
for COMMIT in $COMMITS
do
    echo -e "Checking out $Cyan$COMMIT$Color_Off..."
    git checkout $COMMIT
    git reset --hard && git clean -f -d

    FILE=../tmp/progress/`printf "%04d" $i`_$COMMIT.txt

    # Making setup is necessary as tmc_strings is introduced later
    make setup

    make -j$(nproc) > $FILE 2>&1 
    if [ $? -eq 0 ]; then
        echo -e ${BIGreen}OK $Color_Off
        echo OK >> $FILE
    else
        echo FAIL >> $FILE
        echo -e ${BIRed}FAIL $Color_Off
        continue
    fi
    echo "Calculating progress..."

    cp ../progress.py .
    
    python progress.py >> ../tmp/reports/progress_tmc.csv
    python progress.py -m >> ../tmp/reports/progress_tmc_matching.csv
    #BUILD_NAME=`cat Makefile  | grep BUILD_NAME | head -n 1 | cut -d "=" -f 2 | xargs`
    #perl calcrom.pl $BUILD_NAME.map >> $FILE
    git reset --hard HEAD
    echo 'done'
    ((i+=1))
done
echo 'Finished all commits'
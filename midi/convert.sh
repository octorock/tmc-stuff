#!/bin/bash
set -e
#../tools/mid2agb/mid2agb se_bike_bell.mid orig2.s -E -R50 -G128 -V090 -P4
#../tools/mid2agb/mid2agb mus_title.mid title.s -E -R50 -G059 -V090

# Assembly a.out
#arm-none-eabi-as orig2.s -o a.o
#arm-none-eabi-ld -T test.ld -o b.out

#arm-none-eabi-as title.s -o title.o
#arm-none-eabi-ld -T title.ld -o title.out

START=0xeea30c

PARAMS="-G1 -E"
AGB2MID_PARAMS=" -v"
# -t 8 4 960 -t 4 4 1080 -t 12 4 1560" #" -v -t 7 4 960 -t 4 4 1080"
# bgmRoyalCrypt? -t 4 4 984"
# VaatiWrath:? -t 3 4 108 -t 4 4 540 -t 4 4 636"

#-n2 -d4 -t 4 4 72"
#" -n4 -d2 -t2302"
#-n12 -d5 -t96"

BASEROM=../../github/baserom_eu.gba
#BASEROM=../../github/baserom.gba

INITIAL=false

if [ $INITIAL = true ]; then
    ../tools/mid2agb/mid2agb mus_end.mid test.s $PARAMS
    cp test.s a.s
    echo "Add .word 0xffffffff to a.s to find start address"
    read
    arm-none-eabi-as a.s -o a.o
    arm-none-eabi-ld -T test.ld -o b.out
    echo "Edit convert.sh, set INITIAL=false and edit START"
    exit
fi


# Offset of .s file: 0x34
# header start: 0x44
cd ../../github/tools/agb2mid/ && make
cd ../../../scripts/midi
#../tools/agb2mid/agb2mid ../baserom.gba 0x44 ../baserom.gba test.mid
#../tools/agb2mid/agb2mid b.out 0x1c b.out test.mid $PARAMS
#../tools/agb2mid/agb2mid title.out 0x2DE4 title.out test.mid -E -R50 -G059 -V090

#START=0x1f8
#START=0xbc

#START=0xDD52FC

#../tools/agb2mid/agb2mid ../baserom.gba $START ../baserom.gba test.orig.s -s $PARAMS$AGB2MID_PARAMS
#gdb -ex=r -args ../tools/agb2mid/agb2mid ../baserom.gba $START ../baserom.gba test.orig.s -s $PARAMS$AGB2MID_PARAMS
#python ../tools/agb2mid/dump_sound_s.py ../baserom.gba 0x8a11dbc 0x8de7d28  0x8a11c3c 0x8a11dbc

#exit
#../tools/agb2mid/agb2mid b.out $START b.out test.mid $PARAMS
../../github/tools/agb2mid/agb2mid $BASEROM $START $BASEROM test.mid $PARAMS$AGB2MID_PARAMS | tee test.log
# gdb -ex=r -args ../tools/agb2mid/agb2mid ../baserom.gba $START ../baserom.gba test.mid 
#../../github/tools/mid2agb/mid2agb test.mid test.s $PARAMS
gdb -ex=r -args ../../github/tools/mid2agb/mid2agb test.mid test.s $PARAMS

python annotate_sound_s.py
python compare.py $START $BASEROM

# Convert gbamus reference
#../tools/mid2agb/mid2agb ~/Downloads/gbamus/credits.mid credits.s $PARAMS

# TODO print pattern counts and durations for both to see if they match
# TODO use differing start time signature to prevent a pattern at the start
# TODO while resorting the events with the same time, mid2agb puts the LoopBegin before the TEMPO
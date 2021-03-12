 source common.py
 cat $TMC_FOLDER/tmc.map  | grep -e "^ \." | grep 0000000008 | awk {'print $2" "$4" "$1'} > tmp/structure.txt
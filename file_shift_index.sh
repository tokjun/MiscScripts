#! /bin/bash
#
# Usage:  file_shift_index.sh <FILE_PREFIX> <FILE_SUFFIX> <FIRST_INDEX> <LAST_INDEX> <OFFSET>
#
#   Ex)  file_shift_index.sh "data/img_" ".nrrd" 1 100 -2
#
#     This will rename data/img_012.nrrd to data/img_010.nrrd, for example.
#     Note that the script assumes 3-digit numbering (i.e. 001, 002, ..., )
#

if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <FILE_PREFIX> <FILE_SUFFIX> <FIRST_INDEX> <LAST_INDEX> <OFFSET>" >&2
    exit 1
fi

FILE_PREFIX=$1
FILE_SUFFIX=$2
FIRST_INDEX=$3
LAST_INDEX=$4
OFFSET=$5

for (( i=$FIRST_INDEX; i<=$LAST_INDEX; i++ ))
do
    dst_index=`expr $i + $OFFSET`
    INPUT_PATH=`printf "%s%03d%s" $FILE_PREFIX $i $FILE_SUFFIX`
    OUTPUT_PATH=`printf "%s%03d%s" $FILE_PREFIX $dst_index $FILE_SUFFIX`
    if [ -f "$INPUT_PATH" ]; then
	echo "Renaming "$INPUT_PATH"..."
	mv "$INPUT_PATH" "$OUTPUT_PATH"
    fi
done




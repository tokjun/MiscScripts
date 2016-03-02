#! /bin/bash
#
# Usage:  file_rename_series_nrrd.sh <ORG_DIR> <DST_DIR> <ORG_PREFIX> <DST_SUFFIX> <FIRST_INDEX> <LAST_INDEX>
#
#   Ex)  dicom_extract_by_tag.sh inputDir outputDir " Kidney2-echoPETRA2.1MM3CRYO25000SPKFOV33GRAD9" "echo1-" 1 100
#

if [ "$#" -ne 6 ] || ! [ -d "$1" ]; then
    echo "Usage: $0 <ORG_DIR> <DST_DIR> <ORG_PREFIX> <DST_SUFFIX> <FIRST_INDEX> <LAST_INDEX>" >&2
    exit 1
fi

ORG_DIR=$1
DST_DIR=$2
ORG_PREFIX=$3
DST_SUFFIX=$4
FIRST_INDEX=$5
LAST_INDEX=$6

if ! [ -d $DST_DIR ]; then
    mkdir $DST_DIR
fi

for (( i=$FIRST_INDEX; i<=$LAST_INDEX; i++ ))
do
    INPUT_PATH=`printf "$ORG_DIR/%d $ORG_PREFIX.nrrd" $i`
    OUTPUT_PATH=`printf "$DST_DIR/$DST_SUFFIX-%03d.nrrd" $i`
    if [ -f "$INPUT_PATH" ]; then
	echo "Copying "$INPUT_PATH"..."
	cp "$INPUT_PATH" "$OUTPUT_PATH"
    fi
done




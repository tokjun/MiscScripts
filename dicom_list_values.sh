#! /usr/local/bin/bash

#
# Usage:  dicom_list_values.sh <INPUT_DIR> <DICOM_TAG>
#
#   Ex)  dicom_extract_by_tag.sh . "0008,103e" "0008,0032"
#
#   This script extract the values for the specified two tags from every file in the foler and list them
#   Requires Bash > 3.x. on macOS (for associative array)


if [ "$#" -ne 3 ] || ! [ -d "$1" ]; then
  echo "Usage: $0 <INPUT_DIR> <TAG 1> <TAG 2>" >&2
  exit 1
fi

INPUT_DIR=$1
TAG_1=$2
TAG_2=$3

cd $INPUT_DIR

echo "Processing $INPUT_DIR ..."

LIST=`find $INPUT_DIR -depth 1 -type f`

for FILE in $LIST
do
    STUDY=`dcmdump +P '0020,0010' $FILE| sed -e 's/.*\[\(.*\)\].*/\1/'`
    SERIES=`dcmdump +P '0020,0011' $FILE| sed -e 's/.*\[\(.*\)\].*/\1/'`
    VALUE1=`dcmdump +P $TAG_1 $FILE| sed -e 's/.*\[\(.*\)\].*/\1/'`
    VALUE2=`dcmdump +P $TAG_2 $FILE| sed -e 's/.*\[\(.*\)\].*/\1/'`

    echo $STUDY,$SERIES,$VALUE1,$VALUE2
done


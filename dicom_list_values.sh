#! /usr/local/bin/bash

#
# Usage:  dicom_list_values.sh <INPUT_DIR> <depth> <DICOM_TAG>
#
#   Ex)  dicom_extract_by_tag.sh . 1 "0008,103e" "0008,0032"
#
#   This script extract the values for the specified two tags from every file in the foler and list them
#   Requires Bash > 3.x. on macOS (for associative array)

if [ "$#" -ne 4 ] || ! [ -d "$1" ]; then
  echo "Usage: $0 <INPUT_DIR> <depth> <TAG 1> <TAG 2>" >&2
  exit 1
fi

INPUT_DIR=$1
DEPTH=$2
TAG_1=$3
TAG_2=$4

echo "Processing $INPUT_DIR ..."

LIST=`find $INPUT_DIR -depth $DEPTH -type f`

if [$LIST == ""]; then
    LIST=$INPUT_DIR
fi

for _FILE in $LIST
do
    FILE="$_FILE"
    STUDY=`dcmdump +P '0020,0010' "$FILE"| sed -e 's/.*\[\(.*\)\].*/\1/'`
    SERIES=`dcmdump +P '0020,0011' "$FILE"| sed -e 's/.*\[\(.*\)\].*/\1/'`
    VALUE1=`dcmdump +P $TAG_1 "$FILE"| sed -e 's/.*\[\(.*\)\].*/\1/'`
    VALUE2=`dcmdump +P $TAG_2 "$FILE"| sed -e 's/.*\[\(.*\)\].*/\1/'`

    echo $STUDY,$SERIES,$VALUE1,$VALUE2
done


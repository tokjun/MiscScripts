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

unset AVALUE2
unset AFILENAME
declare -A AVALUE2
declare -A AFILEPATH

for FILEPATH in $LIST
do
    SIUID=_`dcmdump +P '0020,000E' $FILEPATH| sed -e 's/.*\[\(.*\)\].*/\1/'` #Series Instance UID
    VALUE2=`dcmdump +P $TAG_2 $FILEPATH| sed -e 's/.*\[\(.*\)\].*/\1/'`

    if [[ ${AVALUE2[$SIUID]} == "" ]]; then
	AVALUE2[$SIUID]="$VALUE2"
	AFILEPATH[$SIUID]="$FILEPATH"
    elif [[ ${AVALUE2[$SIUID]} > $VALUE2 ]]; then
	AVALUE2[$SIUID]=$VALUE2
	AFILEPATH[$SIUID]="$FILEPATH"
    fi
    echo ${AFILEPATH[$SIUID]}, $VALUE2
done

for key in "${!AVALUE2[@]}";
do
    SIUID=$key
    VALUE2=${AVALUE2[$SIUID]}
    FILE=${AFILEPATH[$SIUID]}
    STUDY=`dcmdump +P '0020,0010' $FILE| sed -e 's/.*\[\(.*\)\].*/\1/'`
    SERIES=`dcmdump +P '0020,0011' $FILE| sed -e 's/.*\[\(.*\)\].*/\1/'`
    VALUE1=`dcmdump +P $TAG_1 $FILE| sed -e 's/.*\[\(.*\)\].*/\1/'`
    
    echo $STUDY,$SERIES,$VALUE1,$VALUE2
done

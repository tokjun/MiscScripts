#! /bin/bash

#
# Usage:  dicom_edit_protocol_name.sh <INPUT_DIR> <PREFIX>
#
#   Ex)  dicom_extract_by_tag.sh . "TEMPLATE"
#

if [ "$#" -ne 2 ] || ! [ -d "$1" ]; then
  echo "Usage: $0 <INPUT_DIR> " >&2
  exit 1
fi

INPUT_DIR=$1
PREFIX=$2

LIST=`find $INPUT_DIR -depth 1 -type d`

for dir in $LIST
do
    echo "Processing $dir ..."

    DIRNAME=$(basename "$dir")
    export DEDNEWDESC=$PREFIX$DIRNAME

    # Study description
    #find $dir/* -type f -exec sh -c 'dcmodify -m "(0008,103e)=$DEDNEWDESC" {}' -- {} \;
    # Protocol Name
    find $dir/* -type f -exec sh -c 'dcmodify -m "(0018,1030)=$DEDNEWDESC" {}' -- {} \;

    
done
    


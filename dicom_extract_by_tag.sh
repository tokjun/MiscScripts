#! /bin/bash

#
# Usage:  dicom_extract_by_tag.sh <INPUT_DIR> <DICOM_TAG> <KEY>
#
#   Ex)  dicom_extract_by_tag.sh . "0008,103e" "TEMPLATE"
#

if [ "$#" -ne 3 ] || ! [ -d "$1" ]; then
  echo "Usage: $0 <INPUT_DIR> <DICOM_TAG> <KEY>" >&2
  exit 1
fi

INPUT_DIR=$1
export DEBDTAG=$2
export DEBDKEY=$3

LIST=`find $INPUT_DIR -depth 1 -type d`

echo $LIST

if [$LIST == ""]; then
    LIST=$INPUT_DIR
fi

for dir in $LIST
do
    echo "Processing $dir ..."
    export DEBDNEWDIR=$dir"-"$DEBDKEY
    mkdir $DEBDNEWDIR
    
    find $dir/* -type f -exec sh -c 'RET=`dcmdump -q +P "$DEBDTAG" "$1"`; if echo "$RET" | grep "$DEBDKEY" >/dev/null ; then cp "$1" "$DEBDNEWDIR"; fi' -- {} \;
    
done
    


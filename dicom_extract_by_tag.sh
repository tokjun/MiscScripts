#! /bin/bash

#
# Usage:  dicom_extract_by_tag.sh <INPUT_DIR> <DICOM_TAG> <KEY> <COMMAND>
#
#   Ex)  dicom_extract_by_tag.sh . "0008,103e" "TEMPLATE" cp
#   Do not add '/' at the end of <INPUT_DIR>

if [[ "$#" -ne 4 ]] || ! [[ -d "$1" ]]; then
  echo "Usage: $0 <INPUT_DIR> <DICOM_TAG> <KEY> <COMMAND>" >&2
  exit 1
fi

INPUT_DIR=$1
export DEBDTAG=$2
export DEBDKEY=$3
export COMMAND=$4

export GREPSTR="$DEBDKEY"

LIST=`find $INPUT_DIR -depth 1 -type d`

if [[ $LIST == "" ]]; then
    LIST=$INPUT_DIR
fi

# Extended regular expression -
# -r GNU
# -E FreeBSD, NetBSD, OpenBSD, and OS X
SUFFIX=`echo $DEBDKEY |sed -E 's/\;|\%/-/g'`


for dir in $LIST
do
    echo "Processing $dir ..."
    export DEBDNEWDIR=$dir"-"$SUFFIX
    mkdir $DEBDNEWDIR
    
    find $dir/* -type f -exec sh -c 'RET=`dcmdump -q +P "$DEBDTAG" "$1"`; if echo "$RET" | grep "$GREPSTR" >/dev/null ; then $COMMAND "$1" "$DEBDNEWDIR"; fi' -- {} \;
    
done
    


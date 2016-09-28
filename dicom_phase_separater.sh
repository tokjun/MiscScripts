#! /bin/bash
#
# Use this script to separate phase image from magnitude images. The script 
#
# Usage:  dicom_split.sh <ORG_DIR> <DST_DIR>
#

if [ "$#" -ne 2 ] || ! [ -d "$1" ]; then
    echo "Usage: $0 <ORG_DIR> <DST_DIR>" >&2
    exit 1
fi

ORG_DIR=$1
DST_DIR=$2


if ! [ -d $ORG_DIR ]; then
    echo $ORG_DIR "does not exist..."
    exit 1
fi

if ! [ -d $DST_DIR ]; then
    mkdir $DST_DIR
fi

echo "Processing "$ORG_DIR"..."
if ! [ -d $DST_DIR/MAG ]; then
    mkdir $DST_DIR/MAG
fi
if ! [ -d $DST_DIR/PH ]; then
    mkdir $DST_DIR/PH
fi
cd $DST_DIR
find ../$ORG_DIR/* -type f -exec sh -c 'RET=`dcmdump +P "0008,0008" $1`; if echo "$RET" | grep "M\\\NORM" >/dev/null ; then cp $1 MAG; else cp $1 PH; fi' -- {} \;
cd ..

    


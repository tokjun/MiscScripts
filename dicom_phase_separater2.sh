#! /bin/bash
#
# Use this script to separate phase image from real images. The script 
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
if ! [ -d $DST_DIR/RE ]; then
    mkdir $DST_DIR/RE
fi
if ! [ -d $DST_DIR/PH ]; then
    mkdir $DST_DIR/PH
fi

function sep_dcm ()
{
    while read line1; do
        RET=`dcmdump +P "0008,0008" $line1`
	if echo "$RET" | grep "P\\\DIS2D" >/dev/null ; then
	    cp $line1 ../$DST_DIR/PH
	else
	    cp $line1 ../$DST_DIR/RE
	fi
    done
}

cd $ORG_DIR
ls -p | grep -v / | sep_dcm


    


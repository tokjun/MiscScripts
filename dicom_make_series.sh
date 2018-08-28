#! /bin/bash

#
# Usage:  dicom_make_sereis.sh <INPUT_DIR> <PREFIX>
#
#   Ex)  dicom_make_series.sh . 105
#
#   The script scan the specified folder and unify the series numbers
#   of the all DICOM files.


if [ "$#" -ne 2 ] || ! [ -d "$1" ]; then
  echo "Usage: $0 <INPUT_DIR> <SERIES_NUMBER>" >&2
  exit 1
fi

INPUT_DIR=$1
export SERIES=$2

cd $INPUT_DIR

echo "Processing $INPUT_DIR ..."

# Series #
find * -type f -exec sh -c 'dcmodify -m "(0020,0011)=$SERIES" {}' -- {} \;
find * -type f -exec sh -c 'dcmodify -m "(0020,000e)=$SERIES" {}' -- {} \;
rm *.bak

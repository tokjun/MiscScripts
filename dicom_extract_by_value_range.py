#!/usr/bin/env python3

import os
import sys
import os.path
import argparse
import shutil

import pydicom
from pydicom.data import get_testdata_files


#
# Match DICOM attriburtes
#
def checkDICOMAttributes(path, tag, lowerLimitString, upperLimitString):

    # When match == True, the attributes must match the dictionary value.
    # When match == False, the attributes only need to contain the dictionary values
    dataset = pydicom.dcmread(path, specific_tags=None)

    key = tag.replace(',', '')
    
    if key in dataset:
        element = dataset[key]
        value = 0.0
        lowerLimitValue = 0.0
        upperLimitValue = 0.0

        try:
            value = float(element.value)
            if lowerLimitString != None:
                lowerLimitValue = float(lowerLimitString)
            if upperLimitString != None:
                upperLimitValue = float(upperLimitString)
        except ValueError:
            print("Could not convert a string to a numerical value.")
            return False
        
        if lowerLimitString and value < lowerLimitValue:
            return False
        if upperLimitString and value > upperLimitValue:
            return False
        
        return True

    else:
        return False



def main():
    
    parser = argparse.ArgumentParser(description='Extract DICOM files based on tags')
    parser.add_argument('tag', metavar='TAG', type=str, nargs=1,
                        help='Target DICOM tag (e.g. "0020,000E")')
    parser.add_argument('src', metavar='SRC_DIR', type=str, nargs=1,
                        help='source directory')
    parser.add_argument('dst', metavar='DST_DIR', type=str, nargs=1,
                        help='destination directory')
    parser.add_argument('-r', dest='recursive', action='store_const',
                        const=True, default=False,
                        help='search the source directory recursively')
    parser.add_argument('-M', dest='move', action='store_const',
                        const=True, default=False,
                        help='move file instead of copying')
    parser.add_argument('-l', dest='lower', default=None, help='lower limit')
    parser.add_argument('-u', dest='upper', default=None, help='upper limit')

    args = parser.parse_args()
    srcdir = args.src[0]
    dstdir = args.dst[0]
    tag = args.tag[0]
    lowerLimit = args.lower
    upperLimit = args.upper
    

    # Make the destination directory, if it does not exists.
    os.makedirs(dstdir, exist_ok=True)

    # Convert tags (e.g. "0020,000E=XXX") to dictionary ( {0x0020000E: XXXX})
    postfix = 0
    for root, dirs, files in os.walk(srcdir):
        for file in files:
            filepath = os.path.join(root, file)
            if checkDICOMAttributes(filepath, tag, lowerLimit, upperLimit):
                newfilepath = os.path.join(dstdir, file)
                dstfilepath = ''
                if os.path.exists(newfilepath):
                    filename, file_extension = os.path.splitext(file)
                    newfilename = filename + '_%04d' % postfix + file_extension
                    postfix = postfix + 1
                    dstfilepath = os.path.join(dstdir, newfilename)
                else:
                    dstfilepath = os.path.join(dstdir, file)
                if args.move:
                    print("Moving: %s" % filepath)
                    shutil.move(filepath, dstfilepath)
                else:
                    print("Copying: %s" % filepath)
                    shutil.copy(filepath, dstfilepath)
                
        if args.recursive == False:
            break
    
if __name__ == "__main__":
    main()




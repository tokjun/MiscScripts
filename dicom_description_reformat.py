#!/usr/bin/env python

import os
import sys
import os.path
import argparse
import shutil

import pydicom
from pydicom.data import get_testdata_files


#
# Generate description string based on DICOM tags
#
def generateDescription(path, tagDict):

    dataset = pydicom.dcmread(path, specific_tags=None)
    newdesc = ''
    
    for key in tagDict:
        tag = tagDict[key]
        element = dataset[tag]
        newdesc = newdesc + ' ' + key + '=' + str(element.value)
        
    return newdesc

def main():
    
    parser = argparse.ArgumentParser(description='Reformat DICOM description using specified DICOM tags')
    parser.add_argument('tags', metavar='TAG', type=str, nargs='+',
                        help='Pairs of variable name and DICOM tag separated by "=" (e.g. "TI=0018,0082")')
    parser.add_argument('src', metavar='SRC_DIR', type=str, nargs=1,
                        help='source directory')
    parser.add_argument('dst', metavar='DST_DIR', type=str, nargs=1,
                        help='destination directory')
    parser.add_argument('-r', dest='recursive', action='store_const',
                        const=True, default=False,
                        help='search the source directory recursively')

    args = parser.parse_args()
    srcdir = args.src
    dstdir = args.dst
    tagDict = {}

    if not os.path.isdir(dstdir[0]):
        sys.exit("Error: the destination directory does not exist.")
        
    # Convert tags (e.g. "0020,000E=XXX") to dictionary ( {0x0020000E: XXXX})
    for tag in args.tags:
        pair = tag.split('=')
        if len(pair) != 2:
            sys.exit('ERROR: Invalid argument: %s' % tag)
        tagHexStr = '0x' + pair[1].replace(',', '')
        tagNum = int(tagHexStr, 16)
        tagDict[pair[0]] = tagNum

    postfix = 0
    for root, dirs, files in os.walk(srcdir[0]):
        for file in files:
            filepath = os.path.join(root, file)
            newdesc = generateDescription(filepath, tagDict)
            print (newdesc)
            
            #newfilepath = os.path.join(dstdir[0], file)
            #dstfilepath = ''
            #if os.path.exists(newfilepath):
            #    filename, file_extension = os.path.splitext(file)
            #    newfilename = filename + '_%04d' % postfix + file_extension
            #    postfix = postfix + 1
            #    dstfilepath = os.path.join(dstdir[0], newfilename)
            #else:
            #    dstfilepath = os.path.join(dstdir[0], file)
            
            #print("Copying: %s" % filepath)
            #shutil.copy(filepath, dstfilepath)
                
        if args.recursive == False:
            break
    
if __name__ == "__main__":
    main()

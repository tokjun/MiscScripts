#!/usr/bin/env python3

import os
import sys
import os.path
import argparse
import shutil

import pydicom
from pydicom.data import get_testdata_files


#
# Count DICOM image - returns the number of times the identical image has been appeard previously
#
def countDICOMImage(path, taglist, imageCount):

    dataset = pydicom.dcmread(path, specific_tags=None)

    fFirstTime = True
    
    attrs = () # Tuple of attributes
    for tag in taglist:
        if tag in dataset:
            element = dataset[tag]
            attrs = attrs + (str(element.value),)
    if attrs in imageCount:
        imageCount[attrs] = imageCount[attrs] + 1
    else:
        imageCount[attrs] = 1

    return (imageCount[attrs] - 1)



def main():
    
    parser = argparse.ArgumentParser(description='Copy or move DICOM files and remove duplicated images.')
    parser.add_argument('tags', metavar='TAG', type=str, nargs='*',
                        help='DICOM tags. (Study Instance UID, Series Instance UID, and Image Instance Number are used in default, )')
    parser.add_argument('src', metavar='SRC_DIR', type=str, nargs=1,
                        help='source directory')
    parser.add_argument('dst', metavar='DST_DIR', type=str, nargs=1,
                        help='destination directory')
    parser.add_argument('-r', dest='recursive', action='store_const',
                        const=True, default=False,
                        help='search the source directory recursively')
    parser.add_argument('-m', dest='match', action='store_const',
                        const=True, default=False,
                        help='attributes must exactly match')
    parser.add_argument('-M', dest='move', action='store_const',
                        const=True, default=False,
                        help='move file instead of copying')


    args = parser.parse_args()
    srcdir = args.src
    dstdir = args.dst

    # Make the destination directory, if it does not exists.
    os.makedirs(dstdir[0], exist_ok=True)

    # The following tags are used to find identical image files in default
    #   - 0020,000D StudyInstanceUID
    #   - 0020,000E SeriesInstanceUID
    #   - 0020,0013 InstanceNumber

    # Default tag list
    tagStrList = ['0020,000D', '0020,000E',  '0020,0013']
    taglist = []
    for tagstr in tagStrList:
        tagHexStr = '0x' + tagstr.replace(',','')
        taglist.append(int(tagHexStr, 16))
        
    # Add tags specified by the user
    for tag in args.tags:
        tagHexStr = '0x' + tag.replace(',', '')
        taglist.append(int(tagHexStr, 16))

    imageCounts = {}

    postfix = 0
    for root, dirs, files in os.walk(srcdir[0]):
        for file in files:
            filepath = os.path.join(root, file)
            if countDICOMImage(filepath, taglist, imageCounts) == 0:
                newfilepath = os.path.join(dstdir[0], file)
                dstfilepath = ''
                if os.path.exists(newfilepath):
                    filename, file_extension = os.path.splitext(file)
                    newfilename = filename + '_%04d' % postfix + file_extension
                    postfix = postfix + 1
                    dstfilepath = os.path.join(dstdir[0], newfilename)
                else:
                    dstfilepath = os.path.join(dstdir[0], file)
                if args.move:
                    print("Moving: %s" % filepath)
                    shutil.move(filepath, dstfilepath)
                else:
                    print("Copying: %s" % filepath)
                    shutil.copy(filepath, dstfilepath)
            else:
                print("Found a duplicated image.")
                
        if args.recursive == False:
            break

    
if __name__ == "__main__":
    main()



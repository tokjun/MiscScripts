#!/usr/bin/env python3

import pydicom
from pydicom.data import get_testdata_files

import argparse
import os
import shutil

def getDICOMAttributes(path, tagNums):

    dataset = pydicom.dcmread(path, specific_tags=None)
    attrs = []

    for tagNum in tagNums:
        if tagNum in dataset:
            element = dataset[tagNum]
            attrs.append(element.value)
    return attrs

def main():
    
    parser = argparse.ArgumentParser(description='List DICOM attribute values. Only works for a single-slice image.')
    #parser.add_argument('tags', metavar='TAG', type=str, nargs='+',
    #                    help='DICOM Tags (e.g. "0020,000E")')
    parser.add_argument('tag', metavar='TAG', type=str, nargs=1,
                        help='DICOM Tag (e.g. "0020,000E")')
    parser.add_argument('dir', metavar='DIR', type=str, nargs=1,
                        help='source directory')
    parser.add_argument('-r', dest='recursive', action='store_const',
                        const=True, default=False,
                        help='search the source directory recursively')
    parser.add_argument('-t', dest='trash', default=None, help='Trash folder to keep the discarded files')
    
    args = parser.parse_args()
    srcdir = args.dir
    trashDir = args.trash
    tagNums = []

    f = None

    ## Convert tag string (e.g. "0020,000E") to tag number (0x0020000E)
    #for tag in args.tags:
    #    tagHexStr = '0x' + tag.replace(',', '')
    #    tagNum = int(tagHexStr, 16)
    #    tagNums.append(tagNum)

    tag = args.tag[0]
    tagHexStr = '0x' + tag.replace(',', '')
    tagNum = int(tagHexStr, 16)
    tagNums.append(tagNum)
    tagNums.append('0x00080032') # Time stamp

    ## Print header
    #linestr = ''
    #for tag in tagNums:
    #    linestr = linestr + hex(tag) + ","

    for root, dirs, files in os.walk(srcdir[0]):

        pathDict = {}
        acqTimeDict = {}
        
        for file in files:
            #if file.endswith(""):
            values = getDICOMAttributes(os.path.join(root, file), tagNums)

            #linestr = os.path.join(root, file) + ","

            if len(values) > 1:
                value = values[0]
                acqTime = values[1]
                if value in pathDict:
                    # Found previous image
                    print('Found a previous image value = %s, path= %s' % (value, os.path.join(root, file)))
                    # Check time stamp
                    fileToRemove = ''
                    if acqTime > acqTimeDict[value]: # The image is newer than the previously found
                        fileToRemove = pathDict[value]
                        pathDict[value] = os.path.join(root, file) # Record the path for the new image
                        acqTimeDict[value] = acqTime
                    else:
                        fileToRemove = os.path.join(root, file)
                        
                    # Remove
                    if trashDir:
                        trashPath = os.path.join(root, trashDir)
                        if not os.path.exists(trashPath):
                            os.makedirs(trashPath)
                        shutil.move(fileToRemove, trashPath)
                    else:
                        os.remove(fileToRemove)
                else:
                    # No previous image
                    pathDict[value] = os.path.join(root, file) # Record the path for the new image
                    acqTimeDict[value] = acqTime


        if args.recursive == False:
            break

if __name__ == "__main__":
    main()

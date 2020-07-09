#!/usr/bin/env python

import pydicom
from pydicom.data import get_testdata_files

import argparse
import os

def getDICOMAttributes(path, tagNums):

    dataset = pydicom.dcmread(path, specific_tags=None)
    attrs = []

    for tagNum in tagNums:
        if tagNum in dataset:
            element = dataset[tagNum]
            attrs.append(element.value)
    return attrs

def main():
    
    parser = argparse.ArgumentParser(description='List DICOM attribute values')
    parser.add_argument('tags', metavar='TAG', type=str, nargs='+',
                        help='DICOM Tags (e.g. "0020,000E")')
    parser.add_argument('dir', metavar='DIR', type=str, nargs=1,
                        help='source directory')
    parser.add_argument('-r', dest='recursive', action='store_const',
                        const=True, default=False,
                        help='search the source directory recursively')
    parser.add_argument('-p', dest='printpath', action='store_const',
                        const=True, default=False,
                        help='print path')
    parser.add_argument('-c', dest='countfile', action='store_const',
                        const=True, default=False,
                        help='count files')
    parser.add_argument('-o', dest='out', help='Output file (CSV format)')
    
    args = parser.parse_args()
    srcdir = args.dir
    outputFile = args.out
    tagNums = []

    f = None
    if outputFile:
        f = open(outputFile, "w")

    # Convert tag string (e.g. "0020,000E") to tag number (0x0020000E)
    for tag in args.tags:
        tagHexStr = '0x' + tag.replace(',', '')
        tagNum = int(tagHexStr, 16)
        tagNums.append(tagNum)

    # Print header
    linestr = ''
    for tag in tagNums:
        linestr = linestr + hex(tag) + ","
    if outputFile:
        f.write(linestr[0:-1] + '\n')
    else:
        print(linestr[0:-1])

    for root, dirs, files in os.walk(srcdir[0]):

        count = 0
        
        for file in files:
            #if file.endswith(""):
            values = getDICOMAttributes(os.path.join(root, file), tagNums)
            linestr = ''
            
            if args.printpath:
                linestr = os.path.join(root, file) + ","

            if len(values) > 0:
                count = count + 1
            
            for value in values:
                linestr = linestr + '"%s"' % value + ","
                
            if outputFile:
                f.write(linestr[0:-1] + '\n')
            else:
                if linestr != '' and not args.countfile:
                    print(linestr[0:-1])

        if args.countfile and count > 0:
            print("%s, %d" % (root, count))
                
        if args.recursive == False:
            break

    if outputFile:
        f.close()
    
if __name__ == "__main__":
    main()

#!/usr/bin/env python3

# anonymize.py
"""Read a dicom file (or directory of files), partially "anonymize" it (them),
by replacing Person names, patient id, optionally remove curves
and private tags, and write result to a new file (directory)
This is an example only; use only as a starting point.
"""
#
# Original code was retrieved from pydicom:
#
# Copyright (c) 2008-2012 Darcy Mason
# This file is part of pydicom, relased under an MIT license.
#    See the file license.txt included with this distribution, also
#    available at http://pydicom.googlecode.com
# Use at your own risk!!
# Many more items need to be addressed for proper de-identifying DICOM data.
# In particular, note that pixel data could have confidential data "burned in"
# Annex E of PS3.15-2011 DICOM standard document details what must be done to
# fully de-identify DICOM data

import os
import os.path
import argparse
import pydicom
import sys


def anonymize(filename, output_filename, new_person_name="anonymous",
              new_patient_id="id", remove_curves=False, remove_private_tags=False):
    """Replace data element values to partly anonymize a DICOM file.
    Note: completely anonymizing a DICOM file is very complicated; there
    are many things this example code does not address. USE AT YOUR OWN RISK.
    """

    # Define call-back functions for the dataset.walk() function
    def PN_callback(ds, data_element):
        """Called from the dataset "walk" recursive function for all data elements."""
        if data_element.VR == "PN":
            data_element.value = new_person_name

    def curves_callback(ds, data_element):
        """Called from the dataset "walk" recursive function for all data elements."""
        if data_element.tag.group & 0xFF00 == 0x5000:
            del ds[data_element.tag]

    # Load the current dicom file to 'anonymize'
    dataset = pydicom.read_file(filename)

    # Remove patient name and any other person names
    dataset.walk(PN_callback)

    # Change ID
    dataset.PatientID = new_patient_id

    # Remove data elements (should only do so if DICOM type 3 optional)
    # Use general loop so easy to add more later
    # Could also have done: del ds.OtherPatientIDs, etc.
    for name in ['OtherPatientIDs', 'OtherPatientIDsSequence']:
        if name in dataset:
            delattr(dataset, name)

    # Same as above but for blanking data elements that are type 2.
    for name in ['PatientBirthDate']:
        if name in dataset:
            dataset.data_element(name).value = ''

    # Remove private tags if function argument says to do so. Same for curves
    if remove_private_tags:
        dataset.remove_private_tags()
    if remove_curves:
        dataset.walk(curves_callback)

    # write the 'anonymized' DICOM out under the new filename
    dataset.save_as(output_filename)

# Can run as a script:
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Anonymize DICOM files in the specified folder. ')
    #parser.add_argument('tags', metavar='TAG', type=str, nargs='+',
    #                    help='Pairs of variable name and DICOM tag separated by "=" (e.g. "TI=0018,0082")')
    parser.add_argument('src', metavar='SRC_DIR', type=str, nargs=1,
                        help='source directory')
    parser.add_argument('dst', metavar='DST_DIR', type=str, nargs=1,
                        help='destination directory')
    parser.add_argument('-r', dest='recursive', action='store_const',
                        const=True, default=False,
                        help='search the source directory recursively')
    parser.add_argument('-p', dest='private', action='store_const',
                        const=True, default=False,
                        help='Remoeve private tags')

    args = parser.parse_args()
    srcdir = args.src
    dstdir = args.dst

    ## Make sure that the source directory exists.
    if os.path.isdir(srcdir[0]) == False:
        exit()
    
    ## Make sure that the destination directory exists.
    os.makedirs(dstdir[0], exist_ok=True)

    
    postfix = 0
    
    if args.recursive: # If the recursive option is enabled.
        for root, dirs, files in os.walk(srcdir[0]):
            for file in files:
                relpath = os.path.relpath(root, srcdir[0])
                srcfilepath = os.path.join(root, file)
                dstdirpath = os.path.join(dstdir[0], relpath)
                dstfilepath = os.path.join(dstdirpath, file)
                os.makedirs(dstdirpath, exist_ok=True)
                print("%s -> %s" % (srcfilepath, dstfilepath))
                anonymize(srcfilepath, dstfilepath, remove_private_tags=args.private)
    else:             # If the recursive option is disabled
        for file in os.listdir(srcdir[0]):
            if os.path.isfile(os.path.join(srcdir[0], file)):
                srcfilepath = os.path.join(srcdir[0], file)
                dstfilepath = os.path.join(dstdir[0], file)
                print("%s -> %s" % (srcfilepath, dstfilepath))
                anonymize(srcfilepath, dstfilepath,  remove_private_tags=args.private)

    print("Done.")


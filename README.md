MiscScripts
===========

Introduction
------------
This repository contains my utility scripts for my research activity. Please note that I'm currently converting the DICOM shell scripts to Python scripts and there are several commands that are implemented in Python and BASH scripts. BASH scripts are left in this folder just for compatibility and will not be supported in the future. 

Installation
------------

### Python
The Python scripts that manipulate DICOM files depend on [pydicom](https://pydicom.github.io/). To install pydicom in your environment:

~~~~
$ pip install -U pydicom
~~~~

See [pydicom Installation page](https://pydicom.github.io/pydicom/stable/getting_started.html#installing) for detail.


Individual Commands
-------------------

## dicom_extract_by_tag.sh

This scrip extracts DICOM files with a specified DICOM Tag in the input directory tree.

For example, if you want to extract DICOM files that have a string "TEMPLATE" in the series description (0008,103e), run:

  dicom_extract_by_tag.sh /path/to/inputdir "0008,103e" "TEMPLATE"

where /path/to/inputdir is the path to the input directory. The script will create output directories named /path/to/inputdir/*-TEMPLATE for each sub-directories under the input directory.

Make sure that you can run a "dcmdump" command in your environment.


## dicom_split.sh

This scirpt demonstrates how to separate DICOM files based on Tag (0008,0008). It checks the types of images (either magnitude or phase) and copy them to sub-folders depending on their types (either MAG/ or PH/). Once it copies all the files to the sub-folders, it rename and move the sub-folders to the upper level.


Some Useful DICOM Tags...
-------------------------

- (0051,100f) : Coil element (Siemens)

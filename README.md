MiscScripts
===========

Introduction
------------
This repository contains utility scripts for my research activities. I used to make all the scripts in BASH, but have started migrating to Python scripts. BASH scripts are still in the repository just for compatibility, but will be phased out in the future.

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

## dicom_extract_by_tag.py

This scrip extracts DICOM files with a specified DICOM Tag in the input directory tree.

Example: Consider copying DICOM files that contains real images from a coil element "BO2" to "dicom/R" folder. Since the coil element and real/imaginal information for Siemens DICOM header are (0051,100f) and (0051,1016) respectively, the files can be extracted with the following command:

~~~~
$ dicom_extract_by_tag.py -r -m "0051,100f=BO2" "0051,1016=R/DIS2D" <source folder> "./dicom/R"
~~~~

To show the full list of the arguments, run:

~~~~
$ dicom_extract_by_tag.py -h
~~~~


Some Useful DICOM Tags...
-------------------------

- Siemens MR Header
  - (0051,100f) : Coil element (Siemens)
  - (0051,1016) : Real/Imaginal (e.x. "R/DIS2D": real; "P/DIS2D": phase)

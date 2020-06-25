# TG_OpenBCI_newCyton
This is a minimalist Python module for controlling the biomedical signal sampling board OpenBCI Cyton. This module aims to recover the functionality of the Python code available in the OpenBCI site, specifically for the control of the OpenBCI Cyton board in the Python language. Originally the code was deprecated, as it can be seen on this link: https://docs.openbci.com/docs/09Deprecated/Python , but through this project, part of its functionality was restored.

If you are planning on using the OpenBCI_GUI, be aware that it does not work on 32-bit operating systems, as it was tested in this project.



The "newCyton.py" file contains the functions to control the OpenBCI Cyton board, such as customizing the sampling channels and changing the sample rate. The documentation and comments describe the possible functions you can send to control your Cyton.


The "useCyton.py" file is used as an interface with the OpenBCI Cyton board, using the functions available in newCyton.py.


Within the "docs" folder, there is documentation available for the files, made with the Sphinx extension for Python.


This project is under the GNU General Public License version 3.

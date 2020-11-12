# PyDocScanner
## Requirements
- Python 3 (tested on Python 3.8)
- tesseract
- opencv-python built with gpu (if you won't use super resolution regular opencv-python will do it)
## Installation
Install with Git:  
```sh
$ git clone https://github.com/Yuvix25/PyDocScanner.git
$ cd PyDocScanner
$ python setup.py install
```
Install with pip - Coming Soon
# Usage
```python
# imports
from PyDocScanner import Scan
import cv2

# read image from file:
image = cv2.imread("path_to_file")

# scan the document with all features (color filter, super resolution, and ocr):
document_image, text = Scan(image, apply_color_filter=True, do_super_reso=True, do_ocr=True)

# scan the document without ocr:
document_image = Scan(image, apply_color_filter=True, do_super_reso=True, do_ocr=False)
```
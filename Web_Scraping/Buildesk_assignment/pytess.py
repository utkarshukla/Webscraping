import pytesseract as tess
import sys
import re
import argparse
try:
    import Image
except ImportError:
    from PIL import Image
from subprocess import check_output

im = Image.open('Screenshot from 2020-03-28 18-16-31.png')
captcha = tess.image_to_string(im)
ls = captcha.split('\n')
for x in ls:
	if x.find('TOTAL ESTIMATED VALUE OF CLAIM') != -1:
		total = re.findall(r'[$][\d|,|.]+',x)
print(total)
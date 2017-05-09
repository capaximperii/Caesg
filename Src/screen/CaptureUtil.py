import os
import cv2
import tempfile
import numpy as np
import pytesseract
from PIL import Image
from resizeimage import resizeimage


class CaptureUtil:
    """
    Wrapper class for pytesseract and binary.

    """
    def __init__(self):
        """
        Constructor takes no argument.
        """
        self.path = tempfile.mkdtemp()

    def get_string(self, img_path):
        """
        Return all strings in an image as a string.

        """
        basewidth = 6400 # works better on linux
        # basewidth = 3096 # works better on windows
        img = Image.open(img_path)
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        img = img.resize((img.size[0], img.size[1]), Image.ANTIALIAS)
        img.save(os.path.join(self.path, 'zoomed.jpg'))
        img = cv2.imread(os.path.join(self.path, 'zoomed.jpg'))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)
        cv2.imwrite(os.path.join(self.path, "removed_noise.png"), img)
        # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #                             cv2.THRESH_BINARY, 11, 2)
        cv2.imwrite(os.path.join(self.path, "thres.png"), img)
        result = pytesseract.image_to_string(Image.open(os.path.join(self.path, "thres.png")), lang="eng")
        return result




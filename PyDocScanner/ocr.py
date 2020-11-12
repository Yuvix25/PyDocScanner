import cv2
import pytesseract
from PIL import Image
import os

def ocr(image):
    temp_save_dir = "./temp_img.jpg"
    cv2.imwrite(temp_save_dir, image)

    text = pytesseract.image_to_string(Image.open(temp_save_dir))
    os.remove(temp_save_dir)
    return text

if __name__ == "__main__":
    ocr(cv2.imread("./test_img1.jpg"))
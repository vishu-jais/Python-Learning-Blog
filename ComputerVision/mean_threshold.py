"""Mean and Otsu thresholding demo."""
from utils.common_imports import cv2, np, imshow
import sys
def mean_threshold(image_path, block_size=11, C=2):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f'Unable to read image: {image_path}')
    _, otsu = cv2.threshold(img,0,255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    mean_thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, C)
    combined = np.hstack([img, otsu, mean_thresh])
    return combined
if __name__=='__main__':
    if len(sys.argv)<2:
        print('Usage: python mean_threshold.py path/to/image.jpg'); sys.exit(1)
    out = mean_threshold(sys.argv[1])
    imshow('Original | Otsu | Adaptive Mean', out)
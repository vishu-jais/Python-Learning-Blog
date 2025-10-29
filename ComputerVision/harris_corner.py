"""Harris Corner Detection example."""
from utils.common_imports import cv2, np, imshow
import sys
def detect_harris_corners(image_path, block_size=2, ksize=3, k=0.04, thresh=0.01):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f'Unable to read image: {image_path}')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, block_size, ksize, k)
    dst = cv2.dilate(dst, None)
    img_corners = img.copy()
    img_corners[dst > thresh * dst.max()] = [0,0,255]
    return img_corners
if __name__=='__main__':
    if len(sys.argv)<2:
        print('Usage: python harris_corner.py path/to/image.jpg'); sys.exit(1)
    out = detect_harris_corners(sys.argv[1])
    imshow('Harris Corners', out)
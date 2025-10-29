"""Create a 2x2 mosaic from up to 4 images."""
from utils.common_imports import cv2, np, imshow
import sys
from pathlib import Path
def make_mosaic(image_paths, size=(256,256)):
    imgs = []
    for p in image_paths:
        img = cv2.imread(str(p))
        if img is None:
            raise FileNotFoundError(f'Unable to read image: {p}')
        img = cv2.resize(img, size)
        imgs.append(img)
    while len(imgs)<4:
        imgs.append(imgs[-1].copy())
    top = np.hstack((imgs[0], imgs[1]))
    bottom = np.hstack((imgs[2], imgs[3]))
    mosaic = np.vstack((top,bottom))
    return mosaic
if __name__=='__main__':
    if len(sys.argv)<2:
        print('Usage: python mosaic_augmentation.py path/to/image1 [image2 ...]'); sys.exit(1)
    out = make_mosaic(sys.argv[1:])
    imshow('Mosaic', out)
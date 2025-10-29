"""Image flipping augmentation demo."""
from utils.common_imports import cv2, np, imshow
import sys
def flip_augments(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f'Unable to read image: {image_path}')
    h_flip = cv2.flip(img,1)
    v_flip = cv2.flip(img,0)
    both = cv2.flip(img,-1)
    combined = np.hstack([img, h_flip, v_flip, both])
    return combined
if __name__=='__main__':
    if len(sys.argv)<2:
        print('Usage: python flip_augmentation.py path/to/image.jpg'); sys.exit(1)
    out = flip_augments(sys.argv[1])
    imshow('Original | H | V | Both', out)
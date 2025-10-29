"""Haralick texture descriptors using scikit-image."""
from utils.common_imports import cv2, np, imshow
import sys
try:
    from skimage.feature import greycomatrix, greycoprops
except Exception:
    raise ImportError('scikit-image required. Install with `pip install scikit-image`')
def compute_haralick(image_path, distances=[1], angles=[0], levels=256):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f'Unable to read image: {image_path}')
    img = (img / (256 // levels)).astype(np.uint8)
    glcm = greycomatrix(img, distances=distances, angles=angles, symmetric=True, normed=True)
    contrast = greycoprops(glcm, 'contrast')
    results = {'contrast': contrast.mean()}
    return results
if __name__=='__main__':
    if len(sys.argv)<2:
        print('Usage: python haralick_descriptors.py path/to/image'); sys.exit(1)
    res = compute_haralick(sys.argv[1])
    print('Haralick (mean):', res)
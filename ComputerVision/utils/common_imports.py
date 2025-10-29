"""Common imports for ComputerVision scripts."""
import sys
try:
    import cv2
except Exception as e:
    raise ImportError('OpenCV (cv2) is required. Install with `pip install opencv-python`') from e
try:
    import numpy as np
except Exception as e:
    raise ImportError('NumPy is required. Install with `pip install numpy`') from e
try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None
def imshow(title, image):
    if plt:
        plt.figure(figsize=(6,6))
        if image.ndim==2:
            plt.imshow(image, cmap='gray')
        else:
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title(title)
        plt.axis('off')
        plt.show()
    else:
        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

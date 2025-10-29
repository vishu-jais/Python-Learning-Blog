"""Horn-Schunck optical flow (simple educational impl)."""
from utils.common_imports import cv2, np, imshow
import sys
def horn_schunck(img1, img2, alpha=1.0, num_iter=100):
    u = np.zeros(img1.shape)
    v = np.zeros(img1.shape)
    img1 = img1.astype(np.float32)
    img2 = img2.astype(np.float32)
    Ix = cv2.Sobel(img1, cv2.CV_32F,1,0,ksize=3)
    Iy = cv2.Sobel(img1, cv2.CV_32F,0,1,ksize=3)
    It = img2 - img1
    kernel = np.array([[1/12,1/6,1/12],[1/6,0,1/6],[1/12,1/6,1/12]], dtype=np.float32)
    for _ in range(num_iter):
        u_avg = cv2.filter2D(u, -1, kernel)
        v_avg = cv2.filter2D(v, -1, kernel)
        term = (Ix * u_avg + Iy * v_avg + It) / (alpha**2 + Ix**2 + Iy**2)
        u = u_avg - Ix * term
        v = v_avg - Iy * term
    return u, v
if __name__=='__main__':
    if len(sys.argv)<3:
        print('Usage: python horn_schunck.py frame1 frame2'); sys.exit(1)
    f1 = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    f2 = cv2.imread(sys.argv[2], cv2.IMREAD_GRAYSCALE)
    if f1 is None or f2 is None:
        raise FileNotFoundError('Provide two image files')
    u, v = horn_schunck(f1, f2)
    step = 16
    h, w = f1.shape
    vis = cv2.cvtColor(f1, cv2.COLOR_GRAY2BGR)
    for y in range(0,h,step):
        for x in range(0,w,step):
            pt1 = (x,y)
            dx = int(u[y,x]*5)
            dy = int(v[y,x]*5)
            pt2 = (x+dx, y+dy)
            cv2.arrowedLine(vis, pt1, pt2, (0,255,0),1, tipLength=0.3)
    imshow('Optical Flow (Horn-Schunck)', vis)
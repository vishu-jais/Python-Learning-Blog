

import cv2
import numpy as np


classNames = {0: 'background',
              1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
              5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat',
              9: 'chair', 10: 'cow', 11: 'diningtable', 12: 'dog',
              13: 'horse', 14: 'motorbike', 15: 'person', 16: 'pottedplant',
              17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor'}


model = "MobileNetSSD_deploy.caffemodel"
prototxt = "MobileNetSSD_deploy.prototxt"


net = cv2.dnn.readNetFromCaffe(prototxt, model)

image_path = "example.jpg"   
image = cv2.imread(image_path)
(h, w) = image.shape[:2]


blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)


net.setInput(blob)
detections = net.forward()


for i in range(detections.shape[2]):
    confidence = detections[0, 0, i, 2]

    
    if confidence > 0.4:
        idx = int(detections[0, 0, i, 1])
        label = classNames.get(idx, "Unknown")
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

      
        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
        text = f"{label}: {confidence*100:.1f}%"
        cv2.putText(image, text, (startX, startY - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
cv2.imshow("Object Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

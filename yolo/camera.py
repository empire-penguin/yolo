import cv2

# cv2.setNumThreads(0)

cap = cv2.VideoCapture(0)

ret, frame = cap.read()
print(ret)

cap.release()
cv2.destroyAllWindows()
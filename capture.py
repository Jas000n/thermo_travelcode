import cv2
def capture():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    return frame

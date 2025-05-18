import cv2
from followIcon import getRedWhite, ssimCheck

def scaleImage(image, scale):
    width = int(image.shape[1] * scale)
    height = int(image.shape[0] * scale)
    return cv2.resize(image, (width, height))

# Open the default camera
cam = cv2.VideoCapture(0)
redT = cv2.imread('template/red.png', cv2.IMREAD_GRAYSCALE)
whiteT = cv2.imread('template/white.png', cv2.IMREAD_GRAYSCALE)

while True:
    ret, frame = cam.read()
    if not ret:
        continue
    frame = scaleImage(frame, 0.5)

    red, white = getRedWhite(frame)
    
    if ssimCheck(red, redT) > 0.7 and ssimCheck(white, whiteT)> 0.7:
        frame = cv2.rectangle(frame, (460, 583), (533, 670), (0,255,0), 10)
    else:
        # frame = cv2.rectangle(frame, (639, 485), (665, 511), (0,0,255), 10)
        frame = cv2.rectangle(frame, (460, 583), (533, 670), (0,0,255), 10)

    # Display the captured frame
    cv2.imshow('Camera', frame)
    cv2.imshow('red', red)
    cv2.imshow('white', white)
    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and writer objects
cam.release()
cv2.destroyAllWindows()
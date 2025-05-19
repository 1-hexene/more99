import cv2
import numpy as np
from followIcon import follow_icon_Check

def scaleImage(image, scale):
    width = int(image.shape[1] * scale)
    height = int(image.shape[0] * scale)
    return cv2.resize(image, (width, height))

# Open the default camera
cam = cv2.VideoCapture(0)
template = scaleImage(cv2.imread('template/original_fc.png', cv2.IMREAD_GRAYSCALE), 0.39)
w, h = template.shape[:2]
print(template.shape)

while True:
    ret, frame = cam.read()
    if not ret:
        continue

    frame = scaleImage(frame, 0.5)
    
    # 提取 ROI（保持彩色）
    roi = frame[500:800, 485:511]

    # 颜色范围（BGR）
    lower_red = np.array([60, 0, 220])     # 注意顺序是BGR，不是RGB
    upper_red = np.array([100, 40, 255])

    lower_white = np.array([220, 200, 230])
    upper_white = np.array([255, 255, 255])

    # 创建红色和白色掩码
    mask_red = cv2.inRange(roi, lower_red, upper_red)
    mask_white = cv2.inRange(roi, lower_white, upper_white)
    kernel = np.ones((3,3), np.int8)
    mask_red = cv2.dilate(mask_red, kernel)
    mask_white = cv2.dilate(mask_white, kernel)
    mask = cv2.bitwise_or(mask_red, mask_white)

    filtered_roi = cv2.bitwise_and(roi, roi, mask=mask)

    # 将处理后的 ROI 转为灰度图用于模板匹配
    gray_roi = cv2.cvtColor(filtered_roi, cv2.COLOR_BGR2GRAY)

    # 模板匹配
    res = cv2.matchTemplate(gray_roi, template, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    confidence = 1 - min_val

    if confidence >= 0.6:
        top_left = (min_loc[0] + 485, min_loc[1] + 500)
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(frame, top_left, bottom_right, (255, 0, 0), 3)

    # 显示结果
    cv2.imshow('frame', frame)
    cv2.imshow('roi', gray_roi)  # 显示处理后的 ROI

    if cv2.waitKey(1) == ord('q'):
        break


# Release the capture and writer objects
cam.release()
cv2.destroyAllWindows()
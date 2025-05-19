# %%
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


def getRedWhite(image):

    # === 2. 提取固定区域 ===
    roi = image[639:665, 485:511]  # [y1:y2, x1:x2]
    cv2.imshow('roi', roi)
    roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)

    # === 3. 定义颜色范围（RGB）===
    lower_red = np.array([220, 0, 60])
    upper_red = np.array([255, 40, 100])

    lower_white = np.array([230, 200, 220])
    upper_white = np.array([255, 255, 255])

    # === 4. 创建遮罩并应用 ===
    mask_red = cv2.inRange(roi_rgb, lower_red, upper_red)
    mask_white = cv2.inRange(roi_rgb, lower_white, upper_white)
    # mask_combined = cv2.bitwise_or(mask_red, mask_white)

    # roi_masked = cv2.bitwise_and(roi_rgb, roi_rgb, mask=mask_combined)
    # cv2.imshow("white", mask_white)
    # cv2.imshow("red", mask_red)

    return mask_red, mask_white


def follow_icon_Check(img, template):
    
 
    # 提取 ROI（保持彩色）
    roi = img[500:800, 485:511]

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

    return confidence


if __name__ == "__main__":
    image = cv2.imread('images/normal.png')
    redT = cv2.imread('template/red.png', cv2.IMREAD_GRAYSCALE)
    whiteT = cv2.imread('template/white.png', cv2.IMREAD_GRAYSCALE)
    red, white = getRedWhite(image)
    cv2.imshow("image", image)
    cv2.imshow("white", white)
    cv2.imshow("red", red)
    cv2.imshow("whiteT", whiteT)
    cv2.imshow("redT", redT)
    while cv2.waitKey(1) != ord('q'):
        pass

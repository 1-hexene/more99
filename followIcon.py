# %%
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


def getRedWhite(image):

    if image is None:
        raise ValueError("图像加载失败")

    # === 2. 提取固定区域 ===
    roi = image[639:665, 485:511]  # [y1:y2, x1:x2]
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


def ssimCheck(img, template):
    resized_img = cv2.resize(img, template.shape)
    score, _ = ssim(resized_img, template, full=True)
    # print("SSIM 相似度分数:", score)
    return score


if __name__ == "__main__":
    image = cv2.imread('Camera_screenshot_16.05.2025.png')
    redT = cv2.imread('template/red.png', cv2.IMREAD_GRAYSCALE)
    whiteT = cv2.imread('template/white.png', cv2.IMREAD_GRAYSCALE)
    red, white = getRedWhite(image)
    cv2.imshow("white", white)
    cv2.imshow("red", red)
    cv2.imshow("whiteT", whiteT)
    cv2.imshow("redT", redT)
    while cv2.waitKey(1) != ord('q'):
        pass
    ssimCheck(red,redT)
    ssimCheck(white, whiteT)

import cv2

# 读取图像
img = cv2.imread('baby.png')

# 显示图像
cv2.imshow('Original Image', img)

# 保存图像
cv2.imwrite('output.jpg', img)

cv2.waitKey(0)
cv2.destroyAllWindows()

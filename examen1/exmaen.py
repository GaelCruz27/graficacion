import cv2
import numpy as np

# ==============================
# MISION 1
# ==============================

img = cv2.imread("m1_oscura.png", cv2.IMREAD_GRAYSCALE)

alto, ancho = img.shape
m1_raw = np.zeros((alto, ancho), dtype=np.uint8)

for y in range(alto):
    for x in range(ancho):
        valor = int(img[y, x]) * 50
        if valor > 255:
            valor = 255
        m1_raw[y, x] = valor

cv2.imwrite("m1_raw.png", m1_raw)

m1_opencv = np.clip(img.astype(np.uint16) * 50, 0, 255).astype(np.uint8)
cv2.imwrite("m1_opencv.png", m1_opencv)

cv2.imshow("Original", img)
cv2.imshow("Mision 1 - Raw", m1_raw)
cv2.imshow("Mision 1 - OpenCV", m1_opencv)


# ==============================
# MISION 2
# ==============================

mitad1 = cv2.imread("m2_mitad1.png")
mitad2 = cv2.imread("m2_mitad2.png")

lienzo = np.ones((400, 400, 3), dtype=np.uint8) * 255

lienzo[0:200, 0:400] = mitad1

h, w = mitad2.shape[:2]
centro = (w // 2, h // 2)

M = cv2.getRotationMatrix2D(centro, 180, 1.0)
mitad2_rotada = cv2.warpAffine(mitad2, M, (w, h))

lienzo[200:400, 0:400] = mitad2_rotada

cv2.imwrite("m2_qr_reconstruido.png", lienzo)

cv2.imshow("QR reconstruido", lienzo)

cv2.waitKey(0)
cv2.destroyAllWindows()
import cv2
import numpy as np
import math


# ==============================
# MISION 1
# ==============================

img = cv2.imread("/Users/josecruz/graficacion/examen1/m1_oscura.png", cv2.IMREAD_GRAYSCALE)

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

# ==============================
# MISION 3
# ==============================

sello = np.zeros((500, 500, 3), np.uint8)

sello[:] = (50, 20, 20)

centro = (250, 250)
radio = 100
cv2.circle(sello, centro, radio, (0, 255, 255), 3)

cv2.rectangle(sello, (200, 200), (300, 300), (0, 0, 255), -1)

cv2.line(sello, (0, 0), (500, 500), (255, 255, 255), 2)
cv2.line(sello, (500, 0), (0, 500), (255, 255, 255), 2)

cv2.imwrite("m3_sello_forjado.png", sello)

cv2.imshow("El Sello Biometrico", sello)

# ==============================
# MISION 4
# ==============================


img = cv2.imread("m4_ruido.png")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

bajo = np.array([80, 100, 100])
alto = np.array([100, 255, 255])

mascara = cv2.inRange(hsv, bajo, alto)

cv2.imwrite("m4_mensaje.png", mascara)

cv2.imshow("Imagen original", img)
cv2.imshow("Mascara CYAN", mascara)


# ==============================
# MISION 5
# ==============================

lienzo = np.zeros((500, 500, 3), dtype=np.uint8)

t = 0

while t <= 6.28:

    x = int(250 + 200 * math.sin(3 * t))
    y = int(250 + 200 * math.sin(4 * t))

    cv2.circle(lienzo, (x, y), 1, (255, 255, 255), -1)

    t += 0.01

cv2.imwrite("m5_curva_parametrica.png", lienzo)

cv2.imshow("Mision 5 - Curva Parametrica", lienzo)

cv2.waitKey(0)
cv2.destroyAllWindows()
import cv2
import numpy as np
import math
import time

def guardar(nombre, img):
    cv2.imwrite(nombre, img)
    print(f"[OK] Guardado: {nombre}")

def medir_tiempo(func, *args, **kwargs):
    t0 = time.perf_counter()
    resultado = func(*args, **kwargs)
    t1 = time.perf_counter()
    return resultado, (t1 - t0)

def mision1_raw(img, tx=300, ty=200):
    h, w = img.shape[:2]
    destino = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            nx = x + tx
            ny = y + ty
            if 0 <= nx < w and 0 <= ny < h:
                destino[ny, nx] = img[y, x]
    return destino

def mision1_opencv(img, tx=300, ty=200):
    h, w = img.shape[:2]
    M = np.float32([[1, 0, tx], [0, 1, ty]])
    return cv2.warpAffine(img, M, (w, h))

def mision2_raw(img, angulo_grados=-45):
    h, w = img.shape[:2]
    cx = w / 2.0
    cy = h / 2.0
    destino = np.zeros_like(img)
    theta = math.radians(angulo_grados)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    for y_dst in range(h):
        for x_dst in range(w):
            x_shift = x_dst - cx
            y_shift = y_dst - cy
            x_src = x_shift * cos_t + y_shift * sin_t + cx
            y_src = -x_shift * sin_t + y_shift * cos_t + cy
            x_src_i = int(round(x_src))
            y_src_i = int(round(y_src))
            if 0 <= x_src_i < w and 0 <= y_src_i < h:
                destino[y_dst, x_dst] = img[y_src_i, x_src_i]
    return destino

def mision2_opencv(img, angulo_grados=-45):
    h, w = img.shape[:2]
    centro = (w / 2.0, h / 2.0)
    M = cv2.getRotationMatrix2D(centro, angulo_grados, 1.0)
    return cv2.warpAffine(img, M, (w, h))

def extraer_recorte_central(img, tam=200):
    h, w = img.shape[:2]
    cx = w // 2
    cy = h // 2
    mitad = tam // 2
    return img[cy - mitad:cy + mitad, cx - mitad:cx + mitad]

def mision3_raw_vecino_cercano(img_crop, escala_x=5, escala_y=5):
    h, w = img_crop.shape[:2]
    new_h = h * escala_y
    new_w = w * escala_x
    destino = np.zeros((new_h, new_w, 3), dtype=np.uint8)
    for y in range(new_h):
        for x in range(new_w):
            src_x = x // escala_x
            src_y = y // escala_y
            destino[y, x] = img_crop[src_y, src_x]
    return destino

def mision3_opencv(img_crop, escala_x=5, escala_y=5):
    return cv2.resize(img_crop, None, fx=escala_x, fy=escala_y, interpolation=cv2.INTER_CUBIC)

def main():
    img1 = cv2.imread("vehiculo.jpg")
    if img1 is not None:
        r1_raw, t1_raw = medir_tiempo(mision1_raw, img1, 300, 200)
        r1_cv, t1_cv = medir_tiempo(mision1_opencv, img1, 300, 200)
        guardar("m1_raw.png", r1_raw)
        guardar("m1_opencv.png", r1_cv)
        print(f"Misión 1 - Raw: {t1_raw:.6f} s")
        print(f"Misión 1 - OpenCV: {t1_cv:.6f} s")
    else:
        print("Falta vehiculo.jpg")

    img2 = cv2.imread("qr_rotado.jpg")
    if img2 is not None:
        r2_raw, t2_raw = medir_tiempo(mision2_raw, img2, -45)
        r2_cv, t2_cv = medir_tiempo(mision2_opencv, img2, -45)
        guardar("m2_raw.png", r2_raw)
        guardar("m2_opencv.png", r2_cv)
        print(f"Misión 2 - Raw: {t2_raw:.6f} s")
        print(f"Misión 2 - OpenCV: {t2_cv:.6f} s")
    else:
        print("Falta qr_rotado.jpg")

    img3 = cv2.imread("microfilm.jpg")
    if img3 is not None:
        crop = extraer_recorte_central(img3, tam=200)
        r3_raw, t3_raw = medir_tiempo(mision3_raw_vecino_cercano, crop, 5, 5)
        r3_cv, t3_cv = medir_tiempo(mision3_opencv, crop, 5, 5)
        guardar("m3_crop.png", crop)
        guardar("m3_raw.png", r3_raw)
        guardar("m3_opencv.png", r3_cv)
        print(f"Misión 3 - Raw: {t3_raw:.6f} s")
        print(f"Misión 3 - OpenCV: {t3_cv:.6f} s")
    else:
        print("Falta microfilm.jpg")

if __name__ == "__main__":
    main()

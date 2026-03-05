import numpy as np
import cv2 as cv

# Cargar haarcascade (recomendado: desde la instalación de OpenCV)
rostro = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

cap = cv.VideoCapture(0)

if rostro.empty():
    print("ERROR: No se pudo cargar el Haarcascade. Revisa tu instalación de OpenCV.")
    raise SystemExit

while True:
    ret, img = cap.read()
    if not ret:
        print("ERROR: No se pudo leer la camara.")
        break

    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Detectar rostros
    rostros = rostro.detectMultiScale(gris, scaleFactor=1.3, minNeighbors=5, minSize=(80, 80))

    for (x, y, w, h) in rostros:
        # Marco de la cara
        cv.rectangle(img, (x, y), (x + w, y + h), (234, 23, 23), 3)

        # ---------------- OJOS ----------------
        ojo_y = y + int(h * 0.40)
        ojo_x1 = x + int(w * 0.30)
        ojo_x2 = x + int(w * 0.70)

        # contorno ojos
        cv.circle(img, (ojo_x1, ojo_y), 21, (0, 0, 0), 2)
        cv.circle(img, (ojo_x2, ojo_y), 21, (0, 0, 0), 2)
        # relleno blanco
        cv.circle(img, (ojo_x1, ojo_y), 20, (255, 255, 255), -1)
        cv.circle(img, (ojo_x2, ojo_y), 20, (255, 255, 255), -1)
        # pupila roja
        cv.circle(img, (ojo_x1, ojo_y), 5, (0, 0, 255), -1)
        cv.circle(img, (ojo_x2, ojo_y), 5, (0, 0, 255), -1)

        # ---------------- CEJAS ----------------
        ceja_y = y + int(h * 0.28)
        ceja_len = int(w * 0.18)
        ceja_th = 6

        # ceja izquierda
        cv.line(img,
                (x + int(w * 0.18), ceja_y),
                (x + int(w * 0.18) + ceja_len, ceja_y - 5),
                (0, 0, 0), ceja_th)

        # ceja derecha
        cv.line(img,
                (x + int(w * 0.62), ceja_y - 5),
                (x + int(w * 0.62) + ceja_len, ceja_y),
                (0, 0, 0), ceja_th)

        # ---------------- NARIZ ----------------
        nariz_cx = x + w // 2
        nariz_cy = y + int(h * 0.55)

        p1 = (nariz_cx, nariz_cy - int(h * 0.05))
        p2 = (nariz_cx - int(w * 0.06), nariz_cy + int(h * 0.06))
        p3 = (nariz_cx + int(w * 0.06), nariz_cy + int(h * 0.06))
        cv.polylines(img, [np.array([p1, p2, p3])], True, (0, 0, 0), 3)

        # puntita nariz
        tip_y = nariz_cy + int(h * 0.07)
        cv.circle(img, (nariz_cx, tip_y), 6, (0, 150, 255), -1)
        cv.circle(img, (nariz_cx, tip_y), 6, (0, 0, 0), 2)

        # ---------------- BIGOTE ----------------
        bigote_y = y + int(h * 0.63)
        bigote_th = 6

        # bigote centro
        cv.line(img,
                (x + int(w * 0.40), bigote_y),
                (x + int(w * 0.60), bigote_y),
                (0, 0, 0), bigote_th)

        # bigote izquierda (3 pelitos)
        cv.line(img, (x + int(w * 0.40), bigote_y),
                (x + int(w * 0.28), bigote_y - 10), (0, 0, 0), bigote_th)
        cv.line(img, (x + int(w * 0.40), bigote_y),
                (x + int(w * 0.26), bigote_y), (0, 0, 0), bigote_th)
        cv.line(img, (x + int(w * 0.40), bigote_y),
                (x + int(w * 0.28), bigote_y + 10), (0, 0, 0), bigote_th)

        # bigote derecha (3 pelitos)
        cv.line(img, (x + int(w * 0.60), bigote_y),
                (x + int(w * 0.72), bigote_y - 10), (0, 0, 0), bigote_th)
        cv.line(img, (x + int(w * 0.60), bigote_y),
                (x + int(w * 0.74), bigote_y), (0, 0, 0), bigote_th)
        cv.line(img, (x + int(w * 0.60), bigote_y),
                (x + int(w * 0.72), bigote_y + 10), (0, 0, 0), bigote_th)

        # ---------------- SONRISA ----------------
        boca_cx = x + w // 2
        boca_cy = y + int(h * 0.72)

        axes = (int(w * 0.18), int(h * 0.10))
        cv.ellipse(img, (boca_cx, boca_cy), axes, 0, 0, 180, (0, 0, 0), 4)

        # hoyitos sonrisa
        cv.circle(img, (x + int(w * 0.35), boca_cy), 3, (0, 0, 0), -1)
        cv.circle(img, (x + int(w * 0.65), boca_cy), 3, (0, 0, 0), -1)

        # ---------------- SOMBRERO DE MARIACHI ----------------
        ala_cx = x + w // 2
        ala_cy = max(0, y - int(h * 0.05))  # evita salir de la pantalla
        ala_axes = (int(w * 0.55), int(h * 0.18))

        # Ala rellena
        cv.ellipse(img, (ala_cx, ala_cy), ala_axes, 0, 0, 360, (30, 30, 30), -1)
        cv.ellipse(img, (ala_cx, ala_cy), ala_axes, 0, 0, 360, (0, 0, 0), 3)

        # Copa
        copa_w = int(w * 0.45)
        copa_h = int(h * 0.30)
        copa_x1 = ala_cx - copa_w // 2
        copa_y1 = max(0, ala_cy - copa_h)
        copa_x2 = ala_cx + copa_w // 2
        copa_y2 = ala_cy

        cv.rectangle(img, (copa_x1, copa_y1), (copa_x2, copa_y2), (40, 40, 40), -1)
        cv.rectangle(img, (copa_x1, copa_y1), (copa_x2, copa_y2), (0, 0, 0), 3)

        # Detalle dorado
        cv.line(img,
                (copa_x1, copa_y1 + int(copa_h * 0.35)),
                (copa_x2, copa_y1 + int(copa_h * 0.35)),
                (0, 215, 255), 4)

        # ---------------- OREJAS (opcional) ----------------
        oreja_y = y + int(h * 0.50)
        oreja_r = max(8, int(w * 0.06))  # minimo para que se vea

        # izquierda
        cv.circle(img, (x - int(w * 0.03), oreja_y), oreja_r, (180, 180, 180), -1)
        cv.circle(img, (x - int(w * 0.03), oreja_y), oreja_r, (0, 0, 0), 2)

        # derecha
        cv.circle(img, (x + w + int(w * 0.03), oreja_y), oreja_r, (180, 180, 180), -1)
        cv.circle(img, (x + w + int(w * 0.03), oreja_y), oreja_r, (0, 0, 0), 2)

        # ---------------- LENTES (opcional) ----------------
        lentes_y = ojo_y
        lentes_r = 24

        cv.circle(img, (ojo_x1, lentes_y), lentes_r, (0, 0, 0), 3)
        cv.circle(img, (ojo_x2, lentes_y), lentes_r, (0, 0, 0), 3)
        cv.line(img, (ojo_x1 + lentes_r, lentes_y),
                (ojo_x2 - lentes_r, lentes_y), (0, 0, 0), 3)

    cv.imshow('img', img)

    # salir con q o ESC
    k = cv.waitKey(1) & 0xFF
    if k == ord('q') or k == 27:
        break

cap.release()
cv.destroyAllWindows()
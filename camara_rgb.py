import cv2
import numpy as np

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

    if not cap.isOpened():
        print("No se pudo abrir la cámara. Revisa permisos en macOS (Privacy & Security -> Camera).")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No pude leer frames de la cámara.")
            break

        frame = cv2.flip(frame, 1)

        b, g, r = cv2.split(frame)
        zeros = np.zeros_like(b)

        azul = cv2.merge([b, zeros, zeros])
        verde = cv2.merge([zeros, g, zeros])
        rojo = cv2.merge([zeros, zeros, r])

        cv2.imshow("Normal", frame)
        cv2.imshow("Azul", azul)
        cv2.imshow("Verde", verde)
        cv2.imshow("Rojo", rojo)

        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord("q"):  # ESC o q
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

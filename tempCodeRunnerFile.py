import cv2
import numpy as np
import random
import time 

cap = cv2.VideoCapture("hihway.mp4")

# Inisialisasi kecepatan awal
kecepatan = {}

# Faktor konversi dari piksel/frame ke km/jam (secara kasar)
konversi_piksel_ke_km_jam = 0.04

# Untuk mengambil frame video
ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    # Mencari perbedaan di antara dua frame (perbedaan intensitas antar piksel)
    diff = cv2.absdiff(frame1, frame2)
    # Merubah video ke abu-abu
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    # Filter untuk pengurangan noise (dalam perbedaan intensitas piksel)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Nilai ambang untuk piksel di bawah 20 maka akan diubah menjadi hitam dan jika lebih maka akan diubah ke putih
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    dilated = cv2.dilate(thresh, None, iterations=3)
    # Menemukan batas tepi dalam gambar
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Reset jumlah objek yang terdeteksi bergerak pada setiap iterasi frame
    jumlah_objek_frame = 0

    for contour in contours:
        # Menggambar kotak
        (x, y, w, h) = cv2.boundingRect(contour)
        # Menghitung area
        if cv2.contourArea(contour) < 700:
            continue
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame1, "status: {}".format('Bergerak'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        # Menambahkan 1 ke jumlah objek yang terdeteksi bergerak pada frame ini
        jumlah_objek_frame += 1


        # Menghasilkan kecepatan untuk setiap objek
        if (x, y) not in kecepatan:
            kecepatan[(x, y)] = random.randint(20, 150)  # Kecepatan dalam km/jam

        # Menggambar kecepatan pada frame
        cv2.putText(frame1, f"Kecepatan: {kecepatan[(x, y)]:.2f} km/jam", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        

    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    

    if cv2.waitKey(30) == 27:
        break

    # Menampilkan total jumlah objek yang terdeteksi bergerak
print(f"Total Objek Bergerak: {jumlah_objek_bergerak}")

cv2.destroyAllWindows()
cap.release()

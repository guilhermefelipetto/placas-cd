import cv2
import pytesseract
from re import match
from time import sleep


def plate_is_valid(plate_text: str):
    pattern = r'^[A-Z]{3}\d[A-Z]\d{2}$'

    return match(pattern, plate_text) is not None


def plate_insert(conn, cursor, valid_plate: str):
    if conn.is_connected():
        cursor.execute('SELECT COUNT(*) FROM placas_registradas WHERE placa IN (%s)', (valid_plate,))
        res = cursor.fetchone()

        if res[0] > 0:
            cursor.execute('INSERT INTO registro (placa, tipo) VALUES (%s, "Registrada")', (valid_plate,))
        else:
            cursor.execute('INSERT INTO registro (placa, tipo) VALUES (%s, "NR")', (valid_plate,))
    
    conn.commit()
    print('inserido no banco!')


def detect_recognize_plate(frame, model: str, conn, cursor):
    try:
        plate_cascade = cv2.CascadeClassifier(model)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in plates:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
            plate_roi = gray[y:y + h, x:x + w]

            plate_text = pytesseract.image_to_string(plate_roi, config='--psm 11').replace('|', '').replace(' ', '').replace('\n', '')
            
            if plate_is_valid(plate_text):
                print("Placa valida:", plate_text)
                plate_insert(conn, cursor, plate_text)
                sleep(5)

    except Exception as err:
        print(f"Ocorreu um erro: {err}")

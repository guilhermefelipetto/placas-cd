import cv2
import pytesseract
import mysql.connector
from os import getenv

from database_scripts.plate_processing import detect_recognize_plate

if __name__ == "__main__":
    print("Variáveis de ambiente:")
    print("MYSQL_HOST:", getenv("MYSQL_HOST"))
    print("MYSQL_USER:", getenv("MYSQL_USER"))
    print("MYSQL_PASSWORD:", getenv("MYSQL_PASSWORD"))
    print("MYSQL_DB:", getenv("MYSQL_DB"))
    print("TESSERACT_CMD:", getenv('TESSERACT_CMD'))
    print("HAAR_MODEL_PATH:", getenv('HAAR_MODEL_PATH'))

    # Conexao com o banco
    try:
        conn = mysql.connector.connect(
            host=getenv("MYSQL_HOST"),
            port=getenv("MYSQL_PORT"),
            user=getenv("MYSQL_USER"),
            password=getenv("MYSQL_PASSWORD"),
            database=getenv("MYSQL_DB")
        )
        cursor = conn.cursor()

    except mysql.connector.Error as err:
        print(f'Atencao!\nErro ao tentar se conectar com o banco de dados.\n{err}')

    # Diretorio do Tesseract
    pytesseract.pytesseract.tesseract_cmd = getenv('TESSERACT_CMD')

    # Modelo HAAR Cascade (xml)
    model = getenv('HAAR_MODEL_PATH')

    # cap = cv2.VideoCapture(0) # webcam
    cap = cv2.VideoCapture("video.MTS") # video

    desired_width = 640
    desired_height = 480

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.resize(frame, (desired_width, desired_height))

        plate_result = detect_recognize_plate(frame=frame, model=model, conn=conn, cursor=cursor)

        if plate_result == "sim":
            print("Placa autorizada!")
        
        elif plate_result == "não":
            print("Placa não autorizada. Acesso negado!")

        # cv2.imshow('Video com Placas Detectadas', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    cursor.close()
    conn.close()

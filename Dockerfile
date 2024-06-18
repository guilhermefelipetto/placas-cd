FROM python:3.12.3-slim

RUN apt-get update && apt-get install -y \
    libsm6 libxext6 libxrender-dev libglib2.0-0 \
    libgl1-mesa-glx \
    tesseract-ocr tesseract-ocr-por \
    mariadb-server \
    build-essential pkg-config libmariadb-dev-compat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=banco_placas
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=root

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY cascade/ cascade/
COPY video.MTS .
COPY database_scripts/ database_scripts/
COPY my.cnf /etc/mysql/my.cnf
COPY start.sh /app/
RUN chmod +x /app/start.sh

ENV MYSQL_HOST=localhost \
    TESSERACT_CMD=/usr/bin/tesseract \
    HAAR_MODEL_PATH=/app/cascade/cascade.xml \
    TEST_VIDEO_PATH=/app/video.MTS

EXPOSE 3306

CMD ["/app/start.sh"]
# CMD ["bash"]

# docker run -e MYSQL_HOST='host.docker.internal' -e MYSQL_USER='root' -e MYSQL_PASSWORD='root' -e MYSQL_DB='banco_placas' -e TESSERACT_CMD='/usr/bin/tesseract' -e HAAR_MODEL_PATH='/app/cascade/cascade.xml' -e TEST_VIDEO_PATH='/app/video.MTS' -it --name bpkedu project_image_bash
# mysql -u root -p -e "SHOW DATABASES;"

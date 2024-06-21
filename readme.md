# Treinamento de Haar Cascade para projeto placas_cd do 3º Semestre

descricao

## Índice

- [Instalação](#instalação)

## Instalação

Instruções passo a passo para rodar o projeto localmente.

Requisitos:
- Python 3.12.3+
- Docker 4.27.2+ 
- Git

1.  Clone o repositório:
```bash
git clone https://github.com/guilhermefelipetto/projeto-placas-cd
cd projeto
```

2. Configure o Docker:
```bash
docker build -t project_image
docker run -e MYSQL_HOST='host.docker.internal' -e MYSQL_USER='root' -e MYSQL_PASSWORD='root' -e MYSQL_DB='banco_placas' -e TESSERACT_CMD='/usr/bin/tesseract' -e HAAR_MODEL_PATH='/app/cascade/cascade.xml' -e TEST_VIDEO_PATH='/app/video.MTS' -it --name bpkedu project_image_bash
```

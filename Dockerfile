FROM python:3.10.7-alpine3.16 
LABEL MAINTAINER="Eduardo Pagotto <eduardo.pagotto@newspace.com.br>"

WORKDIR /var/app

ENV SSF_CFG_IP "0.0.0.0"
ENV SSF_CFG_PORT "5151"
ENV SSF_CFG_DB "/opt/db"
ENV SSF_CFG_STORAGE "/opt/storage"

EXPOSE 5151/tcp

COPY ./dist/SSF-1.0.0.tar.gz .
COPY ./deploy/install.sh .
COPY ./app.py .
COPY ./main.py .
COPY ./requirements.txt .

RUN ./install.sh

# Iniciar aplicação
CMD ["python3", "./main.py"]
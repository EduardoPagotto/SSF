FROM python:3.10.7-alpine3.16 
LABEL MAINTAINER="Eduardo Pagotto <eduardo.pagotto@newspace.com.br>"

WORKDIR /var/app

ENV SSF_CFG_IP "0.0.0.0"
ENV SSF_CFG_PORT "5151"
ENV SSF_CFG_DB "/opt/db"
ENV SSF_CFG_STORAGE "/opt/storage"

COPY ./requirements.txt .
COPY ./app.py .
COPY ./main.py .
COPY ./setup.py .

ADD ./SSF /var/app/SSF/.

RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt 

RUN pip3 install .

EXPOSE 5151/tcp

# Iniciar aplicação
CMD ["python3", "./main.py"]
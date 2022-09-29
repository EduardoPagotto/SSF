FROM python:3.10.7-alpine3.16 
LABEL MAINTAINER="Eduardo Pagotto <eduardo.pagotto@newspace.com.br>"

# install dep of RPC
WORKDIR /var/app/sJsonRpc
ADD ./sJsonRpc/sJsonRpc ./sJsonRpc
COPY ./sJsonRpc/requirements.txt .
COPY ./sJsonRpc/setup.py .

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    pip3 install . 

# install api client server of SSF
WORKDIR /var/app/SSF
ADD ./SSF ./SSF
COPY ./requirements.txt .
COPY ./setup.py .

RUN pip3 install -r requirements.txt && \
    pip3 install .

# install service
WORKDIR /var/app

COPY ./app.py .
COPY ./main.py .

ENV SSF_CFG_IP "0.0.0.0"
ENV SSF_CFG_PORT "5151"
ENV SSF_CFG_DB "/opt/db"
ENV SSF_CFG_STORAGE "/opt/storage"

EXPOSE 5151/tcp

# Iniciar aplicação
CMD ["python3", "./main.py"]
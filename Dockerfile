FROM python:3.10.7-alpine3.16 
LABEL MAINTAINER="Eduardo Pagotto <eduardo.pagotto@newspace.com.br>"

RUN apk update
RUN apk add git

# set venv
# ENV VIRTUAL_ENV=/opt/venv
# RUN python3 -m venv $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip3 install --upgrade pip

WORKDIR /var/app

#lib deps
RUN git clone https://github.com/EduardoPagotto/sJsonRpc.git
WORKDIR /var/app/sJsonRpc/
RUN pip3 install -r requirements.txt && \
    pip3 install .
WORKDIR /var/app
RUN rm -rf sJsonRpc

# install api client and server of SSF
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
#ENV SSF_ALLOWED_EXTENSIONS "[\"txt\", \"pdf\", \"zip\", \"jpg\"]"

EXPOSE 5151/tcp

# start server
CMD ["python", "main.py"]
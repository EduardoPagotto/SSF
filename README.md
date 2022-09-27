# SSF
Simple Storage File Server


# RestApi RPC init

Class Client:
- ServiceBus
- ConnectionControl
- ProxyObject
- RPC_Call


## Manutencao do container
```bash
docker run --name zdev -it ssf_server_img /bin/sh
docker exec -it server_ssf_dev /bin/sh
```
## Teste cliente local
```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requeriment.txt
./client_rpc.py

```
## Deploy do Servico
```bash
make dist
cd deploy
docker-compose up -d

# testar com browser: http://127.0.0.1:5151
```

refs: 
- https://roytuts.com/python-flask-rest-api-file-upload/
# SSF
Simple Storage File

## Command python in ClientSSf.py
- upload(self, path_file: str, opt: dict = {}) -> Tuple[int, str]:
    upload file of 'path_file' with optinal 'opt' dictionary 
- download(self, id : int, pathfile : str) -> Tuple[bool, str]:
- info('id') 
- keep(self, id : int) -> bool:
- remove(self, id : int) -> bool:
- cleanAt(self, days : int, hours : int, minute : int):


## Running and debug local
1. Set VENV:
    ```bash
    # set env
    python3 -m venv .venv
    source .venv/bin/activate
    # install deps
    pip3 install -r requirements.txt
    ```

2. Start Server in line command
    ```bash
    cd ..
    ./main.py
    ```

3. Start test client
    ```bash
    # In other terminal im projet directory
    ./client_rpc.py
    ```
    obs: No browser: http://127.0.0.1:5151 


## Service build, deply and test
1. Set VENV:
    ```bash
    # set env
    python3 -m venv .venv
    source .venv/bin/activate
    # install deps
    pip3 install -r requirements.txt
    ```

2. Build:
    ```bash
    # create ./dist/SSF.1.0.1.tar.gz
    make dist
    ```

3. Deploy
    ```bash
    cd deploy
    docker-compose up -d
    ```

4. Test local client
    ```bash
    cd ..
    ./client_rpc.py
    ```
    obs: No browser: http://127.0.0.1:5151 

## Maintenance of container
```bash
# Start the container and enter it for maintenance
docker run --name zdev -it ssf_server_img /bin/sh

# access the container working in interactive mode
docker exec -it server_ssf_dev /bin/sh
```

refs: 
- https://roytuts.com/python-flask-rest-api-file-upload/
#!/usr/bin/env python3
'''
Created on 20220917
Update on 20220926
@author: Eduardo Pagotto
'''

import json
import logging
import pathlib
import shutil
from typing import Tuple
import requests

from RPC.ConnectionControl import ConnectionControl
from RPC.ProxyObject import ProxyObject

class ConnectionRestApi(ConnectionControl):
    def __init__(self, addr : str):
        super().__init__(addr)

    def exec(self, input_rpc : dict, *args, **kargs) -> str:
        url : str
        headers : dict= {'rpc-Json': json.dumps(input_rpc)}
        payload : dict ={}

        if '_Xfer' not in input_rpc['method']:
            # comandos rpc's
            url = self.getUrl() + "/rpc-call-base"
            files = None
        else:
            # comando rpc com upload junto
            url = self.getUrl() + "/rpc-call-upload"
            path_file = pathlib.Path(input_rpc['params'][0])
            final = path_file.resolve()
            files= {'file': open(final,'rb')}

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        if response.status_code != 201:
            raise Exception(response.text)

        return response.text # string com dict do rpcjson

class ClienteRPC(object):
    def __init__(self, s_address: str):
        self.restAPI = ConnectionRestApi(s_address)

    def __rpc(self):
        return ProxyObject(self.restAPI)

    ''' Infos of file '''
    def info(self, id : int) -> dict | None:
        return self.__rpc().info(id)

    ''' keep more cleanAt cicle '''
    def keep(self, id : int) -> bool:
        return self.__rpc().keep(id)

    ''' Remove file '''
    def remove(self, id : int) -> bool:
        return self.__rpc().remove(id)

    def cleanAt(self, days : int, hours : int, minute : int):
        self.__rpc().set_server_expire(days, hours, minute)

    ''' Upload of file '''
    def upload(self, path_file: str, opt: dict = {}) -> Tuple[int, str]:
        return self.__rpc().save_Xfer(path_file, opt)

    ''' Download file '''
    def download(self, id : int, pathfile : str) -> Tuple[bool, str]:

        url = self.restAPI.getUrl() + '/download/' + str(id)
        response = requests.get(url, stream=True)
        if (response.status_code == 201) or (response.status_code == 200):
            with open(pathfile, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
                
            return True, 'OK'

        motivo : dict = json.loads(response.text)

        return False, motivo['message']


def main():

    try:
        log = logging.getLogger('Client')

        client = ClienteRPC('http://127.0.0.1:5151')
        client.cleanAt(0, 0, 5)

        id = 1000
        ggg = client.info(id)
        ttt = client.remove(id)
        kkk = client.keep(id)
        valid, msg_erro = client.download(id, './testez1.jpg')
        log.debug(f'Id:{id}: msg:{msg_erro} info:{str(client.info(id))}')

        count=0
        while (count < 500):

            id, msg = client.upload('./data/disco1.jpg')
            log.debug(f'Id:{id}: msg:{msg} info:{str(client.info(id))}')

            id, msg = client.upload('./data/disco1.jpg')
            log.debug(f'Id:{id}: msg:{msg} info:{str(client.info(id))}')

            zzz = client.remove(id)

            valid, msg_erro = client.download(id, './testez1.jpg')
            log.debug(f'Id:{id}: msg:{msg_erro} info:{str(client.info(id))}')

            id, msg = client.upload('./data/disco1.jpg')
            log.debug(f'Id:{id}: msg:{msg} info:{str(client.info(id))}')
            
            valid, msg_erro = client.download(id, './testez1.jpg')
            log.debug(f'Id:{id}: msg:{msg_erro} info:{str(client.info(id))}')

            id, msg = client.upload('./data/disco1.jpg')
            log.debug(f'Id:{id}: msg:{msg} info:{str(client.info(id))}')

            id, msg = client.upload('./data/disco1.jpg')
            log.debug(f'Id:{id}: msg:{msg} info:{str(client.info(id))}')

            client.keep(id)
            log.debug(f'Id {id}: {str(client.info(id))}')

            #time.sleep(10)

            count += 1
        
    except Exception as exp:
        log.error('{0}'.format(str(exp)))

    log.info('App desconectado')

if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(threadName)-16s %(funcName)-20s %(message)s',
        datefmt='%H:%M:%S',
    )

    logging.getLogger('werkzeug').setLevel(logging.CRITICAL) 
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)

    main()
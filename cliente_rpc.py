#!/usr/bin/env python3
'''
Created on 20220917
Update on 20220921
@author: Eduardo Pagotto
'''

import json
import logging
import shutil
from typing import Tuple
import requests

from RPC.ServiceBus import ServiceBus

class ClienteRPC(ServiceBus):
    def __init__(self, s_address: str):
        super().__init__(s_address)

    def __rpc(self):
        return self.getObject()

    ''' Upload of file '''
    def upload(self, path_file: str, opt: dict = {}) -> int:
        return self.__rpc().save_Xfer(path_file, opt)

    ''' Download file '''
    def download(self, id : int, pathfile : str):

        url = self.addr + '/download/' + str(id)
        response = requests.get(url, stream=True)

        if (response.status_code == 201) or (response.status_code == 200):
            with open(pathfile, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
                
            return

        motivo : dict = json.loads(response.text)
        raise Exception(motivo['message'])

    ''' Infos of file '''
    def info(self, id : int) -> dict:
        return self.__rpc().info(id)

    ''' keep more cleanAt cicle '''
    def keep(self, id : int):
        self.__rpc().keep(id)

    ''' Remove file '''
    def remove(self, id : int):
        self.__rpc().remove(id)

    def cleanAt(self, days : int, hours : int, minute : int):
        self.__rpc().set_server_expire(days, hours, minute)


def main():

    try:
        log = logging.getLogger('Client')

        client = ClienteRPC('http://127.0.0.1:5151')
        client.cleanAt(0, 0, 5)

        #ggg= client.info(1000)
        #client.download_file(100, './testez1.jpg')
        #log.debug(f'InfoZ: {str(client.info(1))}')

        count=0
        while (count < 100):

            id = client.upload('./data/disco1.jpg')
            log.debug(f'Id {id}: {str(client.info(id))}')

            id = client.upload('./data/disco1.jpg')
            log.debug(f'Id {id}: {str(client.info(id))}')

            client.remove(id)

            id = client.upload('./data/disco1.jpg')
            log.debug(f'Id {id}: {str(client.info(id))}')

            id = client.upload('./data/disco1.jpg')
            log.debug(f'Id {id}: {str(client.info(id))}')

            client.download(id, './testez1.jpg')
            log.debug(f'Id {id}: {str(client.info(id))}')

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
#!/usr/bin/env python3
'''
Created on 20220917
Update on 20220921
@author: Eduardo Pagotto
'''

import logging
from typing import Tuple

from RPC.ServiceBus import ServiceBus

class ClienteRPC(ServiceBus):
    def __init__(self, s_address: str):
        super().__init__(s_address)

    def __rpc(self):
        return self.getObject()

    ''' Salva um novo arquivo e inicia seu ciclo '''
    def upload_file(self, path_file: str, opt: dict = {}) -> int:
        return self.__rpc().save_Xfer(path_file, opt)

    ''' Carrega um arquivo existente '''
    def download_file(self, id : int, pathfile : str) -> Tuple [bool, str]:




        return self.__rpc().load_Xfer(id)

    ''' Retorna os dados do arquivo '''
    def info(self, id : int) -> dict:
        return self.__rpc().info(id)

    ''' Mantem ele por mais um ciclo '''
    def keep(self, id : int)-> Tuple [bool, str] :
        return self.__rpc().keep(id)

    ''' Remove arquivo existente '''
    def remove(self, id : int)-> Tuple [bool, str] :
        return self.__rpc().remove(id)

    def set_server_expire(self, days : int, hours : int, minute : int):
        self.__rpc().set_server_expire(days, hours, minute)


def main():

    try:
        log = logging.getLogger('Client')

        client = ClienteRPC('http://127.0.0.1:5151')
        client.set_server_expire(0, 0, 59)

        log.debug(f'InfoZ: {str(client.info(1))}')

        count=0
        while (count < 300):

            id = client.upload_file('./data/disco1.jpg') # TODO refazer abaixo !!!!
            log.debug(f'Id: {id}')

            id = client.upload_file('./data/disco1.jpg')
            log.debug(f'Id: {id}')

            id = client.upload_file('./data/disco1.jpg')
            log.debug(f'Id: {id}')

            id = client.upload_file('./data/disco1.jpg')
            log.debug(f'Id: {id}')

            id = client.upload_file('./data/disco1.jpg')
            log.debug(f'Id: {id}')

            res = client.download_file(id, './testez1.jpg')
            log.debug(f'Res: {str(res)}')
            log.debug(f'Info1: {str(client.info(id))}')

            client.keep(id)
            log.debug(f'Info2: {str(client.info(id))}')

            #time.sleep(10)

            client.remove(id)
            log.debug(f'Info3: {str(client.info(id))}')

            count += 1
        


    except Exception as exp:
        log.error('Falha: {0}'.format(str(exp)))

    log.info('App desconectado')

if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(threadName)-16s %(funcName)-20s %(message)s',
        datefmt='%H:%M:%S',
    )

    main()
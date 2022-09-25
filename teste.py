#!/usr/bin/env python3
'''
Created on 20220924
Update on 20220924
@author: Eduardo Pagotto
'''

import logging
import requests


def download_tese():
    url = "http://127.0.0.1:5151/file-upload"

    payload={}
    files=[('file',('Consultar Consignação.pdf',
        open('/home/pagotto/Projetos/SSF/exemplo/Consultar Consignação.pdf','rb'),'application/pdf'))
    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    log.debug(response.text)


if __name__ == '__main__':


    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(threadName)-16s %(funcName)-20s %(message)s',
        datefmt='%H:%M:%S',
    )

    log = logging.getLogger('SSF.DEBUG')
    #log.info('>>>>>> ServerZSF v-%s (%s) Listen(%s) ', __version__, __date_deploy__, config_addr)
    download_tese()
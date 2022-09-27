#!/usr/bin/env python3
'''
Created on 20220917
Update on 20220927
@author: Eduardo Pagotto
'''

import logging
from Client.ClientSSF import ClientSSF

def main():

    try:
        log = logging.getLogger('Client')

        client = ClientSSF('http://127.0.0.1:5151')
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

            # valid, msg_erro = client.download(id, '.')
            # log.debug(f'Id:{id}: msg:{msg_erro} info:{str(client.info(id))}')

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
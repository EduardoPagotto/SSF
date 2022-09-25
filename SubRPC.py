'''
Created on 20220924
Update on 20220924
@author: Eduardo Pagotto
'''

import logging
import pathlib
from datetime import datetime, timedelta, timezone
import threading
import time
from typing import Tuple
from threading import Lock

from tinydb import TinyDB, Query
from RPC.RPC_Responser import RPC_Responser

from RPC.__init__ import __version__ as VERSION
from RPC.__init__ import __date_deploy__ as DEPPLOY

class SubRPC(RPC_Responser):
    def __init__(self, path_db : str, path_storage : str) -> None:
        super().__init__(self)

        self.lock_db = Lock()

        path1 = pathlib.Path(path_db)
        path1.mkdir(parents=True, exist_ok=True)
        self.db = TinyDB(str(path1) + '/master.json')

        self.storage = pathlib.Path(path_storage)
        self.storage.mkdir(parents=True, exist_ok=True)

        self.delta = timedelta(days=0, hours=2, minutes=0)

        self.count_file : int = 0
        self.tot_in = 0
        self.done = False

        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(threadName)-16s %(funcName)-20s %(message)s',
            datefmt='%H:%M:%S',
        )

        self.log = logging.getLogger('RPC.SubRPC')
        self.log.info(f'>>>>>> SSF v-{VERSION} ({DEPPLOY}), DB: {str(path1)} Storage: {str(self.storage)}')

        self.t_cleanner : threading.Thread = threading.Thread(target=self.cleanner, name='cleanner_files')
        self.t_cleanner.start()

    def cleanner(self) ->None:
        """[Garbage collector of files]
        """

        time.sleep(10)
        self.log.info('thread cleanner_files start')
        ticktack : int = 0
        tot_out : int = 0
        while self.done is False:

            if (ticktack % 12) == 0:

                now = datetime.now(tz=timezone.utc)
                limit = (now - self.delta).timestamp()

                with self.lock_db:
                    q = Query()
                    itens = self.db.search(q.last < limit)
                    for val in itens:

                        file = pathlib.Path(val['internal'])
                        file.unlink(missing_ok=True)

                        self.log.debug(f"Remove ID:{val.doc_id} file: {val['internal']}")
                        self.db.remove(doc_ids=[val.doc_id])
                        tot_out += 1

                self.log.debug(f'Tick-Tack: {int(ticktack / 12)} In: {self.tot_in} Del: {tot_out} Tot: {tot_out - self.tot_in}')

            ticktack += 1
            time.sleep(5)

        self.log.info('thread cleanner_files stop')


    def call(self, incoming : str) -> dict:
        return self.rpc_exec_func(incoming, None)
        
    def save_Xfer(self, path_file_in: str , opt: dict) -> Tuple[bool, str]:

        path_file = pathlib.Path(path_file_in)

        id : int = 0
        now = datetime.now(tz=timezone.utc)
        ts = now.timestamp() 
        data_file = {'pathfile': str(path_file.resolve()),
                     'created': ts,
                     'last': ts,
                     'internal' : 'Invalid'}

        suffix = path_file.suffix

        path1 : pathlib.Path = pathlib.Path(str(self.storage) + '/' + now.strftime('%Y%m%d/%H/%M'))
        if path1.exists() is False:
            path1.mkdir(parents=True)

        self.count_file += 1
        final : str = str(path1) + '/file{:05d}{}'.format(self.count_file, suffix)
        data_file['internal'] = final

        with self.lock_db:
            id = self.db.insert(data_file)
         
        try:
            #protocolo.receiveFile(final)
            self.log.debug(f'new ID: {id} File:{str(final)}')
            self.tot_in += 1
            #protocolo.sendErro('Arquivo nao existe')
            
        except Exception as exp:
            with self.lock_db:
                self.db.remove(doc_ids=[id])

            return False, str(exp.args[0])
            
        return True, str(id)

    def load_Xfer(self, id : int, protocolo : bytes) -> Tuple [bool, str]:
        try:

            param : dict | None = None
            with self.lock_db:
                param = self.db.get(doc_id=id)
                if (param is not None) and (param['last'] != 0):
                    self.db.update({'last': datetime.now(tz=timezone.utc).timestamp()}, doc_ids=[id])
                else:
                    #protocolo.sendErro('Arquivo nao existe')
                    return False, 'Arquivo nao existe'

            #protocolo.sendFile(param['internal'])

        except Exception as exp:
            return False, str(exp.args[0])
            
        return True, 'ok' 

    def info(self, id : int) -> dict | None:
        with self.lock_db:
            data = self.db.get(doc_id=id)
            if data:
                del data['internal']
                if data['last'] == 0:
                    return None

            return data

    def infoAll(self, id : int) -> dict | None:
        with self.lock_db:
            return self.db.get(doc_id=id)


    def keep(self, id : int)-> Tuple [bool, str] :
        now = datetime.now(tz=timezone.utc)
        with self.lock_db:
            self.db.update({'last': now.timestamp()}, doc_ids=[id])

        return True, 'ok'

    def remove_file(self, id : int)-> Tuple [bool, str] :

        with self.lock_db:
            self.db.update({'last': 0}, doc_ids=[id]) # set to delete now

        return True, 'ok'

    def set_server_expire(self, days : int, hours : int, minute : int):
        with self.lock_db:
            self.delta = timedelta(days=days, hours=hours, minutes=minute)
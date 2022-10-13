'''
Created on 20220924
Update on 20221013
@author: Eduardo Pagotto
'''

import json
import logging
import os
import pathlib
import time

from typing import Any, Optional, Tuple
from threading import Lock, Thread
from datetime import datetime, timedelta, timezone

from werkzeug.utils import secure_filename
from tinydb import TinyDB, Query

from sJsonRpc.RPC_Responser import RPC_Responser
from .__init__ import __version__ as VERSION
from .__init__ import __date_deploy__ as DEPLOY

class ServerSSF(RPC_Responser):
    def __init__(self, path_db : str, path_storage : str) -> None:
        super().__init__(self)

        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(threadName)-16s %(funcName)-20s %(message)s',
            datefmt='%H:%M:%S',
        )

        logging.getLogger('werkzeug').setLevel(logging.CRITICAL)
        logging.getLogger('urllib3').setLevel(logging.CRITICAL)

        path1 = pathlib.Path(path_db)
        path1.mkdir(parents=True, exist_ok=True)
        self.db = TinyDB(str(path1) + '/master.json')
        self.lock_db = Lock()

        self.storage = pathlib.Path(path_storage)
        self.storage.mkdir(parents=True, exist_ok=True)

        self.log = logging.getLogger('SSF')
        self.log.info(f'>>>>>> SSF v-{VERSION} ({DEPLOY}), DB: {str(path1)} Storage: {str(self.storage)}')

        self.allowed : Optional[set] = None
        allowed = os.getenv('SSF_ALLOWED_EXTENSIONS')
        if allowed:
            try:
                env_list : list = json.loads(allowed)
                self.allowed = set(env_list)
                self.log.info('SSF_ALLOWED_EXTENSIONS: ' + str(self.allowed))
            except Exception as exp:
                self.log.error('SSF_ALLOWED_EXTENSIONS is invalid: ' + str(exp.args[0]))
        else:
             self.log.info('SSF_ALLOWED_EXTENSIONS: *')


        self.delta = timedelta(days=0, hours=2, minutes=0)
        self.cleanAt : tuple = (0,2,0)

        self.count_file : int = 0
        self.tot_in = len(self.db)
        self.tot_out : int = 0
        self.tot_dowload : int = 0
        self.ticktack : int = 0
        self.done : bool = False

        self.t_cleanner : Thread = Thread(target=self.cleanner, name='cleanner_files')
        self.t_cleanner.start()

    def sumario(self) -> str :
        msg = f'>>>>>> SSF v-{VERSION} ({DEPLOY})<p>\
                Tick-Tack: {int(self.ticktack / 12)} File Index {self.count_file} <p> \
                Uploads: {self.tot_in},  Downloads: {self.tot_dowload} <p>\
                Deleted: {self.tot_out}, Remain: {self.tot_in - self.tot_out} <p>\
                Clean at-> Days: {self.cleanAt[0]} hours: {self.cleanAt[1]} minutes: {self.cleanAt[2]}'

        return msg

    def allowed_file(self, filename : str) -> bool:
        if self.allowed:
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed

        return True

    def removeEmptyFolders(self, path : str, removeRoot : bool = True):
        """Remove empty directorys

        Args:
            path (_type_): path to find and remove
            removeRoot (bool, optional): if true remove root path . Defaults to True.
        """

        if not os.path.isdir(path):
            return

        # remove empty subfolders
        files = os.listdir(path)
        if len(files):
            for f in files:
                fullpath = os.path.join(path, f)
                if os.path.isdir(fullpath):
                    self.removeEmptyFolders(fullpath)

        # if folder empty, delete it
        files = os.listdir(path)
        if len(files) == 0 and removeRoot:
            self.log.info(f"path: {path}")
            os.rmdir(path)

    def cleanner(self) ->None:
        """[Garbage collector of files]
        """

        time.sleep(10)
        self.log.info('thread cleanner_files start')
        while self.done is False:

            if (self.ticktack % 12) == 0:

                now = datetime.now(tz=timezone.utc)
                limit = (now - self.delta).timestamp()

                with self.lock_db:
                    q = Query()
                    itens = self.db.search(q.last < limit)

                ll = []
                for val in itens:
                    ll.append(val.doc_id)
                    file = pathlib.Path(val['internal'])
                    file.unlink(missing_ok=True)

                    self.log.debug(f"Remove Id:{val.doc_id}, {val['internal']}")
                    self.tot_out += 1

                if len(ll) > 0:
                    with self.lock_db:
                        self.db.remove(doc_ids=ll)
                        self.removeEmptyFolders(str(self.storage), False)

                self.log.debug(f'Tick-Tack: {int(self.ticktack / 12)} In: {self.tot_in} Del: {self.tot_out} Tot: {self.tot_in - self.tot_out}')

            self.ticktack += 1
            time.sleep(5)

        self.log.info('thread cleanner_files stop')

    def info(self, id : int) -> dict | None:
        data : dict = {}
        with self.lock_db:
            data = self.db.get(doc_id=id)

        if (data is not None) and (data['last'] != 0):
            data['name'] = str(pathlib.Path(data['internal']).name)
            del data['internal']
            return data
                
        return None

    def keep(self, id : int) -> bool:
        try:
            with self.lock_db:
                self.db.update({'last': datetime.now(tz=timezone.utc).timestamp()}, doc_ids=[id])
            
            return True

        except Exception:
            return False

    def remove(self, id : int) -> bool:
        try:
            with self.lock_db:
                self.db.update({'last': 0}, doc_ids=[id])

            return True

        except Exception:
            return False

    def set_server_expire(self, days : int, hours : int, minute : int):
        with self.lock_db:
            self.cleanAt = (days, hours, minute)
            self.delta = timedelta(days=days, hours=hours, minutes=minute)

    def save_Xfer(self, path_file_in: str , opt: dict, file: Any) -> Tuple[int, str]:

        if file is None:
            return -1, 'No file part in the request'

        if self.allowed_file(file.filename) is False:
            return -1, f'Allowed file types are: {str(self.allowed)}'

        id : int = 0
        try:
            now = datetime.now(tz=timezone.utc)
            ts = now.timestamp() 

            pp = pathlib.Path(path_file_in).parent
            path_file = pathlib.Path(pp, secure_filename(file.filename))
            suffix = path_file.suffix.lower()

            path1 : pathlib.Path = pathlib.Path(str(self.storage) + '/' + now.strftime('%Y%m%d/%H/%M'))
            if path1.exists() is False:
                path1.mkdir(parents=True)

            self.count_file += 1
            final : str = str(path1) + '/f{:04d}{}'.format(self.count_file, suffix)
            data_file = {'pathfile': str(path_file.resolve()),
                         'created': ts,
                         'last': ts,
                         'opt': opt,
                         'internal' : final}

            with self.lock_db:
                id = self.db.insert(data_file)
            
                file.save(final)
                #self.log.debug(f'new ID: {id} File:{str(final)}')
                self.tot_in += 1

        except Exception as exp:
            with self.lock_db:
                self.db.remove(doc_ids=[id])

            return -1 , str(exp.args[0])
            
        return id , 'OK'


    def infoAll(self, id : int) -> dict:
        with self.lock_db:
            data = self.db.get(doc_id=id)
            if (data is not None) and (data['last'] != 0):
                self.db.update({'last': datetime.now(tz=timezone.utc).timestamp()}, doc_ids=[id])
                return data

        raise FileNotFoundError(f'File not found id {str(id)}')

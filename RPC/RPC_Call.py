'''
Created on 20190823
Update on 20210212
@author: Eduardo Pagotto
'''

import json
import threading
import random

from .__init__ import __json_rpc_version__ as json_rpc_version
from .__init__ import ExceptionZeroRPC
from .ConnectionControl import ConnectionControl

class RPC_Call(object):
    """[Midlleware json Protocol]
    Args:
        object ([type]): [description]
    Raises:
        ExceptionZeroRPC: [Raised exception on Server of RPC]
        ExceptionZeroRPC: [FATAL!!! invalid ID]
    Returns:
        [type]: [description]
    """

    __serial_lock : threading.Lock = threading.Lock()
    __serial : int = random.randint(0,10000)

    def __init__(self, nome_metodo : str, control : ConnectionControl):
        """[Constructor json message builder]
        Args:
            nome_metodo (str): [method name do send to Server of RPC]
            control (ConnectionControl): [Valid Connection with Server RPC]
        """

        self.serial : int = RPC_Call.__createId()
        self.method : str = nome_metodo
        self.control : ConnectionControl = control

    @staticmethod
    def __createId() -> int:
        """[Identicatos Json Protocol]
        Returns:
            int: [description]
        """
        with RPC_Call.__serial_lock:
            serial = RPC_Call.__serial
            RPC_Call.__serial += 1

            return serial

    def encode(self, *args, **kargs) -> dict:
        """[encode json Protocol]
        Returns:
            str: [json with data encoded]
        """

        keys = {}
        arguments = []
        if args:
            arguments = args[0]
            keys = args[1]

        #return json.dumps({'jsonrpc':json_rpc_version, 'id':self.serial, 'method': self.method, 'params': arguments, 'keys': keys})
        return {'jsonrpc':json_rpc_version, 'id':self.serial, 'method': self.method, 'params': arguments, 'keys': keys}


    def decode(self, msg : str) -> dict:
        """[decode json Protocol]
        Args:
            msg (str): [text with json]
        Raises:
            ExceptionZeroRPC: [Raised exception on Server of RPC]
            ExceptionZeroRPC: [FATAL!!! invalid ID]
        Returns:
            dict: [description]
        """

        # TODO: get exceptions from json
        dados = json.loads(msg)
        if dados['id'] == self.serial:
            if 'error' in dados:
                raise ExceptionZeroRPC(dados['error']['message'], dados['error']['code'])

            return dados['result']

        raise ExceptionZeroRPC('Parse error, id {0} should be {1}'.format(dados['id'], self.serial), -32700)

    def __call__(self, *args, **kargs) -> dict:
        """[Execut RPC on server and get result]
        Returns:
            (dict): [Result of RPC call]
        """
        return self.decode(self.control.execute_file(self.encode(args, kargs), args, kargs))

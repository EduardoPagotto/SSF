'''
Created on 20190822
Update on 20210212
@author: Eduardo Pagotto
'''

from typing import Union
from datetime import timedelta

from .ConnectionControl import ConnectionControl
from .ProxyObject import ProxyObject

class ServiceBus(object):
    def __init__(self, s_address : str):
        """[Container of Wrapper Client RPC]
        Args:
            s_address (str): [valid's : ( http://127.0.0.1:5151 ) ]
            max_threads (int, optional): [Numero maximo de threads de conexao simultaneas]. Defaults to 5.
        """
        self.addr = s_address
        self.conn_control : ConnectionControl | None =  None

    def getObject(self) -> ProxyObject:
        """[Get connectd exchange with server RPC]
        Returns:
            ProxyObject: [Proxy conectado com controle de conexao e reentrada]
        """
        if self.conn_control is None:
            self.conn_control = ConnectionControl(self.addr)

        return ProxyObject(self.conn_control)

'''
Created on 20190824
Update on 20220917
@author: Eduardo Pagotto
'''

import logging
import socket
import json

import threading

from .__init__ import __json_rpc_version__ as json_rpc_version
from .__init__ import ExceptionZeroRPC

class RPC_Responser(object):
    """[Connection thread with server RPC ]
    Args:
        object ([type]): [description]
    """

    def __init__(self, target : object):
        """[summary]
        Args:
            target (object): [Method Name to run in RPC Server]
        """
        self.target : object= target

    def rpc_exec_func(self, msg : str, protocol : object) -> dict:
        """[Execule methodo local with paramters in json data (msg)]
        Args:
            msg (str): [json Protocol data received (id, method, parameters)]
        Returns:
            str: [Resulto of method in json Protocol]
        """

        dados : dict = json.loads(msg)
        serial : int = dados['id']
        metodo : str = dados['method']

        # suffix used to add protocol used to extra communication with peer
        # if '_Xfer' in metodo:
        #     dados['params'].append(protocol)

        try:
            val = getattr(self.target, metodo)(*dados['params'], **dados['keys'])
            return {'jsonrpc': json_rpc_version, 'result': val, 'id': serial}

        except AttributeError as exp:
            return {'jsonrpc': json_rpc_version, 'error': {'code': -32601, 'message': 'Method not found: '+ str(exp)}, 'id': serial}

        except TypeError as exp1:
            return {'jsonrpc': json_rpc_version, 'error': {'code': -32602, 'message': 'Invalid params: '+ str(exp1)}, 'id': serial}

        except ExceptionZeroRPC as exp2:
            tot = len(exp2.args)
            if tot == 0:
                return {'jsonrpc': json_rpc_version, 'error': {'code': -32000, 'message': 'Server error: Generic Zero RPC Exception'}, 'id': serial}
            elif tot == 1:
                return {'jsonrpc': json_rpc_version, 'error': {'code': -32001, 'message': 'Server error: ' + exp2.args[0]}, 'id': serial}
            else:
                return {'jsonrpc': json_rpc_version, 'error': {'code': exp2.args[1], 'message': 'Server error: ' + exp2.args[0]}, 'id': serial}

        except Exception as exp3:
            return {'jsonrpc': json_rpc_version, 'error': {'code': -32603, 'message': 'Internal error: ' + str(exp3)}, 'id': serial}
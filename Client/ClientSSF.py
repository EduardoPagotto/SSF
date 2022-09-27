#!/usr/bin/env python3
'''
Created on 20220917
Update on 20220927
@author: Eduardo Pagotto
'''

import json
import logging
import pathlib
import shutil
from typing import Tuple
import requests

from SimplestRPC.ConnectionControl import ConnectionControl
from SimplestRPC.ProxyObject import ProxyObject

class ConnectionRestApi(ConnectionControl):
    def __init__(self, addr : str):
        super().__init__(addr)

    def exec(self, input_rpc : dict, *args, **kargs) -> dict:
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

        return json.loads(response.text) # dict do rpcjson

class ClientSSF(object):
    def __init__(self, s_address: str):
        self.restAPI = ConnectionRestApi(s_address)

    def __rpc(self):
        """Internal method to call server

        Returns:
            _type_: Connection controller
        """

        return ProxyObject(self.restAPI)

    def info(self, id : int) -> dict | None:
        """ Get a dictionary with properties of file stored

        Args:
            id (int): id of exiting file
        Returns:
            dict | None: Dict with data properties ou None is not exist
        """

        return self.__rpc().info(id)


    def keep(self, id : int) -> bool:
        """ Refresh life time of file in Server

        Args:
            id (int): id of exiting file
        Returns:
            bool: True if success
        """

        return self.__rpc().keep(id)


    def remove(self, id : int) -> bool:
        """Remove a file from server

        Args:
            id (int): id of exiting file
        Returns:
            bool: True if sucess
        """

        return self.__rpc().remove(id)

    def cleanAt(self, days : int, hours : int, minute : int):
        """ Max time of file in server

        Args:
            days (int): num of days, default (2)
            hours (int): num of hours, default (0)
            minute (int): num of minutes, default (0)
        """

        self.__rpc().set_server_expire(days, hours, minute)


    def upload(self, path_file: str, opt: dict = {}) -> Tuple[int, str]:
        """ Upload a file

        Args:
            path_file (str): path file to store
            opt (dict, optional): extra data. Defaults to {}.

        Returns:
            Tuple[int, str]: id of file and "ok" or -1 and error
        """

        return self.__rpc().save_Xfer(path_file, opt)


    def download(self, id : int, pathfile : str) -> Tuple[bool, str]:
        """ Download file

        Args:
            id (int): id of file stored
            pathfile (str): path file or only path 

        Returns:
            Tuple[bool, str]: true and path file or False and error
        """
        final : str = ''
        url = self.restAPI.getUrl() + '/download/' + str(id)

        pt = pathlib.Path(pathfile)
        if pt.is_dir() is True:
            data = self.info(id)
            if data is None:
                return False, f'File Not Found {str(id)}'

            final = str(pt.joinpath(data['name']).resolve())
        else:
            final = str(pt.resolve()) #pathfile
            
        response = requests.get(url, stream=True)
        if (response.status_code == 201) or (response.status_code == 200):
            with open(final, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
                
            return True, final

        try:
            motivo : dict = json.loads(response.text)
        except:
            return False, str(response.content)

        return False, motivo['message']
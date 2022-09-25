'''
Created on 20190914
Update on 20210212
@author: Eduardo Pagotto
'''

import json
import logging
import pathlib
import requests

class ConnectionControl(object):
    def __init__(self, addr : str):
        self.addr = addr
        self.log = logging.getLogger('Client')

    def execute_file(self, input_rpc : dict, *args, **kargs) -> str:

        url : str
        headers : dict= {'rpc-Json': json.dumps(input_rpc)}
        payload : dict ={}

        if '_Xfer' not in input_rpc['method']:
            url = self.addr + "/rpc-call-base"
            files = None
        else:
            url = self.addr + "/rpc-call-upload"
            path_file = pathlib.Path(input_rpc['params'][0])
            final = path_file.resolve()
            files= {'file': open(final,'rb')}

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        if response.status_code != 201:
            raise Exception(response.text)

        return response.text

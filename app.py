'''
Created on 20220924
Update on 20220924
@author: Eduardo Pagotto
'''

from os import getenv
from flask import Flask

from Server.ServerSSF import ServerSSF

# mypy: ignore-errors

SSF_CFG_IP : str  = getenv('SSF_CFG_IP') if getenv('SSF_CFG_IP') != None else '0.0.0.0' 
SSF_CFG_PORT : int  = int(getenv('SSF_CFG_PORT')) if getenv('SSF_CFG_PORT') != None else 5151
SSF_CFG_DB : str  = getenv('SSF_CFG_DB') if getenv('SSF_CFG_DB') != None else './data/db'
SSF_CFG_STORAGE : str = getenv('SSF_CFG_STORAGE') if getenv('SSF_CFG_STORAGE') != None else './data/storage'

rpc = ServerSSF(SSF_CFG_DB, SSF_CFG_STORAGE)

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = SSF_CFG_STORAGE
app.config['MAX_CONTENT_LENGTH'] = 256 * 1024 * 1024
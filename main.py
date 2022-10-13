#!/usr/bin/env python3
'''
Created on 20220924
Update on 20221013
@author: Eduardo Pagotto
'''

import json
import os
import pathlib
from app import app, rpc, SSF_CFG_IP, SSF_CFG_PORT 
from flask import request, jsonify, send_from_directory

@app.route("/")
def home():
    return rpc.sumario()

@app.route('/rpc-call-base', methods=['POST'])
def rpc_call_base():

	try :
		input_rpc : dict = json.loads(request.headers.get('rpc-Json'))
		output_rpc = rpc.call(input_rpc)
		resp = jsonify(output_rpc)
		resp.status_code = 201
		return resp

	except Exception as exp:
		msg = exp.args[0]
		rpc.log.error(msg)
		resp = jsonify({'message' : msg})
		resp.status_code = 400
		return resp


@app.route('/rpc-call-upload', methods=['POST'])
def rpc_call_upload():

	try :
		input_rpc : dict = json.loads(request.headers.get('rpc-Json'))
		if 'file' in request.files:
			input_rpc['params'].append(request.files['file'])
		else:
			input_rpc['params'].append(None)

		output_rpc = rpc.call(input_rpc)
		resp = jsonify(output_rpc)
		resp.status_code = 201
		return resp

	except Exception as exp:
		msg = exp.args[0]
		rpc.log.error(msg)
		resp = jsonify({'message' : msg})
		resp.status_code = 400
		return resp


@app.route('/download/<path:path>',methods = ['GET','POST'])
def rpc_call_download(path):
	"""Download a file."""
	try:
		data : dict = rpc.infoAll(int(path))
		path_all =  pathlib.Path(data['internal'])
		uploads = os.path.join(app.config.root_path, path_all.parent)
		rpc.tot_dowload += 1
		return send_from_directory(uploads, path_all.name, as_attachment=True)

	except Exception as exp:
		msg = exp.args[0]
		rpc.log.error(msg)
		resp = jsonify({'message' : msg})
		resp.status_code = 400
		return resp	

if __name__ == "__main__":
	app.run(host=SSF_CFG_IP, port=SSF_CFG_PORT)
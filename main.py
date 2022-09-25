#!/usr/bin/env python3
'''
Created on 20220924
Update on 20220924
@author: Eduardo Pagotto
'''

from fileinput import filename
import json
import os
import pathlib
import shutil
import tempfile
from app import app, rpc, SSF_CFG_IP, SSF_CFG_PORT 
from flask import request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'zip', 'jpg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return "Versao Teste!!!!!"

@app.route('/rpc-call-base', methods=['POST'])
def rpc_call_base():

	try :
		input_rpc : dict = json.loads(request.headers.get('rpc-Json'))
		output_rpc = rpc.call(input_rpc)
		resp = jsonify(output_rpc)
		resp.status_code = 201
		return resp

	except Exception as exp:
		resp = jsonify({'message' : str(exp.args[0])})
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
		resp = jsonify({'message' : str(exp.args[0])})
		resp.status_code = 400
		return resp


@app.route('/download/<path:path>',methods = ['GET','POST'])
def rpc_call_download(path):
	"""Download a file."""
	try:
		rpc.log.debug('Val path ' + str(path))
		data : dict = rpc.infoAll(int(path))
		if data is None:
			raise FileNotFoundError

		path_all =  pathlib.Path(data['internal'])
		uploads = os.path.join(app.config.root_path, path_all.parent)
		return send_from_directory(uploads, path_all.name, as_attachment=True)

	except FileNotFoundError:

		resp = jsonify({'message' : 'File not found'})
		resp.status_code = 404
		return resp
		#abort(404)

	except TypeError as etp:
		resp = jsonify({'message' : str(etp.args[0])})
		resp.status_code = 400
		return resp		

	except Exception as exp:
		return exp

# @app.route('/get-files/<path:path>',methods = ['GET','POST'])
# def get_files(path):

#     """Download a file."""
#     try:
#         return send_from_directory(UPLOAD_FOLDER, path, as_attachment=True)
#     except FileNotFoundError:
#         abort(404)

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join('', '')
    return send_from_directory(directory=uploads, filename=filename)


# def do_download_file(book, book_format, client, data, headers):

#         # filename = os.path.join(config.config_calibre_dir, book.path)
#         # if not os.path.isfile(os.path.join(filename, data.name + "." + book_format)):
#         #     # ToDo: improve error handling
#         #     log.error('File not found: %s', os.path.join(filename, data.name + "." + book_format))

#         # if client == "kobo" and book_format == "kepub":
#         #     headers["Content-Disposition"] = headers["Content-Disposition"].replace(".kepub", ".kepub.epub")

# 		#https://www.fullstackpython.com/flask-helpers-make-response-examples.html

#         response = make_response(send_from_directory(filename, data.name + "." + book_format))
#         # ToDo Check headers parameter
#         for element in headers:
#             response.headers[element[0]] = element[1]
#         return response


if __name__ == "__main__":
	app.run(host=SSF_CFG_IP, port=SSF_CFG_PORT)
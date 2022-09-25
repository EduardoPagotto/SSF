#!/usr/bin/env python3
'''
Created on 20220924
Update on 20220924
@author: Eduardo Pagotto
'''

import os
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
    return "Versao inicial!!!!!"

@app.route('/rpc-call-base', methods=['POST'])
def rpc_call_base():

	try :
		output = rpc.call(request.headers.get('rpc-Json'))
		resp = jsonify(output)
		resp.status_code = 201
		return resp

	except Exception as exp:
		resp = jsonify({'message' : str(exp.args[0])})
		resp.status_code = 400
		return resp


@app.route('/rpc-call-upload', methods=['POST'])
def rpc_call_upload():

	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
        
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
        
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)

		with tempfile.TemporaryDirectory() as tmp:
			arquivoTemp = os.path.join(tmp, filename)
			file.save(arquivoTemp)

			# TODO: Aqui!!! preciso do nome do arquivo
			output = rpc.call(request.headers.get('rpc-Json'))
			
			if output['result'][0] is True:
				id = int(output['result'][1])
				reg = rpc.infoAll(id)
				file_final = reg['internal']

			shutil.move(arquivoTemp, file_final)
			
			resp = jsonify(output)
			resp.status_code = 201
			return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
		resp.status_code = 400
		return resp


@app.route('/rpc-call-download/<path:path>',methods = ['GET','POST'])
def rpc_call_download(path):

	"""Download a file."""
	# try:

	output = rpc.call(request.headers.get('rpc-Json'))

	return send_from_directory('111.jpg', path, as_attachment=True)
	# except FileNotFoundError:
	# 	abort(404)


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

#From flask import Response

# @app.route('/sendFile', methods=['POST'])
# def sendFile():
#     content = str(request.form['jsonval'])
#     return Response(content, 
#             mimetype='application/json',
#             headers={'Content-Disposition':'attachment;filename=zones.geojson'})

def do_download_file(book, book_format, client, data, headers):

        # filename = os.path.join(config.config_calibre_dir, book.path)
        # if not os.path.isfile(os.path.join(filename, data.name + "." + book_format)):
        #     # ToDo: improve error handling
        #     log.error('File not found: %s', os.path.join(filename, data.name + "." + book_format))

        # if client == "kobo" and book_format == "kepub":
        #     headers["Content-Disposition"] = headers["Content-Disposition"].replace(".kepub", ".kepub.epub")

		#https://www.fullstackpython.com/flask-helpers-make-response-examples.html

        response = make_response(send_from_directory(filename, data.name + "." + book_format))
        # ToDo Check headers parameter
        for element in headers:
            response.headers[element[0]] = element[1]
        return response


if __name__ == "__main__":
	app.run(host=SSF_CFG_IP, port=SSF_CFG_PORT)
import time
import threading
import flask
import json

from os import stat
from flask_cors import CORS

from repo import alarm, data_node, main_node

class Server:
	def __init__(self, host:str, port:int) -> None:
		app = flask.Flask(__name__)
		CORS(app, allow_headers=["*", "Content-Type", "Authorization", "Access-Control-Allow-Credentials"], supports_credentials=True)
		self.app = app
		self.host = host
		self.port = port

		@app.route('/alarm', methods=['POST'])
		def handle_alarm_set():
			data = flask.request.json
			data['ip'] = flask.request.remote_addr
			data['last_update'] = time.time()
			alarm.set(data['id'], data)
			return 'success'
		
		@app.route('/alarm/error', methods=['POST'])
		def handle_alarm_add_error():
			data = flask.request.json
			data['ip'] = flask.request.remote_addr
			data['last_update'] = time.time()
			alarm.add_error(data['id'], data['error'])
			return 'success'

		@app.route('/alarm', methods=['GET'], defaults={'id': None})
		@app.route('/alarm/<id>', methods=['GET'])
		def handle_alarm_get(id:str):
			return json.dumps(alarm.get(id))


		@app.route('/data_node', methods=['POST'])
		def handle_data_node_set():
			data = flask.request.json
			data['ip'] = flask.request.remote_addr
			data['last_update'] = time.time()
			data_node.set(data['id'], data)
			return 'success'

		@app.route('/alarm/error', methods=['POST'])
		def handle_data_node_add_error():
			data = flask.request.json
			data['ip'] = flask.request.remote_addr
			data['last_update'] = time.time()
			data_node.add_error(data['id'], data['error'])
			return 'success'

		@app.route('/data_node', methods=['GET'], defaults={'id': None})
		@app.route('/data_node/<id>', methods=['GET'])
		def handle_data_node_get(id:str):
			return json.dumps(data_node.get(id))

		
		@app.route('/main_node', methods=['POST'])
		def handle_main_node_set():
			data = flask.request.json
			data['ip'] = flask.request.remote_addr
			data['last_update'] = time.time()
			main_node.set(data['id'], data)
			return 'success'

				
	def start(self):
		t = threading.Thread(name='flask', target=lambda:self.app.run(host=self.host, port=self.port))
		t.setDaemon(True)
		t.start()

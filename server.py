import threading
import flask
import json

from os import stat

import repo

class Server:
	def __init__(self, host:str, port:int) -> None:
		app = flask.Flask(__name__)
		self.app = app
		self.host = host
		self.port = port

		@app.route('/alarm', methods=['POST'])
		def handle_alarm_auction_queue():
			data = flask.request.json
			data['ip'] = flask.request.remote_addr
			repo.set_alarm(data['id'], data)
			return 'success'
		
		@app.route('/alarm/error', methods=['POST'])
		def handle_alarm_add_error():
			data = flask.request.json
			data['ip'] = flask.request.remote_addr
			repo.add_alarm_error(data['id'], data['error'])
			return 'success'

		@app.route('/alarm', methods=['GET'], defaults={'id': None})
		@app.route('/alarm/<id>', methods=['GET'])
		def handle_alarm_get(id:str):
			return json.dumps(repo.get_alarm(id))
				
	def start(self):
		t = threading.Thread(name='flask', target=lambda:self.app.run(host=self.host, port=self.port))
		t.setDaemon(True)
		t.start()

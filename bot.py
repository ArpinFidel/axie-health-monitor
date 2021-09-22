import time
import threading
from util import stack_trace

from config import Config
from client import Client
from repo import alarm, data_node, main_node

class Bot:
	def __init__(self, client:Client) -> None:
		self.client = client

	def loop(self):
		while True:
			alarms = alarm.get()
			data_nodes = data_node.get()
			main_nodes = main_node.get()
			
			for m, xs, mod in [('alarm', alarms, alarm), ('data node', data_nodes, data_node), ('main node', main_nodes, main_node)]:
				for x in xs:
					try:
						last_update = time.time() - x['last_update']
						if last_update > Config.last_update_threshold:
							if 'sent_alarm' not in x or not x['sent_alarm']:
								self.client.send_message(f'{m} {x["id"]} is down ({last_update:.2f}s)', True, 'urgent-alert')
								mod.set(x['id'], {'sent_alarm': True})
						else:
							mod.set(x['id'], {'sent_alarm': False})
					except Exception as e:
						msg = stack_trace(e)
						print(msg)
						print(x)
			
	def start(self):
		t = threading.Thread(name='flask', target=self.loop)
		t.setDaemon(True)
		t.start()
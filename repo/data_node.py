import time
import threading

data_nodes = {}
data_nodes_lock = threading.RLock()

def set(id:str, data_node:dict):
	with data_nodes_lock:
		if id not in data_nodes:
			data_nodes[id] = {}
		data_nodes[id] |= data_node

def add_error(id:str, msg:str):
	with data_nodes_lock:
		if id not in data_nodes:
			data_nodes[id] = {}
		if 'errors' not in data_nodes[id]:
			data_nodes[id]['errors'] = {
				'errors': []
			}
		data_nodes[id]['errors']['errors'].append((msg, time.time()))

def get(id:str=None):
	with data_nodes_lock:
		if id is None:
			return list(data_nodes.values())
		return data_nodes[id].copy()

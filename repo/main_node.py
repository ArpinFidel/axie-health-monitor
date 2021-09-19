import time
import threading

main_nodes = {}
main_nodes_lock = threading.RLock()

def set(id:str, main_node:dict):
	with main_nodes_lock:
		if id not in main_nodes:
			main_nodes[id] = {}
		main_nodes[id] |= main_node

def add_error(id:str, msg:str):
	with main_nodes_lock:
		if id not in main_nodes:
			main_nodes[id] = {}
		if 'errors' not in main_nodes[id]:
			main_nodes[id]['errors'] = {
				'errors': []
			}
		main_nodes[id]['errors']['errors'].append((msg, time.time()))

def get(id:str=None):
	with main_nodes_lock:
		if id is None:
			return list(main_nodes.values())
		return main_nodes[id].copy()

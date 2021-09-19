import time
import threading

alarms = {}
alarms_lock = threading.RLock()

def set(id:str, alarm:dict):
	with alarms_lock:
		if id not in alarms:
			alarms[id] = {}
		alarms[id] |= alarm

def add_error(id:str, msg:str):
	with alarms_lock:
		if id not in alarms:
			alarms[id] = {}
		if 'errors' not in alarms[id]:
			alarms[id]['errors'] = {
				'errors': []
			}
		alarms[id]['errors']['errors'].append((msg, time.time()))

def get(id:str=None):
	with alarms_lock:
		if id is None:
			return list(alarms.values())
		return alarms[id].copy()
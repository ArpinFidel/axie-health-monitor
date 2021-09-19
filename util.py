import time
import requests
import datetime
import os
import sys

import git

class Timer:
	def __init__(self):
		self.last = [time.perf_counter()]
	def time(self, idx=-1):
		diff = time.perf_counter()-self.last[idx]
		self.last.append(time.perf_counter())
		return diff

def stack_trace(e):
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	msg = f'{exc_type} {exc_obj} "./{fname}", line {exc_tb.tb_lineno}\n{e}'
	return msg

def log(file_name:str, msg:str):
	with open(file_name, 'a') as f:
		f.write(msg+'\n')

def get_ip() -> str:
	ip = requests.get('https://api.ipify.org').text
	return ip

def get_last_commit_date() -> datetime.datetime:
	repo = git.Repo(search_parent_directories=True)
	return repo.head.object.committed_datetime
	
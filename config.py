import os
import dotenv
import requests
import threading

from util import *

dotenv.load_dotenv()

class Config:
	configurator_url = os.getenv('CONFIGURATOR_URL')
	configurator_url_lock = threading.RLock()

	http_port = 8083
	discord_key = os.getenv('DISCORD_KEY')
	last_update_threshold = 120

	@staticmethod
	def set_configurator_url(url:str):
		with Config.configurator_url_lock:
			Config.configurator_url = url

	@staticmethod
	def set_config(**kwargs):
		for k, v in kwargs:
			vars()[k] = v

	@staticmethod
	def fetch_config() -> str:
		try:
			resp = requests.get(Config.configurator_url).json()
			Config.set_config(**resp)
		except Exception as e:
			return stack_trace(e)

		return None
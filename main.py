from server import Server
from config import Config

if __name__ == '__main__':
	server = Server('0.0.0.0', Config.http_port)
	server.start()

	input()
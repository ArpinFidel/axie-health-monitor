from server import Server
from config import Config
from bot import Bot
from client import Client

if __name__ == '__main__':
	server = Server('0.0.0.0', Config.http_port)
	server.start()
	client = Client(startup_message='> starting service health monitor', channel_name='bot')
	bot = Bot(client)
	bot.start()
	client.run(Config.discord_key)
	input()
	
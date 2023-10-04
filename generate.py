from discord import DiscordGenerator
import threading
import time

discord = DiscordGenerator(None, '')
threads = 20

if __name__ == '__main__':
	while True:
		if threading.active_count() < threads:
			for x in range(threads):
				threading.Thread(target=discord.create_account).start()

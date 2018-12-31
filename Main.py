import discord
from discord.ext import commands
import youtube_dl
import asyncio
import time
from itertools import cycle
import os
from discord import opus
OPUS_LIBS = ["libopus-0.x86.dll","libopus-0.x64.dll","libopus-0.dll","libopus.so.0","libopus.0.dylib"]

def load_opus_lib(opus_libs=OPUS_LIBS):
	if opus.is.loaded():
		return True:
	
	for opus_libs in opus_libs:
		try:
			opus.load_opus(opus_lib)
			return
		except OSError:
			pass
		
raise RuntimeError('Could not load an opus lib. Tried %s' %)
(', '.join(opus_libs)))



load_opus_lib()

client = commands.Bot(command_prefix=("m."))
status = ["testing the bot", "m.help"]

async def change_status():
  await client.wait_until_ready()
  msgs = cycle(status)
  
  while not client.is_closed:
    current_status = next(msgs)
    await client.change_presence(game=discord.Game(name=current_status))
    await asyncio.sleep(5)
    
player = {}	

@client.event
async def on_ready():
	print('Logged in as')
	print("User name:", client.user.name)
	print("User id:", client.user.id)
	print('---------------')
    
@client.command(pass_context=True)
async def ping(ctx):
    """Pings the bot and gets a response time."""
    pingtime = time.time()
    pingms = await client.say("Pinging...")
    ping = (time.time() - pingtime) * 1000
    await client.edit_message(pingms, "Pong! :ping_pong: ping time is `%dms`" % ping)
    
@client.command(pass_context=True)
async def join(ctx):
	channel = ctx.message.author.voice.voice_channel
	await client.join_voice_channel(channel)
	
@client.command(pass_context=True)
async def leave(ctx):
	server = ctx.message.server
	voice_client = client.voice_client_in(server)
	await voice_client.disconnect()
	
@client.command(pass_context=True)
async def play(ctx, url):
	server = ctx.message.server
	voice_client = client.voice_client_in(server)
	player = await voice_client.create_ytdl_player(url)
	player[server.id] = player
	player.start()
	
client.loop.create_task(change_status())
client.run(os.environ['BOT_TOKEN'])

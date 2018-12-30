import discord
from discord.ext import commands
import asyncio
import time
from itertools import cycle
import os

bot = commands.Bot(command_prefix=("m."))
status = ["testing the bot", "m.help"]

async def change_status():
  await bot.wait_until_ready()
  msgs = cycle(status)
  
  while not bot.is_closed:
    current_status = next(msgs)
    await bot.change_presence(game=discord.Game(name=current_status))
    await asyncio.sleep(5)
    
@bot.event
async def on_ready():
	print('Logged in as')
	print("User name:", bot.user.name)
	print("User id:", bot.user.id)
	print('---------------')
    
@bot.command(pass_context=True)
async def ping(ctx):
    """Pings the bot and gets a response time."""
    pingtime = time.time()
    pingms = await bot.say("Pinging...")
    ping = (time.time() - pingtime) * 1000
    await bot.edit_message(pingms, "Pong! :ping_pong: ping time is `%dms`" % ping)
    
@bot.command(pass_context=True)
async def join(ctx):
	channel = ctx.message.author.voice.voice_channel
	await bot.join_voice_channel(channel)
	
@bot.command(pass_context=True)
async def leave(ctx):
	server = ctx.message.server
	voice_client = bot.voice_client_in(server)
	
bot.loop.create_task(change_status())
bot.run(os.environ['BOT_TOKEN'])

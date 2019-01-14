import discord
from discord.ext import commands
import asyncio
import requests, bs4
from itertools import cycle
import os
import time
import youtube_dl
from discord import opus

client = commands.Bot(command_prefix=("m."))
client.remove_command("help")
status = ["testing the bot", "m.help", "created by noobperson"]

async def change_status():
	await client.wait_until_ready()
	msgs = cycle(status)
	
	while not client.is_closed:
		current_status = next(msgs)
		await client.change_presence(game=discord.Game(name=current_status))
		await asyncio.sleep(4)

players = {}	

@client.event 
async def on_ready():
	print('Logged in as')
	print("User name:", client.user.name)
	print("User id:", client.user.id)
	print('---------------')

@client.command(pass_context=True, no_pm=True)
async def ping(ctx):
    pingtime = time.time()
    pingms = await client.say("Pinging...")
    ping = (time.time() - pingtime) * 1000
    await client.edit_message(pingms, "Pong! :ping_pong: ping time is `%dms`" % ping)
    
@client.command(pass_context=True, no_pm=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    embed = discord.Embed(description=" ")
    embed.add_field(name="Successfully connected to voice channel:", value=channel)
    await client.say(embed=embed)
	
@client.command(pass_context=True, no_pm=True)
async def leave(ctx):
    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()
    embed = discord.Embed(description=" ")
    embed.add_field(name="Successfully disconnected from:", value=channel)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def pause(ctx):
    author = ctx.message.author
    id = ctx.message.server.id
    players[id].pause()
    embed = discord.Embed(description=" ")
    embed.add_field(name="Player Paused", value=f"Requested by {ctx.message.author.name}")
    await client.say(embed=embed)

@client.command(pass_context=True)
async def stop(ctx):
    author = ctx.message.author
    id = ctx.message.server.id
    players[id].stop()
    embed = discord.Embed(description=" ")
    embed.add_field(name="Player Stopped", value=f"Requested by {ctx.message.author.name}")
    await client.say(embed=embed)
	
@client.command(pass_context=True)
async def play(ctx, *, name):
	author = message.author
	name = message.content.replace("m.play ", '')
	fullcontent = ('http://www.youtube.com/results?search_query=' + name)
	text = requests.get(fullcontent).text
	soup = bs4.BeautifulSoup(text, 'html.parser')
	img = soup.find_all('img')
	div = [ d for d in soup.find_all('div') if d.has_attr('class') and 'yt-lockup-dismissable' in d['class']]
	a = [ x for x in div[0].find_all('a') if x.has_attr('title') ]
	title = (a[0]['title'])
	a0 = [ x for x in div[0].find_all('a') if x.has_attr('title') ][0]
	url = ('http://www.youtube.com'+a0['href'])
	delmsg = await client.say('Now Playing ** >> ' + title + '**')
	server = ctx.message.server
	voice_client = client.voice_client_in(server)
	player = await voice_client.create_ytdl_player(url)
	players[server.id] = player
	print("User: {} From Server: {} is playing {}".format(author, server, title))
	player.start()
	embed = discord.Embed(description=" ")
	embed.add_field(name="Now Playing", value=title)
	await client.say(embed=embed)

@client.command(pass_context=True)
async def resume(ctx):
    author = ctx.message.author
    id = ctx.message.server.id
    players[id].resume()
    embed = discord.Embed(description=" ")
    embed.add_field(name="Player Resumed", value=f"Requested by {ctx.message.author.name}")
    await client.say(embed=embed)

@client.command(no_pm=True)
async def credits():
	"""credits who helped me"""
	await client.say('iHoverZz#2321 helped me with this music bot')
	
@client.command(pass_context=True, no_pm=True)
async def help(ctx):
	embed = discord.Embed(title="Help section", description=" ", color=0xFFFF)
	embed.add_field(name="m.join", value="make the bot join voice channel")
	embed.add_field(name="m.leave", value="make the bot leave the voice channel")
	embed.add_field(name="m.play", value="please be careful when using this command it will break if theres music playing.")
	embed.add_field(name="m.stop", value="to stop the music from playing")
	embed.add_field(name="m.pause", value="to pause the playing music")
	embed.add_field(name="m.resume", value="to resume the music")
	embed.add_field(name="m.credits", value="shows who helped me with this bot")
	embed.add_field(name="m.ping", value="get bot's ping time")
	await client.say(embed=embed)
	
client.loop.create_task(change_status())
client.run(os.environ['BOT_TOKEN'])

from discord.ext import commands
from dotenv import load_dotenv
from discord.utils import get
from llama_utils import *
import discord
import asyncio
import json
import time
import os

load_dotenv()
URL = os.getenv('URL')
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')

intents = discord.Intents.default()
intents.message_content=True
bot = commands.Bot(command_prefix="!", intents=intents)

llms = {'chat': ['gemma3:4b'],
        'code': ['qwen2.5-coder:7b']}


@bot.event
async def on_ready():
	guild = get(bot.guilds, name=GUILD)
	print(f'{bot.user} in online')


@bot.command(name='ping')
async def ping(ctx):
	await ctx.send('AYOOOOO :wave:')


@bot.command(name='models')
async def show_models(ctx):
	client = setup_client(URL)
	m = list_models(client)
	models = '\n'.join(m)
	reply = f'**I am Equipped to use the following Models:**\n{models}'
	await ctx.send(reply)


@bot.command(name='ask')
async def ask_llm(ctx, *arg):
	question = ' '.join(arg[:])
	# assume longer questions take longer to answer
	if len(question) > 42:
		await ctx.send('*working on it...*')
		time.sleep(0.1)
		await ctx.send(':robot:')
	client = setup_client(URL)
	try:
		reply = ask_model(client,'gemma3:4b', question).message.content
	except:
		reply = ':x: **ERROR** Sorry about that. Something seems to have gone wrong.'
		pass
	await send_discord_reply(ctx, reply)


@bot.command(name='code')
async def vibe_code(ctx, *arg):
	prompt = ' '.join(arg[:])
	# assume longer questions take longer to answer
	if len(prompt) > 42:
		await ctx.send('*working on it...*')
		time.sleep(0.1)
		await ctx.send(':robot:')
	client = setup_client(URL)
	try:
		reply = ask_model(client,'qwen2.5-coder:7b', prompt).message.content
	except:
		reply = ':x: **ERROR** Sorry about that. Something seems to have gone wrong.'
		pass
	await send_discord_reply(ctx, reply)

async def send_discord_reply(ctx,reply):
	# if reply is longer than 2000 characters send in chunks
	MAX_LEN = 2000
	MSG_LEN = len(reply)
	if MSG_LEN > MAX_LEN:
		N = round(MSG_LEN / MAX_LEN)
		for i in range(N):
			chunk = ''.join(list(reply)[i * MAX_LEN:(i + 1) * MAX_LEN])
			await ctx.send(chunk)
	else:
		await ctx.send(reply)


@bot.command(name='delete', aliases=['del','rm'])
async def delete_last_three(ctx, *arg):
	"""Deletes the last 3 messages from the channel where this command was used."""
	try:
		if len(arg) >= 1:
			N = int(arg[-1])
		else:
			N = 2
		# Get the messages in the channel
		await ctx.channel.purge(limit=N)
		await ctx.send(f':wastebasket: **{N}** Messages Deleted')
	except Exception as e:
		await ctx.send(f"An error occurred: {e}")


def main():
	bot.run(TOKEN)


if __name__ == '__main__':
	main()

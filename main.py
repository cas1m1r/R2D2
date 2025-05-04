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

llms = {'chat': 'gemma3:4b',
        'code': 'qwen3:8b'}


@bot.event
async def on_ready():
	guild = get(bot.guilds, name=GUILD)
	print(f'{bot.user} in online')


@bot.command(name='ping')
async def ping(ctx):
	await ctx.send('Hey! :wave:')


@bot.command(name='models')
async def show_models(ctx):
	client = setup_client(URL)
	m = list_models(client)
	models = '\n'.join(m)
	reply = f'**I am Equipped to use the following Models:**\n{models}'
	await ctx.send(reply)


@bot.command(name='ask')
async def ask_llm(ctx, *arg):
	global llms
	question = ' '.join(arg[:])
	# assume longer questions take longer to answer
	if len(question) > 42:
		await ctx.send('*working on it...*')
		time.sleep(0.1)
		await ctx.send(':robot:')
	client = setup_client(URL)
	try:
		reply = ask_model(client, llms['chat'], question).message.content
	except:
		reply = ':x: **ERROR** Sorry about that. Something seems to have gone wrong.'
		pass
	await send_discord_reply(ctx, reply.split('</think>')[-1])


@bot.command(name='code',aliases=['w','write'])
async def vibe_code(ctx, *arg):
	global llms
	prompt = ' '.join(arg[:])
	# assume longer questions take longer to answer
	if len(prompt) > 42:
		await ctx.send('*working on it...*')
		time.sleep(0.1)
		await ctx.send(':robot:')
	client = setup_client(URL)
	try:
		reply = ask_model(client, llms['code'], prompt).message.content
	except:
		reply = ':x: **ERROR** Sorry about that. Something seems to have gone wrong.'
		pass
	await send_discord_reply(ctx, reply.split('</think>')[-1])


@bot.command(name='delete-model',aliases=['rm-model'])
async def delete_model(ctx, *arg):
	if len(arg) >=1:
		model_name = arg[-1]
		client = setup_client(URL)
		models = list_models(client)
		if model_name not in models:
			confused = f"I don't have that model... :thinking:\n"
			confused += "maybe try `!models`"
			await ctx.send(confused)
		else:
			client.delete(model_name)
			await ctx.send(f':boom: {model_name} has been **deleted**')
	else:
		await ctx.send(f'Please give me a model name to remove')


@bot.command(name='get-model')
async def get_model(ctx, *arg):
	if len(arg) >=1:
		model_name = arg[-1]
		client = setup_client(URL)
		models = list_models(client)
		if model_name in models:
			confused = f"I already have {model_name}... :thinking:\n"
			await ctx.send(confused)
		else:
			await ctx.send(f':satellite_orbital: downloading {model_name}')
			client.pull(model_name)
			await ctx.send(f':brain: {model_name} has been **added**')
	else:
		await ctx.send(f'Please give me a model name to download')


@bot.command(name='set-coder')
async def change_coder(ctx, *arg):
	global llms
	if len(arg)>=1:
		new_model = arg[-1]
		client = setup_client(URL)
		models = list_models(client)
		# verify we have this model
		if new_model not in models:
			await ctx.send(f":thinking: I can't use that model because I cannot find it.")
		else:
			llms['code'] = new_model
			await ctx.send(f":white_check_mark: All set!")
	else:
		await ctx.send(f'Please give me a model to switch to')


@bot.command(name='set-chat')
async def change_chatter(ctx, *arg):
	global llms
	if len(arg)>=1:
		new_model = arg[-1]
		client = setup_client(URL)
		models = list_models(client)
		# verify we have this model
		if new_model not in models:
			await ctx.send(f":thinking: I can't use that model because I cannot find it.")
		else:
			llms['chat'] = new_model
			await ctx.send(f":white_check_mark: All set!")
	else:
		await ctx.send(f'Please give me a model to switch to')


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
async def delete_messages(ctx, *arg):
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

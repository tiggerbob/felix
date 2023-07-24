# bot.py
import os

import discord
from discord.ext import commands
from datetime import datetime, timedelta

TOKEN = "MTEzMjE2MDM3OTMxNzkxOTc5Nw.GyFqpm.x5EOqIogKoJI0IWpHvl5TD2RjXMEDqPz4J1EsE"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!")

embed = discord.Embed(title="Unread Messages", description="Here's what you missed", color=0x0000ff)
tiggen_messages = ""
loyl_messages = ""
tiggen_time = ""
loyl_time = ""
# The person that sent the messages
current_reader = ""

UTC_TIME_DIFF = 7

@bot.event
async def on_ready():
	print(bot.user.name, "is connected to Discord!")

@bot.event
async def on_message(message):
	global embed, tiggen_messages, loyl_messages, current_reader, tiggen_time, loyl_time, UTC_TIME_DIFF

	await bot.process_commands(message)

	if message.author == bot.user:
		return

	if message.content != "!delete" and message.content != "!inbox":
		if message.author.id == 1131062164866744350:
			# loyl
			if current_reader == message.author.name:
				loyl_messages += message.content + "\n"
				timestamp = message.created_at + timedelta(hours=UTC_TIME_DIFF)
				loyl_time += timestamp.strftime("%H:%M") + "\n"
			else:
				current_reader = message.author.name
				embed = discord.Embed(title="Unread Messages", description="Here's what you missed", color=0x0000ff)
				loyl_messages = message.content + "\n"
				timestamp = message.created_at + timedelta(hours=UTC_TIME_DIFF)
				loyl_time = timestamp.strftime("%H:%M") + "\n"
				tiggen_messages = ""
				tiggen_time = ""
		elif message.author.id == 689281847469015130:
			# tiggen
			if current_reader == message.author.name:
				tiggen_messages += message.content + "\n"
				timestamp = message.created_at + timedelta(hours=UTC_TIME_DIFF)
				tiggen_time += timestamp.strftime("%H:%M") + "\n"
			else:
				current_reader = message.author.name
				embed = discord.Embed(title="Unread Messages", description="Here's what you missed", color=0x0000ff)
				tiggen_messages = message.content + "\n"
				timestamp = message.created_at + timedelta(hours=UTC_TIME_DIFF)
				tiggen_time = timestamp.strftime("%H:%M") + "\n"
				loyl_messages = ""
				loyl_time = ""

@bot.command(name="inbox")
async def show_inbox(ctx):
	global embed, tiggen_messages, loyl_messages, tiggen_time, loyl_time
	if ctx.message.author.id == 1131062164866744350:
		# show tiggentime's messages
		if not embed.fields:
			embed.add_field(name="tiggen", value=tiggen_time, inline=True)
			embed.add_field(name="\u200b", value=tiggen_messages, inline=True)
		await ctx.send(embed=embed)
	elif ctx.message.author.id == 689281847469015130:
		# show loyl's messages
		if not embed.fields:
			embed.add_field(name="loyl", value=loyl_time, inline=True)
			embed.add_field(name="\u200b", value=loyl_messages, inline=True)
		await ctx.send(embed=embed)

@bot.command(name="delete")
async def delete_channel(ctx):
	for c in ctx.guild.channels:
		await c.delete()
	await ctx.guild.create_category("Text Channels")
	await ctx.guild.create_category("Voice Channels")

	text_category = discord.utils.get(ctx.guild.categories, name="Text Channels")
	voice_category = discord.utils.get(ctx.guild.categories, name="Voice Channels")

	await ctx.guild.create_text_channel('general', category=text_category)
	await ctx.guild.create_voice_channel('General', category=voice_category)

bot.run(TOKEN)

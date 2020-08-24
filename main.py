from dotenv import load_dotenv
import discord
import io
import os

load_dotenv()

prefix = '!'
rules_channel_id = '637046065140596774';

async def package_cmd(message, args):
	history = await message.channel.history(limit = 2).flatten()

	file_content = history[1].content

	await message.channel.delete_messages(history)
	
	if (file_content.startswith('```') and file_content.endswith('```')):
		file_content = file_content[file_content.index('\n') + 1:len(file_content) - 1 - file_content[::-1].index('\n')]

	data = io.BytesIO(bytearray(file_content, encoding='utf-8'))
	filename = 'index.' + args[1]
	await message.channel.send(file=discord.File(filename=filename, fp=data))


class Client(discord.Client):
	async def on_ready(self):
		print('Bot running')

	async def on_message(self, message):
		# filter
		if ('discord.gg' in message.content):
			await message.channel.delete_messages([message])
			await message.channel.send('As stated by rule #1 in <#{channel}>, discord links are not allowed in this server.'
			.format(channel=rules_channel_id))

		if (not message.content.startswith(prefix)):
			return
		
		args = message.content[1:].split(' ')
		command = args[0]

		if (command == 'package' or command == 'pkg'):
			await package_cmd(message, args)
	
	async def on_member_join(self, member):
		await member.add_roles(discord.utils.find(lambda m: m.name.lower() == 'member', member.guild.roles))
		await discord.utils.find(lambda m: m.name.lower() == 'welcome', member.guild.channels).send(':small_blue_diamond:'+ member.name + ' Joined!')

	async def on_member_remove(self, member):
		await discord.utils.find(lambda m: m.name.lower() == 'welcome', member.guild.channels).send(':small_orange_diamond:'+ member.name + ' Left.')

	async def on_command_error(self, ctx, error):
		print(error)
		ctx.message.channel.send('An unexpected error has occured:\n```' + error + '```');

client = Client()
client.run(os.getenv('DISCORD_TOKEN'))
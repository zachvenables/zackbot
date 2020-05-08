import discord
import group
import user
import os
from discord.ext import commands

client = commands.Bot(command_prefix = '.')
group_list = []


def contains_group(msg):
	for item in group_list:
		if item.name == msg:
			return True

	return False


def get_user_id(user):
	for item in client.users:
		if item.name.lower() == user:
			return str(item.id)

def get_group(groupname):
	for item in group_list:
		if item.name.lower() == groupname.lower():
			return item

	return None


def is_valid_username(username):
	for item in client.users:
		if item.name.lower() == username.lower():
			return True

	return False


async def message_group(groupname, channel):
	message = ''
	for item in group_list:
		if item.name == groupname:
			for user in item.users:
				message += '<@' + get_user_id(user) + '> '

	await channel.send(message)


@client.event
async def on_ready():
	for file in os.listdir():
		if '_boys' in file:
			group_name = file[:-4]
			current_group = group.Group(group_name)
			group_list.append(current_group)
			f = open(file, 'r')
			for line in f.read().splitlines():
				current_group.add_user(line)

			f.close()

	print('Bot is running.')


@client.event
async def on_message(msg):
	msg_list = msg.content.split(' ')
	channel = msg.channel


	if msg.content == 'ping':
		await channel.send('pong')
	

	if contains_group(msg.content):
		await message_group(msg.content, channel)
	

	if msg_list[0] == 'new_group':
		if msg_list[1] != None and '_boys' in msg_list[1] and not contains_group(msg_list[1]):
			group_name = msg_list[1]
			group_list.append(group.Group(group_name))
			file = open(group_name + '.txt', 'w+')
			file.close()
			await channel.send('New group ' + group_name + ' added.')
		else:
			await channel.send('Must provide valid group name.')


	if msg_list[0] == 'add_user':
		addgroup = None
		if('to' in msg_list):
			addgroup = get_group(msg_list[msg_list.index('to')+1])

		if addgroup != None:
			i=1
			while msg_list[i] != 'to':
				username = msg_list[i].lower()
				if is_valid_username(username):
					if username not in addgroup.users:
						addgroup.add_user(username)
						file = open(addgroup.name + '.txt', 'a')
						file.write(username + '\n')
						file.close()
						await channel.send(addgroup.name + ' updated.')
					else:
						await channel.send(username + ' is already in that group.')
				else:
					await channel.send(username + ' is an invalid username.')
				i += 1
		else:
			await channel.send('Not a valid group name')


	#if msg_list[0] == 'delete_group':
	#	if contains_group(msg_list[1].lower()):
			

client.run('NzA4MzAxNjA4NjMwMzUzOTcw.XrVZeQ.WCFr7VNw41dFB2hkSYLy8JdPk5k')
import discord
from discord.ext import commands, tasks
import json

with open('setting.json','r', encoding='utf8') as setting:
    data = json.load(setting)

bot = commands.Bot(command_prefix = '!')
@bot.event
async def on_ready():
    print('>>Bot is OK!')
@bot.event
async def on_message(msg):
    t = msg.content
    ans = data["ANS"]
    use = [0,0,0,0,0]
    a = 0
    b = 0
    if(len(t) == 5 and str(msg.channel) == data["GAME"] and msg.author != bot.user and t[0] != '!'):
        for i in range(5):
            if t[i] == ans[i]:
                a+=1
                use[i] = 1
        for i in range(5):
            for j in range(5):
                if t[j] == ans[i] and not use[j]:
                    b+=1
                    use[j] = 1
        await msg.reply(f'{a}A{b}B')
        if(a == 5):
            await msg.delete(delay = 0.01)
            role_name = data["ROLE"]
            
            guild = bot.get_guild(msg.guild.id)
            role_id = 0
            for i in guild.roles:
                if(i.name == role_name):
                    role_id = i.id
            if role_id == 0:
                await guild.create_role(name = role_name)
            for i in guild.roles:
                if(i.name == role_name):
                    role_id = i.id
            role = guild.get_role(role_id)
            await msg.author.add_roles(role)
        elif(a>0 or b > 0):
            await msg.delete(delay = 0.5)
    elif (len(t) == 4 and str(msg.channel) == data["GAME"] and msg.author != bot.user and t[0] != '!'):
        if(t == data["CANCEL"]):
            await msg.delete(delay = 0.5)
            role_name = data["ROLE"]
            guild = bot.get_guild(msg.guild.id)
            role_id = 0
            for i in guild.roles:
                if(i.name == role_name):
                    role_id = i.id
            if role_id == 0:
                await guild.create_role(name = role_name)
            for i in guild.roles:
                if(i.name == role_name):
                    role_id = i.id
            role = guild.get_role(role_id)
            await msg.author.remove_roles(role)

bot.run(data["TOKEN"])
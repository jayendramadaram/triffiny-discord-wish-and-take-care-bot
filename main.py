
import os
import discord
from subprocess import run

import sqlite3
import random
from keep_alive import keep_alive

from discord.ext import tasks
import asyncio
from replit import db




my_secret = os.environ['TOKEN']


client = discord.Client()
flag = 0

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@tasks.loop(hours = 24)
async def msg1():
    message_channel = client.get_channel(880048418339295272)
    await message_channel.send("test 1")


@msg1.before_loop
async def before_msg1():
    while 1:
        print("its time")
        return


def sql_fetch(con):

    cursorObj = con.cursor()

    cursorObj.execute('SELECT * FROM tasks')

    rows = cursorObj.fetchall()

    return rows

def sql_insert(con, entities):

    cursorObj = con.cursor()
    
    cursorObj.execute('INSERT INTO tasks( name, date_s , date_end) VALUES( ?, ?, ?)', entities)
    
    con.commit()
def sql_del(con, entity):

    cursorObj = con.cursor()
    
    cursorObj.execute('DELETE FROM tasks WHERE name=?',(entity,))
    
    con.commit()


@client.event
async def on_message(message):

    global flag

    if message.author == client.user:
        return

    if message.content.startswith('##'):
      await message.reply("yo i am with ya")


    #PUBLIC SEARCH
    if message.content.startswith('!'):
        print("REQUEST:", message.content,'> requested by {}'.format(message.author.name))
        content = message.content.strip().split()
        if len(content) >= 1 :
            # print(1)
            if 'random' in content or 'randomize' in content and flag==0:
                
                await message.reply('cool i will randomize dude tell me what are your picks')
                flag = 1
        else:
            await message.reply('Check usage guide...')
    elif flag==1:
        await message.reply(random.choice(message.content.strip().split()))
        flag=0
    elif message.content.startswith('$'):
        con = sqlite3.connect('mydatabase.db')
        if "show" in message.content.split() and "tasks" in message.content.split():
            rows = sql_fetch(con)
            for i in rows:
                await message.channel.send(i)
            await message.reply("yo reached bottom honey")
            con.close()
        elif "add" in message.content.split():
            await message.reply('umm hmm alright bud i will insert tell me your tasks in < TASK | DATE_START | DATE_END  > format is must make about spaces and symbols')
        elif "delete" or "done" in message.content.split():
            await message.reply('Congrats honey your task log is becomming short ')
    elif message.content.startswith('<') and message.content.endswith('>'):
        con = sqlite3.connect('mydatabase.db')
        msg = message.content.split()
        if len(msg)>= 7:
            entities = (  msg[1] , msg[3] , msg[5])
            sql_insert(con, entities)
            rows = sql_fetch(con)
            for i in rows:
                await message.channel.send(i)
            await message.reply("yep added it to db check it out")
            con.close()
        elif len(msg)== 3:
            entity = msg[1]
            sql_del(con, entity)
            rows = sql_fetch(con)
            for i in rows:
                await message.channel.send(i)
            await message.reply("oh yeah deleted fro db check it out")
            con.close()
    elif "change" in message.content and "dp" in message.content:
      rand = random.randint(1,7)
      if rand == int(db['8']):
        rand = random.randint(1,7)
      # print(rand , db['8'] , type(rand) , type(db['8']))
      img = '{}.jpg'.format(db[str(rand)])
      # print(img)
      with open(img, 'rb') as image:
        await message.reply("alright here i go how is my new look")
        await client.user.edit(avatar=image.read())
        db['8'] = rand


keep_alive()
client.run(my_secret)




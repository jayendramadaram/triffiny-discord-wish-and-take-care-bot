import sqlite3
import os
import discord
from subprocess import run

import asyncio
import datetime as dt
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
    msg1.start()


@tasks.loop(hours=24)
async def msg1():
    message_channel = client.get_channel(884854235441791086)
    num = db["day"]
    await message_channel.send("hey honey you have only `{}` days to achevie your dreams here are your tasks".format(num))
    con = sqlite3.connect('mydatabase.db')
    rows = sql_fetch(con)
    for i in rows:
        await message_channel.send(i)
    con.close()

    await message_channel.send("-----------------------------------------------------------------------")
    
    await message_channel.send("-----------------------------------------------------------------------")
    db["day"] = int(db["day"]) - 1


@msg1.before_loop
async def before_msg1():
    for _ in range(60*60*24):
      if dt.datetime.now().hour == 9:  
            return
      await asyncio.sleep(1)


def sql_note(entities , con):
    cursorObj = con.cursor()

    
    cursorObj.execute('INSERT INTO note( name) VALUES( ?)', [entities])
    
    con.commit()

def sql_nots(con):

    cursorObj = con.cursor()

    cursorObj.execute('SELECT * FROM note')

    rows = cursorObj.fetchall()

    return rows


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
            con.close()
        elif "delete" or "done" in message.content.split():
            await message.reply('Congrats honey your task log is becomming short ')
            con.close()
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
      if rand == int(db["rand"]):
        rand = random.randint(1,7)
      img = '{}.jpg'.format(db[str(rand)])
      with open(img, 'rb') as image:
        await message.reply("alright here i go how is my new look")
        await client.user.edit(avatar=image.read())
        db["rand"] = rand
    elif message.content.startswith("note:"):
      entities =  str(message.content.split(":")[1])
      # print(entities)
      con = sqlite3.connect('mydatabase.db')
      sql_note(entities , con)
      con.close()
    elif "notes" in message.content and "show" in message.content:
      con = sqlite3.connect('mydatabase.db')
      for i in sql_nots(con):
        await message.channel.send(i)
      await message.reply("this is your current list")
      con.close()
    elif message.content.startswith("strategy:"):
      entities =  str(message.content.split(":")[1])
      db["strat"] = entities
    elif "strat" in message.content and "show" in message.content:
      con = sqlite3.connect('mydatabase.db')
      await  message.channel.send("strat")
      con.close()
    


keep_alive()
client.run(my_secret)


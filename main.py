import sqlite3
import os
import discord

import asyncio
import datetime as dt
import random
from keep_alive import keep_alive

from discord.ext import tasks
import asyncio
from replit import db
import json




my_secret = os.environ['TOKEN']


client = discord.Client()
flag = 0

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    activity = discord.Game(name="with jay")
    await client.change_presence(status=discord.Status.offline, activity=activity)
    msg1.start()


@tasks.loop(hours=24)
async def msg1():
    message_channel = client.get_channel(884854235441791086)
    num = db["day"]
    myid = '<@763029387674124288>'
    await message_channel.send("%s honey you have only `{}` days to achevie your dreams here are your tasks".format(num) % myid)
    con = sqlite3.connect('mydatabase.db')
    rows = sql_fetch(con)
    for i in rows:
        await message_channel.send(i)
    con.close()

    await message_channel.send("-----------------------------------------------------------------------")
    if db['strat'] != "":
      await message_channel.send(db['strat'])
      await message_channel.send("-----------------------------------------------------------------------")
    db["day"] = int(db["day"]) - 1
    with open(r'tasks.json' , "r") as js:
      data = json.loads(js.read())
      for i in range(len(data)):
        if int(data[i]["dueDate"].split("-")[2]) < int(dt.datetime.now().strftime("%d")):
          await message_channel.send("pending schedule `{0}` on `{1}`".format(data[i]['task'] ,data[i]['dueDate'] ))
        elif int(data[i]["dueDate"].split("-")[2]) == int(dt.datetime.now().strftime("%d")):
          await message_channel.send("```todays schedule {}```".format(data[i]['task']))
          break



@msg1.before_loop
async def before_msg1():
    for _ in range(60*60*24):
      if dt.datetime.now().hour == 1:  
            return
      await asyncio.sleep(1)
def sql_note(entities , con):
    cursorObj = con.cursor()

    
    cursorObj.execute('INSERT INTO note( name) VALUES( ?)', [entities])
    
    con.commit()

def task_com(task):
  with open(r'tasks.json' , "r") as js:
    data = json.loads(js.read())
    for i in range(len(data)):
      if data[i]['dueDate'].split("-")[2] == task:
        data.pop(i)
        break
    with open("tasks.json" , "w") as dat:
      dat.write(
      json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
  
  

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

    elif message.content.startswith('##'):
      await message.reply("yo i am with ya")

    elif message.content.strip() == "help":
      await message.channel.send("""
      ```
      ## --> to check uptime of bot\n
      ! + randomize/random  --> to random choice\n
      < content | date end | time will be taken > --> task add to sqlite3\n
      < content_name > --> delete task from sqlite3\n
      input ==sentence with **change && dp** --> changes profile pic\n
      note: content --> adds to notice list\n
      strategy: content  --> adds stretegy\n
      complete! content  --> deletes from JSON
      ```
      """)

    #PUBLIC SEARCH
    elif message.content.startswith('!'):
        print("REQUEST:", message.content,'> requested by {}'.format(message.author.name))
        content = message.content.strip().split()
        if len(content) >= 1 :
            if 'random' in content or 'randomize' in content and flag==0:
                await message.reply('cool i will randomize dude tell me what are your picks')
                flag = 1
        else:
            await message.reply('Check usage guide...')
    elif flag==1:
        await message.reply(random.choice(message.content.strip().split()))
        flag=0
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
    elif message.content.startswith("strategy:"):
      entities =  str(message.content.split(":")[1])
      db["strat"] = entities
    elif message.content.startswith("completed!"):
      task = message.content.split("!")[1]
      task_com(task)
    elif "show" in  message.content:
      if "schedule" in message.content:
        with open(r'tasks.json' , "r") as js:
          data = json.loads(js.read())
          for i in data:
            await message.channel.send("```you have task:`{0}` on {1}```".format(i["task"],i["dueDate"]))
      elif "strat" in message.content:
        con = sqlite3.connect('mydatabase.db')
        await  message.channel.send(db["strat"])
        con.close()
      elif "notes" in message.content :
        con = sqlite3.connect('mydatabase.db')
        for i in sql_nots(con):
          await message.channel.send(i)
        await message.reply("this is your current list")
        con.close()
      elif  "tasks" in message.content.split():
        con = sqlite3.connect('mydatabase.db')
        rows = sql_fetch(con)
        for i in rows:
            await message.channel.send(i)
        await message.reply("yo reached bottom honey")
        con.close()
      
      
    


keep_alive()
client.run(my_secret)

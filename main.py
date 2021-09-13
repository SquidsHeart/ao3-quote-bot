
import discord
from discord import message
from discord.ext import commands

import random
import urllib.parse

import os

from requests import NullHandler

token = os.environ.get("token")


import AO3

bot = commands.Bot(command_prefix=["r!", "R!", "r! ", "R! "])

@bot.event
async def on_ready():
    print("Bot's up!")
    
@bot.command(name="archive", help="Fetches a random quote")
async def archive(ctx, *tags):
    if not tags:
        tags = ["dream smp"]
    search_list = []
    search = AO3.Search(any_field=tags)
    search.update()
    for i in search.results:
        search_list.append(i)

    
    number_of_chapters = 0
    if number_of_chapters == 0:
        rand_work = random.choice(search_list)
        
        number_of_chapters = rand_work.nchapters
    
    chosen_chapt = random.randint(0, number_of_chapters-1)

    work_id = rand_work.id 

    work = AO3.Work(work_id)

    sample = work.chapters[chosen_chapt].text
    
    split_ver = sample.split(".")
    sentence = random.choice(split_ver)
    new_sentence = ""

    for i in sentence:
        if i == "*":
            i = "\*"
        new_sentence = new_sentence + i

    sentence = new_sentence + "\n - ***" + work.title + "***"

    try:
        await ctx.send(sentence)
    except:
        await ctx.send("THIS IS A MESSAGE FROM THE BOT CREATOR TELLING U SOMETHING BROKE. NOT A QUOTE.")

@bot.command(name="wave", help="Waves the attached image")
async def wave(ctx):
    try:
        image = ctx.message.attachments[0].url
        image = image.replace("cdn", "media")
        image = image.replace("com", "net")
        image = urllib.parse.quote_plus(image)
        url = "https://krikienoid.github.io/flagwaver/#?src=" + image
        embed=discord.Embed(title="Flag!", url=url, color=0xFFC7C4)
        await ctx.send(embed=embed)
    except SyntaxError:
        await ctx.send("not a valid option!")

bot.run(token)
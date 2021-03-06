
import discord
from discord import message
from discord.ext import commands

import random
import urllib.parse

import os
import time

from requests import NullHandler

import AO3

token = os.environ.get("token")
#token = ""
#### uncomment the value above and fill in your own token if you don't want to use evironment variables

leader_board_dict = {}
 

bot = commands.Bot(command_prefix=["r!", "R!", "r! ", "R! "])

@bot.event
async def on_ready():
    print("Bot's up!")

"""
def leader_board(id):
    if id in leader_board_dict:
        leader_board_dict[id] = leader_board_dict[id] + 1
    else:
        leader_board_dict.update({id: 1})
"""        

def chunk_splitter(text, n):
    chunks = []
    for i in range(0, len(text), n):
        chunks.append(text[i:i+n])
    return chunks


@bot.command(name="archive", help="Fetches a random quote: r!archive (search term) [search term 2, 3, ...]")
async def archive(ctx, *tags):
    if len(tags) == 0:
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

    sentence = new_sentence + "\n - ***" + work.title + " - work id: " + str(work_id) + "***"

    try:
        await ctx.send(sentence)
    except:
        await ctx.send("THIS IS A MESSAGE FROM THE BOT CREATOR TELLING U SOMETHING BROKE. NOT A QUOTE.")

@bot.command(name="story", help="Allows you to read the story: r!story (story example) [chapter number] [confirm]]")
async def story(ctx, work, chapter = "1", confirm="false"):
    try:
        chapter = int(chapter) - 1
    except:
        chapter = 0
    search = AO3.Search(title=work)
    search.update()
    if len(search.results) != 0:
        search_result = search.results[0]
        chosen_work_id = search_result.id
        chosen_work = AO3.Work(chosen_work_id)
        work = chosen_work.chapters[chapter]
        text = "***" + work.title + " - " + str(chapter + 1) + "/" + str(chosen_work.nchapters - 1) + "***\n" +  work.text
        if len(text) < 8000 or confirm=="true":
            if len(text) > 15000 and not ctx.message.author.guild_permissions.administrator:
                await ctx.send("This work is over 15,000 characters! you need admin to open it.")
            else:
                for i in chunk_splitter(text, 2000):
                    await ctx.send(i)
                    time.sleep(2)
        else:
            await ctx.send("This chapter is over 8,000 characters(" + str(len(text)) + " characters), if you REALLY want to read it set confirm to true")
    else:
        await ctx.send("this ain't a thing")


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

@bot.command(name="idsearch", help="does what the search does but by id: r!idsearch [id] [chapter number] [confirmation]")
async def idsearch(ctx, id, chapter="1", confirm="false", **kwargs):
    try:
        chapter = int(chapter) - 1
    except:
        chapter = 0
    valid = False
    try:
        work = AO3.Work(int(id))
        valid = True
    except:
        await ctx.send("not a valid work id!")
    if valid:
        try:
            worktext = work.chapters[chapter].text
        except:
            worktext = work.text[1]
        text = "***" + work.title + " - " + str(chapter + 1) + "/" + str(work.nchapters) + "***\n" +  worktext
        if len(text) < 5000 or confirm == "true":
            for i in chunk_splitter(text, 2000):
                await ctx.send(i)
                time.sleep(2)
        else:
            await ctx.send("This chapter is over 5,000 characters, if you REALLY want to read it set confirm to true")
        pass

"""
@bot.command(name="leaderboard", help="Returns the current leaderboard")
def leaderboard(ctx):
    return False
    leader_board_str = ""
    for i in leader_board_dict.keys():
        user = bot.get_user(i)
        
"""

bot.run(token)
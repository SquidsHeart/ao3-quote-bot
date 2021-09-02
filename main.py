
import discord
import random
from discord.ext import commands
import os

token = os.environ.get("token")

import AO3

bot = commands.Bot(command_prefix=["randquote ", "Randquote", "r!"])

@bot.event
async def on_ready():
    print("Bot's up!")
    
@bot.command()
async def archive(ctx, tag="dreamsmp"):
    search_list = []
    search = AO3.Search(any_field=tag)
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


bot.run(token)
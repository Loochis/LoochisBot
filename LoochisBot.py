# GENERAL BOT FUNCTIONS

# bot.py
import googletrans
import pytube

import BeatRequests
from Beans import BeanHandler
from Movies import MovieHandler
import Music
import glob
import math
import os
import random
import time
import asyncio
import datetime
import math
import feedparser
from bs4 import BeautifulSoup

import discord
from discord.ext import commands
from dotenv import load_dotenv
from googletrans import Translator

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ADMINID = int(os.getenv('DISCORD_ADMINID'))

identifier = os.getenv('IDENTIFIER_STR')

intents = discord.Intents().default()
intents.members = True

bot = commands.Bot(command_prefix='+', intents=intents)
bot.remove_command('help')

beanHandler = BeanHandler()
movieHandler = MovieHandler(0)
reqManager = BeatRequests.BSReqHandler()

musicDict = dict()
# service_urls=['translate.googleapis.com']
translator = Translator()


# START OF BOT COMMANDS

@bot.event
async def on_ready():
    currentSongIndex = 0
    print(
        f'{bot.user} is Online!'
    )


# HELP CMDS ----------------------------------------------------------------------------- ###

@bot.command(name="help")
async def help(ctx):
    print(str(ctx.author.id))
    outStr = "COMMANDS:"
    outStr += "\n+musicHelp: Explains how to request, skip, and manage songs"
    outStr += "\n+movieHelp: Explains how to add, remove, and view requested movies"
    outStr += "\n+beanHelp: Explains the Beanking System(tm)"
    outStr += "\n+sCasm(commment): Makes a comment sarcastic"
    outStr += "\n+myIQ: Accurate IQ reading"
    outStr += "\n+pfpGrabMe: Grabs ya PFP son"
    outStr += "\n+pfpGrab(Mention User): Grabs someones PFP son"
    outStr += "\n+goodBot: He is a good bot after all asd"
    await ctx.send(outStr)


@bot.command()
async def beanHelp(ctx):
    outStr = "BEAN COMMANDS:"
    outStr += "\n+beanCounter: Shows your Beank Statement"
    outStr += "\n+beanMe: High Quality Beanking(c)"
    await ctx.send(outStr)


@bot.command()
async def movieHelp(ctx):
    outStr = "MOVIE COMMANDS:"
    outStr += "\n+movieLS: Lists currently requested movies"
    outStr += "\n+movieADD(name): Adds a movie to the list"
    outStr += "\n+movieDEL(index): Removes a movie at index from the list"
    outStr += "\n+movieRAND: Picks a movie! ( Don't use this one yet ;) )"
    await ctx.send(outStr)


@bot.command(aliases=['songHelp'])
async def musicHelp(ctx):
    outStr = "MUSIC COMMANDS:"
    outStr += "\n+play(search term / YouTube link): Plays a song or adds it to the queue"
    outStr += "\n+skip: Skips the current song"
    outStr += "\n+queue: Lists the current song queue"
    await ctx.send(outStr)


# FUN CMDS ------------------------------------------------------------------------------ ###
@bot.command(aliases=["CAT", "CATME", "catme", "cat"])
async def catMe(ctx):
    embed = discord.Embed(
        title='Random Image 🐈',
        description='Random',
        colour=discord.Colour.purple()
    )
    embed.set_image(url='https://source.unsplash.com/1600x900/?cat')
    embed.set_footer(text="")
    await ctx.send(embed=embed)


@bot.command(aliases=["XKCD", "xkcd", "xme", "XME", "XkMe", "XKME"])
async def xkme(ctx):
    Feed = feedparser.parse("https://xkcd.com/rss.xml")
    pointer = Feed.entries[0]
    soup = BeautifulSoup(pointer.description, "html.parser")

    embed = discord.Embed(
        title="XKCD " + pointer.link.split('/')[3] + " - " + pointer.title,
        colour=discord.Colour.dark_gray()
    )
    embed.set_image(url=soup.img["src"])
    embed.set_footer(text=soup.img["alt"])
    await ctx.send(embed=embed)


@bot.command(aliases=["Troll", "TROLL"])
async def troll(ctx, user: discord.User):
    if ctx.author.id != ADMINID:
        return
    for i in range(10):
        await asyncio.sleep(1)
        await ctx.send(f"HEY <@{user.id}>")


@bot.command()
async def goom(ctx):
    destStr = random.choice(list(googletrans.LANGCODES.items()))[1]
    result = translator.translate("Good Morning", src="en", dest=destStr)
    await ctx.send(result.text)


@bot.command()
async def sCasm(ctx, *args):
    sarcStr = sarcasify(args)
    await ctx.send(sarcStr)
    i = beanHandler.account_from_id(ctx.author.id)
    gain = random.randint(5, 20)
    beanHandler.add_beans(gain)
    await ctx.send("+" + str(gain) + " BND")


@bot.command()
async def doomsgay(ctx):
    if ctx.author.id != ADMINID:
        return
    doomTime = datetime.datetime(2025, 9, 9, 0, 0, 0) - datetime.datetime.now()
    outStr = "Ricky will become homosexual in "
    years = math.floor(doomTime.days / 365.25)
    days = doomTime.days - math.floor(years * 365.25)
    hours = math.floor(doomTime.seconds / 3600)
    minutes = math.floor(doomTime.seconds / 60) - hours * 60
    outStr += str(years) + " years, "
    outStr += str(days) + " days, "
    outStr += str(hours) + " hours, "
    outStr += str(minutes) + " minutes"
    await ctx.send(outStr)


@bot.command()
async def myIQ(ctx):
    if ctx.author.id == ADMINID:
        # g*mer IQ
        await ctx.send("Loochis Daddy's IQ is: 300")
    else:
        # pleb IQ
        random.seed(ctx.author.id)
        await ctx.send(ctx.author.name + "'s IQ is: " + str(random.randint(10, 90)))


@bot.command()
async def pfpGrabMe(ctx):
    await ctx.send(str(ctx.author.avatar_url))


@bot.command()
async def pfpGrabYou(ctx, user: discord.User):
    await ctx.send(str(user.avatar_url))


@bot.command()
async def cringe(ctx):
    await ctx.send(str.upper(random.choice(ctx.guild.members).name) + " IS CRINGE!")
    i = beanHandler.account_from_id(ctx.author.id)
    gain = random.randint(5, 20)
    beanHandler.add_beans(gain)
    await ctx.send("+" + str(gain) + " BND")


@bot.command()
async def goodBot(ctx):
    await ctx.send("thanks B0s")
    i = beanHandler.account_from_id(ctx.author.id)
    gain = random.randint(5, 20)
    beanHandler.add_beans(gain)
    await ctx.send("+" + str(gain) + " BND")


# BEAN CMDS ----------------------------------------------------------------------------- ###

@bot.command()
async def beanMe(ctx):
    i = beanHandler.account_from_id(ctx.author.id)
    gain = random.randint(5, 20)
    oldBal = beanHandler.beanAccount.beans
    beanHandler.add_beans(gain)
    if i == 0:
        await ctx.send(ctx.author.name + "'s Bean Account has been succesfully created!")

    await ctx.send(str.upper(ctx.author.name) + " GOT BEANED: \n```\nOld Balance: " + numFormat(
        oldBal) + "Transaction: " + numFormat(gain) + lineFormat() + "New Balance: " + balFormat(beanHandler) + "```")


@bot.command()
async def beanYou(ctx, user: discord.User, *args):
    outAcc = beanHandler.account_from_id(ctx.author.id)
    gain = int(args[0])
    oldBal = beanHandler.beanAccount.beans
    newBal = oldBal - gain
    if outAcc == 0:
        await ctx.send(ctx.author.name + "'s Bean Account has been succesfully created!")
    if beanHandler.beanAccount.beans - gain < 0:
        await ctx.send(ctx.author.name + ", You dont have enough BND to perform this Beansaction")
        return
    beanHandler.add_beans(-gain)
    inAcc = beanHandler.account_from_id(user.id)
    if inAcc == 0:
        await ctx.send(user.name + "'s Bean Account has been succesfully created!")

    await ctx.send(str.upper(ctx.author.name) + " BEANED " + str.upper(user.name) + "\n```\nOld Balance: " + numFormat(
        oldBal) + "Transaction: " + numFormat(-gain) + lineFormat() + "New Balance: " + numFormat(newBal) + "```")
    oldBal = beanHandler.beanAccount.beans
    beanHandler.add_beans(gain)
    await ctx.send(
        str.upper(user.name) + " GOT BEANED BY " + str.upper(ctx.author.name) + "\n```\nOld Balance: " + numFormat(
            oldBal) + "Transaction: " + numFormat(gain) + lineFormat() + "New Balance: " + balFormat(
            beanHandler) + "```")


@bot.command()
async def beanCounter(ctx):
    i = beanHandler.account_from_id(ctx.author.id)
    if i == 0:
        await ctx.send(ctx.author.name + "'s Bean Account has been succesfully created!")

    await ctx.send(ctx.author.name + "'s Bean Account: \n```\nBalance: " + balFormat(beanHandler) + "```")


# MOVIE CMDS ---------------------------------------------------------------------------- ###

@bot.command()
async def movieLS(ctx):
    movieHandler = MovieHandler(ctx.guild.id)
    movieHandler.get_movies()
    if len(movieHandler.movies) != 0:
        await ctx.send("Here are the curently requested movies:\n```" + movieHandler.moviesToOrderedString() + "\n```")
    else:
        await ctx.send("There are no requested movies!")


@bot.command()
async def movieADD(ctx, *args):
    movieHandler = MovieHandler(ctx.guild.id)
    movieHandler.get_movies()
    name = ' '.join([x for x in args])
    movieHandler.add_movie(name)

    await ctx.send("Succesfully Added **" + name + "**")
    await ctx.send("Here are the curently requested movies:\n```" + movieHandler.moviesToOrderedString() + "\n```")


@bot.command()
async def movieDEL(ctx, *args):
    movieHandler = MovieHandler(ctx.guild.id)
    movieHandler.get_movies()
    try:
        name = movieHandler.del_movie(int(args[0]))
    except:
        await ctx.send("Must be a valid index!")
        return

    await ctx.send("Succesfully Deleted **" + name + "**")
    if len(movieHandler.movies) != 0:
        await ctx.send("Here are the curently requested movies:\n```" + movieHandler.moviesToOrderedString() + "\n```")
    else:
        await ctx.send("There are no requested movies!")


@bot.command()
async def movieRAND(ctx):
    movieHandler = MovieHandler(ctx.guild.id)
    movieHandler.get_movies()
    if len(movieHandler.movies) != 0:
        await ctx.send("PICKING FROM A HAT...")
        await asyncio.sleep(2)
        await ctx.send("3...")
        await asyncio.sleep(2)
        await ctx.send("2...")
        await asyncio.sleep(2)
        await ctx.send("1...")
        await asyncio.sleep(2)
        await ctx.send("0.5...")
        await asyncio.sleep(2)
        await ctx.send("0.25...")
        await asyncio.sleep(2)
        await ctx.send("0.125...")
        await asyncio.sleep(2)
        await ctx.send("0.0625...")
        await asyncio.sleep(2)
        await ctx.send("0... FRICK IT ROUNDED DO-")
        await ctx.send("The Chosen Movie is: **" + random.choice(movieHandler.movies) + "**")
    else:
        await ctx.send("There are no requested movies!")


# MUSIC CMDS ---------------------------------------------------------------------------- ###

@bot.command(aliases=['p', 'P', 'Play', 'PLAY'])
async def play(ctx, *args):
    video = Music.getVideo(args)
    if video is None:
        await ctx.send("ERR: Cannot find song.")
        return

    guildID = ctx.guild.id
    if str(guildID) not in musicDict:
        musicDict[str(guildID)] = []

    if ctx.author.voice is None:
        await ctx.send("ERR: User not in channel.")
        return

    voice_channel = ctx.author.voice.channel

    bot_channel = None
    if not (ctx.guild.voice_client is None):
        bot_channel = ctx.guild.voice_client.channel

    if bot_channel is not None:
        if voice_channel == bot_channel:
            vc = ctx.guild.voice_client
        else:
            await ctx.send("ERR: Bot is in another channel, permission denied.")
            return
    else:
        await ctx.send("Joined VC")
        vc = await voice_channel.connect()

    print(video)
    if len(video) == 1:
        musicDict[str(guildID)].append(video[0])
        if vc.is_playing():
            await ctx.send("Queued: **" + video[0].title + "**")
    else:
        for v in video:
            musicDict[str(guildID)].append(v)
        await ctx.send("Queued " + str(len(video)) + " videos")

    print(len(musicDict[str(guildID)]))
    if not vc.is_playing():
        await playNext(ctx)


@bot.command(aliases=['s', 'S', 'Skip', 'SKIP'])
async def skip(ctx):
    if ctx.author.voice is None:
        await ctx.send("ERR: User not in channel.")
        return

    voice_channel = ctx.author.voice.channel
    bot_channel = None
    if not (ctx.guild.voice_client is None):
        bot_channel = ctx.guild.voice_client.channel

    if bot_channel is not None:
        if voice_channel == bot_channel:
            vc = ctx.guild.voice_client
        else:
            await ctx.send("ERR: Bot is in another channel, permission denied.")
            return
    else:
        await ctx.send("ERR: Bot not in channel.")
        return

    guildID = ctx.guild.id
    if not musicDict[str(guildID)]:
        await ctx.send("Nothing in Queue!")
        return

    try:
        # del musicDict[str(guildID)][0]
        voice_channel = ctx.message.guild.voice_client
        voice_channel.stop()
        await ctx.send("Skipped!")
    except:
        await ctx.send("ERR: Nothing playing.")
        return

    # await playNext(ctx)


async def playNext(ctx):
    guildID = ctx.guild.id
    if len(musicDict[str(guildID)]) >= 1:
        await ctx.send("Now Playing: **" + musicDict[str(guildID)][0].title + "**")
        if len(musicDict[str(guildID)]) == 0:
            return
        vc = ctx.guild.voice_client
        Music.getYTFile(musicDict[str(guildID)][0], ctx.guild.id)
        vc.play(discord.FFmpegPCMAudio(source="Audio/" + str(ctx.guild.id) + ".mp4"))
        while vc.is_playing():
            await asyncio.sleep(1)
        del musicDict[str(guildID)][0]
        print("Deleted.")
        await playNext(ctx)
    else:
        await ctx.send("Queue Finished!")


@bot.command(aliases=['q', 'Q', 'Queue'])
async def queue(ctx, *args):
    guildID = ctx.guild.id
    if str(guildID) not in musicDict:
        musicDict[str(guildID)] = []
    if not musicDict[str(guildID)]:
        await ctx.send("Nothing in Queue!")
        return

    pageNum = 1
    if args:
        try:
            pageNum = int(args[0])
        except:
            await ctx.send("Invalid Page Number")

    outStr = pageListFormatter([x.title for x in musicDict[str(guildID)]], pageNum)

    await ctx.send(outStr)


# BEAT SABER REQUEST FUNCS -------------------------------------------------------------- ###

@bot.command(aliases=["BS", "beatsaber", "BEATSABER", "bs", "bsrequest", "BEATSABERREQUEST"])
async def BeatSaber(ctx, *args):
    msg = await ctx.send("Searching...")
    url = reqManager.getBeatsaverPage(' '.join(args))
    if url[0:8] == "https://":
        await msg.edit(content="Verifying...")
        bsSong = BeatRequests.BSSong(url)
        reqStatus = reqManager.add_req(bsSong)
        if not reqStatus:
            await msg.edit(content="Song already in queue!")
            return

        embed = discord.Embed(
            title="[{}] ".format(bsSong.id) + bsSong.name,
            description="Mapped By: {}".format(bsSong.mapper),
            colour=discord.Colour.red()
        )
        embed.set_image(url=bsSong.coverArt)
        embed.set_footer(text=bsSong.description)
        embed.add_field(name="Votes", value="\👍 "+str(bsSong.upvotes) + " | \👎"+str(bsSong.downvotes), inline=False)
        await msg.edit(content="Successfully added!", embed=embed)
    else:
        await msg.edit(content=url)

@bot.command(aliases=["BSLS", "beatsaberlist", "BEATSABERLIST", "bsls", "bslist"])
async def BeatSaberList(ctx, *args):
    pageNum = 1
    if args:
        try:
            pageNum = int(args[0])
        except:
            await ctx.send("Invalid Page Number")

    reqManager.get_reqs()
    if not reqManager.requests:
        await ctx.send("Nothing in Queue!")
        return

    print([x.split("")[1] for x in reqManager.requests])
    outStr = pageListFormatter([x.split("")[1] for x in reqManager.requests], pageNum)
    await ctx.send(outStr)

# HELPER FUNCS -------------------------------------------------------------------------- ###

def pageListFormatter(pagedList, pageNum):
    maxPageNum = math.floor(len(pagedList) / 10.0) + 1
    if pageNum < 1:
        pageNum = 1
    if pageNum > maxPageNum:
        pageNum = maxPageNum

    outStr = "Queue Page " + str(pageNum) + "/" + str(maxPageNum) + ":\n```"
    outStr += "\n>> " + pagedList[0]
    for i in range((pageNum - 1) * 10, min(pageNum * 10, len(pagedList))):
        outStr += "\n(" + str(i + 1) + "). " + pagedList[i]
    outStr += "```"
    return outStr

def sarcasify(*args):
    random.seed(time.time())
    outStr = '"'
    for arg in args:
        for argSt in arg:
            for argCh in argSt:
                outStr += random.choice([str.lower(argCh), str.upper(argCh)])
            outStr += " "
    outStr += '"'
    return outStr


def balFormat(bHandler):
    return str(bHandler.beanAccount.beans) + " BND\n"


def numFormat(num):
    return str(num) + " BND\n"


def lineFormat():
    return "-----------------------\n"


bot.run(TOKEN)

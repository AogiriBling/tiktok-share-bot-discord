import os
import asyncio
from click import command
from cmd2 import CommandSet
import discord
from discord.ext import commands
import threading
import asyncio
import json
from backend import request
from datetime import datetime
import pytz
from webserver import keep_alive
config = json.load(open("config.json"))
main_channel = config["bot_channel"]
log_channel = config["logs_channel"]
color = 0x2ac3d4
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

my_secret = os.environ['token']
token = os.environ['token']

def time_check():
    tz_NY = pytz.timezone('America/New_York') 
    datetime_NY = datetime.now(tz_NY)
    current_time = datetime_NY.strftime("%I:%M")
    return current_time


@bot.event
async def on_ready():
 members = sum([guild.member_count for guild in bot.guilds])
 await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Aogiri Tree"))
 print("Members")


@bot.command()
async def ts(ctx, link):
    ammount = 200
    if ctx.channel.id == main_channel:
        embed = discord.Embed(color=color, description = "sending **{}** shares to [video]({})".format(ammount, link))
        await ctx.send(embed=embed)
        embed = discord.Embed(
            color=color, description=f"{ctx.author.mention} has sent ``{ammount}`` shares to [video]({link})")
        embed.set_footer(text=f"invoked at {time_check()} est", icon_url=ctx.message.author.avatar_url)
        await ctx.guild.get_channel(log_channel).send(embed=embed)
        for x in range(ammount):
            threading.Thread(target=request, args=[link]).start()
    else:
        embed = discord.Embed(color=color, description = "Please use the correct channel")
        await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    if ctx.channel.type != discord.ChannelType.private:
        if ctx.channel.id == main_channel:
            pfp = ctx.author.avatar_url
            embed = discord.Embed(color=0x2ac3d4, title="Novas TikTok Share Bot | Commands")
            embed.add_field(name='TikTok shares', value=f'`!share (link)`', inline=True)
            embed.set_footer(text=f"invoked by {ctx.author.display_name} | {time_check()}", icon_url=pfp)
            await ctx.send(embed=embed)

keep_alive()
bot.run(token)

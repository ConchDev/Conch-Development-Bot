import asyncio
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = "cb?", intents = discord.Intents.all())

cogs = ['jishaku', 'cogs.owner', 'cogs.commands']
ConchRed = "<:ConchRed:842884638375936010>"
ConchYellow = "<:ConchYellow:842578572303400970>"
ConchGreen = "<:ConchGreen:842578572014256148>"

for cog in cogs:
    client.load_extension(cog)
    print(cog + " has been loaded.")

async def status_loop():
    statuses = cycle(["you", 'Conch Development', 'your shit code', 'your awesome project', 'you make bad decisions'])
    while True:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=(next(statuses))))
        await asyncio.sleep(15)

@client.event
async def on_ready():
    print("Conch Development is online.")
    await client.loop.create_task(status_loop())
    

@client.before_invoke
async def before_command(ctx):
    if ctx.cog.qualified_name == "Owner" and not ctx.author.id == 579041484796461076:
        embed = discord.Embed(title=f"{ConchRed} You are not permitted to use this command.", color=discord.Color.red())
        return await ctx.message.reply(embed=embed)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"\"{error.param}\" is a required argument that is missing.")
        await ctx.message.reply(embed=embed)
    elif isinstance(error, commands.CommandInvokeError):
        embed=discord.Embed(title="You have timed out.", color=discord.Color.red())
        await ctx.message.reply(embed=embed)
        raise error
    else:
        raise error
    
load_dotenv('.env')
client.run(os.getenv("TOKEN"))
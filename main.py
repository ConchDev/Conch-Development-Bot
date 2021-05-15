import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

client = commands.Bot(command_prefix = "cb?", intents = discord.Intents.all())

cogs = ['jishaku', 'cogs.owner', 'cogs.commands']
ConchRed = "<:ConchRed:842884638375936010>"
ConchYellow = "<:ConchYellow:842578572303400970>"
ConchGreen = "<:ConchGreen:842578572014256148>"

for cog in cogs:
    client.load_extension(cog)
    print(cog + " has been loaded.")

@client.event
async def on_ready():
    print("Conch Development is online.")

@client.before_invoke
async def before_command(ctx):
    if ctx.cog.qualified_name == "Owner":
        embed = discord.Embed(title=f"{ConchRed} You are not permitted to use this command.", color=discord.Color.red())
        return await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"{ConchRed} \"{error.param} is a required argument that is missing.\"")
        await ctx.send(embed=embed)
    
    else:
        raise error
    
load_dotenv('.env')
client.run(os.getenv("TOKEN"))
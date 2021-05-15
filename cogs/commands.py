import discord
from discord.ext import commands
from Tools.Functions import Funcs

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def suggest(self, ctx, *, suggestion=None):
        if suggestion is None:
            embed=discord.Embed(title=f"What do you want to suggest?", color=discord.Color.gold())
            await ctx.send(embed=embed)
            suggestion = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
            suggestion = suggestion.content
        if len(suggestion) < 10 or len(suggestion) > 500:
            embed = discord.Embed(title="Your suggestion must be between 5 and 100 characters. That was " + len(suggestion))
            await ctx.send(embed=embed)
        else:
            channel = self.client.get_channel(842732610803073035)
            suggest_num = await Funcs.get_suggest_num(self)
            embed = discord.Embed(title=f"Suggestion #{suggest_num}", color=discord.Color.random(), description=suggestion)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(f"Suggestion submitted! You can view it in {channel.mention}")
            msg = await channel.send(embed=embed)
            await msg.add_reaction('')

def setup(client):
    client.add_cog(Commands(client))

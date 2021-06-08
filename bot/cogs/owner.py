import discord
from discord.ext import commands
from jishaku import Jishaku as jsk
from jishaku.codeblocks import codeblock_converter
import aiosqlite
import asyncio
import os
from dotenv import load_dotenv
import sys

load_env = load_dotenv()

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def eval(self, ctx, *, code: codeblock_converter):
        """Eval some code"""
        cog = self.client.get_cog("Jishaku")
        await cog.jsk_python(ctx, argument=code)

    @commands.command(aliases=['su'])
    async def sudo(self, ctx):
        """
        Reinvoke someone's command, running with all checks overridden
        """
        try:
            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        except discord.errors.NotFound:
            return await ctx.send(embed=ctx.error('That message doesn\'t exist.'))
        await ctx.message.add_reaction('\U00002705')
        context = await ctx.bot.get_context(message)
        await context.reinvoke()

    @commands.command()
    async def commit(self, ctx):
        db = await aiosqlite.connect(f'db/main.sqlite')
        cursor = await db.cursor()

        await cursor.execute("INSERT INTO suggesnum (num) VALUES ('1')")

        await db.commit()

        await cursor.execute("DELETE FROM suggesnum WHERE num = '1'")

        await db.commit()
        await cursor.close()
        await db.close()

        await ctx.send("Database committed.")
    
    @commands.command()
    @commands.is_owner()
    async def refresh(self, ctx):
        cog = self.client.get_cog("Jishaku")
        await cog.jsk_git(ctx, argument=codeblock_converter(f'stash'))
        await asyncio.sleep(2)
        await cog.jsk_git(ctx, argument=codeblock_converter(f'pull --ff-only https://github.com/ConchDev/Conch-Development-Bot master'))
        await asyncio.sleep(2)
        restart = self.client.get_command('restart')
        await ctx.invoke(restart)

    @commands.command()
    @commands.has_role(794015347018956821)
    async def restart(self, ctx):
        def restarter():
            python = sys.executable
            os.execl(python, python, * sys.argv)

        embed = discord.Embed(title="Bot Restarting...")
        embed.add_field(name="I'll be back soon...", value="Don't worry", inline=True)
        await ctx.send(embed=embed)
        restarter()
        

def setup(client):
    client.add_cog(Owner(client))
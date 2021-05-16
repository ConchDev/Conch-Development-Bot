import discord
from discord.ext import commands
from jishaku import Jishaku as jsk
from jishaku.codeblocks import codeblock_converter
import aiosqlite

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

def setup(client):
    client.add_cog(Owner(client))
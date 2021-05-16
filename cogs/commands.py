import discord
from discord.embeds import _EmptyEmbed
from discord.ext import commands
from Tools.Functions import Funcs
from datetime import datetime
import DiscordUtils
import aiosqlite

questions = {
    1 : "Why do you want to be a moderator?",
    2 : "How active are you on Discord?",
    3 : "How old are you?",
    4 : "How strict will your moderation actions be?",
    5 : "Do you have any prior moderation experience?",
    6 : "What is your time zone?",
    7 : "Someone is mildly cursing in general chat. What do you do?",
    8 : "Someone is asking for mod. What do you do?",
    9 : "Someone is calling others names and starting problems in a chat. What do you do?",
    10 : "Someone posts NSFW content in chat. What do you do?"
}

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
            embed = discord.Embed(title=f"Your suggestion must be between 5 and 100 characters. That was {len(suggestion)}.")
            await ctx.message.reply(embed=embed)
        else:
            channel = self.client.get_channel(842732610803073035)
            suggest_num = await Funcs.get_suggest_num(self)
            embed = discord.Embed(title=f"Suggestion #{suggest_num}", color=discord.Color.random(), description=suggestion)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(f"Suggestion submitted! You can view it in {channel.mention}.")
            msg = await channel.send(embed=embed)
            await msg.add_reaction('⬆')
            await msg.add_reaction('⬇')

    @commands.group(invoke_without_command=True)
    async def apply(self, ctx):
        embed = discord.Embed(title="Available Applications:", description="Moderator Application", color=discord.Color.blurple())
        embed.set_footer(text="To apply for an application, please use \"cb?apply {application}.\"")
        await ctx.send(embed=embed)

    @apply.command(aliases=["moderator"])
    async def mod(self, ctx):
        check = await Funcs.check_mod_apps(self, ctx.author.id)
        if check is True:
            embed = discord.Embed(title="You have already submitted a moderator application.", color=discord.Color.red())
            return await ctx.send(embed=embed)
        abortion = discord.Embed(title="Aborting the moderator application...", color=discord.Color.red())
        embed = discord.Embed(title="This will continue in DMs.", color=discord.Color.dark_magenta())
        await ctx.send(embed=embed)
        embed0=discord.Embed(title="Welcome to the Conch Development Mod Application!", color=discord.Color.green(), description="There are 10 questions to this application. Would you like to start? `y/n`")
        embed0.set_footer(text="You can type \"cancel\" at any time to cancel the mod application.")
        await ctx.author.send(embed=embed0)
        conf = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
        if conf.content == "Y" or conf.content == "y":
            pass
        elif conf.content == "N" or conf.content == "n":
            return await ctx.send(embed=abortion)

        embed = discord.Embed(title="Question One:", color=discord.Color.random(), description="Why do you want to be a moderator?")
        await ctx.author.send(embed=embed)
        why = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
        if why.content == "Cancel" or why.content == "cancel":
            return await ctx.author.send(embed=abortion)

        embed = discord.Embed(title="Question Two:", color=discord.Color.random())
        embed.add_field(name="How active are you on Discord?", value="1. Very Active\n2. Plenty Active\n3. Moderately Active\n4. Somewhat Active\n5. Barely Active")
        await ctx.author.send(embed=embed)
        activity = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
        if activity.content == "Cancel" or activity.content == "cancel":
            return await ctx.author.send(embed=abortion)

        embed = discord.Embed(title="Question Three:", color=discord.Color.random(), description="How old are you? Please answer in an integer.")
        await ctx.author.send(embed=embed)
        age = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
        if age.content == "Cancel" or age.content == "cancel":
            return await ctx.author.send(embed=abortion)

        embed=discord.Embed(title="Question Four:", color=discord.Color.random())
        embed.add_field(name="How strict will your moderation actions be?", value="1. Very Strict\n2. Plenty Strict\n3. Moderately Strict\n4. Loose\n5. Very Loose\n6. I won't make moderator decisions.")
        await ctx.author.send(embed=embed)
        strictness = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
        if strictness.content == "Cancel" or strictness.content == "cancel":
            return await ctx.author.send(embed=abortion)

        embed=discord.Embed(title="Question Five:", color=discord.Color.random(), description="Do you have any prior moderation experience? If so, please state.")
        await ctx.author.send(embed=embed)
        exp = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
        if exp.content == "Cancel" or exp.content == "cancel":
            return await ctx.author.send(embed=abortion)

        embed = discord.Embed(title="Question Six:", color=discord.Color.random(), description="What is your time zone?")
        await ctx.author.send(embed=embed)
        timezone = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
        if timezone.content == "Cancel" or timezone.content == "cancel":
            return await ctx.author.send(embed=abortion)
        
        embed = discord.Embed(title="Good! Now, on to section two!", color=discord.Color.gold(), description="Do you want to continue? `y/n`.")
        await ctx.author.send(embed=embed)
        conf2 = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
        if conf2.content == "Y" or conf2.content == "y":
            pass
        elif conf2.content == "N" or conf2.content == "n":
            return await ctx.author.send(embed=abortion)

        embed = discord.Embed(title="Question Seven:", color=discord.Color.random(), description="Someone is mildly cursing in general chat. What do you do?")
        await ctx.author.send(embed=embed)
        cursing = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
        if cursing.content == "Cancel" or cursing.content == "cancel":
            return await ctx.author.send(embed=abortion)

        embed = discord.Embed(title="Question Eight:", color=discord.Color.random(), description="Someone is asking for mod. What do you do?")
        await ctx.author.send(embed=embed)
        askmod = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
        if askmod.content == "Cancel" or askmod.content == "cancel":
            return await ctx.author.send(embed=abortion)

        embed = discord.Embed(title="Question Nine:", color=discord.Color.random(), description="Someone is calling others names and starting problems in a chat. What do you do?")
        await ctx.author.send(embed=embed)
        problems = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
        if problems.content == "Cancel" or problems.content == "cancel":
            return await ctx.author.send(embed=abortion)

        embed = discord.Embed(title="Question Ten:", color=discord.Color.red(), description="Someone posts NSFW content in chat. What do you do?")
        await ctx.author.send(embed=embed)
        nsfw = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
        if nsfw.content == "Cancel" or nsfw.content == "cancel":
            return await ctx.author.send(embed=abortion)

        finembed = discord.Embed(title=f"{ctx.author.name}'s Mod App", color=discord.Color.random())
        finembed.set_footer(text=f"ID: {ctx.author.id} | Date: {datetime.now()}")

        whyem = discord.Embed(title="Question One", color=discord.Color.random())
        whyem.add_field(name=questions[1], value=why.content)

        activityem = discord.Embed(title="Question Two", color=discord.Color.random())
        activityem.add_field(name=questions[2], value=activity.content)

        ageem = discord.Embed(title="Question Three", color=discord.Color.random())
        ageem.add_field(name=questions[3], value=age.content)

        strictnessem = discord.Embed(title="Question Four", color=discord.Color.random())
        strictnessem.add_field(name=questions[4], value=strictness.content)

        expem = discord.Embed(title="Question Five", color=discord.Color.random())
        expem.add_field(name=questions[5], value=exp.content)

        timezoneem = discord.Embed(title="Question Six", color=discord.Color.random())
        timezoneem.add_field(name=questions[6], value=timezone.content)

        cursingem = discord.Embed(title="Question Seven", color=discord.Color.random())
        cursingem.add_field(name=questions[7], value=cursing.content)

        askmodem = discord.Embed(title="Question Eight", color=discord.Color.random())
        askmodem.add_field(name=questions[8], value=askmod.content)

        problemsem = discord.Embed(title="Question Nine", color=discord.Color.random())
        problemsem.add_field(name=questions[9], value=problems.content)

        nsfwem = discord.Embed(title="Question Ten", color=discord.Color.random())
        nsfwem.add_field(name=questions[10], value=nsfw.content)

        embeds = [finembed, whyem, activityem, ageem, strictnessem, expem, timezoneem, cursingem, askmodem, problemsem, nsfwem]

        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True, timeout=15)
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('⏩', "next")

        await ctx.author.send(f"Alrighty! Come back to {ctx.channel.mention}!")
        await ctx.message.reply("Here is a copy of your responses. You have fifteen seconds to view them.")
        msg = await paginator.run(embeds)

        await ctx.send("Submit application? `y/n`")
        conf3 = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=180)
        await msg.delete()
        if conf3.content == 'Y' or conf3.content == "y":
            pass
        else:
            return await ctx.author.send(embed=abortion)

        await Funcs.add_mod_app(self, ctx.author.id, why.content, activity.content, age.content, strictness.content, exp.content, timezone.content, cursing.content, askmod.content, problems.content, nsfw.content)

        channel = self.client.get_channel(843212113715658773)
        finalem = discord.Embed(title=f"{ctx.author}'s Mod Application", color=ctx.author.color)
        finalem.add_field(name=questions[1], value=why.content)
        finalem.add_field(name=questions[2], value=activity.content)
        finalem.add_field(name=questions[3], value=age.content)
        finalem.add_field(name=questions[4], value=strictness.content)
        finalem.add_field(name=questions[5], value=exp.content)
        finalem.add_field(name=questions[6], value=timezone.content)
        finalem.add_field(name=questions[7], value=cursing.content)
        finalem.add_field(name=questions[8], value=askmod.content)
        finalem.add_field(name=questions[9], value=problems.content)
        finalem.add_field(name=questions[10], value=nsfw.content)
        finalem.set_footer(text=f"ID: {ctx.author.id} | Date: {datetime.now()} | Click author name to direct message.")
        finalem.set_author(name=ctx.author, icon_url=ctx.author.avatar_url, url=f"https://discord.com/channels/@me/{ctx.author.id}")
        await channel.send(embed=finalem)

        embed = discord.Embed(title="Success! Mod application submitted.", color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command()
    async def thank(self, ctx, user:discord.Member, reason=None):
        db = await aiosqlite.connect('db/main.sqlite')
        cursor = await db.cursor()
        if user == ctx.author:
            embed=discord.Embed(title="You can't thank yourself.", color=discord.Color.red())
            return await ctx.send(embed=embed)
        elif user.bot:
            embed=discord.Embed(title="You can't thank bots.", color=discord.Color.red())
            return await ctx.send(embed=embed)

        await Funcs.open_thank_account(self, ctx.author.id)
        thanknum = await Funcs.open_thank_account(self, ctx.author.id)

        await cursor.execute(f"UPDATE thanks SET thanks = {thanknum + 1} WHERE id = {ctx.author.id}")
        
        await db.commit()
        await cursor.close()
        await db.close()
        embed = discord.Embed(title=f"You have thanked **{user.mention}**.", color=discord.Color.green())
        await ctx.send(embed=embed)
        embed = discord.Embed(title="You have been thanked in **Conch Development** For the reason:", color=discord.Color.green(), description=reason)
        await user.send(embed=embed)

def setup(client):
    client.add_cog(Commands(client))

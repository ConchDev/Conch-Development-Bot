import asyncio
import discord
from discord.ext import commands
from bot.Tools.Functions import Funcs
from datetime import datetime
import DiscordUtils
import aiosqlite
import urllib

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
        embed = discord.Embed(title="Available Applications:", description="- Moderator Application\n- Bot Application", color=discord.Color.blurple())
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
    
    @commands.group(invoke_without_command=True)
    async def bot(self, ctx):
        main = discord.Embed(title="Bot Command Group", color=discord.Color.light_grey())
        main.add_field(name="Commands:", value="`submit`: submits a bot to the server.\n`status`: the status of a bot awaiting review.\n`guidelines`: The bot submission guidelines.", inline=False)
        main.add_field(name="Pages:", value="Page 1: This page\nPage 2: Bot Submission Guidelines\nPage 3: `submit` command overview.\nPage 4: `status` command overview.", inline=False)
        main.set_footer(text="Use the below reactions to switch pages. | Page 1")

        guides=discord.Embed(title="**__Bot Submission Guidelines__**", description="These are the guidelines your bot has to follow to be submitted into Conch Development.\nYou can add your bot via `cb?bot submit`.", color=discord.Color.random())
        guides.add_field(name="**1. Your bot must be online at time of testing.**", value="If your bot is offline when testers go to test the bot, it will be immediately rejected.", inline=False)
        guides.add_field(name="**2. Prefix must be correct.**", value="If the prefix you defined with your bot submission does not work, testers will not spend time trying to figure"
        " out the prefix. Instead, the bot will be rejected.", inline=False)
        guides.add_field(name="**3. Your bot must not DM any member of the server unwillingly.**", value="If your bot ends up direct messaging a user of our server without invoking any"
        " command that requires direct messaging, your bot will be removed and you will be blacklisted from submitting bots.", inline=False)
        guides.add_field(name="**4. Your bot must not spam.**", value="Your bot will have a slowmode of 2 seconds between each message in the testing channels. If the bot is caught spamming"
        ", it will be removed, and you might be blacklisted depending on severity.", inline=False)
        guides.add_field(name="**5. Your bot must not display NSFW content outside of NSFW channels.**", value="This includes words, images, videos, GIFs, and other forms of media that may"
        " be linked to NSFW content.", inline=False)
        guides.add_field(name="**6. Your bot must not respond to anything that isn't a prefix.**", value="This includes responding to swear words and messages by other people.", inline=False)
        guides.add_field(name="**Additional Information:**", value="- Your bot has near the same permissions as the average user.\n- Your bot is limited to the bot testing areas."
        "\n- Your bot should have a leave command to leave the server on your request. We will not kick it for you.\n- We have the full right to remove your bot at any time if we"
        " find that it breaks any rules or other undisclosed reasons.", inline=False)
        guides.set_footer(text="If you have any questions or concerns about the bot addition process, please ask an admin or the owner of Conch Development. | Page 2")

        submit = discord.Embed(title="`submit` - `bot` Subcommand", color=discord.Color.random())
        submit.add_field(name="Usage:", value="`cb?bot submit`. The bot will then walk you through the bot submission process.", inline=False)
        submit.add_field(name="Questions:", value="When submitting your bot, we ask the following questions:\nWhat is your bot's ID?\nWhat is your bot's prefix?\nWhy do you want to add your bot?", inline=False)
        submit.set_footer(text="To see submission guidlines, go back a page or use `cb?bot guidelines`. | Page 3")

        status = discord.Embed(title="`status` - `bot` Subcommand", color=discord.Color.random())
        status.add_field(name="Usage:", value="`cb?bot status {bot ID}`", inline=False)
        status.add_field(name="Key:", value = "0 - Pending Approval\n1 - Pending Addition\n2 - Added\n3 - Bot not submitted\n4 - Denied (usually accompanied by reason)\n5 - User Blacklisted\n6 - Something went wrong", inline=False)
        status.set_footer(text="To add your bot, use `cb?bot submit`. | Page 4")

        embeds = [main, guides, submit, status]

        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('⏩', "next")

        await paginator.run(embeds)

    @bot.command()
    async def submit(self, ctx):
        embed = discord.Embed(title="Bot Submission", description="You are about to start the bot submission process. We only ask a few things, including your bot's ID, the bot's prefix"
        ", and why you want to add the bot. Reasons don't have to be paragraphs, a sentence or two is the best.", color=discord.Color.light_gray())
        embed.set_footer(text="The submission process will start in five seconds.")
        await ctx.send(embed=embed)
        await asyncio.sleep(5)

        embed = discord.Embed(title="What is your bot's ID?", color=discord.Color.random())
        await ctx.send(embed=embed)
        id = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)

        embed = discord.Embed(title="What is your bot's prefix?", color=discord.Color.random())
        await ctx.send(embed=embed)
        prefix = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)

        embed = discord.Embed(title="Finally, why do you want to add your bot to Conch Development?", color=discord.Color.random())
        await ctx.send(embed=embed)
        reason = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)

        statuse = await Funcs.check_bot_status(self, int(id.content))
        status = int(statuse[0])

        bot = await commands.UserConverter().convert(ctx, id.content)

        if not bot:
            embed=discord.Embed(title="❌ Error submitting bot", color=discord.Color.red())
            embed.add_field(name="Problem:", value="Bot user does not exist. / Invalid bot ID.")
            embed.set_footer(text="If you think we made a mistake, please contact UnsoughtConch#9225.")
            return await ctx.send(embed=embed)

        if not bot.bot:
            embed=discord.Embed(title="❌ Error submitting bot", color=discord.Color.red())
            embed.add_field(name="Problem:", value="Not a bot user.")
            embed.set_footer(text="If you think we made a mistake, please contact UnsoughtConch#9225.")
            return await ctx.send(embed=embed)

        if len(reason.content) < 10:
            embed=discord.Embed(title="❌ Error submitting bot", color=discord.Color.red())
            embed.add_field(name="Problem:", value="Reason must be more than ten characters.")
            embed.set_footer(text="If you think we made a mistake, please contact UnsoughtConch#9225.")
            return await ctx.send(embed=embed)

        if status != 3:
            if status == 1 or status == 0:
                msg = "You already submitted a bot to Conch Development."
            elif status == 2:
                msg = "Your bot is already added to Conch Development."
            embed=discord.Embed(title="❌ Error submitting bot", color=discord.Color.red())
            embed.add_field(name="Problem:", value=msg)
            embed.set_footer(text="If you think we made a mistake, please contact UnsoughtConch#9225.")
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title="✅ Bot submitted.", color=discord.Color.green())
        await ctx.send(embed=embed)

        channel = self.client.get_channel(851584960955416658)
        
        invite = discord.utils.oauth_url(id.content, guild=self.client.get_guild(851608963921215519))

        embed = discord.Embed(title="New Bot Submission", color=discord.Color.random(), description="To approve or deny a bot, use `cb?deny [bot ID]`. Click the bot name to invite it to the test server.")
        embed.set_author(name=bot, url=invite, icon_url=bot.avatar_url)
        embed.add_field(name="Submitted by:", value=ctx.author.mention + ' (' + str(ctx.author) + ')', inline=False)
        embed.add_field(name="Reason:", value=reason.content, inline=False)
        embed.add_field(name="Bot Prefix:", value="`" + prefix.content + "`", inline=False)
        embed.add_field(name="Bot Account:", value=bot.mention + ' (' + str(bot) + ')', inline=False)
        embed.set_footer(text=f"Bot ID: {bot.id}")
        msg = await channel.send(embed=embed)

        await Funcs.submit_bot(self, ctx.author.id, id.content, urllib.parse.quote(prefix.content, safe=" "), urllib.parse.quote(reason.content, safe=" "), msg_id=msg.id)

    @bot.command(aliases=['guides', 'gl'])
    async def guidelines(self, ctx):
        guides=discord.Embed(title="**__Bot Submission Guidelines__**", description="These are the guidelines your bot has to follow to be submitted into Conch Development.\nYou can add your bot via `cb?bot submit`.", color=discord.Color.random())
        guides.add_field(name="**1. Your bot must be online at time of testing.**", value="If your bot is offline when testers go to test the bot, it will be immediately rejected.", inline=False)
        guides.add_field(name="**2. Prefix must be correct.**", value="If the prefix you defined with your bot submission does not work, testers will not spend time trying to figure"
        " out the prefix. Instead, the bot will be rejected.", inline=False)
        guides.add_field(name="**3. Your bot must not DM any member of the server unwillingly.**", value="If your bot ends up direct messaging a user of our server without invoking any"
        " command that requires direct messaging, your bot will be removed and you will be blacklisted from submitting bots.", inline=False)
        guides.add_field(name="**4. Your bot must not spam.**", value="Your bot will have a slowmode of 2 seconds between each message in the testing channels. If the bot is caught spamming"
        ", it will be removed, and you might be blacklisted depending on severity.", inline=False)
        guides.add_field(name="**5. Your bot must not display NSFW content outside of NSFW channels.**", value="This includes words, images, videos, GIFs, and other forms of media that may"
        " be linked to NSFW content.", inline=False)
        guides.add_field(name="**6. Your bot must not respond to anything that isn't a prefix.**", value="This includes responding to swear words and messages by other people.", inline=False)
        guides.add_field(name="**Additional Information:**", value="- Your bot has near the same permissions as the average user.\n- Your bot is limited to the bot testing areas."
        "\n- Your bot should have a leave command to leave the server on your request. We will not kick it for you.\n- We have the full right to remove your bot at any time if we"
        " find that it breaks any rules or other undisclosed reasons.", inline=False)
        guides.set_footer(text="If you have any questions or concerns about the bot addition process, please ask an admin or the owner of Conch Development.")

        await ctx.send(embed=guides)

    @bot.command()
    async def status(self, ctx, bot_id):
        statusw = await Funcs.check_bot_status(self, bot_id)

        status, colorstr = statusw.split(":;")

        emcolor = getattr(discord.Color, colorstr)

        embed = discord.Embed(title="Bot Status", color=emcolor())
        embed.add_field(name=f"Status: {status[0]}", value=status[2:])
        embed.set_footer(text="If you think the status of your bot is wrong or broken, please contact the owner of Conch Development, UnsoughtConch#9225.")

        await ctx.send(embed=embed)

    @bot.command()
    @commands.has_role(842233600853278751)
    async def deny(self, ctx, bot_id, reason):
        status = await Funcs.check_bot_status(self, bot_id)

        if int(status[0]) != 0:
            embed=discord.Embed(title=f"This bot is not awaiting approval.", color=discord.Color.red())
            embed.add_field(name="Status: " + status[0], value=status[2:])
            return await ctx.send(embed=embed)

        else:
            info = await Funcs.get_bot_info(self, bot_id, 5)
            user = self.client.get_user(int(info[0]))
            prefix = info[1]
            msg_id = info[2]
            reasona = info[3]
            bot = await commands.UserConverter().convert(ctx, bot_id)
            await Funcs.reject_bot(self, bot_id)

            await user.send(f"Your bot, {bot.name}, has been denied from Conch Development for the following reason:\n{reason}")
            await ctx.send(f"Successfully approved {user.name}'s bot, {bot.name}.")

            channel = self.client.get_channel(851584960955416658)
            msg = channel.get_partial_message(msg_id)

            embed = discord.Embed(title="Denied Bot Submission", color=discord.Color.red())
            embed.set_author(name=bot, icon_url=bot.avatar_url)
            embed.add_field(name="Submitted by:", value=user.mention + " (" + str(user) + ")")
            embed.add_field(name="Reason:", value=reasona, inline=False)
            embed.add_field(name="Bot Prefix:", value=prefix, inline=False)
            embed.add_field(name="Bot Account:", value=bot.mention + " (" + str(bot) + ")", inline=False)

            await msg.edit(embed=embed)

    @bot.command()
    @commands.has_role(842233600853278751)
    async def approve(self, ctx, bot_id):
        status = await Funcs.check_bot_status(self, bot_id)

        if int(status[0]) != 0:
            embed=discord.Embed(title=f"This bot is not awaiting approval.", color=discord.Color.red())
            embed.add_field(name="Status: " + status[0], value=status[2:])
            return await ctx.send(embed=embed)

        else:
            info = await Funcs.get_bot_info(self, bot_id, 5)
            user = self.client.get_user(int(info[0]))
            prefix = info[1]
            msg_id = info[2]
            reason = info[3]
            bot = await commands.UserConverter().convert(ctx, bot_id)
            await Funcs.approve_bot(self, bot_id)

            await user.send(f"Your bot, {bot.name}, has been approved and is now awaiting addition to Conch Development.")
            await ctx.send(f"Successfully approved {user.name}'s bot, {bot.name}.")

            channel = self.client.get_channel(851584960955416658)
            msg = channel.get_partial_message(msg_id)
            invite = discord.utils.oauth_url(bot_id, guild=self.client.get_guild(851608963921215519))

            embed = discord.Embed(title="Approved Bot Submission", color=discord.Color.green())
            embed.set_author(name=bot, icon_url=bot.avatar_url, url=invite)
            embed.add_field(name="Submitted by:", value=user.mention + " (" + str(user) + ")")
            embed.add_field(name="Reason:", value=reason, inline=False)
            embed.add_field(name="Bot Prefix:", value=prefix, inline=False)
            embed.add_field(name="Bot Account:", value=bot.mention + " (" + str(bot) + ")", inline=False)

            await msg.edit(embed=embed)

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

import discord
from discord.ext import commands
from bot.Tools.Functions import Funcs

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(842232034356756505)
        if member.bot:
            await Funcs.add_bot(self, member.id)

            user_id = await Funcs.get_bot_info(self, member.id, 1)

            user = self.client.get_user(user_id)

            await channel.send(f"Bot Added: {member.mention} - submitted by {user.mention}")

            await member.add_roles(member.guild.get_role(851628160340328459))

        else:
            await channel.send(member.mention)
            embed = discord.Embed(title=f"Welcome, {member.name}!", description=f"Make sure to check out {self.client.get_channel(842234203487076362).mention} and"
            f" {self.client.get_channel(851549028508500039).mention}!")
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_thumbnail(url=member.avatar_url)

            await channel.send(embed=embed)

def setup(client):
    client.add_cog(Events(client))
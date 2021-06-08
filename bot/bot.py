import asyncio
import os
from itertools import cycle
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_env = load_dotenv()

class Client(commands.Bot):
    def __init__(self):
        allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
        super().__init__(command_prefix=['cb??', 'cB?', 'Cb?', 'CB?'], intents=discord.Intents.all(), allowed_mentions=allowed_mentions, case_insensitive=True)
    

    def load_cogs(self):
        print("Loading All cogs...")
        print("------")
        for filename in os.listdir(f"./bot/cogs"):
            if filename.endswith(f".py"):
                self.load_extension(f"bot.cogs.{filename[:-3]}")
                print(f"Loaded `{filename[:20]}` Cog")
        print("Loaded Error Handler")
        print("------")
        self.load_extension('jishaku')
        print("Loaded `jishaku`")
        print("------")

    @tasks.loop(seconds=15.0)
    async def status_loop(self):
        statuses = cycle(["you", 'Conch Development', 'your shit code', 'your awesome project', 'you make bad decisions'])
        while True:
            await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=(next(statuses))))
            await asyncio.sleep(15)
            
    async def on_ready(self):
        print("------")
        print("Conch Development is online!")
        await self.status_loop()
    
    async def shutdown(self):
        print("------")
        print("Conch Development Closing connection to Discord...")
        print("------")

    async def close(self):
        print("------")
        print("Conch Development Closing on keyboard interrupt...\n")
        print("------")

    async def on_connect(self):
        print("------")
        print(f"Conch Development Connected to Discord (latency: {self.latency*1000:,.0f} ms).")

    async def on_resumed(self):
        print("------")
        print("Conch Development resumed.")

    async def on_disconnect(self):
        print("------")
        print("Conch Development disconnected.")

    def run(self):
        self.load_cogs()
        print("Running bot...")
        
        super().run("ODA3MDk1NzEyMjE0MTU1MjY0.YBzAdA.tUvMr3pd8Fh-tp3cBhelwc5NVd0", reconnect=True)

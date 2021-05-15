import discord
import aiosqlite

class Funcs():
    def __init__(self, ctx):
        self.ctx = ctx

    async def get_suggest_num(self):
        db = await aiosqlite.connect('suggestions.sqlite')
        cursor = await db.cursor()

        await cursor.execute("SELECT num FROM main")
        num = await cursor.fetchone()

        newnum = int(num[0]) + 1
        await cursor.execute(f"UPDATE main SET num = {newnum} WHERE num = {num[0]}")

        await db.commit()
        await cursor.close()
        await db.close()

        return num[0]
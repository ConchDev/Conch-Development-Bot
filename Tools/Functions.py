import discord
import aiosqlite

class Funcs():
    def __init__(self, ctx):
        self.ctx = ctx

    async def get_suggest_num(self):
        db = await aiosqlite.connect('db/main.sqlite')
        cursor = await db.cursor()

        await cursor.execute("SELECT num FROM suggesnum")
        num = await cursor.fetchone()

        newnum = int(num[0]) + 1
        await cursor.execute(f"UPDATE suggesnum SET num = {newnum} WHERE num = {num[0]}")

        await db.commit()
        await cursor.close()
        await db.close()

        return num[0]

    async def add_mod_app(self, ID, ques1, ques2, ques3, ques4, ques5, ques6, ques7, ques8, ques9, ques10):
        db = await aiosqlite.connect('db/main.sqlite')
        cursor = await db.cursor()

        await cursor.execute(f"INSERT INTO modapps (memberID, ques1, ques2, ques3, ques4, ques5, ques6, ques7, ques8, ques9, ques10) VALUES ('{ID}', '{ques1}', '{ques2}', '{ques3}', '{ques4}', '{ques5}', '{ques6}', '{ques7}', '{ques8}', '{ques9}', '{ques10}')")

        await db.commit()
        await cursor.close()
        await db.close()

    async def check_mod_apps(self, ID):
        db = await aiosqlite.connect('db/main.sqlite')
        cursor = await db.cursor()

        await cursor.execute(f"SELECT memberID FROM modapps WHERE memberID = '{id}'")
        result = await cursor.fetchone()

        if result is None:
            return False
        else:
            return True

    async def open_thank_account(self, id):
        db = await aiosqlite.connect('db/main.sqlite')
        cursor = await db.cursor()

        await cursor.execute(f"SELECT id FROM thanks WHERE id = {id}")
        result = await cursor.fetchone()

        if result is None:
            await cursor.execute(f"INSERT INTO thanks (id, thanks) VALUES ({id}, 0)")
            await db.commit()
            await cursor.close()
            await db.close()

        else:
            return True

    async def get_thanks(self, id):
        db = await aiosqlite.connect('db/main.sqlite')
        cursor = await db.cursor()

        await cursor.execute(f"SELECT thanks FROM thanks WHERE id = {id}")
        amount = await cursor.fetchone()

        return amount[0]

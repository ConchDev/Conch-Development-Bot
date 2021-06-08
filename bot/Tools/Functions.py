import discord
import aiosqlite

class Funcs():
    def __init__(self, ctx):
        self.ctx = ctx

    async def get_suggest_num(self):
        db = await aiosqlite.connect('./bot/db/main.sqlite')
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
        db = await aiosqlite.connect('./bot/db/main.sqlite')
        cursor = await db.cursor()

        await cursor.execute(f"INSERT INTO modapps (memberID, ques1, ques2, ques3, ques4, ques5, ques6, ques7, ques8, ques9, ques10) VALUES ('{ID}', '{ques1}', '{ques2}', '{ques3}', '{ques4}', '{ques5}', '{ques6}', '{ques7}', '{ques8}', '{ques9}', '{ques10}')")

        await db.commit()
        await cursor.close()
        await db.close()

    async def check_mod_apps(self, ID):
        db = await aiosqlite.connect('./bot/db/main.sqlite')
        cursor = await db.cursor()

        await cursor.execute(f"SELECT memberID FROM modapps WHERE memberID = '{id}'")
        result = await cursor.fetchone()

        if result is None:
            return False
        else:
            return True

    async def open_thank_account(self, id):
        db = await aiosqlite.connect('./bot/db/main.sqlite')
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
        db = await aiosqlite.connect('./bot/db/main.sqlite')
        cursor = await db.cursor()

        await cursor.execute(f"SELECT thanks FROM thanks WHERE id = {id}")
        amount = await cursor.fetchone()

        return amount[0]

    async def submit_bot(self, user_id, bot_id, prefix, reason, msg_id):
        db = await aiosqlite.connect('./bot/db/main.sqlite')
        cursor = await db.cursor()

        await cursor.execute(f"INSERT INTO botsubs (user_id, bot_id, prefix, reason, status, msg_id) VALUES ({user_id}, {bot_id}, '{prefix}', '{reason}', 0, '{msg_id}')")

        await db.commit()
        await cursor.close()
        await db.close()

    async def check_bot_status(self, bot_id):
        db = await aiosqlite.connect('./bot/db/main.sqlite')
        cursor = await db.cursor()

        await cursor.execute(f"SELECT status FROM botsubs WHERE bot_id = {bot_id}")
        result = await cursor.fetchone()

        await cursor.close()
        await db.close()

        if result is None:
            return "3-Bot Not Submitted:;light_gray"

        elif result[0] == 0:
            return "0-Pending Approval:;blue"
        
        elif result[0] == 1:
            return "1-Pending Server Addition:;gold"

        elif result[0] == 2:
            return "2-Added to Server:;green"

        elif result[0] == 4:
            return "4-Denied:;red"

        elif result[0] == 5:
            return "5-User Blacklisted:;dark_red"

        else:
            return "6-Something went terribly wrong:;darker_gray"

    async def get_bot_info(self, bot_id, info):
        db = await aiosqlite.connect('./bot/db/main.sqlite')
        cursor = await db.cursor()

        if info == 1:
            await cursor.execute(f"SELECT user_id FROM botsubs WHERE bot_id = {bot_id}")
            result = await cursor.fetchone()
            return result[0]

        elif info == 2:
            await cursor.execute(f"SELECT prefix FROM botsubs WHERE bot_id = {bot_id}")
            result = await cursor.fetchone()
            return result[0]

        elif info == 3:
            await cursor.execute(f"SELECT reason FROM botsubs WHERE bot_id = {bot_id}")
            result = await cursor.fetchone()
            return result[0]

        elif info == 4:
            await cursor.execute(f"SELECT msg_id FROM botsubs WHERE bot_id = {bot_id}")
            result = await cursor.fetchone()
            return result[0]

        elif info == 5:
            await cursor.execute(f"SELECT user_id, prefix, msg_id, reason FROM botsubs WHERE bot_id = {bot_id}")
            result = await cursor.fetchall()
            return result[0]

    async def reject_bot(self, bot_id):
        db = await aiosqlite.connect("./bot/db/main.sqlite")
        cursor = await db.cursor()

        await cursor.execute(f"DELETE FROM botsubs WHERE bot_id = {bot_id}")

        await db.commit()
        await cursor.close()
        await db.close()

    async def approve_bot(self, bot_id):
        db = await aiosqlite.connect("./bot/db/main.sqlite")
        cursor = await db.cursor()

        await cursor.execute(f"UPDATE botsubs SET status = 1 WHERE bot_id = {bot_id}")

        await db.commit()
        await cursor.close()
        await db.close()

    async def add_bot(self, bot_id):
        db = await aiosqlite.connect("./bot/db/main.sqlite")
        cursor = await db.cursor()

        await cursor.execute(f"UPDATE botsubs SET status = 2 WHERE bot_id = {bot_id}")

        await db.commit()
        await cursor.close()
        await db.close()

from discord.ext import commands
import discord

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.xp = {}  # dict: {user_id: xp}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        user_id = message.author.id
        self.xp[user_id] = self.xp.get(user_id, 0) + 10  # dapat 10 XP tiap pesan

        level = self.xp[user_id] // 100  # tiap 100 XP naik level
        if self.xp[user_id] % 100 == 0:
            await message.channel.send(f'{message.author.mention} naik ke level {level}! 🎉')

    @commands.command()
    async def level(self, ctx):
        xp = self.xp.get(ctx.author.id, 0)
        level = xp // 100
        await ctx.send(f'{ctx.author.mention}, kamu di level {level} dengan XP {xp}.')

async def setup(bot):
    await bot.add_cog(Leveling(bot))

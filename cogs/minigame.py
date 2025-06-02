from discord.ext import commands
import random

class MiniGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}  # simpan state game per user {user_id: angka_rahasia}

    @commands.command()
    async def tebak(self, ctx):
        number = random.randint(1, 20)
        self.games[ctx.author.id] = number
        await ctx.send(f'{ctx.author.mention}, saya sudah memikirkan angka 1-20. Tebak dengan perintah !jawab <angka>')

    @commands.command()
    async def jawab(self, ctx, guess: int):
        number = self.games.get(ctx.author.id)
        if number is None:
            await ctx.send('Kamu belum mulai permainan! Gunakan !tebak dulu.')
            return
        if guess == number:
            await ctx.send(f'Selamat {ctx.author.mention}, tebakanmu benar! 🎉')
            del self.games[ctx.author.id]
        elif guess < number:
            await ctx.send('Tebakanmu terlalu kecil.')
        else:
            await ctx.send('Tebakanmu terlalu besar.')

async def setup(bot):
    await bot.add_cog(MiniGame(bot))

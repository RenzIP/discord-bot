from discord.ext import commands
import discord

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Pastikan yang menggunakan punya permission kick
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.send(f'{member} telah di-kick. Alasan: {reason}')
        except Exception as e:
            await ctx.send(f'Gagal kick: {e}')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.ban(reason=reason)
            await ctx.send(f'{member} telah di-ban. Alasan: {reason}')
        except Exception as e:
            await ctx.send(f'Gagal ban: {e}')

async def setup(bot):
    await bot.add_cog(Admin(bot))

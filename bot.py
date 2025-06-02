import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')


intents = discord.Intents.default()
intents.message_content = True  # Penting ini supaya bot bisa baca pesan command
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def load_cogs():
    await bot.load_extension('cogs.help_cog')
    # load cogs lain juga
    await bot.load_extension('cogs.admin')
    await bot.load_extension('cogs.general')
    await bot.load_extension('cogs.leveling')
    await bot.load_extension('cogs.autoresponder')
    await bot.load_extension('cogs.minigame')
    await bot.load_extension('cogs.music')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Perintah tidak ditemukan. Gunakan `!help` untuk daftar perintah.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Argumen yang diperlukan tidak diberikan.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Perintah ini sedang cooldown. Coba lagi dalam {error.retry_after:.2f} detik.")
    else:
        await ctx.send(f"Terjadi kesalahan: {error}")

async def setup_hook():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            await bot.load_extension(f'cogs.{filename[:-3]}')

bot.setup_hook = setup_hook

bot.run(TOKEN)

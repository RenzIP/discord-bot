import discord
from discord.ext import commands
import logging

logger = logging.getLogger('discord_bot')
logging.basicConfig(level=logging.INFO)

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help_command(self, ctx):
        embed = discord.Embed(title="Help Menu", color=discord.Color.blue())
        embed.add_field(name="Music Commands", value=(
            "`!play <url>` - Play a song from YouTube\n"
            "`!stop` - Stop the current music\n"
            "`!leave` - Disconnect the bot from voice channel\n"
            "`!loop` - Toggle loop current song\n"
        ), inline=False)

        # Tambah command lain sesuai kebutuhan kamu, misal:
        embed.add_field(name="Admin Commands", value=(
            "`!kick <user>` - Kick a user\n"
            "`!ban <user>` - Ban a user\n"
        ), inline=False)

        embed.add_field(name="Mini-games", value=(
            "`!guess` - Start a guessing game\n"
            # dan seterusnya
        ), inline=False)
        
        embed.add_field(name="Leveling", value=(
            "`!level` - Check your current level and XP\n"
        ), inline=False)
        
        embed.add_field(name="autoresponder", value=(
            "`!autoresponder <trigger> <response>` - Set an autoresponder\n"
        ), inline=False)
        
        embed.add_field(name="General Commands", value=(
            "`!ping` - Check bot latency\n"
            "`!info` - Get information about the bot\n"
            "`!invite` - Get the bot invite link\n"
        ) , inline=False)
        
        embed.set_footer(text="Use !command_name for more details on a specific command.")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))

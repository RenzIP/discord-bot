from discord.ext import commands

class AutoResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.responses = {
            'halo': 'Halo juga! Ada yang bisa saya bantu?',
            'bot': 'Ya, saya bot siap melayani!',
            'ping': 'Pong!'
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        msg_lower = message.content.lower()
        for key, response in self.responses.items():
            if key in msg_lower:
                await message.channel.send(response)
                break

async def setup(bot):
    await bot.add_cog(AutoResponder(bot))

from discord.ext import commands

class TeamsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(TeamsCommands(bot))
import discord
from discord.ext import commands
import os
import asyncio

import config
from database.db_manager import DatabaseManager

intents = discord.Intents.default()

intents.members = True

intents.message_content = True

class FirelemonadeBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_manager = DatabaseManager()

    async def setup_hook(self):
        print("carregando cogs...")
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('__'):
                cog_name = f'cogs.{filename[:-3]}'
                try:
                    await self.load_extension(cog_name)
                    print(f'->cog "{cog_name}" carregado')
                except Exception as e:
                    print(f'Erro ao carregar o cog "{cog_name}": {e}')
        print("cogs carregados")

bot = FirelemonadeBot(command_prefix = config.BOT_PREFIX, intents = intents)

#evento que é iniciado quando o bot está pronto pra ficar online
@bot.event
async def on_ready():
    
    print(f'Bot conectado como {bot.user.name}')
    print(f'ID do bot: {bot.user.id}')
    print('------')
    
    await bot.change_presence(activity = discord.Game(name = "Inazuma Eleven: Victory Road")) #muda o status do bot para mostrar uma atividade

@bot.command()
async def ping(ctx):
    """Um comando de teste simples."""
    await ctx.send("Pong!")

#ponto de início - inicializa o bot
if __name__ == "__main__":
    async def main():
        await bot.start(config.DISCORD_TOKEN)

    asyncio.run(main())
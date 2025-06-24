import discord
from discord.ext import commands
import config

intents = discord.Intents.default()

intents.members = True

intents.message_content = True

bot = commands.Bot(command_prefix = config.BOT_PREFIX, intents = intents)

#evento que é iniciado quando o bot está pronto pra ficar online
@bot.event
async def on_ready():
    
    print(f'Bot conectado como {bot.user.name}')
    print(f'ID do bot: {bot.user.id}')
    print('------')
    
    await bot.change_presence(activity = discord.Game(name = "Inazuma Eleven: Victory Road")) #muda o status do bot para mostrar uma atividade
    
#ponto de início - inicializa o bot
if __name__ == "__main__":
    bot.run(config.DISCORD_TOKEN)
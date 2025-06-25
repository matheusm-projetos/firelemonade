import discord
from discord.ext import commands

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name = "registro", help = "Registra você para jogar Firelemonade")
    async def registro(self, ctx):
        
        user_id = ctx.author.id
        username = ctx.author.name
        
        if self.bot.db_manager.get_usuarios_data(user_id):
            await ctx.send(f"{username} já está registrado!!")
            return
        
        success = self.bot.db_manager.criar_usuario(user_id, username)
        
        if success:
            embed = discord.Embed(
                title = "Bem-vindo ao time!!",
                description = f"Parabéns **{username}**! Você foi registrado com sucesso.\n\n"
                            f"Use 'fl!recrutar' para conseguir seu primeiro jogador!!",
                color = discord.Color.blue()  
            )
            embed.set_thumbnail(url = ctx.author.avatar.url)
            await ctx.send(embed = embed)
        else:
            await ctx.send("Erro!! Algo deu errado no seu registro.")
            
    @commands.command(name = "perfil", help = "Mostra sua carta de perfil no Firelemonade")
    async def mostrar_perfil(self, ctx):
        user_id = ctx.author.id
        usuario_data = self.bot.db_manager.get_usuarios_data(user_id)
        
        if not usuario_data:
            await ctx.send(f"Você ainda não se registrou, {ctx.author.name}. Use `fl!join` para entrar na equipe!")
            return
        
        embed = discord.Embed(
        title=f"Licença de Treinador de {usuario_data['username']}",
        color=discord.Color.gold()
        )
        embed.set_thumbnail(url=ctx.author.avatar.url)
        
        moedas = usuario_data.get('moedas', {})
        embed.add_field(name = "Pontos de Espírito", value = f"{moedas.get('pontos_espirito', 0)}", inline = True)
        embed.add_field(name = "Medalhas da Raimon", value = f"{moedas.get('medalhas_raimon', 0)}", inline = True)
        embed.add_field(name = "Relâmpagos Dourados", value = f"{moedas.get('relampagos_dourados', 0)}", inline = True)
        
        num_jogadores = len(usuario_data.get('elenco', {}))
        embed.add_field(name = "Elenco", value = f"{num_jogadores}", inline = False)
        
        await ctx.send(embed = embed)
        
async def setup(bot):
    await bot.add_cog(UserCommands(bot))          
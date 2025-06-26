import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

class PlayerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name = "recrutar", help = "Recruta um jogador para seu elenco. Pode ser usado a cada x tempo")
    async def recrutar(self, ctx):
        user_id = ctx.author.id
        usuario_data = self.bot.db_manager.get_usuarios_data(user_id)
        
        if not usuario_data:
            await ctx.send(f"Você precisa se registrar primeiro!! Use `fl!registro`")
            return
        
        random_jogador_id = self.bot.db_manager.get_random_jogador_id()
        
        if not random_jogador_id:
            await ctx.send("Opa, parece que não há jogadores na base de dados no momento")
            return
        
        info_jogador = self.bot.db_manager.get_jogador_por_id(random_jogador_id)
        
        self.bot.db_manager.adicionar_jogador_elenco(user_id, random_jogador_id)
        
        embed = discord.Embed(
            title = "Novo Jogador Recrutado!",
            description = f"Olhe, {ctx.author.mention}! **{info_jogador['nome']}** entrou na sua equipe!!",
            color = discord.Color.green()
        )
        embed.set_thumbnail(url = info_jogador['imagem'])
        embed.add_field(name = "Posição", value = info_jogador['posicao_inicial'], inline = True)
        embed.add_field(name = "Elemento", value = info_jogador['elemento'], inline = True)
        
        await ctx.send(embed = embed)
        
    @commands.command(name = "elenco", help = "Mostra todos os jogadores que você recutou")
    async def mostrar_elenco(self, ctx):
        user_id = ctx.author.id
        usuario_data = self.bot.db_manager.get_usuarios_data(user_id)
        
        if not usuario_data:
            await ctx.send(f"Você precisa se registrar primeriro!! Use `fl!registro`")
            return
        
        elenco = usuario_data.get("elenco", {})
        
        if not elenco:
            await ctx.send(f"{ctx.author.mention} seu elenco está vazio! Use `fl!recrutar`!!")
            return
        
        embed = discord.Embed(
            title = f"Elenco de **{ctx.author.name}**",
            color = discord.Color.orange()
        )
        embed.set_thumbnail(url = ctx.author.avatar.url)
        
        lista_jogadores = []
        
        for elenco_id, jogador_no_elenco in elenco.items():
            id_base = jogador_no_elenco.get("id_base")
            info_base = self.bot.db_manager.get_jogador_por_id(id_base)
            
            if info_base:
                nome_jogador = info_base.get("nome", "Desconhecido")
                nivel_jogador = jogador_no_elenco.get("nivel", 1)
                lista_jogadores.append(f"• **{nome_jogador}** - Nível {nivel_jogador}")
                
        if not lista_jogadores:
            await ctx.send("Não foi possível carregar as informações do seu elenco. Tente novamente.")
            return
        
        embed.add_field(name = "Jogadores:", value = "\n".join(lista_jogadores), inline = False)
        
        await ctx.send(embed = embed)
        
    @commands.command(name = "jogador", help = "Mostra o card de um jogador específico")
    async def jogador(self, ctx, *, nome_jogador: str):
        await ctx.send(f"Buscando informações para **{nome_jogador}**")
        
        info_jogador = self.bot.db_manager.get_jogador_por_nome(nome_jogador)
        
        if not info_jogador:
            await ctx.send(f"Não consegui encontrar o jogador ´{nome_jogador}´. Você é burro??")
            return
        
        try:
            response = requests.get(info_jogador['imagem'])
            img_jogador = Image.open(BytesIO(response.content)).convert("RGBA")
            
            card = Image.new("RGBA", (800, 300), (44, 47, 51, 255))
            
            img_jogador = img_jogador.resize((200, 200))
            card.paste(img_jogador, (50, 50), img_jogador)
            
            draw = ImageDraw.Draw(card)
            
            '''try:
                fonte_titulo = ImageFont.truetype("assets/fonts/arial.ttf", 40)
                fonte_stats = ImageFont.truetype("assets.fonts/arial.ttf", 24)
            except IOError:
                fonte_titulo = ImageFont.load_default()
                fonte_stats = ImageFont.load_default()'''
                
            fonte_titulo = ImageFont.load_default()
            fonte_stats = ImageFont.load_default()
            
            draw.text((300, 30), info_jogador['nome'], font=fonte_titulo, fill=(255, 255, 255))
            draw.text((300, 80), f"Posição: {info_jogador['posicao_inicial']}", font=fonte_stats, fill=(200, 200, 200))
            draw.text((500, 80), f"Elemento: {info_jogador['elemento']}", font=fonte_stats, fill=(200, 200, 200))
            
            pos_y = 130
            for attr, valor in info_jogador['atributos'].items():
                draw.text((300, pos_y), f"{attr.capitalize()}: {valor}", font = fonte_stats, fill = (255, 255, 255))
                pos_y += 30
                
            buffer = BytesIO()
            card.save(buffer, format = 'PNG')
            buffer.seek(0)
            
            await ctx.send(file = discord.File(buffer, filename = F"{nome_jogador.lower().replace(' ', '_')}.png"))
        except Exception as e:
            print(f"Erro ao gerar card de jogador: {e}")
            await ctx.send("Não foi possível gerar o card do jogador")
            
async def setup(bot):
    await bot.add_cog(PlayerCommands(bot))
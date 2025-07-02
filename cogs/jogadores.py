import discord
from discord.ext import commands
import random
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

RARITY_CHANCES = {'Comum': 65, 'Raro': 26, 'SR': 7, 'SSR': 1.8, 'Lendário': 0.2}
MIXIMAX_CHANCES = {'SR': 0.05, 'SSR': 0.10, 'Lendário': 0.15}

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
        
        raridades = list(RARITY_CHANCES.keys())
        chances = list(RARITY_CHANCES.values())
        raridade_sorteada = random.choices(raridades, weights = chances, k = 1)
        
        todos_jogadores = self.bot.db_manager.get_jogadores()
        pool_de_jogadores = [p for p in todos_jogadores.values() if p.get('raridade') == raridade_sorteada]
        
        if not pool_de_jogadores:
            await ctx.send(f"Parece não há jogadores da raridade '{raridade_sorteada}' no jogo ainda. Tente Novamente")
            return
        
        jogador_sorteado_base = random.choice(pool_de_jogadores)
        
        is_mixi_max = False
        
        chance_mixi_max = MIXIMAX_CHANCES.get(raridade_sorteada, 0)
        if random.random() < chance_mixi_max and jogador_sorteado_base.get("mixi_max_info"):
            is_mixi_max = True
            
        info_final_jogador = jogador_sorteado_base.copy()
        
        if is_mixi_max:
            info_final_jogador['nome'] = jogador_sorteado_base['mixi_max_info']['nome_mixi_max']
            info_final_jogador['imagem'] = jogador_sorteado_base['mixi_max_info']['imagem_mixi_max']
            
            novos_atributos = {stat: int(valor * 1.20) for stat, valor in info_final_jogador['atributos'].items()}
            info_final_jogador['atributos'] = novos_atributos
            
        self.bot.db_manager.adicionar_jogador_elenco(user_id, str(info_final_jogador['id']), is_mixi_max)
        
        cor_embed = discord.Color.green()
        titulo_embed = "Novo Jogador Recrutado"
        if is_mixi_max:
            cor_embed = discord.Color.purple()
            titulo_embed = "RECRUTAMENTO MIXI MAX!"
            
        embed = discord.Embed(
            title=titulo_embed,
            description=f"Olhe, {ctx.author.mention}! **{info_final_jogador['nome']}** entrou na sua equipe!!",
            color=cor_embed
        )
        embed.set_thumbnail(url=info_final_jogador['imagem'])
        embed.add_field(name="Raridade", value=info_final_jogador['raridade'], inline=True)
        embed.add_field(name="Posição", value=info_final_jogador['posicao_inicial'], inline=True)
        embed.add_field(name="Elemento", value=info_final_jogador['elemento'], inline=True)
        
        await ctx.send(embed=embed)
        
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
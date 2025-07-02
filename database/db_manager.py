import json
import os
import random

JOGADOR_FILE = os.path.join('database', 'data', 'jogadores.json')
USUARIOS_FILE = os.path.join('database', 'data', 'usuarios.json')

#classe que gerencia o acesso e carregamento dos dados do jogo
class DatabaseManager:
    def __init__(self):
        self._jogadores_data = self.load_json(JOGADOR_FILE, "jogadores")
        self._usuarios_data = self.load_json(USUARIOS_FILE, "usuários")
    
    #carrega a lista de jogadores da base de dados    
    def load_json(self, file_path, data_name):
        try:
            with open(file_path, 'r', encoding = 'utf-8') as f:
                print(f" Carregando banco de dados de {data_name}...")
                data = json.load(f)
                print(f"Dadis de {data_name} carregados com sucesso")
                return data
        except FileNotFoundError:
            print(f"Erro: o arquivo '{file_path}' não foi encontrado. Criando novo")
            return {}
        except json.JSONDecodeError:
            print(f"Erro: O arquivo '{file_path}' contém um erro de formatação JSON")
            return {}
    
    #salva os dados do usuário na base de dados    
    def save_usuarios_data(self):
        try:
            with open(USUARIOS_FILE, "w", encoding = 'utf-8') as f:
                json.dump(self._usuarios_data, f, indent = 4)
        except Exception as e:
            print(f"Erro ao salvar dados dos usuários: {e}")
        
    #retorna a lista dos jogadores da base de dados
    def get_jogadores(self):
        return self._jogadores_data
    
    def get_random_jogador_id(self):
        if not self._jogadores_data:
            return None
        return random.choice(list(self._jogadores_data.keys()))
    
    def get_jogador_por_id(self, player_id):
        return self._jogadores_data.get(str(player_id))
    
    def get_jogador_por_nome(self, nome_procurado):
        nome_lower = nome_procurado.lower()
        
        for jogador_id, jogador_info in self._jogadores_data.items():
            if jogador_info['nome'].lower() == nome_lower:
                return jogador_info
        return None
    
    def get_usuarios_data(self, user_id):
        return self._usuarios_data.get(str(user_id))
    
    def adicionar_jogador_elenco(self, user_id, player_id, is_mixi_max = False):
        user_id_str = str(user_id)
        player_id_str = str(player_id)
        
        usuario_data = self.get_usuarios_data(user_id_str)
        
        if not usuario_data:
            return
        
        elenco_id = f"{player_id_str}_{random.randint(10000, 99999)}"
        
        usuario_data["elenco"][elenco_id] = {
            "id_base": player_id_str,
            "nivel": 1,
            "exp": 0,
            "tier": "Mixi Max" if is_mixi_max else "Comum"
        }
        
        self.save_usuarios_data()
    
    def criar_usuario(self, user_id, username):
        user_id_str = str(user_id)
        if user_id_str in self._usuarios_data:
            return False
        
        self._usuarios_data[user_id_str] = {
            "username": username,
            "elenco": {},
            "times": {},
            "moedas": {
                "pontos_espirito": 0,
                "relampagos_dourados": 0,
                "medalhas_raimon": 0
            }
        }
        
        self.save_usuarios_data()
        return True
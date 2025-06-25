import json
import os

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
    
    def get_usuarios_data(self, user_id):
        return self._usuarios_data.get(str(user_id))
    
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
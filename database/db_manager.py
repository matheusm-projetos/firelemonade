import json
import os

DB_FILE = os.path.join('database', 'data', 'jogadores.json')

#classe que gerencia o acesso e carregamento dos dados do jogo
class DatabaseManager:
    def __init__(self):
        self._jogadores = self.load_jogadores()
    
    #carrega a lista de jogadores da base de dados    
    def load_jogadores(self):
        try:
            with open(DB_FILE, 'r', encoding = 'utf-8') as f:
                print(" Carregando banco de dados de jogadores...")
                data = json.load(f)
                print(f"{len(data)} jogadores carregados com sucesso")
                return data
        except FileNotFoundError:
            print(f"Erro: o arquivo '{DB_FILE}' não foi encontrado")
            return {}
        except json.JSONDecodeError:
            print(f"Erro: O arquivo '{DB_FILE}' contém um erro de formatação JSON")
            return {}
        
    def get_jogadores(self):
        return self._jogadores
    
if __name__ == "__main__":
    db = DatabaseManager()
    
    todos_jogadores = db.get_jogadores()
    
    if todos_jogadores:
        primeiro_jogador = todos_jogadores.get('1')
        
        if primeiro_jogador:
            print("\nTeste de carregamento:")
            print(f"Nome do primeiro jogador carregado: {primeiro_jogador.get('nome')}")
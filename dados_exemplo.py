import sqlite3
from datetime import datetime, timedelta
import random

exemplos_chamados = [
    {
        'titulo': 'Computador não liga',
        'descricao': 'O computador da sala 201 não está ligando. Testei a tomada e está funcionando.',
        'categoria': 'Hardware',
        'prioridade': 'Alta'
    },
    {
        'titulo': 'Erro no sistema de vendas',
        'descricao': 'O sistema está apresentando erro ao tentar finalizar uma venda.',
        'categoria': 'Software',
        'prioridade': 'Urgente'
    },
    {
        'titulo': 'Internet lenta',
        'descricao': 'A internet do departamento financeiro está muito lenta desde ontem.',
        'categoria': 'Rede',
        'prioridade': 'Média'
    },
    {
        'titulo': 'Acesso ao sistema bloqueado',
        'descricao': 'Não consigo acessar o sistema com minhas credenciais.',
        'categoria': 'Acesso',
        'prioridade': 'Alta'
    },
    {
        'titulo': 'Impressora com papel preso',
        'descricao': 'A impressora do RH está com papel preso e não conseguimos remover.',
        'categoria': 'Hardware',
        'prioridade': 'Baixa'
    },
    {
        'titulo': 'Solicitar novo mouse',
        'descricao': 'O mouse do meu computador está com defeito. Preciso de um novo.',
        'categoria': 'Hardware',
        'prioridade': 'Média'
    },
    {
        'titulo': 'Atualização de software',
        'descricao': 'Preciso atualizar o Office para a versão mais recente.',
        'categoria': 'Software',
        'prioridade': 'Baixa'
    },
    {
        'titulo': 'Rede sem sinal no auditório',
        'descricao': 'O Wi-Fi não está funcionando no auditório. Temos uma reunião importante hoje.',
        'categoria': 'Rede',
        'prioridade': 'Urgente'
    },
]

status_possiveis = ['Aberto', 'Em andamento', 'Resolvido', 'Encerrado']

def popular_banco():
    conn = sqlite3.connect('database/chamados.db')
    cursor = conn.cursor()
    
    count = cursor.execute('SELECT COUNT(*) FROM chamados').fetchone()[0]
    
    if count > 0:
        print(f"O banco já contém {count} chamado(s).")
        resposta = input("Deseja adicionar mais dados de exemplo? (s/n): ")
        if resposta.lower() != 's':
            print("Operação cancelada.")
            conn.close()
            return
    
    print("\nInserindo dados de exemplo...")
    
    data_base = datetime.now()
    
    for i, chamado in enumerate(exemplos_chamados):
        dias_atras = random.randint(0, 7)
        data_criacao = (data_base - timedelta(days=dias_atras)).strftime('%Y-%m-%d %H:%M:%S')
        
        status = random.choice(status_possiveis)
        
        cursor.execute('''
            INSERT INTO chamados (titulo, descricao, categoria, prioridade, status, data_criacao)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            chamado['titulo'],
            chamado['descricao'],
            chamado['categoria'],
            chamado['prioridade'],
            status,
            data_criacao
        ))
        
        print(f"  Chamado {i+1}: {chamado['titulo']}")
    
    conn.commit()
    conn.close()
    
    print(f"\n{len(exemplos_chamados)} chamados de exemplo inseridos com sucesso!")
    print("Execute 'python app.py' e acesse http://localhost:5000")

if __name__ == '__main__':
    try:
        popular_banco()
    except sqlite3.OperationalError as e:
        print(f"\nErro: {e}")
        print("Execute 'python app.py' primeiro para criar o banco de dados.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")

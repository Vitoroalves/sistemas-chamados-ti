from flask import Flask, render_template, request, jsonify
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

app.config['DATABASE'] = 'database/chamados.db'
app.config['JSON_AS_ASCII'] = False

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS chamados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            categoria TEXT NOT NULL,
            prioridade TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Aberto',
            data_criacao TEXT NOT NULL,
            data_atualizacao TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chamados', methods=['GET'])
def listar_chamados():
    try:
        conn = get_db_connection()
        chamados = conn.execute('SELECT * FROM chamados ORDER BY id DESC').fetchall()
        conn.close()
        
        lista = [dict(chamado) for chamado in chamados]
        
        return jsonify(lista), 200
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/chamados', methods=['POST'])
def criar_chamado():
    try:
        dados = request.get_json()
        
        campos_obrigatorios = ['titulo', 'descricao', 'categoria', 'prioridade']
        for campo in campos_obrigatorios:
            if campo not in dados or not dados[campo]:
                return jsonify({'erro': f'Campo obrigatório: {campo}'}), 400
        
        data_criacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn = get_db_connection()
        cursor = conn.execute('''
            INSERT INTO chamados (titulo, descricao, categoria, prioridade, status, data_criacao)
            VALUES (?, ?, ?, ?, 'Aberto', ?)
        ''', (dados['titulo'], dados['descricao'], dados['categoria'], dados['prioridade'], data_criacao))
        
        conn.commit()
        novo_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'mensagem': 'Chamado criado com sucesso',
            'id': novo_id
        }), 201
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/chamados/<int:id>', methods=['GET'])
def obter_chamado(id):
    try:
        conn = get_db_connection()
        chamado = conn.execute('SELECT * FROM chamados WHERE id = ?', (id,)).fetchone()
        conn.close()
        
        if chamado is None:
            return jsonify({'erro': 'Chamado não encontrado'}), 404
        
        return jsonify(dict(chamado)), 200
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/chamados/<int:id>', methods=['PUT'])
def atualizar_chamado(id):
    try:
        dados = request.get_json()
        
        conn = get_db_connection()
        chamado = conn.execute('SELECT * FROM chamados WHERE id = ?', (id,)).fetchone()
        
        if chamado is None:
            conn.close()
            return jsonify({'erro': 'Chamado não encontrado'}), 404
        
        campos_atualizaveis = ['titulo', 'descricao', 'categoria', 'prioridade', 'status']
        
        updates = []
        valores = []
        
        for campo in campos_atualizaveis:
            if campo in dados:
                updates.append(f'{campo} = ?')
                valores.append(dados[campo])
        
        if not updates:
            conn.close()
            return jsonify({'erro': 'Nenhum campo para atualizar'}), 400
        
        updates.append('data_atualizacao = ?')
        valores.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        valores.append(id)
        
        query = f"UPDATE chamados SET {', '.join(updates)} WHERE id = ?"
        conn.execute(query, valores)
        conn.commit()
        conn.close()
        
        return jsonify({'mensagem': 'Chamado atualizado com sucesso'}), 200
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/chamados/<int:id>', methods=['DELETE'])
def excluir_chamado(id):
    try:
        conn = get_db_connection()
        
        chamado = conn.execute('SELECT * FROM chamados WHERE id = ?', (id,)).fetchone()
        
        if chamado is None:
            conn.close()
            return jsonify({'erro': 'Chamado não encontrado'}), 404
        
        conn.execute('DELETE FROM chamados WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        
        return jsonify({'mensagem': 'Chamado excluído com sucesso'}), 200
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    try:
        conn = get_db_connection()
        
        total = conn.execute('SELECT COUNT(*) as count FROM chamados').fetchone()['count']
        
        abertos = conn.execute("SELECT COUNT(*) as count FROM chamados WHERE status = 'Aberto'").fetchone()['count']
        em_andamento = conn.execute("SELECT COUNT(*) as count FROM chamados WHERE status = 'Em andamento'").fetchone()['count']
        resolvidos = conn.execute("SELECT COUNT(*) as count FROM chamados WHERE status = 'Resolvido'").fetchone()['count']
        encerrados = conn.execute("SELECT COUNT(*) as count FROM chamados WHERE status = 'Encerrado'").fetchone()['count']
        
        conn.close()
        
        return jsonify({
            'total': total,
            'abertos': abertos,
            'em_andamento': em_andamento,
            'resolvidos': resolvidos + encerrados
        }), 200
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists('database'):
        os.makedirs('database')
    
    init_db()
    
    app.run(debug=True, host='0.0.0.0', port=5000)

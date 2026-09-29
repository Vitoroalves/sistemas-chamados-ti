# 🎫 Sistema de Chamados de TI

Sistema web Full Stack para gerenciamento de chamados de suporte técnico, desenvolvido com Flask, SQLite e JavaScript vanilla.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Sobre o Projeto

Uma aplicação web completa que permite registrar, acompanhar e gerenciar chamados de suporte de TI. O sistema oferece uma interface intuitiva para que funcionários possam abrir chamados e a equipe de suporte possa gerenciá-los eficientemente.

### ✨ Funcionalidades

- ✅ **Criar chamados** com título, descrição, categoria e prioridade
- 📊 **Dashboard** com estatísticas em tempo real
- 🔄 **Alterar status** dos chamados (Aberto → Em andamento → Resolvido → Encerrado)
- 🗑️ **Excluir chamados** com confirmação
- 💾 **Persistência de dados** com SQLite
- 📱 **Interface responsiva** (mobile-friendly)
- 🔔 **Notificações** de sucesso e erro
- 🎨 **Design moderno** e intuitivo

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **Flask 3.0** - Framework web
- **SQLite** - Banco de dados

### Frontend
- **HTML5** - Estrutura
- **CSS3** - Estilização
- **JavaScript (ES6+)** - Interatividade
- **Fetch API** - Comunicação com backend

### Conceitos Aplicados
- 🏗️ Arquitetura MVC
- 🌐 API REST
- 📡 CRUD completo (Create, Read, Update, Delete)
- 🔄 Comunicação assíncrona (async/await)
- 🔒 Validações server-side
- 🛡️ Proteção contra XSS

---

## 📁 Estrutura do Projeto

```
sistema-chamados/
│
├── app.py                      # Servidor Flask e API REST
│
├── database/
│   └── chamados.db            # Banco SQLite (gerado automaticamente)
│
├── templates/
│   └── index.html             # Interface principal
│
├── static/
│   ├── css/
│   │   └── style.css          # Estilos da aplicação
│   │
│   └── js/
│       └── script.js          # Lógica frontend e comunicação API
│
├── requirements.txt           # Dependências Python
├── dados_exemplo.py          # Script para popular banco com dados de exemplo
├── .gitignore                # Arquivos ignorados pelo Git
└── README.md                 # Este arquivo
```

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior instalado
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/Vitoroalves/sistemas-chamados-ti.git
cd sistemas-chamados-ti
```

2. **Crie um ambiente virtual** (recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**
```bash
python app.py
```

5. **Acesse no navegador**
```
http://localhost:5000
```

O banco de dados será criado automaticamente na primeira execução.

---

## 🎯 Como Usar

### Criar um Chamado

1. Clique no botão **"+ Novo chamado"**
2. Preencha o formulário:
   - **Título**: Resumo do problema
   - **Descrição**: Detalhes do problema
   - **Categoria**: Hardware, Software, Rede, Acesso ou Outro
   - **Prioridade**: Baixa, Média, Alta ou Urgente
3. Clique em **"Criar Chamado"**

### Gerenciar Chamados

- **Alterar Status**: Clique no botão "Alterar Status" no card do chamado
  - O status segue o ciclo: Aberto → Em andamento → Resolvido → Encerrado
- **Excluir**: Clique no botão "Excluir" e confirme a ação

### Dashboard

O painel superior mostra estatísticas em tempo real:
- Total de chamados
- Chamados abertos
- Em andamento
- Resolvidos/Encerrados

---

## 🔌 API REST

A aplicação expõe uma API REST completa:

### Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/chamados` | Lista todos os chamados |
| `POST` | `/api/chamados` | Cria um novo chamado |
| `GET` | `/api/chamados/:id` | Obtém um chamado específico |
| `PUT` | `/api/chamados/:id` | Atualiza um chamado |
| `DELETE` | `/api/chamados/:id` | Exclui um chamado |
| `GET` | `/api/dashboard` | Retorna estatísticas |

### Exemplos de Uso

**Criar um chamado:**
```bash
curl -X POST http://localhost:5000/api/chamados \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Impressora não funciona",
    "descricao": "A impressora do 2º andar não está imprimindo",
    "categoria": "Hardware",
    "prioridade": "Média"
  }'
```

**Listar todos os chamados:**
```bash
curl http://localhost:5000/api/chamados
```

**Alterar status:**
```bash
curl -X PUT http://localhost:5000/api/chamados/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "Em andamento"}'
```

---

## 📊 Modelo de Dados

### Tabela: `chamados`

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER | ID único (auto incremento) |
| `titulo` | TEXT | Título do chamado |
| `descricao` | TEXT | Descrição detalhada |
| `categoria` | TEXT | Hardware, Software, Rede, Acesso, Outro |
| `prioridade` | TEXT | Baixa, Média, Alta, Urgente |
| `status` | TEXT | Aberto, Em andamento, Resolvido, Encerrado |
| `data_criacao` | TEXT | Data/hora de criação |
| `data_atualizacao` | TEXT | Data/hora da última atualização |

---

## 🎨 Screenshots

### Tela Principal
Dashboard com estatísticas e lista de chamados

### Modal de Criação
Formulário para criar novo chamado com validações

### Cards de Chamados
Cards informativos com ações de gerenciamento

*(Adicione screenshots reais aqui após capturar)*

---

## 🔧 Desenvolvimento

### Estrutura de Pastas Explicada

- **`app.py`**: Contém toda a lógica backend (rotas Flask, operações no banco)
- **`templates/`**: Arquivos HTML que o Flask renderiza
- **`static/`**: Arquivos estáticos (CSS, JavaScript, imagens)
- **`database/`**: Banco de dados SQLite

### Padrão de Código

- **Backend (Python)**: Segue PEP 8
- **Frontend (JavaScript)**: ES6+ com async/await
- **CSS**: Metodologia BEM-like para classes

---

## 📈 Próximas Melhorias

Ideias para evolução do projeto:

- [ ] Sistema de autenticação (login/logout)
- [ ] Múltiplos usuários com diferentes permissões
- [ ] Atribuir chamados a técnicos específicos
- [ ] Sistema de comentários nos chamados
- [ ] Anexar arquivos aos chamados
- [ ] Filtros e busca avançada
- [ ] Exportar relatórios (PDF/Excel)
- [ ] Notificações em tempo real (WebSocket)
- [ ] Histórico de alterações
- [ ] API de integração com outros sistemas

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 👨‍💻 Autor

**Vitor Alves**

- GitHub: [@Vitoroalves](https://github.com/Vitoroalves)
- Projeto: [Sistema de Chamados TI](https://github.com/Vitoroalves/sistemas-chamados-ti)

---

## 🙏 Agradecimentos

Projeto desenvolvido como parte do aprendizado de desenvolvimento Full Stack, combinando:
- Backend com Python/Flask
- Frontend com HTML/CSS/JavaScript
- Banco de dados SQLite
- API REST
- Git/GitHub

---

**⭐ Se este projeto foi útil, considere dar uma estrela no repositório!**

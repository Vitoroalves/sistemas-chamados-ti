const modal = document.getElementById('modal');
const btnNovoChamado = document.getElementById('btnNovoChamado');
const closeModal = document.getElementById('closeModal');
const cancelBtn = document.getElementById('cancelBtn');
const formChamado = document.getElementById('formChamado');
const ticketsList = document.getElementById('ticketsList');

function abrirModal() {
    modal.classList.add('active');
    formChamado.reset();
}

function fecharModal() {
    modal.classList.remove('active');
}

async function carregarChamados() {
    try {
        const response = await fetch('/api/chamados');
        
        if (!response.ok) {
            throw new Error('Erro ao carregar chamados');
        }
        
        const chamados = await response.json();
        renderizarChamados(chamados);
        
    } catch (erro) {
        console.error('Erro:', erro);
        mostrarErro('Não foi possível carregar os chamados');
    }
}

async function carregarDashboard() {
    try {
        const response = await fetch('/api/dashboard');
        
        if (!response.ok) {
            throw new Error('Erro ao carregar dashboard');
        }
        
        const stats = await response.json();
        atualizarDashboard(stats);
        
    } catch (erro) {
        console.error('Erro:', erro);
    }
}

async function criarChamado(event) {
    event.preventDefault();
    
    const btnSubmit = event.target.querySelector('button[type="submit"]');
    btnSubmit.disabled = true;
    btnSubmit.textContent = 'Criando...';
    
    try {
        const dados = {
            titulo: document.getElementById('titulo').value,
            descricao: document.getElementById('descricao').value,
            categoria: document.getElementById('categoria').value,
            prioridade: document.getElementById('prioridade').value
        };
        
        const response = await fetch('/api/chamados', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });
        
        if (!response.ok) {
            const erro = await response.json();
            throw new Error(erro.erro || 'Erro ao criar chamado');
        }
        
        const resultado = await response.json();
        console.log('Chamado criado:', resultado);
        
        fecharModal();
        
        await carregarChamados();
        await carregarDashboard();
        
        mostrarSucesso('Chamado criado com sucesso!');
        
    } catch (erro) {
        console.error('Erro:', erro);
        mostrarErro(erro.message || 'Erro ao criar chamado');
        
    } finally {
        btnSubmit.disabled = false;
        btnSubmit.textContent = 'Criar Chamado';
    }
}

async function alterarStatus(id, statusAtual) {
    try {
        const statusCiclo = ["Aberto", "Em andamento", "Resolvido", "Encerrado"];
        const indexAtual = statusCiclo.indexOf(statusAtual);
        const proximoIndex = (indexAtual + 1) % statusCiclo.length;
        const novoStatus = statusCiclo[proximoIndex];
        
        const response = await fetch(`/api/chamados/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: novoStatus })
        });
        
        if (!response.ok) {
            throw new Error('Erro ao alterar status');
        }
        
        console.log(`Chamado #${id} → ${novoStatus}`);
        
        await carregarChamados();
        await carregarDashboard();
        
        mostrarSucesso(`Status alterado para: ${novoStatus}`);
        
    } catch (erro) {
        console.error('Erro:', erro);
        mostrarErro('Erro ao alterar status');
    }
}

async function excluirChamado(id) {
    const confirmar = confirm('Tem certeza que deseja excluir este chamado?');
    
    if (!confirmar) return;
    
    try {
        const response = await fetch(`/api/chamados/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Erro ao excluir chamado');
        }
        
        console.log(`Chamado #${id} excluído`);
        
        await carregarChamados();
        await carregarDashboard();
        
        mostrarSucesso('Chamado excluído com sucesso!');
        
    } catch (erro) {
        console.error('Erro:', erro);
        mostrarErro('Erro ao excluir chamado');
    }
}

function renderizarChamados(chamados) {
    ticketsList.innerHTML = '';
    
    if (chamados.length === 0) {
        ticketsList.innerHTML = `
            <div style="text-align: center; padding: 40px; color: #6b7280;">
                <p style="font-size: 18px; margin-bottom: 8px;">Nenhum chamado encontrado</p>
                <p style="font-size: 14px;">Clique em "+ Novo chamado" para criar o primeiro</p>
            </div>
        `;
        return;
    }
    
    chamados.forEach(chamado => {
        const card = criarCardChamado(chamado);
        ticketsList.appendChild(card);
    });
}

function criarCardChamado(chamado) {
    const article = document.createElement('article');
    article.className = 'ticket-card';
    
    const statusClasses = {
        'Aberto': 'status-open',
        'Em andamento': 'status-progress',
        'Resolvido': 'status-resolved',
        'Encerrado': 'status-resolved'
    };
    const statusClass = statusClasses[chamado.status] || 'status-open';
    
    const data = new Date(chamado.data_criacao);
    const dataFormatada = data.toLocaleDateString('pt-BR');
    
    article.innerHTML = `
        <div class="ticket-top">
            <span class="ticket-id">#${chamado.id}</span>
            <span class="status ${statusClass}">${chamado.status}</span>
        </div>

        <h3>${escapeHtml(chamado.titulo)}</h3>

        <p class="ticket-description">
            ${escapeHtml(chamado.descricao)}
        </p>

        <div class="ticket-info">
            <span>${escapeHtml(chamado.categoria)}</span>
            <span>${escapeHtml(chamado.prioridade)} prioridade</span>
            <span>📅 ${dataFormatada}</span>
        </div>

        <div class="ticket-actions">
            <button class="btn-small btn-status" onclick="alterarStatus(${chamado.id}, '${escapeHtml(chamado.status)}')">
                Alterar Status
            </button>
            <button class="btn-small btn-delete" onclick="excluirChamado(${chamado.id})">
                Excluir
            </button>
        </div>
    `;
    
    return article;
}

function atualizarDashboard(stats) {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    if (statNumbers.length >= 4) {
        statNumbers[0].textContent = stats.total;
        statNumbers[1].textContent = stats.abertos;
        statNumbers[2].textContent = stats.em_andamento;
        statNumbers[3].textContent = stats.resolvidos;
    }
}

function mostrarSucesso(mensagem) {
    const notificacao = document.createElement('div');
    notificacao.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: #dcfce7;
        color: #166534;
        padding: 16px 24px;
        border-radius: 8px;
        border: 1px solid #86efac;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        z-index: 10000;
        font-weight: 600;
        animation: slideIn 0.3s ease;
    `;
    notificacao.textContent = mensagem;
    
    document.body.appendChild(notificacao);
    
    setTimeout(() => {
        notificacao.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notificacao.remove(), 300);
    }, 3000);
}

function mostrarErro(mensagem) {
    const notificacao = document.createElement('div');
    notificacao.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: #fee2e2;
        color: #b91c1c;
        padding: 16px 24px;
        border-radius: 8px;
        border: 1px solid #fca5a5;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        z-index: 10000;
        font-weight: 600;
    `;
    notificacao.textContent = mensagem;
    
    document.body.appendChild(notificacao);
    
    setTimeout(() => notificacao.remove(), 4000);
}

function escapeHtml(texto) {
    const div = document.createElement('div');
    div.textContent = texto;
    return div.innerHTML;
}

btnNovoChamado.addEventListener('click', abrirModal);

closeModal.addEventListener('click', fecharModal);

cancelBtn.addEventListener('click', fecharModal);

modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        fecharModal();
    }
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
        fecharModal();
    }
});

formChamado.addEventListener('submit', criarChamado);

document.addEventListener('DOMContentLoaded', async () => {
    console.log('Sistema inicializado');
    
    await carregarChamados();
    await carregarDashboard();
});

const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

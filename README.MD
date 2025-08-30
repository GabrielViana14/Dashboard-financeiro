# 💰 Dashboard Financeiro


Um dashboard financeiro interativo desenvolvido em Python com Streamlit, para gerenciar contas, transações, orçamentos e análises gráficas. Suporta múltiplos usuários e funcionalidades administrativas.

## ⚡ Funcionalidades
| Aba | Funcionalidade |
|--------|----------------|
|Resumo	| Visão geral de saldos, evolução do saldo, top 3 categorias de gasto, alertas de saldo negativo.|
|Transações	| Visualizar, adicionar, remover e exportar transações. Filtrar por data, descrição ou categoria.|
|Orçamento	| Definir limites por categoria, acompanhar gasto em barras de progresso, salvar limites.|
|Gráficos / Análises	| Evolução do saldo, gastos por categoria, fluxo mensal (entradas e saídas).|
|Admin	| Adicionar ou remover contas de qualquer usuário (apenas para admin).|

## 🛠 Tecnologias

* Python 3.11+

* Streamlit – dashboard interativo

* Pandas – manipulação de dados

* Plotly – gráficos interativos

* JSON – armazenamento local de dados

* Datetime – manipulação de datas

## 📁 Estrutura do Projeto
```
dashboard-financeiro/
│
├─ main.py                 # Arquivo principal  
├─ main_page.py            # Lógica das abas  
├─ contas.py               # Funções de contas e transações  
├─ tabs/                   # Código separado por aba  
│   ├─ resumo_tab.py  
│   ├─ transacoes_tab.py  
│   ├─ orcamento_tab.py  
│   ├─ analises_tab.py  
│   └─ admin_tab.py  
├─ contas.json             # Dados de contas e transações  
└─ orcamento_limites.json  # Limites de orçamento por usuário  
```

## 🚀 Como rodar

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/dashboard-financeiro.git
cd dashboard-financeiro
```


2. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```
Windows
```bash
.venv\Scripts\activate
```
Linux / Mac
```bash
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```
4. Gere as chaves e senhas hasheadas:

```bash 
python gerar_chaves.py
```
>Isso cria o arquivo hashed_senhas.pkl com os usuários: Admin (senha padrão: teste).

5. Configure o autenticador (opcional se já for carregado pelo main.py):

```bash
python auth.py
```


6. Execute o dashboard:

```bash
streamlit run main.py
```

7. Abra no navegador:
```
http://localhost:8501
```
## ⚠ Observações

Usuário padrão: ``admin`` (acesso a todas as contas).

Datas devem estar no formato ``YYYY-MM-DD HH:MM:SS``.

Dados são salvos em arquivos JSON. Pode ser adaptado para banco de dados.

## 🔮 Próximos Desenvolvimentos

Gráficos e análises mais detalhadas.

Autenticação com senha segura.

Exportação de relatórios em Excel/PDF.

Dashboard responsivo para dispositivos móveis.
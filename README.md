<div align="center">

  <!-- Imagem da pasta do projeto -->
  <img src="image.png" alt="BolsoUp Banner" width="180"/>

  # 💰 BolsoUp - Seu Dinheiro Organizado

  > Um sistema de gestão financeira pessoal simples, moderno e visual para manter seu orçamento e poupança sob controle.

  ![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
  ![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-7c3aed?style=for-the-badge)
  ![Matplotlib](https://img.shields.io/badge/Data-Matplotlib-111827?style=for-the-badge)
  ![Status](https://img.shields.io/badge/Status-Concluído-10b981?style=for-the-badge)

</div>

---

##  Sobre o Projeto

O **BolsoUp** nasceu para resolver a complicação de planilhas financeiras tradicionais. Ele oferece uma interface limpa e intuitiva baseada em duas carteiras principais: **Gastos do Dia a Dia** e **Poupança**. 

Com gráficos dinâmicos e um sistema inteligente de **resgate de emergência**, o sistema impede que você fique no "vermelho" sem perceber e facilita o acompanhamento de para onde seu dinheiro está indo.

---

## ✨ Funcionalidades Principais

- 📊 **Dashboard Dinâmico:** Visão geral do seu saldo e gráficos interativos atualizados em tempo real.
- 🍕 **Distribuição de Gastos:** Gráfico de pizza que categoriza suas despesas.
- 📈 **Evolução Diária:** Acompanhe seus gastos dia a dia em um gráfico de linha intuitivo.
- 💳 **Gestão de Carteiras:** Separação clara entre dinheiro livre para gasto e reserva de poupança.
- 💸 **Resgate de Emergência:** Tenta registrar um gasto maior que o saldo atual? O sistema oferece uma transferência rápida da poupança com um clique!
- 📜 **Histórico de Transações:** Listagem de todos os gastos e transferências passadas.

---

## 🛠️ Tecnologias Utilizadas

O projeto foi construído em **Python** utilizando a seguinte stack:

- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter):** Para uma interface gráfica (GUI) moderna e elegante.
- **[Matplotlib](https://matplotlib.org/):** Renderização de gráficos financeiros (Pizza, Barras e Linhas) integrados à interface.
- **SQLite / DB:** Armazenamento seguro e persistente dos seus dados financeiros.
- **Arquitetura Modular:** Separação limpa entre a interface (`designer.py`), lógica (`gui.py`), banco de dados (`database.py`), regras de negócio (`services.py`) e modelos (`models.py`).

---

## 📁 Estrutura do Projeto

```text
📂 Sistema-financeiro-UEPB/
 ├── 📄 main.py            # Ponto de inicialização do programa
 ├── 📄 gui.py             # Eventos e controladores da interface
 ├── 📄 designer.py        # Layout visual e componentes da UI
 ├── 📄 services.py        # Regras de negócio e cálculos
 ├── 📄 database.py        # Conexão e manipulação do banco de dados
 ├── 📄 models.py          # Modelos de dados (Gasto, Carteira, Transação)
 ├── 🖼️ image.png          # Logo/Imagem do projeto
 └── 📄 README.md          # Documentação do repositório


🚀 Como Executar o Projeto

Certifique-se de ter o Python 3.10+ instalado na sua máquina.

🛠️ Instalar as dependências:  # pip install customtkinter matplotlib
🤝 Executar a aplicação:   # python main.py



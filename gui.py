import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import services
from models import Gasto

##Aqui é o arquivo da nossa interface grafica, onde o usuario vai interagir com o sistema.

# ==================== ALTERAÇÃO 5 (INÍCIO) - NOVO ====================   #OK
# Lista fixa de categorias, usada na combobox de cadastro de gasto.
CATEGORIAS_GASTO = ["Alimentação", "Transporte", "Lazer", "Moradia", "Saúde", "Educação", "Outros"]
# ==================== ALTERAÇÃO 5 (FIM) ====================


class AppFinanceiro:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Financeiro - Modificações Beatriz")
        # ALTERAÇÃO 6: aumentamos a largura para caber os 3 gráficos lado a lado #OK
        # (era "800x650")
        self.root.geometry("950x700")

        # Menu de abas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        self.tab_dashboard = ttk.Frame(self.notebook)
        self.tab_gastos = ttk.Frame(self.notebook)
        self.tab_poupanca = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_dashboard, text='Dashboard')
        self.notebook.add(self.tab_gastos, text='Carteira de Gastos')
        self.notebook.add(self.tab_poupanca, text='Carteira Poupança')

        self.notebook.bind("<<NotebookTabChanged>>", self.atualizar_todas_telas)

        self.montar_dashboard()
        self.montar_tela_gastos()
        self.montar_tela_poupanca()

        self.atualizar_todas_telas(None)

    def montar_dashboard(self):
        frame_top = tk.Frame(self.tab_dashboard, pady=10)
        frame_top.pack()

        tk.Label(frame_top, text="Adicionar Salário / Entrada", font=("Arial", 12, "bold")).pack()

        tk.Label(frame_top, text="Valor para Poupança (R$):").pack()
        self.entry_sal_poupanca = tk.Entry(frame_top)
        self.entry_sal_poupanca.pack()

        tk.Label(frame_top, text="Valor para Gastos (R$):").pack()
        self.entry_sal_gastos = tk.Entry(frame_top)
        self.entry_sal_gastos.pack()

        tk.Button(frame_top, text="Adicionar Saldo", command=self.adicionar_saldo_inicial, bg="lightblue").pack(pady=10)

        self.frame_grafico = tk.Frame(self.tab_dashboard)
        self.frame_grafico.pack(fill='both', expand=True)

    def adicionar_saldo_inicial(self):
        try:
            val_poup = float(self.entry_sal_poupanca.get() or 0)
            val_gas = float(self.entry_sal_gastos.get() or 0)
            services.adicionar_salario(val_poup, val_gas)
            messagebox.showinfo("Sucesso", "Saldo distribuído com sucesso!")
            self.entry_sal_poupanca.delete(0, tk.END)
            self.entry_sal_gastos.delete(0, tk.END)
            self.atualizar_todas_telas(None)
        except ValueError:
            messagebox.showerror("Erro", "Digite valores numéricos válidos.")

    # ==================== ALTERAÇÃO 7 (INÍCIO) - FUNÇÃO REESCRITA ==================== #OK
    # Antes esta função só desenhava 1 gráfico de pizza. Agora desenha 3.
    def atualizar_grafico(self):
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        # Agora montamos 3 gráficos lado a lado:
        # 1) Pizza com distribuição de gastos por categoria
        # 2) Barras comparando o saldo das duas carteiras
        # 3) Linha com a evolução dos gastos por dia
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))

        gastos = services.obter_todos_gastos()
        if gastos:
            dados_grafico = {}
            for gasto in gastos:
                rotulo= gasto.descricao if gasto.descricao else gasto.nome
                dados_grafico[rotulo] = dados_grafico.get(rotulo, 0) + gasto.valor
            ax1.pie(dados_grafico.values(), labels=dados_grafico.keys(), autopct='%1.1f%%',
                    startangle=90, colors=plt.cm.Pastel1.colors)
            ax1.axis('equal')
            ax1.set_title("Distribuição de Gastos (%)")
        else:
            ax1.text(0.5, 0.5, "Nenhum gasto\nregistrado", ha='center', va='center')
            ax1.axis('off')


        # Gráfico de barras: saldo das carteiras
        carteira_poup = services.obter_carteira(1)
        carteira_gas = services.obter_carteira(2)
        ax2.bar(["Poupança", "Gastos"], [carteira_poup.saldo, carteira_gas.saldo],
                color=["#8fbc8f", "#e88585"])
        ax2.set_title("Saldo por Carteira")

        # Gráfico de linha: evolução dos gastos por dia
        gastos_por_dia = services.obter_gastos_por_dia()
        if gastos_por_dia:
            dias = list(gastos_por_dia.keys())
            valores = list(gastos_por_dia.values())
            ax3.plot(dias, valores, marker='o', color="#d95f5f")
            ax3.set_title("Gastos por Dia")
            ax3.tick_params(axis='x', rotation=45)
        else:
            ax3.text(0.5, 0.5, "Sem histórico\nainda", ha='center', va='center')
            ax3.axis('off')

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack()
    # ==================== ALTERAÇÃO 7 (FIM) ====================

    def montar_tela_gastos(self):
        # Topo com saldo reduzido ligeiramente no espaçamento para caber tudo
        self.lbl_saldo_gastos = tk.Label(self.tab_gastos, text="Saldo Disponível: R$ 0.00", font=("Arial", 16, "bold"), fg="darkred")
        self.lbl_saldo_gastos.pack(pady=10)

        # Formulário de Cadastro de Gasto
        frame_form = tk.Frame(self.tab_gastos)
        frame_form.pack(pady=5)

        # ==================== ALTERAÇÃO 8 (INÍCIO) ====================
        # Antes era: self.entry_nome_gasto = tk.Entry(frame_form)  (campo de texto livre)
        # Trocamos o campo livre de texto por uma combobox com categorias fixas.
        # Isso evita que o mesmo gasto vire "fatias" diferentes no gráfico de
        # pizza por causa de digitação (ex: "alimentação" vs "Alimentação").
        tk.Label(frame_form, text="Categoria do Gasto:").grid(row=0, column=0, pady=5, sticky="e")
        self.combo_nome_gasto = ttk.Combobox(frame_form, values=CATEGORIAS_GASTO, state="readonly")
        self.combo_nome_gasto.grid(row=0, column=1, pady=5)
        self.combo_nome_gasto.current(0)
        # ==================== ALTERAÇÃO 8 (FIM) ====================

        tk.Label(frame_form, text="Descrição:").grid(row=1, column=0, pady=5, sticky="e")
        self.entry_desc_gasto = tk.Entry(frame_form)
        self.entry_desc_gasto.grid(row=1, column=1, pady=5)

        tk.Label(frame_form, text="Valor (R$):").grid(row=2, column=0, pady=5, sticky="e")
        self.entry_valor_gasto = tk.Entry(frame_form)
        self.entry_valor_gasto.grid(row=2, column=1, pady=5)

        tk.Button(self.tab_gastos, text="Registrar Gasto", command=self.processar_novo_gasto, bg="lightcoral").pack(pady=10)

        # --- HISTÓRICO VISUAL DE GASTOS ---
        tk.Label(self.tab_gastos, text="Lista de Gastos Cadastrados", font=("Arial", 12, "bold")).pack(pady=10)

        # ==================== ALTERAÇÃO 9 (INÍCIO) ==================== #OK
        # Adicionamos a coluna "Data" na lista, já que agora salvamos essa informação.
        # (colunas antes era só ("Nome", "Descrição", "Valor (R$)"))
        colunas = ("Nome", "Descrição", "Valor (R$)", "Data")
        self.tree_gastos = ttk.Treeview(self.tab_gastos, columns=colunas, show="headings", height=8)
        self.tree_gastos.heading("Nome", text="Categoria")
        self.tree_gastos.heading("Descrição", text="Descrição detalhada")
        self.tree_gastos.heading("Valor (R$)", text="Valor (R$)")
        self.tree_gastos.heading("Data", text="Data")

        self.tree_gastos.column("Nome", width=130, anchor="center")
        self.tree_gastos.column("Descrição", width=300, anchor="w")
        self.tree_gastos.column("Valor (R$)", width=100, anchor="center")
        self.tree_gastos.column("Data", width=140, anchor="center")
        # ==================== ALTERAÇÃO 9 (FIM) ====================

        self.tree_gastos.pack(pady=5, fill="x", padx=20)

    def processar_novo_gasto(self):
        # ==================== ALTERAÇÃO 10 (INÍCIO) ====================
        # Antes era: nome = self.entry_nome_gasto.get().strip()
        nome = self.combo_nome_gasto.get().strip()
        desc = self.entry_desc_gasto.get().strip()

        if not nome:
            # Antes era: messagebox.showwarning("Aviso", "O nome do gasto é obrigatório.")
            messagebox.showwarning("Aviso", "Selecione uma categoria para o gasto.")
            return
        # ==================== ALTERAÇÃO 10 (FIM) ====================

        try:
            valor = float(self.entry_valor_gasto.get())
            if valor <= 0:
                messagebox.showerror("Erro", "O valor deve ser maior que zero.")
                return
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido.")
            return

        carteira_gastos = services.obter_carteira(2)

        if valor > carteira_gastos.saldo:
            resposta = messagebox.askyesno(
                "Saldo Insuficiente",
                "Você não possui mais saldo suficiente para gastos. Deseja transferir o valor da carteira poupança para a carteira de gastos?"
            )
            if resposta:
                self.abrir_tela_transferencia()
        else:
            novo_gasto = Gasto(nome=nome, descricao=desc, valor=valor)
            services.registrar_gasto(novo_gasto)

            messagebox.showinfo("Sucesso", "Gasto registrado com sucesso!")
            # ALTERAÇÃO 11: antes era self.entry_nome_gasto.delete(0, tk.END)
            self.combo_nome_gasto.current(0)
            self.entry_desc_gasto.delete(0, tk.END)
            self.entry_valor_gasto.delete(0, tk.END)
            self.atualizar_todas_telas(None)

    def abrir_tela_transferencia(self):
        tela_transf = tk.Toplevel(self.root)
        tela_transf.title("Transferência de Emergência")
        tela_transf.geometry("400x250")
        tela_transf.grab_set()

        carteira_poup = services.obter_carteira(1)

        tk.Label(tela_transf, text="Resgate da Poupança", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(tela_transf, text=f"Saldo disponível na Poupança: R$ {carteira_poup.saldo:.2f}", fg="green").pack(pady=5)

        tk.Label(tela_transf, text="Quanto deseja transferir para Gastos? (R$)").pack(pady=5)
        entry_valor_transf = tk.Entry(tela_transf)
        entry_valor_transf.pack(pady=5)

        def confirmar_transferencia():
            try:
                valor_transf = float(entry_valor_transf.get())
                if valor_transf > carteira_poup.saldo:
                    messagebox.showerror("Erro", "Você não tem esse valor na poupança!")
                    return
                if valor_transf <= 0:
                    messagebox.showerror("Erro", "Digite um valor maior que zero.")
                    return

                services.realizar_transferencia_emergencia(valor_transf)
                messagebox.showinfo("Sucesso", "Valor transferido com sucesso!")
                tela_transf.destroy()
                self.atualizar_todas_telas(None)
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido!")

        tk.Button(tela_transf, text="Confirmar Transferência", command=confirmar_transferencia, bg="lightgreen").pack(pady=15)

    def montar_tela_poupanca(self):
        self.lbl_saldo_poupanca = tk.Label(self.tab_poupanca, text="Saldo Disponível: R$ 0.00", font=("Arial", 16, "bold"), fg="darkgreen")
        self.lbl_saldo_poupanca.pack(pady=20)

        tk.Label(self.tab_poupanca, text="Histórico de Transferências para Gastos", font=("Arial", 12)).pack(pady=10)

        colunas = ("Data", "Valor (R$)")
        self.tree_historico = ttk.Treeview(self.tab_poupanca, columns=colunas, show="headings", height=10)
        self.tree_historico.heading("Data", text="Data")
        self.tree_historico.heading("Valor (R$)", text="Valor (R$)")
        self.tree_historico.pack()

    def atualizar_todas_telas(self, event):
        carteira_poup = services.obter_carteira(1)
        carteira_gas = services.obter_carteira(2)

        self.lbl_saldo_poupanca.config(text=f"Saldo Disponível: R$ {carteira_poup.saldo:.2f}")
        self.lbl_saldo_gastos.config(text=f"Saldo Disponível: R$ {carteira_gas.saldo:.2f}")

        self.atualizar_grafico()

        # 1. Atualizar histórico de transferências (Aba Poupança)
        for row in self.tree_historico.get_children():
            self.tree_historico.delete(row)

        historico = services.obter_historico_transferencias()
        for transf in historico:
            self.tree_historico.insert("", "end", values=(transf.data[:16], f"{transf.valor:.2f}"))

        # 2. Atualizar a lista de gastos cadastrados (Aba Gastos), agora com a data
        for row in self.tree_gastos.get_children():
            self.tree_gastos.delete(row)

        # ==================== ALTERAÇÃO 12 (INÍCIO) ====================
        # Antes o insert só tinha (gasto.nome, gasto.descricao, f"{gasto.valor:.2f}")
        gastos = services.obter_todos_gastos()
        for gasto in gastos:
            data_exibida = gasto.data[:16] if gasto.data else ""
            self.tree_gastos.insert("", "end", values=(gasto.nome, gasto.descricao, f"{gasto.valor:.2f}", data_exibida))
        # ==================== ALTERAÇÃO 12 (FIM) ====================

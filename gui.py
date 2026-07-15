import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import services
from models import Gasto

##Aqui é o arquivo da nossa interface grafica, onde o usuario vai interagir com o sistema.

class AppFinanceiro:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Financeiro - Protótipo")
        self.root.geometry("800x650")  # Aumentamos um pouquinho a altura para caber a lista confortavelmente

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

    def atualizar_grafico(self):
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        gastos = services.obter_todos_gastos()
        if not gastos:
            tk.Label(self.frame_grafico, text="Nenhum gasto registrado. O gráfico aparecerá aqui.").pack(pady=50)
            return

        dados_grafico = {}
        for gasto in gastos:
            dados_grafico[gasto.nome] = dados_grafico.get(gasto.nome, 0) + gasto.valor

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(dados_grafico.values(), labels=dados_grafico.keys(), autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors)
        ax.axis('equal')
        ax.set_title("Distribuição de Gastos (%)")

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def montar_tela_gastos(self):
        # Topo com saldo reduzido ligeiramente no espaçamento para caber tudo
        self.lbl_saldo_gastos = tk.Label(self.tab_gastos, text="Saldo Disponível: R$ 0.00", font=("Arial", 16, "bold"), fg="darkred")
        self.lbl_saldo_gastos.pack(pady=10)

        # Formulário de Cadastro de Gasto
        frame_form = tk.Frame(self.tab_gastos)
        frame_form.pack(pady=5)

        tk.Label(frame_form, text="Nome do Gasto (ex: Alimentação):").grid(row=0, column=0, pady=5, sticky="e")
        self.entry_nome_gasto = tk.Entry(frame_form)
        self.entry_nome_gasto.grid(row=0, column=1, pady=5)

        tk.Label(frame_form, text="Descrição (Opcional):").grid(row=1, column=0, pady=5, sticky="e")
        self.entry_desc_gasto = tk.Entry(frame_form)
        self.entry_desc_gasto.grid(row=1, column=1, pady=5)

        tk.Label(frame_form, text="Valor (R$):").grid(row=2, column=0, pady=5, sticky="e")
        self.entry_valor_gasto = tk.Entry(frame_form)
        self.entry_valor_gasto.grid(row=2, column=1, pady=5)

        tk.Button(self.tab_gastos, text="Registrar Gasto", command=self.processar_novo_gasto, bg="lightcoral").pack(pady=10)

        # --- NOVA SEÇÃO: HISTÓRICO VISUAL DE GASTOS ---
        tk.Label(self.tab_gastos, text="Lista de Gastos Cadastrados", font=("Arial", 12, "bold")).pack(pady=10)
        
        colunas = ("Nome", "Descrição", "Valor (R$)")
        self.tree_gastos = ttk.Treeview(self.tab_gastos, columns=colunas, show="headings", height=8)
        self.tree_gastos.heading("Nome", text="Nome/Categoria")
        self.tree_gastos.heading("Descrição", text="Descrição detalhada")
        self.tree_gastos.heading("Valor (R$)", text="Valor (R$)")
        
        self.tree_gastos.column("Nome", width=150, anchor="center")
        self.tree_gastos.column("Descrição", width=350, anchor="w")
        self.tree_gastos.column("Valor (R$)", width=120, anchor="center")
        
        self.tree_gastos.pack(pady=5, fill="x", padx=20)

    def processar_novo_gasto(self):
        nome = self.entry_nome_gasto.get().strip()
        desc = self.entry_desc_gasto.get().strip()
        
        if not nome:
            messagebox.showwarning("Aviso", "O nome do gasto é obrigatório.")
            return

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
            self.entry_nome_gasto.delete(0, tk.END)
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

        # 2. Atualizar a nova lista de gastos cadastrados (Aba Gastos)
        for row in self.tree_gastos.get_children():
            self.tree_gastos.delete(row)

        gastos = services.obter_todos_gastos()
        for gasto in gastos:
            self.tree_gastos.insert("", "end", values=(gasto.nome, gasto.descricao, f"{gasto.valor:.2f}"))
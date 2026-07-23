import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import services
from models import Gasto


CATEGORIAS_GASTO = [
    "Alimentação", "Transporte", "Lazer", "Moradia",
    "Saúde", "Educação", "Vestuário", "Assinaturas", "Presentes",
    "Doações", "Emergências", "Trabalho", "Outros",
]

CORES_CATEGORIAS = {
    "Alimentação": "#f28b82",
    "Transporte": "#65a9e8",
    "Lazer": "#f7bd75",
    "Moradia": "#78c985",
    "Saúde": "#be93e4",
    "Educação": "#e9d36b",
    "Vestuário": "#eb84b3",
    "Assinaturas": "#58c4bd",
    "Presentes": "#e6916b",
    "Doações": "#8096dc",
    "Emergências": "#d56868",
    "Trabalho": "#5f9cce",
    "Outros": "#9ea9b8",
}


class AppFinanceiro:
    """Interface principal do sistema financeiro, organizada em um único painel."""

    FUNDO = "#f5f7fb"
    CARTAO = "#ffffff"
    ROXO = "#6547e8"
    TEXTO = "#202335"
    TEXTO_SUAVE = "#70758a"
    VERDE = "#249b54"
    VERMELHO = "#e05252"

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Financeiro")
        self.root.geometry("1250x760")
        self.root.minsize(1040, 650)
        self.root.configure(bg=self.FUNDO)
        self.canvas_grafico = None

        self.configurar_estilos()
        self.montar_painel()
        self.atualizar_todas_telas()

    def configurar_estilos(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure(
            "Finance.Treeview",
            background=self.CARTAO,
            fieldbackground=self.CARTAO,
            foreground="#171923",
            rowheight=31,
            borderwidth=0,
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "Finance.Treeview.Heading",
            background="#f2efff",
            foreground="#5441aa",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
        )
        style.map("Finance.Treeview", background=[("selected", "#ded8ff")])
        style.configure("TCombobox", padding=7, font=("Segoe UI", 10))

    @staticmethod
    def moeda(valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def criar_cartao(self, pai, cor_borda="#e5e7ee", padding=16):
        return tk.Frame(
            pai,
            bg=self.CARTAO,
            highlightbackground=cor_borda,
            highlightthickness=1,
            padx=padding,
            pady=padding,
        )

    def criar_titulo_cartao(self, pai, texto, cor=None):
        tk.Label(
            pai, text=texto, bg=self.CARTAO, fg=cor or self.TEXTO,
            font=("Segoe UI", 12, "bold"), anchor="center",
        ).pack(fill="x")

    def montar_painel(self):
        cabecalho = tk.Frame(self.root, bg=self.FUNDO, padx=28, pady=20)
        cabecalho.pack(fill="x")

        tk.Label(
            cabecalho, text="Painel Financeiro", bg=self.FUNDO, fg=self.TEXTO,
            font=("Segoe UI", 22, "bold"),
        ).pack(anchor="w")
        tk.Label(
            cabecalho, text="Acompanhe suas carteiras, registre gastos e visualize seu histórico.",
            bg=self.FUNDO, fg=self.TEXTO_SUAVE, font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(3, 0))

        conteudo = tk.Frame(self.root, bg=self.FUNDO, padx=28, pady=2)
        conteudo.pack(fill="both", expand=True)
        conteudo.grid_columnconfigure(0, weight=1, minsize=300)
        conteudo.grid_columnconfigure(1, weight=1, minsize=300)
        conteudo.grid_columnconfigure(2, weight=1, minsize=300)
        conteudo.grid_rowconfigure(0, weight=1)

        self.montar_coluna_grafico(conteudo)
        self.montar_coluna_carteiras(conteudo)
        self.montar_coluna_gastos(conteudo)
        self.montar_resumo()

    def montar_coluna_grafico(self, pai):
        cartao = self.criar_cartao(pai)
        cartao.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.criar_titulo_cartao(cartao, "Distribuição dos gastos", self.ROXO)
        self.lbl_total_gastos = tk.Label(
            cartao, text="Total de gastos: R$ 0,00", bg=self.CARTAO,
            fg=self.TEXTO_SUAVE, font=("Segoe UI", 10), anchor="w",
        )
        self.lbl_total_gastos.pack(fill="x", pady=(4, 8))

        self.frame_grafico = tk.Frame(cartao, bg=self.CARTAO)
        self.frame_grafico.pack(fill="both", expand=True)

    def montar_coluna_carteiras(self, pai):
        coluna = tk.Frame(pai, bg=self.FUNDO)
        coluna.grid(row=0, column=1, sticky="nsew", padx=5)
        coluna.grid_columnconfigure(0, weight=1)
        coluna.grid_rowconfigure(4, weight=1)

        entrada = self.criar_cartao(coluna)
        entrada.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.criar_titulo_cartao(entrada, "Adicionar saldo", self.ROXO)
        campos = tk.Frame(entrada, bg=self.CARTAO)
        campos.pack(fill="x", pady=(10, 8))
        campos.grid_columnconfigure(0, weight=1)
        campos.grid_columnconfigure(1, weight=1)
        self.entry_sal_poupanca = self.criar_campo(campos, "Para poupança", 0)
        self.entry_sal_gastos = self.criar_campo(campos, "Para gastos", 1)
        tk.Button(
            entrada, text="Adicionar saldo", command=self.adicionar_saldo_inicial,
            bg=self.ROXO, fg="white", activebackground="#5137cc", activeforeground="white",
            font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", pady=8,
        ).pack(fill="x")

        poupanca = self.criar_cartao(coluna, "#cdebd8")
        poupanca.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.criar_titulo_cartao(poupanca, "Poupança", self.VERDE)
        tk.Label(
            poupanca, text="Saldo disponível", bg=self.CARTAO, fg=self.TEXTO_SUAVE,
            font=("Segoe UI", 9),
        ).pack(pady=(12, 0))
        self.lbl_saldo_poupanca = tk.Label(
            poupanca, text="R$ 0,00", bg=self.CARTAO, fg=self.VERDE,
            font=("Segoe UI", 21, "bold"),
        )
        self.lbl_saldo_poupanca.pack(pady=(2, 10))

        gastos = self.criar_cartao(coluna, "#f5d5d5")
        gastos.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        self.criar_titulo_cartao(gastos, "Carteira de gastos", self.VERMELHO)
        tk.Label(
            gastos, text="Saldo disponível", bg=self.CARTAO, fg=self.TEXTO_SUAVE,
            font=("Segoe UI", 9),
        ).pack(pady=(12, 0))
        self.lbl_saldo_gastos = tk.Label(
            gastos, text="R$ 0,00", bg=self.CARTAO, fg=self.VERMELHO,
            font=("Segoe UI", 21, "bold"),
        )
        self.lbl_saldo_gastos.pack(pady=(2, 10))

        transferencia = self.criar_cartao(coluna, "#cdebd8")
        transferencia.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        self.criar_titulo_cartao(transferencia, "Transferência", self.VERDE)
        tk.Button(
            transferencia, text="Transferir para gastos", command=self.abrir_tela_transferencia,
            bg="#ecf8ef", fg=self.VERDE, activebackground="#d8f1df",
            font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", pady=8,
        ).pack(fill="x")

        historico = self.criar_cartao(coluna)
        historico.grid(row=4, column=0, sticky="nsew")
        self.criar_titulo_cartao(historico, "Transferências para gastos", self.VERDE)
        self.tree_historico = ttk.Treeview(
            historico, columns=("data", "valor"), show="headings", height=7,
            style="Finance.Treeview",
        )
        self.tree_historico.heading("data", text="Data")
        self.tree_historico.heading("valor", text="Valor")
        self.tree_historico.column("data", width=145, anchor="w")
        self.tree_historico.column("valor", width=105, anchor="e")
        self.tree_historico.pack(fill="both", expand=True, pady=(10, 0))

    def montar_coluna_gastos(self, pai):
        coluna = tk.Frame(pai, bg=self.FUNDO)
        coluna.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        coluna.grid_columnconfigure(0, weight=1)
        coluna.grid_rowconfigure(1, weight=1)

        formulario = self.criar_cartao(coluna, "#dcd5ff")
        formulario.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.criar_titulo_cartao(formulario, "Registrar gasto", self.ROXO)

        linha_um = tk.Frame(formulario, bg=self.CARTAO)
        linha_um.pack(fill="x", pady=(10, 8))
        linha_um.grid_columnconfigure(0, weight=2)
        linha_um.grid_columnconfigure(1, weight=1)

        tk.Label(linha_um, text="Categoria", bg=self.CARTAO, fg=self.TEXTO_SUAVE,
                 font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(linha_um, text="Valor (R$)", bg=self.CARTAO, fg=self.TEXTO_SUAVE,
                 font=("Segoe UI", 9, "bold")).grid(row=0, column=1, sticky="w", padx=(10, 0))

        self.combo_nome_gasto = ttk.Combobox(linha_um, values=CATEGORIAS_GASTO, state="readonly")
        self.combo_nome_gasto.grid(row=1, column=0, sticky="ew", pady=(3, 0))
        self.combo_nome_gasto.current(0)
        self.entry_valor_gasto = tk.Entry(linha_um, font=("Segoe UI", 10), relief="solid", bd=1)
        self.entry_valor_gasto.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=(3, 0), ipady=6)

        tk.Label(formulario, text="Descrição (opcional)", bg=self.CARTAO, fg=self.TEXTO_SUAVE,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.entry_desc_gasto = tk.Entry(formulario, font=("Segoe UI", 10), relief="solid", bd=1)
        self.entry_desc_gasto.pack(fill="x", pady=(3, 10), ipady=6)
        self.entry_valor_gasto.bind("<Return>", lambda _event: self.processar_novo_gasto())

        tk.Button(
            formulario, text="+  Adicionar gasto", command=self.processar_novo_gasto,
            bg=self.ROXO, fg="white", activebackground="#5137cc", activeforeground="white",
            font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", pady=9,
        ).pack(fill="x")

        lista = self.criar_cartao(coluna)
        lista.grid(row=1, column=0, sticky="nsew")
        self.criar_titulo_cartao(lista, "Gastos registrados", self.TEXTO)

        tabela_frame = tk.Frame(lista, bg=self.CARTAO)
        tabela_frame.pack(fill="both", expand=True, pady=(10, 0))
        tabela_frame.grid_columnconfigure(0, weight=1)
        tabela_frame.grid_rowconfigure(0, weight=1)
        self.tree_gastos = ttk.Treeview(
            tabela_frame, columns=("categoria", "descricao", "valor", "data"),
            show="headings", style="Finance.Treeview",
        )
        for coluna_tabela, titulo in (
            ("categoria", "Categoria"), ("descricao", "Descrição"),
            ("valor", "Valor"), ("data", "Data"),
        ):
            self.tree_gastos.heading(coluna_tabela, text=titulo)
        self.tree_gastos.column("categoria", width=120, anchor="w", stretch=False)
        self.tree_gastos.column("descricao", width=185, anchor="w")
        self.tree_gastos.column("valor", width=95, anchor="e", stretch=False)
        self.tree_gastos.column("data", width=120, anchor="center", stretch=False)
        self.tree_gastos.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Scrollbar(tabela_frame, orient="vertical", command=self.tree_gastos.yview)
        barra.grid(row=0, column=1, sticky="ns")
        self.tree_gastos.configure(yscrollcommand=barra.set)

        for categoria in CORES_CATEGORIAS:
            self.tree_gastos.tag_configure(categoria, foreground="#171923")

    def criar_campo(self, pai, rotulo, coluna):
        bloco = tk.Frame(pai, bg=self.CARTAO)
        bloco.grid(row=0, column=coluna, sticky="ew", padx=(0, 8) if coluna == 0 else (8, 0))
        tk.Label(bloco, text=rotulo, bg=self.CARTAO, fg=self.TEXTO_SUAVE,
                 font=("Segoe UI", 9)).pack(anchor="w")
        campo = tk.Entry(bloco, font=("Segoe UI", 10), relief="solid", bd=1)
        campo.pack(fill="x", pady=(3, 0), ipady=5)
        return campo

    def montar_resumo(self):
        rodape = tk.Frame(self.root, bg="#ffffff", padx=28, pady=14)
        rodape.pack(fill="x", side="bottom")
        self.lbl_resumo = tk.Label(
            rodape, text="", bg="#ffffff", fg=self.TEXTO_SUAVE,
            font=("Segoe UI", 10, "bold"),
        )
        self.lbl_resumo.pack()

    def adicionar_saldo_inicial(self):
        try:
            valor_poupanca = float(self.entry_sal_poupanca.get().replace(",", ".") or 0)
            valor_gastos = float(self.entry_sal_gastos.get().replace(",", ".") or 0)
            if valor_poupanca < 0 or valor_gastos < 0 or (valor_poupanca + valor_gastos) == 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Valor inválido", "Digite pelo menos um valor positivo para adicionar.")
            return

        services.adicionar_salario(valor_poupanca, valor_gastos)
        self.entry_sal_poupanca.delete(0, tk.END)
        self.entry_sal_gastos.delete(0, tk.END)
        self.atualizar_todas_telas()
        messagebox.showinfo("Saldo adicionado", "Os valores foram distribuídos entre as carteiras.")

    def processar_novo_gasto(self):
        categoria = self.combo_nome_gasto.get().strip()
        descricao = self.entry_desc_gasto.get().strip()
        try:
            valor = float(self.entry_valor_gasto.get().replace(",", "."))
            if valor <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Valor inválido", "Digite um valor numérico maior que zero.")
            return

        carteira_gastos = services.obter_carteira(2)
        if valor > carteira_gastos.saldo:
            precisa = valor - carteira_gastos.saldo
            if messagebox.askyesno(
                "Saldo insuficiente",
                f"Faltam {self.moeda(precisa)} na carteira de gastos.\n\n"
                "Deseja abrir a transferência da poupança?",
            ):
                self.abrir_tela_transferencia(precisa)
            return

        services.registrar_gasto(Gasto(nome=categoria, descricao=descricao, valor=valor))
        self.combo_nome_gasto.current(0)
        self.entry_desc_gasto.delete(0, tk.END)
        self.entry_valor_gasto.delete(0, tk.END)
        self.atualizar_todas_telas()
        messagebox.showinfo("Gasto registrado", "O gasto foi adicionado com sucesso.")

    def abrir_tela_transferencia(self, valor_sugerido=None):
        janela = tk.Toplevel(self.root)
        janela.title("Transferir da poupança")
        janela.configure(bg=self.FUNDO)
        janela.resizable(False, False)
        janela.transient(self.root)
        janela.grab_set()

        cartao = self.criar_cartao(janela, "#cdebd8", padding=22)
        cartao.pack(padx=18, pady=18)
        tk.Label(cartao, text="Transferir da poupança", bg=self.CARTAO, fg=self.VERDE,
                 font=("Segoe UI", 15, "bold")).pack(anchor="w")
        carteira_poupanca = services.obter_carteira(1)
        tk.Label(
            cartao, text=f"Disponível: {self.moeda(carteira_poupanca.saldo)}",
            bg=self.CARTAO, fg=self.TEXTO_SUAVE, font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(6, 16))
        tk.Label(cartao, text="Valor para gastos (R$)", bg=self.CARTAO, fg=self.TEXTO_SUAVE,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        campo = tk.Entry(cartao, font=("Segoe UI", 11), relief="solid", bd=1, width=30)
        campo.pack(fill="x", pady=(4, 14), ipady=7)
        if valor_sugerido:
            campo.insert(0, f"{valor_sugerido:.2f}".replace(".", ","))
        campo.focus_set()

        def confirmar():
            try:
                valor = float(campo.get().replace(",", "."))
                if valor <= 0 or valor > carteira_poupanca.saldo:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Valor inválido", "Digite um valor positivo disponível na poupança.", parent=janela)
                return
            services.realizar_transferencia_emergencia(valor)
            janela.destroy()
            self.atualizar_todas_telas()
            messagebox.showinfo("Transferência concluída", "O valor já está disponível na carteira de gastos.")

        tk.Button(
            cartao, text="Confirmar transferência", command=confirmar,
            bg=self.VERDE, fg="white", activebackground="#197a40", activeforeground="white",
            relief="flat", font=("Segoe UI", 10, "bold"), cursor="hand2", pady=9,
        ).pack(fill="x")
        campo.bind("<Return>", lambda _event: confirmar())

    def atualizar_grafico(self, gastos):
        if self.canvas_grafico:
            self.canvas_grafico.get_tk_widget().destroy()
            plt.close(self.canvas_grafico.figure)

        dados = {}
        for gasto in gastos:
            dados[gasto.nome] = dados.get(gasto.nome, 0) + gasto.valor

        figura, eixo = plt.subplots(figsize=(4.0, 4.4), dpi=100)
        figura.patch.set_facecolor(self.CARTAO)
        eixo.set_facecolor(self.CARTAO)
        if dados:
            categorias = list(dados)
            valores = list(dados.values())
            cores = [CORES_CATEGORIAS.get(categoria, "#9ea9b8") for categoria in categorias]
            eixo.pie(
                valores, labels=categorias, colors=cores, startangle=90,
                autopct="%1.0f%%", pctdistance=0.72,
                textprops={"fontsize": 9, "color": self.TEXTO},
                wedgeprops={"edgecolor": self.CARTAO, "linewidth": 2},
            )
            eixo.axis("equal")
        else:
            eixo.text(0.5, 0.55, "Nenhum gasto\nregistrado ainda", ha="center", va="center",
                      fontsize=12, color=self.TEXTO_SUAVE)
            eixo.axis("off")

        figura.tight_layout(pad=0.5)
        self.canvas_grafico = FigureCanvasTkAgg(figura, master=self.frame_grafico)
        self.canvas_grafico.draw()
        self.canvas_grafico.get_tk_widget().pack(fill="both", expand=True)

    def atualizar_todas_telas(self, _event=None):
        carteira_poupanca = services.obter_carteira(1)
        carteira_gastos = services.obter_carteira(2)
        gastos = services.obter_todos_gastos()

        self.lbl_saldo_poupanca.config(text=self.moeda(carteira_poupanca.saldo))
        self.lbl_saldo_gastos.config(text=self.moeda(carteira_gastos.saldo))
        total_gastos = sum(gasto.valor for gasto in gastos)
        self.lbl_total_gastos.config(text=f"Total de gastos: {self.moeda(total_gastos)}")
        self.lbl_resumo.config(
            text=(f"Poupança: {self.moeda(carteira_poupanca.saldo)}    •    "
                  f"Gastos: {self.moeda(carteira_gastos.saldo)}    •    "
                  f"Total geral: {self.moeda(carteira_poupanca.saldo + carteira_gastos.saldo)}")
        )

        for linha in self.tree_historico.get_children():
            self.tree_historico.delete(linha)
        for transferencia in services.obter_historico_transferencias():
            data = transferencia.data[:16] if transferencia.data else ""
            self.tree_historico.insert("", "end", values=(data, self.moeda(transferencia.valor)))

        for linha in self.tree_gastos.get_children():
            self.tree_gastos.delete(linha)
        for gasto in gastos:
            data = gasto.data[:16] if gasto.data else ""
            self.tree_gastos.insert(
                "", "end",
                values=(gasto.nome, gasto.descricao or "—", self.moeda(gasto.valor), data),
                tags=(gasto.nome,),
            )

        self.atualizar_grafico(gastos)

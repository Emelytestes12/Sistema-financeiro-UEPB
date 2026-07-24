import os
import customtkinter as ctk
from tkinter import ttk
from PIL import Image

# Configurações do tema CustomTkinter
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# Categorias padrão
CATEGORIAS_GASTO = ["Alimentação", "Transporte", "Lazer", "Moradia", "Saúde", "Educação", "Outros"]

# Caminho para o mascote
IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image.png")


class CTkTreeview(ttk.Treeview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Estilo personalizado para a Treeview
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "Treeview",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            rowheight=35,
            background="#f8fafc",
            foreground="#1e293b",
            fieldbackground="#f8fafc",
            borderwidth=0
        )
        self.style.configure(
            "Treeview.Heading",
            font=ctk.CTkFont(size=13, weight="bold", family="Segoe UI"),
            background="#8b5cf6",
            foreground="white",
            relief="flat",
            borderwidth=0,
            padding=10
        )
        self.style.map(
            "Treeview.Heading",
            background=[("active", "#7c3aed")]
        )
        self.style.map(
            "Treeview",
            background=[("selected", "#ede9fe")],
            foreground=[("selected", "#5b21b6")]
        )


class FinanceiroDesigner(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações básicas da janela
        self.title("💰 BolsoUp - Seu Dinheiro Organizado")
        self.geometry("1400x850")
        self.minsize(1200, 750)
        self.configure(fg_color="#f1f5f9")


        # Grid principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Construção da Interface Visual
        self.build_navigation_menu()
        self.build_main_frames()
        self.build_dashboard()
        self.build_gastos_screen()
        self.build_poupanca_screen()

    def build_navigation_menu(self):
        # Menu lateral esquerdo
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#ffffff", width=320)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)
        self.navigation_frame.grid_propagate(False)
        self.navigation_frame.grid_columnconfigure(0, weight=1)

        # Título/logo no menu lateral
        logo_container = ctk.CTkFrame(self.navigation_frame, fg_color="#8b5cf6", corner_radius=0)
        logo_container.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        logo_container.grid_columnconfigure(0, weight=1)
        self.logo_label = ctk.CTkLabel(
            logo_container,
            text="💰 BolsoUp",
            font=ctk.CTkFont(size=30, weight="bold", family="Segoe UI"),
            text_color="#ffffff",
            height=110
        )
        self.logo_label.grid(row=0, column=0, padx=25, pady=25, sticky="ew")

        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            self.navigation_frame,
            text="Controle suas finanças",
            font=ctk.CTkFont(size=15, family="Segoe UI"),
            text_color="#64748b"
        )
        subtitle_label.grid(row=1, column=0, padx=25, pady=(20, 35), sticky="w")

        # Botões de navegação
        self.nav_button_1 = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=14,
            height=55,
            border_spacing=18,
            text="📊 Dashboard",
            font=ctk.CTkFont(size=16, weight="bold", family="Segoe UI"),
            fg_color="#8b5cf6",
            text_color="#ffffff",
            hover_color="#7c3aed",
            anchor="w",
            command=lambda: self.show_frame("dashboard")
        )
        self.nav_button_1.grid(row=2, column=0, sticky="ew", padx=25, pady=10)

        self.nav_button_2 = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=14,
            height=55,
            border_spacing=18,
            text="💳 Gastos",
            font=ctk.CTkFont(size=16, weight="bold", family="Segoe UI"),
            fg_color="#f1f5f9",
            text_color="#475569",
            hover_color="#e2e8f0",
            anchor="w",
            command=lambda: self.show_frame("gastos")
        )
        self.nav_button_2.grid(row=3, column=0, sticky="ew", padx=25, pady=10)

        self.nav_button_3 = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=14,
            height=55,
            border_spacing=18,
            text="💰 Poupança",
            font=ctk.CTkFont(size=16, weight="bold", family="Segoe UI"),
            fg_color="#f1f5f9",
            text_color="#475569",
            hover_color="#e2e8f0",
            anchor="w",
            command=lambda: self.show_frame("poupanca")
        )
        self.nav_button_3.grid(row=4, column=0, sticky="ew", padx=25, pady=10)

    def build_main_frames(self):
        # Frame principal (conteúdo)
        self.dashboard_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#f1f5f9")
        self.gastos_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#f1f5f9")
        self.poupanca_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#f1f5f9")

    def build_dashboard(self):
        # Tela do Dashboard
        self.dashboard_frame.grid_columnconfigure(0, weight=1)
        self.dashboard_frame.grid_rowconfigure(3, weight=1)

        # Título
        title_label = ctk.CTkLabel(
            self.dashboard_frame,
            text="Olá! Bem-vindo ao seu painel financeiro",
            font=ctk.CTkFont(size=30, weight="bold", family="Segoe UI"),
            text_color="#1e293b"
        )
        title_label.grid(row=0, column=0, padx=10, pady=(0, 25), sticky="w")

        # Cards de saldo rápido
        saldos_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        saldos_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 20))
        saldos_frame.grid_columnconfigure((0, 1), weight=1)

        # Card Poupança
        card_poupanca = ctk.CTkFrame(saldos_frame, fg_color="#ffffff", corner_radius=16)
        card_poupanca.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(card_poupanca, text="💰 Saldo na Poupança", font=ctk.CTkFont(size=14, family="Segoe UI"), text_color="#64748b").grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        self.lbl_card_poupanca = ctk.CTkLabel(card_poupanca, text="R$ 0,00", font=ctk.CTkFont(size=28, weight="bold", family="Segoe UI"), text_color="#10b981")
        self.lbl_card_poupanca.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        # Card Gastos
        card_gastos = ctk.CTkFrame(saldos_frame, fg_color="#ffffff", corner_radius=16)
        card_gastos.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(card_gastos, text="💳 Saldo para Gastos", font=ctk.CTkFont(size=14, family="Segoe UI"), text_color="#64748b").grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        self.lbl_card_gastos = ctk.CTkLabel(card_gastos, text="R$ 0,00", font=ctk.CTkFont(size=28, weight="bold", family="Segoe UI"), text_color="#ef4444")
        self.lbl_card_gastos.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        # Card para adicionar saldo
        add_saldo_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="#ffffff", corner_radius=16)
        add_saldo_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 20))
        add_saldo_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        ctk.CTkLabel(
            add_saldo_frame,
            text="Adicionar Saldo Inicial",
            font=ctk.CTkFont(size=18, weight="bold", family="Segoe UI"),
            text_color="#1e293b"
        ).grid(row=0, column=0, columnspan=5, pady=(25, 20), padx=25, sticky="w")

        ctk.CTkLabel(add_saldo_frame, text="Valor para Poupança (R$):", font=ctk.CTkFont(size=13, family="Segoe UI"), text_color="#475569").grid(row=1, column=0, padx=15, pady=8, sticky="e")
        self.entry_sal_poupanca = ctk.CTkEntry(add_saldo_frame, placeholder_text="0,00", font=ctk.CTkFont(size=13, family="Segoe UI"), height=45, corner_radius=10, fg_color="#f8fafc", border_color="#e2e8f0")
        self.entry_sal_poupanca.grid(row=1, column=1, padx=15, pady=8, sticky="ew")

        ctk.CTkLabel(add_saldo_frame, text="Valor para Gastos (R$):", font=ctk.CTkFont(size=13, family="Segoe UI"), text_color="#475569").grid(row=1, column=2, padx=15, pady=8, sticky="e")
        self.entry_sal_gastos = ctk.CTkEntry(add_saldo_frame, placeholder_text="0,00", font=ctk.CTkFont(size=13, family="Segoe UI"), height=45, corner_radius=10, fg_color="#f8fafc", border_color="#e2e8f0")
        self.entry_sal_gastos.grid(row=1, column=3, padx=15, pady=8, sticky="ew")

        btn_add_saldo = ctk.CTkButton(
            add_saldo_frame,
            text="✅ Adicionar Saldo",
            font=ctk.CTkFont(size=14, weight="bold", family="Segoe UI"),
            height=45,
            corner_radius=10,
            fg_color="#8b5cf6",
            hover_color="#7c3aed",
            command=self.add_saldo
        )
        btn_add_saldo.grid(row=1, column=4, padx=15, pady=8, sticky="ew")

        # Frame para gráficos + mascote
        graphs_mascot_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        graphs_mascot_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        graphs_mascot_frame.grid_columnconfigure(0, weight=3)
        graphs_mascot_frame.grid_columnconfigure(1, weight=1)
        graphs_mascot_frame.grid_rowconfigure(0, weight=1)

        # Frame para os gráficos
        graphs_container = ctk.CTkFrame(graphs_mascot_frame, fg_color="#ffffff", corner_radius=16)
        graphs_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.graphs_frame = ctk.CTkFrame(graphs_container, fg_color="transparent")
        self.graphs_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Frame para o mascote
        mascot_frame = ctk.CTkFrame(graphs_mascot_frame, fg_color="#ffffff", corner_radius=16)
        mascot_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        mascot_frame.grid_rowconfigure(0, weight=1)
        mascot_frame.grid_columnconfigure(0, weight=1)

        if os.path.exists(IMAGE_PATH):
            img = Image.open(IMAGE_PATH)
            img.thumbnail((300, 600), Image.Resampling.LANCZOS)
            self.mascot_image = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)

            mascot_label = ctk.CTkLabel(mascot_frame, image=self.mascot_image, text="")
            mascot_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    def build_gastos_screen(self):
        # Tela de Gastos
        self.gastos_frame.grid_columnconfigure(0, weight=1)
        self.gastos_frame.grid_rowconfigure(3, weight=1)

        # Título
        title_label = ctk.CTkLabel(
            self.gastos_frame,
            text="💳 Carteira de Gastos",
            font=ctk.CTkFont(size=30, weight="bold", family="Segoe UI"),
            text_color="#1e293b"
        )
        title_label.grid(row=0, column=0, padx=10, pady=(0, 25), sticky="w")

        # Card para cadastrar gasto
        add_gasto_frame = ctk.CTkFrame(self.gastos_frame, fg_color="#ffffff", corner_radius=16)
        add_gasto_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 20))
        add_gasto_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        ctk.CTkLabel(
            add_gasto_frame,
            text="Registrar Novo Gasto",
            font=ctk.CTkFont(size=18, weight="bold", family="Segoe UI"),
            text_color="#1e293b"
        ).grid(row=0, column=0, columnspan=5, pady=(25, 20), padx=25, sticky="w")

        ctk.CTkLabel(add_gasto_frame, text="Categoria:", font=ctk.CTkFont(size=13, family="Segoe UI"), text_color="#475569").grid(row=1, column=0, padx=15, pady=8, sticky="e")
        self.combo_nome_gasto = ctk.CTkComboBox(add_gasto_frame, values=CATEGORIAS_GASTO, state="readonly", font=ctk.CTkFont(size=13, family="Segoe UI"), height=45, corner_radius=10, fg_color="#f8fafc", border_color="#e2e8f0")
        self.combo_nome_gasto.grid(row=1, column=1, padx=15, pady=8, sticky="ew")
        self.combo_nome_gasto.set(CATEGORIAS_GASTO[0])

        ctk.CTkLabel(add_gasto_frame, text="Descrição:", font=ctk.CTkFont(size=13, family="Segoe UI"), text_color="#475569").grid(row=1, column=2, padx=15, pady=8, sticky="e")
        self.entry_desc_gasto = ctk.CTkEntry(add_gasto_frame, placeholder_text="Ex: Almoço no shopping", font=ctk.CTkFont(size=13, family="Segoe UI"), height=45, corner_radius=10, fg_color="#f8fafc", border_color="#e2e8f0")
        self.entry_desc_gasto.grid(row=1, column=3, padx=15, pady=8, sticky="ew")

        ctk.CTkLabel(add_gasto_frame, text="Valor (R$):", font=ctk.CTkFont(size=13, family="Segoe UI"), text_color="#475569").grid(row=2, column=0, padx=15, pady=8, sticky="e")
        self.entry_valor_gasto = ctk.CTkEntry(add_gasto_frame, placeholder_text="0,00", font=ctk.CTkFont(size=13, family="Segoe UI"), height=45, corner_radius=10, fg_color="#f8fafc", border_color="#e2e8f0")
        self.entry_valor_gasto.grid(row=2, column=1, padx=15, pady=8, sticky="ew")

        btn_registrar = ctk.CTkButton(
            add_gasto_frame,
            text="💸 Registrar Gasto",
            font=ctk.CTkFont(size=14, weight="bold", family="Segoe UI"),
            height=45,
            corner_radius=10,
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self.add_new_gasto
        )
        btn_registrar.grid(row=2, column=2, columnspan=3, pady=8, padx=15, sticky="ew")

        # Lista de gastos
        list_container = ctk.CTkFrame(self.gastos_frame, fg_color="#ffffff", corner_radius=16)
        list_container.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        list_label = ctk.CTkLabel(
            list_container,
            text="Histórico de Gastos",
            font=ctk.CTkFont(size=18, weight="bold", family="Segoe UI"),
            text_color="#1e293b"
        )
        list_label.pack(pady=(20, 15), padx=25, anchor="w")

        self.tree_gastos = CTkTreeview(
            list_container,
            columns=("nome", "descricao", "valor", "data"),
            show="headings",
            height=10
        )
        self.tree_gastos.heading("nome", text="Categoria")
        self.tree_gastos.heading("descricao", text="Descrição")
        self.tree_gastos.heading("valor", text="Valor (R$)")
        self.tree_gastos.heading("data", text="Data")

        self.tree_gastos.column("nome", width=180, anchor="center")
        self.tree_gastos.column("descricao", width=450, anchor="w")
        self.tree_gastos.column("valor", width=150, anchor="center")
        self.tree_gastos.column("data", width=200, anchor="center")
        self.tree_gastos.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def build_poupanca_screen(self):
        # Tela da Poupança
        self.poupanca_frame.grid_columnconfigure(0, weight=1)
        self.poupanca_frame.grid_rowconfigure(2, weight=1)

        # Título
        title_label = ctk.CTkLabel(
            self.poupanca_frame,
            text="💰 Carteira de Poupança",
            font=ctk.CTkFont(size=30, weight="bold", family="Segoe UI"),
            text_color="#1e293b"
        )
        title_label.grid(row=0, column=0, padx=10, pady=(0, 25), sticky="w")

        # Lista de transferências
        list_container = ctk.CTkFrame(self.poupanca_frame, fg_color="#ffffff", corner_radius=16)
        list_container.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        list_label = ctk.CTkLabel(
            list_container,
            text="Histórico de Transferências",
            font=ctk.CTkFont(size=18, weight="bold", family="Segoe UI"),
            text_color="#1e293b"
        )
        list_label.pack(pady=(20, 15), padx=25, anchor="w")

        self.tree_historico = CTkTreeview(
            list_container,
            columns=("data", "valor"),
            show="headings",
            height=15
        )
        self.tree_historico.heading("data", text="Data")
        self.tree_historico.heading("valor", text="Valor (R$)")

        self.tree_historico.column("data", width=350, anchor="center")
        self.tree_historico.column("valor", width=250, anchor="center")
        self.tree_historico.pack(fill="both", expand=True, padx=20, pady=(0, 20))


    # Métodos VAZIOS
    ##São funcões vazias para resumir basicamente seria o designer.py só avisa ao Python:
    # "olha, o app vai ter uma ação de adicionar saldo", e o gui.py é quem diz como essa ação vai funcionar na prática!
    def show_frame(self, name):
        pass

    def add_saldo(self):
        pass

    def add_new_gasto(self):
        pass
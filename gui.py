import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import services
from models import Gasto
from designer import FinanceiroDesigner, CATEGORIAS_GASTO


class AppFinanceiro(FinanceiroDesigner):
    def __init__(self):
        super().__init__()

        # Inicializa a exibição no dashboard e atualiza todas as informações
        self.show_frame("dashboard")
        self.update_all_screens()

    def show_frame(self, name):
        # Mapeamento de botões e telas
        buttons = {
            "dashboard": self.nav_button_1,
            "gastos": self.nav_button_2,
            "poupanca": self.nav_button_3
        }
        frames = {
            "dashboard": self.dashboard_frame,
            "gastos": self.gastos_frame,
            "poupanca": self.poupanca_frame
        }

        # 1. Esconde TODOS os frames para evitar qualquer sobreposição
        for frame in frames.values():
            frame.grid_forget()

        # 2. Atualiza os destaques visuais dos botões do menu lateral
        for btn_name, button in buttons.items():
            if btn_name == name:
                button.configure(fg_color="#8b5cf6", text_color="#ffffff", hover_color="#7c3aed")
            else:
                button.configure(fg_color="#f1f5f9", text_color="#475569", hover_color="#e2e8f0")

        # 3. Exibe APENAS a tela selecionada
        frames[name].grid(row=0, column=1, sticky="nsew", padx=30, pady=30)

    def add_saldo(self):
        try:
            val_poup = float(self.entry_sal_poupanca.get().replace(',', '.') or 0)
            val_gas = float(self.entry_sal_gastos.get().replace(',', '.') or 0)

            # Validação para impedir valores zerados ou negativos
            if val_poup <= 0 and val_gas <= 0:
                messagebox.showwarning(
                    "Valor Inválido", 
                    "Informe um valor maior que zero em pelo menos uma das carteiras!"
                )
                return

            services.adicionar_salario(val_poup, val_gas)
            messagebox.showinfo("Sucesso!", "Saldo distribuído com sucesso!")
            self.entry_sal_poupanca.delete(0, ctk.END)
            self.entry_sal_gastos.delete(0, ctk.END)
            self.update_all_screens()
        except ValueError:
            messagebox.showerror("Ops!", "Digite valores numéricos válidos.")

    def update_graphs(self):
        # Limpa figuras anteriores do Matplotlib para economizar memória e evitar bugs
        plt.close('all')

        # Limpa o container de gráficos
        for widget in self.graphs_frame.winfo_children():
            widget.destroy()

        # Cria figura com 3 gráficos
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(11, 4.5))
        fig.patch.set_facecolor('#ffffff')

        # Gráfico 1 - Pizza (distribuição de gastos)
        gastos = services.obter_todos_gastos()
        if gastos:
            dados_grafico = {}
            for gasto in gastos:
                rotulo = gasto.descricao if gasto.descricao else gasto.nome
                dados_grafico[rotulo] = dados_grafico.get(rotulo, 0) + gasto.valor
            
            wedges, texts, autotexts = ax1.pie(
                dados_grafico.values(), 
                labels=dados_grafico.keys(), 
                autopct="%1.1f%%",
                startangle=90, 
                colors=["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4", "#84cc16"],
                textprops={"fontsize": 9, "family": "Segoe UI"},
                pctdistance=0.6,
                labeldistance=1.15
            )
            
            for text in texts:
                text.set_color("#1e293b")
                text.set_fontsize(9.5)
                
            for autotext in autotexts:
                autotext.set_color("white")
                autotext.set_weight("bold")
                autotext.set_fontsize(9)
                
            ax1.axis("equal")
            ax1.set_title("Distribuição de Gastos", fontsize=12, fontweight="bold", color="#1e293b", pad=15)
        else:
            ax1.text(0.5, 0.5, "Nenhum gasto\nregistrado", ha="center", va="center", fontsize=12, color="#64748b")
            ax1.axis("off")

        # Gráfico 2 - Barras (saldo das carteiras)
        carteira_poup = services.obter_carteira(1)
        carteira_gas = services.obter_carteira(2)
        bars = ax2.bar(
            ["Poupança", "Gastos"],
            [carteira_poup.saldo, carteira_gas.saldo],
            color=["#10b981", "#ef4444"],
            width=0.6,
            edgecolor='white',
            linewidth=2
        )
        ax2.bar_label(bars, padding=5, fontsize=11, fontweight="bold")
        ax2.set_title("Saldo por Carteira", fontsize=12, fontweight="bold", color="#1e293b", pad=15)
        ax2.tick_params(axis="both", labelsize=11)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.set_facecolor('#ffffff')

        # Gráfico 3 - Linha (gastos por dia)
        gastos_por_dia = services.obter_gastos_por_dia()
        if gastos_por_dia:
            dias = list(gastos_por_dia.keys())
            valores = list(gastos_por_dia.values())
            ax3.plot(dias, valores, marker='o', color="#ef4444", linewidth=3, markersize=8, markeredgecolor="white", markeredgewidth=2)
            ax3.set_title("Gastos por Dia", fontsize=12, fontweight="bold", color="#1e293b", pad=15)
            ax3.tick_params(axis="x", rotation=45, labelsize=9)
            ax3.tick_params(axis="y", labelsize=10)
            ax3.spines['top'].set_visible(False)
            ax3.spines['right'].set_visible(False)
            ax3.set_facecolor('#ffffff')
            ax3.grid(alpha=0.3, linestyle='--')
        else:
            ax3.text(0.5, 0.5, "Sem histórico\nainda", ha="center", va="center", fontsize=12, color="#64748b")
            ax3.axis("off")

        fig.tight_layout()

        # Renderiza o canvas dos gráficos
        canvas = FigureCanvasTkAgg(fig, master=self.graphs_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def add_new_gasto(self):
        nome = self.combo_nome_gasto.get().strip()
        desc = self.entry_desc_gasto.get().strip()

        if not nome:
            messagebox.showwarning("Aviso!", "Selecione uma categoria para o gasto.")
            return

        try:
            valor = float(self.entry_valor_gasto.get().replace(',', '.'))
            if valor <= 0:
                messagebox.showerror("Ops!", "O valor deve ser maior que zero.")
                return
        except ValueError:
            messagebox.showerror("Ops!", "Digite um valor numérico válido.")
            return

        carteira_gastos = services.obter_carteira(2)

        if valor > carteira_gastos.saldo:
            resposta = messagebox.askyesno(
                "Saldo Insuficiente",
                "Você não tem saldo suficiente. Deseja transferir da poupança?"
            )
            if resposta:
                self.open_transfer_window()
        else:
            novo_gasto = Gasto(nome=nome, descricao=desc, valor=valor)
            services.registrar_gasto(novo_gasto)
            messagebox.showinfo("Sucesso!", "Gasto registrado!")
            self.combo_nome_gasto.set(CATEGORIAS_GASTO[0])
            self.entry_desc_gasto.delete(0, ctk.END)
            self.entry_valor_gasto.delete(0, ctk.END)
            self.update_all_screens()

    def open_transfer_window(self):
        # Modal Pop-up de transferência
        tela_transf = ctk.CTkToplevel(self)
        tela_transf.title("💸 Transferência de Emergência")
        tela_transf.geometry("600x400")
        tela_transf.transient(self)
        tela_transf.grab_set()
        tela_transf.configure(fg_color="#f1f5f9")

        frame_inner = ctk.CTkFrame(tela_transf, fg_color="#ffffff", corner_radius=16)
        frame_inner.pack(padx=30, pady=30, fill="both", expand=True)

        ctk.CTkLabel(
            frame_inner,
            text="Resgate da Poupança",
            font=ctk.CTkFont(size=24, weight="bold", family="Segoe UI"),
            text_color="#1e293b"
        ).pack(pady=(30, 15))

        carteira_poup = services.obter_carteira(1)
        ctk.CTkLabel(
            frame_inner,
            text=f"Saldo na Poupança: R$ {carteira_poup.saldo:.2f}".replace('.', ','),
            font=ctk.CTkFont(size=16, family="Segoe UI"),
            text_color="#10b981"
        ).pack(pady=5)

        ctk.CTkLabel(frame_inner, text="Quanto transferir para Gastos? (R$):", font=ctk.CTkFont(size=14, family="Segoe UI"), text_color="#475569").pack(pady=(30, 10))
        entry_valor_transf = ctk.CTkEntry(frame_inner, placeholder_text="0,00", font=ctk.CTkFont(size=14, family="Segoe UI"), height=50, corner_radius=10, fg_color="#f8fafc", border_color="#e2e8f0", width=300)
        entry_valor_transf.pack(pady=5)

        def confirmar():
            try:
                valor_transf = float(entry_valor_transf.get().replace(',', '.'))
                if valor_transf > carteira_poup.saldo:
                    messagebox.showerror("Ops!", "Você não tem esse valor na poupança!")
                    return
                if valor_transf <= 0:
                    messagebox.showerror("Ops!", "Digite um valor maior que zero.")
                    return

                services.realizar_transferencia_emergencia(valor_transf)
                messagebox.showinfo("Sucesso!", "Valor transferido!")
                tela_transf.destroy()
                self.update_all_screens()
            except ValueError:
                messagebox.showerror("Ops!", "Valor inválido!")

        btn_confirmar = ctk.CTkButton(
            frame_inner,
            text="✅ Confirmar Transferência",
            font=ctk.CTkFont(size=15, weight="bold", family="Segoe UI"),
            height=50,
            corner_radius=10,
            fg_color="#10b981",
            hover_color="#059669",
            command=confirmar
        )
        btn_confirmar.pack(pady=25)

    def update_all_screens(self):
        # Atualiza saldos dos cards
        carteira_poup = services.obter_carteira(1)
        carteira_gas = services.obter_carteira(2)

        self.lbl_card_poupanca.configure(text=f"R$ {carteira_poup.saldo:.2f}".replace('.', ','))
        self.lbl_card_gastos.configure(text=f"R$ {carteira_gas.saldo:.2f}".replace('.', ','))

        # Atualiza gráficos
        self.update_graphs()

        # Atualiza histórico de transferências
        for row in self.tree_historico.get_children():
            self.tree_historico.delete(row)

        historico = services.obter_historico_transferencias()
        for transf in historico:
            self.tree_historico.insert("", "end", values=(transf.data[:16], f"R$ {transf.valor:.2f}".replace('.', ',')))

        # Atualiza lista de gastos
        for row in self.tree_gastos.get_children():
            self.tree_gastos.delete(row)

        gastos = services.obter_todos_gastos()
        for gasto in gastos:
            data_exibida = gasto.data[:16] if gasto.data else ""
            self.tree_gastos.insert("", "end", values=(gasto.nome, gasto.descricao, f"R$ {gasto.valor:.2f}".replace('.', ','), data_exibida))


if __name__ == "__main__":
    app = AppFinanceiro()
    app.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox
from control import contas_receber_controller

class ContasReceberView(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Contas a Receber - Orbis Gestão")
        self.geometry("850x500")

        # Frame principal
        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Filtros
        filtros = tk.Frame(frame)
        filtros.pack(fill="x")

        tk.Label(filtros, text="Filtrar por Status:", font=("Arial", 11)).pack(side="left", padx=(0, 5))

        self.combo_status = ttk.Combobox(filtros, values=["Todos", "pendente", "pago"], state="readonly", width=15)
        self.combo_status.current(0)
        self.combo_status.pack(side="left")
        self.combo_status.bind("<<ComboboxSelected>>", lambda e: self.carregar_dados())

        self.botao_pagar = tk.Button(filtros, text="💵 Registrar Pagamento", command=self.registrar_pagamento)
        self.botao_pagar.pack(side="right")

        # Tabela
        self.tabela = ttk.Treeview(frame, columns=("ID", "Venda", "Cliente", "Valor", "Vencimento", "Status"),
                                   show="headings", height=15)
        for col in self.tabela["columns"]:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, anchor="center")

        self.tabela.pack(fill="both", expand=True, pady=10)

        self.carregar_dados()

    def carregar_dados(self):
        status = self.combo_status.get()
        if status == "Todos":
            contas = contas_receber_controller.listar_contas()
        else:
            contas = contas_receber_controller.listar_contas(status=status)

        self.tabela.delete(*self.tabela.get_children())

        for conta in contas:
            self.tabela.insert("", "end", values=(
                conta[0],  # ID
                conta[1],  # Venda
                conta[2],  # Cliente
                f"R$ {conta[3]:.2f}",  # Valor
                conta[4],  # Vencimento
                conta[5]   # Status
            ))

    def registrar_pagamento(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma conta para registrar pagamento.")
            return

        item = self.tabela.item(selecionado)
        conta_id = int(item["values"][0])
        status_atual = item["values"][5]

        if status_atual == "pago":
            messagebox.showinfo("Info", "Essa conta já está marcada como paga.")
            return

        confirmar = messagebox.askyesno("Confirmar", f"Marcar conta ID {conta_id} como paga?")
        if confirmar:
            contas_receber_controller.registrar_pagamento(conta_id)
            messagebox.showinfo("Sucesso", f"Conta {conta_id} registrada como paga.")
            self.carregar_dados()

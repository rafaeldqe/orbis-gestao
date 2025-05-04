import tkinter as tk

class ResumoVendaView(tk.Toplevel):
    def __init__(self, master, venda_id, total, forma_pagamento, itens):
        super().__init__(master)
        self.title("Resumo da Venda")
        self.geometry("600x500")

        self.master = master  # Armazena a referência do pai

        texto = tk.Text(self, font=("Courier", 10))
        texto.pack(fill="both", expand=True)

        conteudo = f"""
        ORBIS GESTÃO - CUPOM SIMPLES
        -----------------------------
        Venda ID: {venda_id}
        Forma de Pagamento: {forma_pagamento}
        -----------------------------
        Itens:
        """

        for item in itens:
            conteudo += f"{item['nome'][:25]:<25} {item['quantidade']} x R${item['preco_unitario']:.2f} = R${item['subtotal']:.2f}\n"

        conteudo += "-----------------------------\n"
        conteudo += f"TOTAL: R${total:.2f}\n"
        conteudo += "-----------------------------\n"
        conteudo += "Obrigado pela preferência!\n"

        texto.insert(tk.END, conteudo)
        texto.config(state="disabled")

        botoes = tk.Frame(self)
        botoes.pack(pady=10)

        tk.Button(botoes, text="Fechar", command=self.destroy).pack(side="left", padx=10)

        tk.Button(botoes, text="🔙 Voltar ao Dashboard", command=self.voltar_dashboard).pack(side="left", padx=10)

    def voltar_dashboard(self):
        self.destroy()
        self.master.deiconify()  # Reexibe a janela principal (Dashboard)

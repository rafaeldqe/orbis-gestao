import tkinter as tk
from tkinter import ttk
import control.produtos_controller as produtos_controller

class SelecionarProdutoView(tk.Toplevel):
    def __init__(self, master, callback):
        super().__init__(master)
        self.title("Selecionar Produto")
        self.geometry("800x500")
        self.callback = callback

        tk.Label(self, text="Buscar produto:").pack(pady=5)
        self.entrada_busca = tk.Entry(self, width=40)
        self.entrada_busca.pack()
        self.entrada_busca.bind("<KeyRelease>", self.filtrar_produtos)

        colunas = ("ID", "Nome", "Preço", "Estoque")
        self.tabela = ttk.Treeview(self, columns=colunas, show="headings")
        for col in colunas:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, anchor="center")
        self.tabela.pack(fill="both", expand=True, pady=10)
        self.tabela.bind("<Double-1>", self.selecionar_produto)

        self.carregar_produtos()

    def carregar_produtos(self):
        self.todos_produtos = produtos_controller.listar_produtos()
        self.atualizar_tabela(self.todos_produtos)

    def atualizar_tabela(self, produtos):
        self.tabela.delete(*self.tabela.get_children())
        for p in produtos:
            self.tabela.insert("", tk.END, values=(p[0], p[1], f"R$ {p[4]:.2f}", p[5]))

    def filtrar_produtos(self, event):
        termo = self.entrada_busca.get().lower()
        filtrados = [p for p in self.todos_produtos if termo in p[1].lower() or termo in str(p[0])]
        self.atualizar_tabela(filtrados)

    def selecionar_produto(self, event):
        selecionado = self.tabela.selection()
        if not selecionado:
            return
        item = self.tabela.item(selecionado[0])
        produto_id = int(item['values'][0])
        produto = next((p for p in self.todos_produtos if p[0] == produto_id), None)
        if produto:
            self.callback(produto)
            self.destroy()
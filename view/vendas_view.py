import tkinter as tk
from tkinter import ttk, messagebox
import control.vendas_controller as controller
import control.produtos_controller as produtos_controller
import control.clientes_pf_controller as clientes_pf_controller
import control.clientes_pj_controller as clientes_pj_controller
import control.contas_receber_controller as contas_receber_controller
import datetime
from view.selecionar_produto_view import SelecionarProdutoView
from util.dav import gerar_dav_pdf

class VendasView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Ponto de Venda - Orbis Gestão")
        self.geometry("1024x720")
        self.itens = []
        self.produto_selecionado = None
        self.cliente_id = None
        self.tipo_cliente = None
        self.nome_cliente = "Consumidor Final"

        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        cliente_frame = tk.Frame(frame)
        cliente_frame.pack(anchor="w")
        tk.Button(cliente_frame, text="👤 Selecionar Cliente", command=self.dialogo_tipo_cliente).pack(side="left")
        self.label_cliente = tk.Label(cliente_frame, text="Cliente: Consumidor Final", font=("Arial", 10))
        self.label_cliente.pack(side="left", padx=10)

        topo = tk.Frame(frame)
        topo.pack(anchor="w")
        tk.Label(topo, text="Produto:").pack(side="left")
        self.entrada_produto_nome = tk.Entry(topo, width=40)
        self.entrada_produto_nome.pack(side="left", padx=5)
        tk.Button(topo, text="🔍 Buscar", command=self.abrir_tela_busca_produto).pack(side="left")
        tk.Label(topo, text="Qtd:").pack(side="left", padx=10)
        self.entrada_quantidade = tk.Entry(topo, width=5)
        self.entrada_quantidade.insert(0, "1")
        self.entrada_quantidade.pack(side="left")
        tk.Button(topo, text="➕ Adicionar", command=self.adicionar_item).pack(side="left", padx=5)

        colunas = ("Produto", "Qtd", "Unitário", "Subtotal")
        self.tabela = ttk.Treeview(frame, columns=colunas, show="headings", height=15)
        for col in colunas:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=150, anchor="center")
        self.tabela.pack(pady=10)
        self.tabela.bind("<Delete>", self.remover_item)

        rodape = tk.Frame(frame)
        rodape.pack(anchor="w", pady=10)
        tk.Label(rodape, text="Desconto (R$):").grid(row=0, column=0, sticky="w")
        self.desconto_entry = tk.Entry(rodape, width=10)
        self.desconto_entry.insert(0, "0.00")
        self.desconto_entry.grid(row=0, column=1, sticky="w", padx=5)
        self.desconto_entry.bind("<KeyRelease>", lambda e: self.atualizar_total())
        tk.Label(rodape, text="Forma de Pagamento:").grid(row=1, column=0, sticky="w")
        self.forma_pagamento = ttk.Combobox(rodape, values=["dinheiro", "pix", "crédito", "débito", "boleto", "carteira", "fiado"], width=15)
        self.forma_pagamento.set("dinheiro")
        self.forma_pagamento.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(rodape, text="Total:", font=("Arial", 14, "bold")).grid(row=0, column=2, sticky="e", padx=10)
        self.total_var = tk.StringVar(value="0.00")
        tk.Label(rodape, textvariable=self.total_var, font=("Arial", 16, "bold"), fg="green").grid(row=0, column=3, sticky="w")

        tk.Button(frame, text="✅ Finalizar Venda", font=("Arial", 12, "bold"), bg="#4caf50", fg="white",
                  command=self.finalizar_venda, width=25).pack(pady=20)

    def dialogo_tipo_cliente(self):
        dialog = tk.Toplevel(self)
        dialog.title("Tipo de Cliente")
        dialog.geometry("300x150")
        tk.Label(dialog, text="Selecione o tipo de cliente:", font=("Arial", 12)).pack(pady=10)
        tk.Button(dialog, text="Pessoa Física", width=20, command=lambda: (dialog.destroy(), self.selecionar_cliente_pf())).pack(pady=5)
        tk.Button(dialog, text="Pessoa Jurídica", width=20, command=lambda: (dialog.destroy(), self.selecionar_cliente_pj())).pack(pady=5)

    def selecionar_cliente_pf(self):
        clientes = clientes_pf_controller.listar_clientes()
        if not clientes:
            messagebox.showinfo("Clientes", "Nenhum cliente pessoa física cadastrado.", parent=self)
            return
        self._abrir_lista_clientes(clientes, tipo="pf")

    def selecionar_cliente_pj(self):
        clientes = clientes_pj_controller.listar_clientes()
        if not clientes:
            messagebox.showinfo("Clientes", "Nenhum cliente pessoa jurídica cadastrado.", parent=self)
            return
        self._abrir_lista_clientes(clientes, tipo="pj")

    def _abrir_lista_clientes(self, clientes, tipo):
        selecao = tk.Toplevel(self)
        selecao.title("Selecionar Cliente")
        selecao.geometry("700x400")

        tabela = ttk.Treeview(selecao, columns=("ID", "Nome", "Doc"), show="headings", height=10)
        tabela.pack(fill="both", expand=True)

        for col in ("ID", "Nome", "Doc"):
            tabela.heading(col, text=col)
            tabela.column(col, width=200, anchor="center")

        for c in clientes:
            doc = c[2] if len(c) > 2 else ""
            tabela.insert("", "end", values=(c[0], c[1], doc))

        def confirmar():
            selecionado = tabela.selection()
            if not selecionado:
                messagebox.showwarning("Seleção", "Selecione um cliente.", parent=selecao)
                return
            dados = tabela.item(selecionado[0])["values"]
            self.cliente_id = dados[0]
            self.tipo_cliente = tipo
            self.nome_cliente = dados[1]
            self.label_cliente.config(text=f"Cliente: {self.nome_cliente}")
            selecao.destroy()

        tk.Button(selecao, text="Selecionar", command=confirmar).pack(pady=10)

    def abrir_tela_busca_produto(self):
        SelecionarProdutoView(self, self.receber_produto_selecionado)

    def receber_produto_selecionado(self, produto):
        self.produto_selecionado = produto
        self.entrada_produto_nome.delete(0, tk.END)
        self.entrada_produto_nome.insert(0, produto[1])

    def adicionar_item(self):
        if not self.produto_selecionado:
            messagebox.showwarning("Produto", "Selecione um produto primeiro.", parent=self)
            return
        try:
            qtd = int(self.entrada_quantidade.get())
            produto = produtos_controller.buscar_produto_por_id(self.produto_selecionado[0])
            estoque_atual = produto[5]
            if qtd > estoque_atual:
                messagebox.showwarning("Estoque insuficiente", f"Quantidade solicitada ({qtd}) excede o estoque atual ({estoque_atual}).", parent=self)
                return
            preco = produto[4]
            subtotal = qtd * preco
            item = {
                'produto_id': produto[0],
                'nome': produto[1],
                'quantidade': qtd,
                'preco_unitario': preco,
                'subtotal': subtotal
            }
            self.itens.append(item)
            self.tabela.insert('', 'end', values=(item['nome'], item['quantidade'], f"{preco:.2f}", f"{subtotal:.2f}"))
            self.atualizar_total()
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.", parent=self)

    def remover_item(self, event):
        selecionado = self.tabela.selection()
        if not selecionado:
            return
        index = self.tabela.index(selecionado[0])
        self.tabela.delete(selecionado)
        del self.itens[index]
        self.atualizar_total()

    def atualizar_total(self):
        total = sum(i['subtotal'] for i in self.itens)
        try:
            desconto = float(self.desconto_entry.get())
        except ValueError:
            desconto = 0
        total -= desconto
        if total < 0:
            total = 0
        self.total_var.set(f"R$ {total:.2f}")

    def finalizar_venda(self):
        if not self.itens:
            messagebox.showwarning("Carrinho vazio", "Adicione produtos antes de finalizar.", parent=self)
            return

        data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total = float(self.total_var.get().replace("R$", "").strip())
        try:
            desconto = float(self.desconto_entry.get())
        except:
            desconto = 0
        forma = self.forma_pagamento.get().lower()

        venda_id = controller.salvar_venda(
            data,
            self.cliente_id,
            self.tipo_cliente,
            total,
            desconto,
            forma,
            "",
            operador="admin"
        )

        for item in self.itens:
            controller.salvar_item_venda(
                venda_id,
                item['produto_id'],
                item['quantidade'],
                item['preco_unitario'],
                item['subtotal']
            )
            produtos_controller.baixar_estoque(item['produto_id'], item['quantidade'])

        formas_a_prazo = ["boleto", "carteira", "fiado"]
        if self.cliente_id and forma in formas_a_prazo:
            vencimento = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
            contas_receber_controller.criar_conta_receber(
                venda_id=venda_id,
                cliente_id=self.cliente_id,
                valor_total=total,
                vencimento=vencimento,
                forma_pagamento=forma
            )

        self.withdraw()
        gerar_dav_pdf(venda_id, self.itens, total, desconto, forma, self.nome_cliente)
        messagebox.showinfo("Venda finalizada", "Venda registrada com sucesso!", parent=self)
        self.destroy()

import tkinter as tk
from tkinter import messagebox, filedialog
import control.produtos_controller as controller
from view.movimentacao_estoque_view import MovimentacaoEstoqueView
from view.movimentacoes_historico_view import HistoricoMovimentacoesView
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class ProdutosView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Cadastro de Produtos")
        self.state('zoomed')
        self.produto_selecionado_id = None

        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Campos de cadastro
        tk.Label(frame, text="Nome do Produto:").grid(row=0, column=0, sticky="w")
        self.nome_entry = tk.Entry(frame, width=50)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame, text="Descrição:").grid(row=1, column=0, sticky="w")
        self.descricao_entry = tk.Entry(frame, width=50)
        self.descricao_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame, text="Preço de Custo:").grid(row=2, column=0, sticky="w")
        self.preco_custo_entry = tk.Entry(frame, width=20)
        self.preco_custo_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        tk.Label(frame, text="Preço de Venda:").grid(row=3, column=0, sticky="w")
        self.preco_entry = tk.Entry(frame, width=20)
        self.preco_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        tk.Label(frame, text="Quantidade:").grid(row=4, column=0, sticky="w")
        self.quantidade_entry = tk.Entry(frame, width=20)
        self.quantidade_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        tk.Label(frame, text="Unidade:").grid(row=5, column=0, sticky="w")
        self.unidade_entry = tk.Entry(frame, width=10)
        self.unidade_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        tk.Label(frame, text="Estoque Mínimo:").grid(row=6, column=0, sticky="w")
        self.estoque_minimo_entry = tk.Entry(frame, width=10)
        self.estoque_minimo_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        # Botões principais
        botoes_frame = tk.Frame(frame)
        botoes_frame.grid(row=7, column=1, pady=10, sticky="w")

        tk.Button(botoes_frame, text="📂 Salvar", command=self.salvar_produto, width=15).pack(side="left", padx=5)
        tk.Button(botoes_frame, text="🔄 Limpar", command=self.limpar_campos, width=15).pack(side="left", padx=5)
        tk.Button(botoes_frame, text="↩ Voltar", command=self.voltar, width=15).pack(side="left", padx=5)

        # Filtro
        filtro_frame = tk.Frame(frame)
        filtro_frame.grid(row=8, column=0, columnspan=2, pady=10, sticky="w")

        tk.Label(filtro_frame, text="Buscar:").pack(side="left")
        self.filtro_entry = tk.Entry(filtro_frame, width=30)
        self.filtro_entry.pack(side="left", padx=5)
        tk.Button(filtro_frame, text="🔍 Buscar", command=self.aplicar_filtro).pack(side="left", padx=5)

        # Tabela
        self.tabela = tk.Listbox(frame, width=120)
        self.tabela.grid(row=9, column=0, columnspan=2, pady=10)
        self.tabela.bind('<<ListboxSelect>>', self.carregar_produto)

        # Botões de exportação e movimentação
        export_frame = tk.Frame(frame)
        export_frame.grid(row=10, column=0, columnspan=2, pady=10)

        tk.Button(export_frame, text="⬇ Exportar Excel", command=self.exportar_excel).pack(side="left", padx=10)
        tk.Button(export_frame, text="⬇ Exportar PDF", command=self.exportar_pdf).pack(side="left", padx=10)
        tk.Button(export_frame, text="📦 Movimentar Estoque", command=self.abrir_movimentacao_estoque).pack(side="left", padx=10)
        tk.Button(export_frame, text="🔁 Histórico", command=self.abrir_historico_movimentacao).pack(side="left", padx=10)

        self.atualizar_tabela()

    def abrir_movimentacao_estoque(self):
        produto_id = self.get_produto_selecionado_id()
        if produto_id:
            MovimentacaoEstoqueView(self, produto_id=produto_id, atualizar_callback=self.atualizar_tabela)

    def abrir_historico_movimentacao(self):
        produto_id = self.get_produto_selecionado_id()
        if produto_id:
            HistoricoMovimentacoesView(self, produto_id=produto_id)

    def get_produto_selecionado_id(self):
        if self.tabela.curselection():
            index = self.tabela.curselection()[0]
            texto = self.tabela.get(index)
            try:
                return int(texto.split('|')[0].split(':')[1].strip())
            except:
                pass
        messagebox.showwarning("Aviso", "Selecione um produto primeiro.", parent=self)
        return None

    def salvar_produto(self):
        try:
            nome = self.nome_entry.get()
            descricao = self.descricao_entry.get()
            preco_custo = float(self.preco_custo_entry.get())
            preco = float(self.preco_entry.get())
            quantidade = int(self.quantidade_entry.get())
            unidade = self.unidade_entry.get()
            estoque_minimo = int(self.estoque_minimo_entry.get())

            if not nome or not preco:
                messagebox.showwarning("Aviso", "Preencha pelo menos nome e preço.", parent=self)
                return

            if self.produto_selecionado_id:
                controller.atualizar_produto(self.produto_selecionado_id, nome, descricao, preco_custo, preco, quantidade, unidade, estoque_minimo)
                messagebox.showinfo("Atualizado", "Produto atualizado com sucesso!", parent=self)
            else:
                controller.salvar_produto(nome, descricao, preco_custo, preco, quantidade, unidade, estoque_minimo)
                messagebox.showinfo("Salvo", "Produto salvo com sucesso!", parent=self)

            self.limpar_campos()
            self.atualizar_tabela()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}", parent=self)

    def carregar_produto(self, event):
        if not self.tabela.curselection():
            return
        index = self.tabela.curselection()[0]
        texto = self.tabela.get(index)
        try:
            produto_id = int(texto.split('|')[0].split(':')[1].strip())
            produto = controller.buscar_produto_por_id(produto_id)
            if produto:
                self.produto_selecionado_id = produto[0]
                self.nome_entry.delete(0, tk.END)
                self.nome_entry.insert(0, produto[1])
                self.descricao_entry.delete(0, tk.END)
                self.descricao_entry.insert(0, produto[2])
                self.preco_custo_entry.delete(0, tk.END)
                self.preco_custo_entry.insert(0, produto[3])
                self.preco_entry.delete(0, tk.END)
                self.preco_entry.insert(0, produto[4])
                self.quantidade_entry.delete(0, tk.END)
                self.quantidade_entry.insert(0, produto[5])
                self.unidade_entry.delete(0, tk.END)
                self.unidade_entry.insert(0, produto[6])
                self.estoque_minimo_entry.delete(0, tk.END)
                self.estoque_minimo_entry.insert(0, produto[7])
        except Exception as e:
            print(f"[ERRO ao carregar produto] {e}")

    def atualizar_tabela(self, filtro=None):
        self.tabela.delete(0, tk.END)
        produtos = controller.listar_produtos()
        for prod in produtos:
            texto = f"ID: {prod[0]} | Nome: {prod[1]} | Venda: {prod[4]} | Qtd: {prod[5]} | Unidade: {prod[6]} | Min: {prod[7]}"
            if not filtro or filtro.lower() in texto.lower():
                self.tabela.insert(tk.END, texto)

    def aplicar_filtro(self):
        filtro = self.filtro_entry.get().strip()
        self.atualizar_tabela(filtro)

    def exportar_excel(self):
        produtos = controller.listar_produtos()
        if not produtos:
            messagebox.showwarning("Aviso", "Nenhum produto para exportar.", parent=self)
            return

        caminho = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Arquivo CSV", "*.csv")])
        if not caminho:
            return

        try:
            with open(caminho, mode='w', newline='', encoding='utf-8') as arquivo:
                writer = csv.writer(arquivo)
                writer.writerow(["ID", "Nome", "Descrição", "Preço Custo", "Preço Venda", "Quantidade", "Unidade", "Estoque Mínimo"])
                for p in produtos:
                    writer.writerow(p)
            messagebox.showinfo("Sucesso", f"Arquivo exportado para {caminho}", parent=self)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar: {e}", parent=self)

    def exportar_pdf(self):
        produtos = controller.listar_produtos()
        if not produtos:
            messagebox.showwarning("Aviso", "Nenhum produto para exportar.", parent=self)
            return

        caminho = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Arquivo PDF", "*.pdf")])
        if not caminho:
            return

        try:
            c = canvas.Canvas(caminho, pagesize=letter)
            c.setFont("Helvetica", 10)
            c.drawString(50, 750, "Relatório de Produtos - Orbis Gestão")
            y = 720
            for p in produtos:
                texto = f"ID: {p[0]} | Nome: {p[1]} | Venda: {p[4]} | Qtd: {p[5]} | Unidade: {p[6]} | Min: {p[7]}"
                c.drawString(50, y, texto)
                y -= 15
                if y < 50:
                    c.showPage()
                    c.setFont("Helvetica", 10)
                    y = 750
            c.save()
            messagebox.showinfo("Sucesso", f"PDF exportado para {caminho}", parent=self)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar PDF: {e}", parent=self)

    def limpar_campos(self):
        self.produto_selecionado_id = None
        self.nome_entry.delete(0, tk.END)
        self.descricao_entry.delete(0, tk.END)
        self.preco_custo_entry.delete(0, tk.END)
        self.preco_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)
        self.unidade_entry.delete(0, tk.END)
        self.estoque_minimo_entry.delete(0, tk.END)

    def voltar(self):
        self.destroy()

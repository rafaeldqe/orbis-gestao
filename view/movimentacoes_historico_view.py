import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import control.movimentacoes_controller as controller
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class HistoricoMovimentacoesView(tk.Toplevel):
    def __init__(self, master, produto_id=None):
        super().__init__(master)
        self.title("Histórico de Movimentações")
        self.geometry("900x500")
        self.produto_id = produto_id

        filtro_frame = tk.Frame(self, padx=10, pady=10)
        filtro_frame.pack(fill="x")

        tk.Label(filtro_frame, text="Produto (Nome ou ID):").grid(row=0, column=0, sticky="w")
        self.produto_entry = tk.Entry(filtro_frame, width=30)
        self.produto_entry.grid(row=0, column=1, padx=5)

        tk.Label(filtro_frame, text="Tipo:").grid(row=0, column=2, sticky="w")
        self.tipo_combobox = ttk.Combobox(filtro_frame, values=["", "entrada", "saida"], width=10)
        self.tipo_combobox.grid(row=0, column=3, padx=5)

        tk.Button(filtro_frame, text="🔍 Buscar", command=self.aplicar_filtro).grid(row=0, column=4, padx=5)

        self.tree = ttk.Treeview(self, columns=("data", "produto", "tipo", "quantidade", "observacao"), show="headings")
        self.tree.heading("data", text="Data")
        self.tree.heading("produto", text="Produto")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("quantidade", text="Quantidade")
        self.tree.heading("observacao", text="Observação")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        botoes_frame = tk.Frame(self, pady=10)
        botoes_frame.pack()

        tk.Button(botoes_frame, text="⬇ Exportar Excel", command=self.exportar_excel).pack(side="left", padx=5)
        tk.Button(botoes_frame, text="⬇ Exportar PDF", command=self.exportar_pdf).pack(side="left", padx=5)
        tk.Button(botoes_frame, text="Fechar", command=self.destroy).pack(side="left", padx=5)

        self.carregar_movimentacoes()

    def carregar_movimentacoes(self):
        self.tree.delete(*self.tree.get_children())
        if self.produto_id:
            resultados = controller.filtrar_movimentacoes_por_id(self.produto_id)
        else:
            resultados = controller.listar_movimentacoes()
        for mov in resultados:
            self.tree.insert("", tk.END, values=mov)

    def aplicar_filtro(self):
        nome_ou_id = self.produto_entry.get().strip()
        tipo = self.tipo_combobox.get().strip()
        resultados = controller.filtrar_movimentacoes(nome_ou_id, tipo)

        self.tree.delete(*self.tree.get_children())
        for mov in resultados:
            self.tree.insert("", tk.END, values=mov)

    def exportar_excel(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Arquivo CSV", "*.csv")])
        if not caminho:
            return
        try:
            with open(caminho, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Data", "Produto", "Tipo", "Quantidade", "Observação"])
                for row in self.tree.get_children():
                    writer.writerow(self.tree.item(row)['values'])
            messagebox.showinfo("Sucesso", f"Arquivo salvo em {caminho}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar: {e}")

    def exportar_pdf(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Arquivo PDF", "*.pdf")])
        if not caminho:
            return
        try:
            c = canvas.Canvas(caminho, pagesize=letter)
            c.setFont("Helvetica", 10)
            c.drawString(50, 750, "Histórico de Movimentações")
            y = 720
            for row in self.tree.get_children():
                dados = self.tree.item(row)['values']
                texto = f"Data: {dados[0]} | Produto: {dados[1]} | Tipo: {dados[2]} | Qtd: {dados[3]} | Obs: {dados[4]}"
                c.drawString(50, y, texto)
                y -= 15
                if y < 50:
                    c.showPage()
                    c.setFont("Helvetica", 10)
                    y = 750
            c.save()
            messagebox.showinfo("Sucesso", f"PDF salvo em {caminho}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar PDF: {e}")
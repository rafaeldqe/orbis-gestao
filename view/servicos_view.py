import tkinter as tk
from tkinter import messagebox, filedialog
import control.servicos_controller as controller
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class ServicosView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Cadastro de Serviços")
        self.geometry("700x600")
        self.servico_selecionado_id = None

        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Nome do Serviço:").grid(row=0, column=0, sticky="w")
        self.nome_entry = tk.Entry(frame, width=50)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame, text="Descrição:").grid(row=1, column=0, sticky="w")
        self.descricao_entry = tk.Entry(frame, width=50)
        self.descricao_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame, text="Valor (R$):").grid(row=2, column=0, sticky="w")
        self.valor_entry = tk.Entry(frame, width=20)
        self.valor_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        botoes_frame = tk.Frame(frame)
        botoes_frame.grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(botoes_frame, text="💾 Salvar", command=self.salvar_servico, width=15).pack(side="left", padx=5)
        tk.Button(botoes_frame, text="🔄 Limpar", command=self.limpar_campos, width=15).pack(side="left", padx=5)
        tk.Button(botoes_frame, text="↩ Voltar", command=self.destroy, width=15).pack(side="left", padx=5)

        filtro_frame = tk.Frame(frame)
        filtro_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky="w")

        tk.Label(filtro_frame, text="Filtro (nome ou valor):").pack(side="left")
        self.filtro_entry = tk.Entry(filtro_frame, width=30)
        self.filtro_entry.pack(side="left", padx=5)
        tk.Button(filtro_frame, text="🔍 Buscar", command=self.aplicar_filtro).pack(side="left")

        self.tabela = tk.Listbox(frame, width=100)
        self.tabela.grid(row=5, column=0, columnspan=2, pady=10)
        self.tabela.bind('<<ListboxSelect>>', self.carregar_servico)

        export_frame = tk.Frame(frame)
        export_frame.grid(row=6, column=0, columnspan=2, pady=10)

        tk.Button(export_frame, text="⬇ Exportar Excel", command=self.exportar_excel).pack(side="left", padx=10)
        tk.Button(export_frame, text="⬇ Exportar PDF", command=self.exportar_pdf).pack(side="left", padx=10)

        self.atualizar_tabela()

    def salvar_servico(self):
        try:
            nome = self.nome_entry.get()
            descricao = self.descricao_entry.get()
            valor = float(self.valor_entry.get())

            if not nome or valor <= 0:
                messagebox.showwarning("Aviso", "Preencha corretamente os campos.", parent=self)
                return

            if self.servico_selecionado_id:
                controller.atualizar_servico(self.servico_selecionado_id, nome, descricao, valor)
                messagebox.showinfo("Atualizado", "Serviço atualizado com sucesso!", parent=self)
            else:
                controller.salvar_servico(nome, descricao, valor)
                messagebox.showinfo("Salvo", "Serviço cadastrado com sucesso!", parent=self)

            self.limpar_campos()
            self.atualizar_tabela()

        except ValueError:
            messagebox.showerror("Erro", "Valor inválido.", parent=self)

    def carregar_servico(self, event):
        if not self.tabela.curselection():
            return
        index = self.tabela.curselection()[0]
        texto = self.tabela.get(index)
        try:
            servico_id = int(texto.split('|')[0].split(':')[1].strip())
            servico = controller.buscar_servico_por_id(servico_id)
            if servico:
                self.servico_selecionado_id = servico[0]
                self.nome_entry.delete(0, tk.END)
                self.nome_entry.insert(0, servico[1])
                self.descricao_entry.delete(0, tk.END)
                self.descricao_entry.insert(0, servico[2])
                self.valor_entry.delete(0, tk.END)
                self.valor_entry.insert(0, servico[3])
        except Exception as e:
            print(f"[ERRO ao carregar serviço] {e}")

    def atualizar_tabela(self, filtro=None):
        self.tabela.delete(0, tk.END)
        servicos = controller.listar_servicos()
        for serv in servicos:
            texto = f"ID: {serv[0]} | Nome: {serv[1]} | Valor: R$ {serv[3]:.2f}"
            if not filtro or filtro.lower() in texto.lower():
                self.tabela.insert(tk.END, texto)

    def aplicar_filtro(self):
        filtro = self.filtro_entry.get().strip()
        self.atualizar_tabela(filtro)

    def exportar_excel(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Arquivo CSV", "*.csv")])
        if not caminho:
            return

        try:
            servicos = controller.listar_servicos()
            with open(caminho, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Nome", "Descrição", "Valor"])
                for s in servicos:
                    writer.writerow(s)
            messagebox.showinfo("Sucesso", f"Arquivo salvo em {caminho}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar: {e}", parent=self)

    def exportar_pdf(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Arquivo PDF", "*.pdf")])
        if not caminho:
            return

        try:
            servicos = controller.listar_servicos()
            c = canvas.Canvas(caminho, pagesize=letter)
            c.setFont("Helvetica", 10)
            c.drawString(50, 750, "Relatório de Serviços - Orbis Gestão")
            y = 720
            for s in servicos:
                texto = f"ID: {s[0]} | Nome: {s[1]} | Valor: R$ {s[3]:.2f}"
                c.drawString(50, y, texto)
                y -= 15
                if y < 50:
                    c.showPage()
                    c.setFont("Helvetica", 10)
                    y = 750
            c.save()
            messagebox.showinfo("Sucesso", f"PDF salvo em {caminho}", parent=self)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar PDF: {e}", parent=self)

    def limpar_campos(self):
        self.servico_selecionado_id = None
        self.nome_entry.delete(0, tk.END)
        self.descricao_entry.delete(0, tk.END)
        self.valor_entry.delete(0, tk.END)
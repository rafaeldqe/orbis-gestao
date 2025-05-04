import tkinter as tk
from tkinter import messagebox
import control.clientes_pj_controller as controller
import re
import requests
import threading

class ClienteJuridicoInterface(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Cadastro de Cliente Pessoa Jurídica")
        self.geometry("1000x650")
        self.master = master
        self.cliente_id = None

        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Razão Social:").grid(row=0, column=0, sticky="w")
        self.razao_entry = tk.Entry(frame, width=50)
        self.razao_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Nome Fantasia:").grid(row=1, column=0, sticky="w")
        self.fantasia_entry = tk.Entry(frame, width=50)
        self.fantasia_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="CNPJ:").grid(row=0, column=2, sticky="w")
        self.cnpj_entry = tk.Entry(frame, width=25)
        self.cnpj_entry.grid(row=0, column=3, padx=5, pady=5)
        self.cnpj_entry.bind("<KeyRelease>", self.aplicar_mascara_cnpj)
        tk.Button(frame, text="🔍 Buscar CNPJ", command=self.buscar_cnpj).grid(row=0, column=4, padx=5)

        tk.Label(frame, text="Email:").grid(row=1, column=2, sticky="w")
        self.email_entry = tk.Entry(frame, width=30)
        self.email_entry.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(frame, text="Telefone:").grid(row=2, column=2, sticky="w")
        self.telefone_entry = tk.Entry(frame, width=20)
        self.telefone_entry.grid(row=2, column=3, padx=5, pady=5)
        self.telefone_entry.bind("<KeyRelease>", self.aplicar_mascara_telefone)

        tk.Label(frame, text="CEP:").grid(row=2, column=0, sticky="w")
        self.cep_entry = tk.Entry(frame, width=15)
        self.cep_entry.grid(row=2, column=1, padx=5, pady=5)
        self.cep_entry.bind("<KeyRelease>", self.aplicar_mascara_cep)

        tk.Label(frame, text="Logradouro:").grid(row=3, column=0, sticky="w")
        self.logradouro_entry = tk.Entry(frame, width=50)
        self.logradouro_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame, text="Número:").grid(row=3, column=2, sticky="w")
        self.numero_entry = tk.Entry(frame, width=10)
        self.numero_entry.grid(row=3, column=3, padx=5, pady=5)

        tk.Label(frame, text="Bairro:").grid(row=4, column=0, sticky="w")
        self.bairro_entry = tk.Entry(frame, width=30)
        self.bairro_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(frame, text="Cidade:").grid(row=4, column=2, sticky="w")
        self.cidade_entry = tk.Entry(frame, width=30)
        self.cidade_entry.grid(row=4, column=3, padx=5, pady=5)

        tk.Label(frame, text="Estado:").grid(row=5, column=0, sticky="w")
        self.estado_entry = tk.Entry(frame, width=5)
        self.estado_entry.grid(row=5, column=1, padx=5, pady=5)

        botoes = tk.Frame(frame)
        botoes.grid(row=6, column=0, columnspan=4, pady=15)
        tk.Button(botoes, text="💾 Salvar", width=15, command=self.salvar).pack(side="left", padx=10)
        tk.Button(botoes, text="🔄 Limpar", width=15, command=self.limpar).pack(side="left", padx=10)
        tk.Button(botoes, text="↩ Voltar ao Dashboard", width=20, command=self.voltar_dashboard).pack(side="left", padx=10)

        self.tabela = tk.Listbox(frame, width=130)
        self.tabela.grid(row=7, column=0, columnspan=4, pady=20)
        self.tabela.bind("<<ListboxSelect>>", self.carregar_cliente)

        self.atualizar_tabela()

    def voltar_dashboard(self):
        self.destroy()
        self.master.deiconify()

    def aplicar_mascara_cnpj(self, event):
        valor = re.sub(r'[^0-9]', '', self.cnpj_entry.get())[:14]
        if len(valor) >= 13:
            formatado = f"{valor[:2]}.{valor[2:5]}.{valor[5:8]}/{valor[8:12]}-{valor[12:14]}"
        elif len(valor) >= 8:
            formatado = f"{valor[:2]}.{valor[2:5]}.{valor[5:8]}/{valor[8:]}"
        elif len(valor) >= 5:
            formatado = f"{valor[:2]}.{valor[2:5]}.{valor[5:]}"
        elif len(valor) >= 2:
            formatado = f"{valor[:2]}.{valor[2:]}"
        else:
            formatado = valor
        self.cnpj_entry.delete(0, tk.END)
        self.cnpj_entry.insert(0, formatado)

    def aplicar_mascara_telefone(self, event):
        valor = re.sub(r'[^0-9]', '', self.telefone_entry.get())[:11]
        if len(valor) == 11:
            formatado = f"({valor[:2]}) {valor[2:7]}-{valor[7:]}"
        elif len(valor) > 6:
            formatado = f"({valor[:2]}) {valor[2:6]}-{valor[6:]}"
        elif len(valor) > 2:
            formatado = f"({valor[:2]}) {valor[2:]}"
        else:
            formatado = valor
        self.telefone_entry.delete(0, tk.END)
        self.telefone_entry.insert(0, formatado)

    def aplicar_mascara_cep(self, event):
        valor = re.sub(r'[^0-9]', '', self.cep_entry.get())[:8]
        if len(valor) > 5:
            formatado = f"{valor[:5]}-{valor[5:]}"
        else:
            formatado = valor
        self.cep_entry.delete(0, tk.END)
        self.cep_entry.insert(0, formatado)

    def buscar_cnpj(self):
        def requisitar():
            cnpj = re.sub(r'[^0-9]', '', self.cnpj_entry.get())
            if len(cnpj) != 14:
                messagebox.showwarning("CNPJ inválido", "Informe um CNPJ com 14 dígitos.", parent=self)
                return
            try:
                resposta = requests.get(f"https://www.receitaws.com.br/v1/cnpj/{cnpj}")
                if resposta.status_code == 200:
                    dados = resposta.json()
                    if dados.get("status") == "OK":
                        self.razao_entry.delete(0, tk.END)
                        self.razao_entry.insert(0, dados.get("nome", ""))
                        self.fantasia_entry.delete(0, tk.END)
                        self.fantasia_entry.insert(0, dados.get("fantasia", ""))
                        self.email_entry.delete(0, tk.END)
                        self.email_entry.insert(0, dados.get("email", ""))
                        self.telefone_entry.delete(0, tk.END)
                        self.telefone_entry.insert(0, dados.get("telefone", ""))
                        self.cep_entry.delete(0, tk.END)
                        self.cep_entry.insert(0, dados.get("cep", ""))
                        self.logradouro_entry.delete(0, tk.END)
                        self.logradouro_entry.insert(0, dados.get("logradouro", ""))
                        self.numero_entry.delete(0, tk.END)
                        self.numero_entry.insert(0, dados.get("numero", ""))
                        self.bairro_entry.delete(0, tk.END)
                        self.bairro_entry.insert(0, dados.get("bairro", ""))
                        self.cidade_entry.delete(0, tk.END)
                        self.cidade_entry.insert(0, dados.get("municipio", ""))
                        self.estado_entry.delete(0, tk.END)
                        self.estado_entry.insert(0, dados.get("uf", ""))
                    else:
                        messagebox.showwarning("Erro", dados.get("message", "CNPJ não encontrado."), parent=self)
                else:
                    messagebox.showerror("Erro", "Erro ao consultar a Receita Federal.", parent=self)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro de rede: {e}", parent=self)

        threading.Thread(target=requisitar).start()

    def salvar(self):
        try:
            razao = self.razao_entry.get().strip()
            fantasia = self.fantasia_entry.get().strip()
            cnpj = self.cnpj_entry.get().strip()
            email = self.email_entry.get().strip()
            telefone = self.telefone_entry.get().strip()
            cep = self.cep_entry.get().strip()
            logradouro = self.logradouro_entry.get().strip()
            numero = self.numero_entry.get().strip()
            bairro = self.bairro_entry.get().strip()
            cidade = self.cidade_entry.get().strip()
            estado = self.estado_entry.get().strip()

            if not razao or not cnpj:
                messagebox.showwarning("Atenção", "Preencha pelo menos a Razão Social e o CNPJ.", parent=self)
                return

            if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                messagebox.showwarning("E-mail inválido", "O e-mail informado não é válido.", parent=self)
                return

            cnpj_limpo = re.sub(r'\D', '', cnpj)
            if len(cnpj_limpo) != 14:
                messagebox.showwarning("CNPJ inválido", "O CNPJ deve conter 14 dígitos.", parent=self)
                return

            if self.cliente_id:
                controller.atualizar_cliente(
                    self.cliente_id, razao, fantasia, cnpj, email, telefone,
                    cep, logradouro, numero, bairro, cidade, estado
                )
                messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!", parent=self)
            else:
                controller.salvar_cliente(
                    razao, fantasia, cnpj, email, telefone,
                    cep, logradouro, numero, bairro, cidade, estado
                )
                messagebox.showinfo("Sucesso", "Cliente salvo com sucesso!", parent=self)

            self.limpar()
            self.atualizar_tabela()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar cliente: {e}", parent=self)

    def atualizar_tabela(self):
        self.tabela.delete(0, tk.END)
        clientes = controller.listar_clientes()
        for cli in clientes:
            self.tabela.insert(tk.END, f"{cli[0]} | {cli[1]} | {cli[2]} | {cli[3]}")

    def carregar_cliente(self, event):
        if not self.tabela.curselection():
            return
        index = self.tabela.curselection()[0]
        linha = self.tabela.get(index)
        cliente_id = int(linha.split('|')[0].strip())
        cliente = controller.buscar_cliente_por_id(cliente_id)
        if cliente:
            self.cliente_id = cliente[0]
            self.razao_entry.delete(0, tk.END)
            self.razao_entry.insert(0, cliente[1])
            self.fantasia_entry.delete(0, tk.END)
            self.fantasia_entry.insert(0, cliente[2])
            self.cnpj_entry.delete(0, tk.END)
            self.cnpj_entry.insert(0, cliente[3])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, cliente[4])
            self.telefone_entry.delete(0, tk.END)
            self.telefone_entry.insert(0, cliente[5])
            self.cep_entry.delete(0, tk.END)
            self.cep_entry.insert(0, cliente[6])
            self.logradouro_entry.delete(0, tk.END)
            self.logradouro_entry.insert(0, cliente[7])
            self.numero_entry.delete(0, tk.END)
            self.numero_entry.insert(0, cliente[8])
            self.bairro_entry.delete(0, tk.END)
            self.bairro_entry.insert(0, cliente[9])
            self.cidade_entry.delete(0, tk.END)
            self.cidade_entry.insert(0, cliente[10])
            self.estado_entry.delete(0, tk.END)
            self.estado_entry.insert(0, cliente[11])

    def limpar(self):
        for entry in [self.razao_entry, self.fantasia_entry, self.cnpj_entry, self.email_entry, self.telefone_entry,
                      self.cep_entry, self.logradouro_entry, self.numero_entry, self.bairro_entry,
                      self.cidade_entry, self.estado_entry]:
            entry.delete(0, tk.END)
        self.cliente_id = None
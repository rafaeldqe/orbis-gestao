import tkinter as tk
from tkinter import messagebox
import control.clientes_pf_controller as controller
import requests
import re

class ClienteFisicoInterface(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Cadastro de Cliente Pessoa Física")
        self.geometry("1000x600")
        self.cliente_id = None

        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Linha 1
        tk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="w")
        self.nome_entry = tk.Entry(frame, width=50)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="CPF:").grid(row=0, column=2, sticky="w")
        self.cpf_entry = tk.Entry(frame, width=20)
        self.cpf_entry.grid(row=0, column=3, padx=5, pady=5)
        self.cpf_entry.bind("<KeyRelease>", self.aplicar_mascara_cpf)

        # Linha 2
        tk.Label(frame, text="Email:").grid(row=1, column=0, sticky="w")
        self.email_entry = tk.Entry(frame, width=40)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Telefone:").grid(row=1, column=2, sticky="w")
        self.telefone_entry = tk.Entry(frame, width=20)
        self.telefone_entry.grid(row=1, column=3, padx=5, pady=5)
        self.telefone_entry.bind("<KeyRelease>", self.aplicar_mascara_telefone)

        # Linha 3
        tk.Label(frame, text="CEP:").grid(row=2, column=0, sticky="w")
        self.cep_entry = tk.Entry(frame, width=20)
        self.cep_entry.grid(row=2, column=1, padx=5, pady=5)
        self.cep_entry.bind("<KeyRelease>", self.aplicar_mascara_cep)
        tk.Button(frame, text="🔍", command=self.buscar_cep).grid(row=2, column=2, sticky="w")

        tk.Label(frame, text="Logradouro:").grid(row=3, column=0, sticky="w")
        self.logradouro_entry = tk.Entry(frame, width=50)
        self.logradouro_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame, text="Número:").grid(row=3, column=2, sticky="w")
        self.numero_entry = tk.Entry(frame, width=10)
        self.numero_entry.grid(row=3, column=3, padx=5, pady=5)

        # Linha 4
        tk.Label(frame, text="Bairro:").grid(row=4, column=0, sticky="w")
        self.bairro_entry = tk.Entry(frame, width=30)
        self.bairro_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(frame, text="Cidade:").grid(row=4, column=2, sticky="w")
        self.cidade_entry = tk.Entry(frame, width=30)
        self.cidade_entry.grid(row=4, column=3, padx=5, pady=5)

        tk.Label(frame, text="Estado:").grid(row=5, column=0, sticky="w")
        self.estado_entry = tk.Entry(frame, width=5)
        self.estado_entry.grid(row=5, column=1, padx=5, pady=5)

        # Botões
        botoes_frame = tk.Frame(frame, pady=15)
        botoes_frame.grid(row=6, column=0, columnspan=4)

        tk.Button(botoes_frame, text="💾 Salvar", command=self.salvar, width=15).pack(side="left", padx=10)
        tk.Button(botoes_frame, text="🔄 Limpar", command=self.limpar_campos, width=15).pack(side="left", padx=10)
        tk.Button(botoes_frame, text="❌ Fechar", command=self.destroy, width=15).pack(side="left", padx=10)

        # Tabela de clientes
        self.tabela = tk.Listbox(frame, width=130)
        self.tabela.grid(row=7, column=0, columnspan=4, pady=20)
        self.atualizar_tabela()

    def aplicar_mascara_cpf(self, event):
        valor = re.sub(r'[^0-9]', '', self.cpf_entry.get())[:11]
        if len(valor) > 9:
            formatado = f"{valor[:3]}.{valor[3:6]}.{valor[6:9]}-{valor[9:11]}"
        elif len(valor) > 6:
            formatado = f"{valor[:3]}.{valor[3:6]}.{valor[6:9]}"
        elif len(valor) > 3:
            formatado = f"{valor[:3]}.{valor[3:6]}"
        else:
            formatado = valor
        self.cpf_entry.delete(0, tk.END)
        self.cpf_entry.insert(0, formatado)

    def aplicar_mascara_telefone(self, event):
        valor = re.sub(r'[^0-9]', '', self.telefone_entry.get())[:11]
        if len(valor) > 6:
            formatado = f"({valor[:2]}) {valor[2:7]}-{valor[7:11]}"
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

    def validar_cpf(self, cpf):
        cpf = re.sub(r'[^0-9]', '', cpf)
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        soma1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
        dig1 = (soma1 * 10 % 11) % 10
        soma2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
        dig2 = (soma2 * 10 % 11) % 10
        return dig1 == int(cpf[9]) and dig2 == int(cpf[10])

    def validar_email(self, email):
        return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email))

    def buscar_cep(self):
        cep = re.sub(r'[^0-9]', '', self.cep_entry.get())
        if len(cep) != 8:
            messagebox.showwarning("CEP Inválido", "Digite um CEP válido com 8 dígitos.", parent=self)
            return
        try:
            resposta = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
            if resposta.status_code == 200:
                dados = resposta.json()
                if 'erro' in dados:
                    messagebox.showwarning("CEP não encontrado", "Nenhum endereço encontrado para o CEP informado.", parent=self)
                else:
                    self.logradouro_entry.delete(0, tk.END)
                    self.bairro_entry.delete(0, tk.END)
                    self.cidade_entry.delete(0, tk.END)
                    self.estado_entry.delete(0, tk.END)
                    self.logradouro_entry.insert(0, dados.get("logradouro", ""))
                    self.bairro_entry.insert(0, dados.get("bairro", ""))
                    self.cidade_entry.insert(0, dados.get("localidade", ""))
                    self.estado_entry.insert(0, dados.get("uf", ""))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar CEP: {e}", parent=self)

    def salvar(self):
        try:
            nome = self.nome_entry.get()
            cpf = self.cpf_entry.get()
            email = self.email_entry.get()
            telefone = self.telefone_entry.get()
            cep = self.cep_entry.get()
            logradouro = self.logradouro_entry.get()
            numero = self.numero_entry.get()
            bairro = self.bairro_entry.get()
            cidade = self.cidade_entry.get()
            estado = self.estado_entry.get()

            if not nome or not cpf:
                messagebox.showwarning("Atenção", "Nome e CPF são obrigatórios.", parent=self)
                return

            if not self.validar_cpf(cpf):
                messagebox.showerror("CPF inválido", "O CPF informado é inválido.", parent=self)
                return

            if email and not self.validar_email(email):
                messagebox.showerror("Email inválido", "O formato do e-mail é inválido.", parent=self)
                return

            if self.cliente_id:
                controller.atualizar_cliente(self.cliente_id, nome, cpf, email, telefone, cep, logradouro, numero, bairro, cidade, estado)
                messagebox.showinfo("Atualizado", "Cliente atualizado com sucesso!", parent=self)
            else:
                controller.salvar_cliente(nome, cpf, email, telefone, cep, logradouro, numero, bairro, cidade, estado)
                messagebox.showinfo("Salvo", "Cliente cadastrado com sucesso!", parent=self)

            self.limpar_campos()
            self.atualizar_tabela()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar cliente: {e}", parent=self)

    def atualizar_tabela(self):
        self.tabela.delete(0, tk.END)
        clientes = controller.listar_clientes()
        for c in clientes:
            linha = f"ID: {c[0]} | Nome: {c[1]} | CPF: {c[2]} | Email: {c[3]} | Telefone: {c[4]} | Cidade: {c[5]}-{c[6]}"
            self.tabela.insert(tk.END, linha)

    def limpar_campos(self):
        self.cliente_id = None
        self.nome_entry.delete(0, tk.END)
        self.cpf_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.cep_entry.delete(0, tk.END)
        self.logradouro_entry.delete(0, tk.END)
        self.numero_entry.delete(0, tk.END)
        self.bairro_entry.delete(0, tk.END)
        self.cidade_entry.delete(0, tk.END)
        self.estado_entry.delete(0, tk.END)
import tkinter as tk
from tkinter import ttk, messagebox
from control.usuarios_controller import obter_usuarios, adicionar_usuario, atualizar_usuario, desativar_usuario_por_id

class UsuariosView:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestão de Usuários")
        self.master.geometry("600x400")

        self.tabela = ttk.Treeview(master, columns=("ID", "Nome", "Login", "Tipo", "Ativo"), show="headings")
        for col in ("ID", "Nome", "Login", "Tipo", "Ativo"):
            self.tabela.heading(col, text=col)
            self.tabela.column(col, anchor=tk.CENTER)
        self.tabela.pack(fill=tk.BOTH, expand=True, pady=10)

        frame = tk.Frame(master)
        frame.pack()

        tk.Button(frame, text="➕ Adicionar", command=self.abrir_adicionar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="✏️ Editar", command=self.abrir_editar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="❌ Desativar", command=self.desativar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="🔁 Atualizar", command=self.carregar_dados).pack(side=tk.LEFT, padx=5)

        self.carregar_dados()

    def carregar_dados(self):
        for i in self.tabela.get_children():
            self.tabela.delete(i)
        for row in obter_usuarios():
            ativo_str = "Sim" if row[5] == 1 else "Não"
            self.tabela.insert("", tk.END, values=(*row[:5], ativo_str))

    def abrir_adicionar(self):
        self._abrir_formulario()

    def abrir_editar(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário para editar.")
            return
        valores = self.tabela.item(selecionado[0], "values")
        self._abrir_formulario(valores)

    def _abrir_formulario(self, dados=None):
        janela = tk.Toplevel(self.master)
        janela.title("Usuário")
        janela.geometry("300x250")

        tk.Label(janela, text="Nome:").pack()
        nome_entry = tk.Entry(janela)
        nome_entry.pack()

        tk.Label(janela, text="Login:").pack()
        usuario_entry = tk.Entry(janela)
        usuario_entry.pack()

        tk.Label(janela, text="Senha:").pack()
        senha_entry = tk.Entry(janela, show="*")
        senha_entry.pack()

        tk.Label(janela, text="Tipo:").pack()
        tipo_entry = tk.Entry(janela)
        tipo_entry.pack()

        if dados:
            id_usuario = dados[0]
            nome_entry.insert(0, dados[1])
            usuario_entry.insert(0, dados[2])
            tipo_entry.insert(0, dados[3])
            senha_entry.insert(0, "*")

        def salvar():
            nome = nome_entry.get().strip()
            usuario = usuario_entry.get().strip()
            senha = senha_entry.get().strip()
            tipo = tipo_entry.get().strip()

            if not nome or not usuario or not tipo or (not dados and not senha):
                messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos obrigatórios.")
                return

            if dados:
                atualizar_usuario(id_usuario, nome, usuario, tipo)
                # Se quiser no futuro, pode tratar senha nova aqui
            else:
                adicionar_usuario(nome, usuario, senha, tipo)

            self.carregar_dados()
            janela.destroy()

        tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)

    def desativar(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário para desativar.")
            return
        valores = self.tabela.item(selecionado[0], "values")
        desativar_usuario_por_id(valores[0])
        self.carregar_dados()

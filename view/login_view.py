import tkinter as tk
from tkinter import messagebox
from control.usuarios_controller import autenticar_usuario
from view.dashboard_view import abrir_dashboard

class LoginView:
    def __init__(self, master):
        self.master = master
        self.master.title("Login - Orbis Gestão")
        self.master.geometry("400x400")
        self.master.configure(bg="white")

        self.frame = tk.Frame(master, bg="white")
        self.frame.pack(expand=True)

        # Título
        self.label_titulo = tk.Label(self.frame, text="LOGIN", font=("Segoe UI", 24, "bold"), fg="#0074D9", bg="white")
        self.label_titulo.pack(pady=(20, 30))

        # Campo usuário
        self.label_usuario = tk.Label(self.frame, text="Usuário", bg="white", anchor="w", font=("Segoe UI", 10))
        self.label_usuario.pack(fill="x", padx=40)
        self.entry_usuario = tk.Entry(self.frame, font=("Segoe UI", 12), bd=1, relief="solid")
        self.entry_usuario.pack(fill="x", padx=40, pady=(0, 15))

        # Campo senha
        self.label_senha = tk.Label(self.frame, text="Senha", bg="white", anchor="w", font=("Segoe UI", 10))
        self.label_senha.pack(fill="x", padx=40)
        self.entry_senha = tk.Entry(self.frame, font=("Segoe UI", 12), show="*", bd=1, relief="solid")
        self.entry_senha.pack(fill="x", padx=40, pady=(0, 25))

        # Botão login
        self.botao_login = tk.Button(
            self.frame, text="Entrar", font=("Segoe UI", 12, "bold"), bg="#0074D9", fg="white",
            activebackground="#005fa3", activeforeground="white",
            command=self.fazer_login
        )
        self.botao_login.pack(padx=40, pady=(0, 10), fill="x")

    def fazer_login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()

        if autenticar_usuario(usuario, senha):
            self.master.destroy()
            abrir_dashboard()
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha inválidos.")

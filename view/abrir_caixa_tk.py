import tkinter as tk
from tkinter import messagebox
from control import caixa_controller
from view.caixa_view import CaixaView

class AbrirCaixaView(tk.Toplevel):
    def __init__(self, master, operador):
        super().__init__(master)
        self.title("Abrir Caixa")
        self.geometry("300x200")
        self.operador = operador

        tk.Label(self, text="Abrir Caixa para operador:", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Label(self, text=f"{operador}", fg="blue", font=("Arial", 12)).pack(pady=5)

        tk.Label(self, text="Valor inicial (R$):").pack()
        self.valor_input = tk.Entry(self)
        self.valor_input.pack(pady=10)

        tk.Button(self, text="✅ Confirmar Abertura", command=self.abrir_caixa).pack(pady=10)

    def abrir_caixa(self):
        try:
            valor = float(self.valor_input.get())
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido.")
            return

        if caixa_controller.caixa_em_aberto_por_operador(self.operador):
            messagebox.showinfo("Caixa Já Aberto", "Este operador já possui um caixa aberto.")
            self.destroy()
            CaixaView(self.master).focus()
            return

        caixa_controller.abrir_caixa(self.operador, valor)
        messagebox.showinfo("Sucesso", "Caixa aberto com sucesso!")
        self.destroy()
        CaixaView(self.master).focus()

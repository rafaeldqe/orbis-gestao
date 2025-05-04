import tkinter as tk

class TipoClienteDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Tipo de Cliente")
        self.geometry("300x150")
        self.resultado = None

        tk.Label(self, text="Selecione o tipo de cliente:", font=("Arial", 12)).pack(pady=10)

        tk.Button(self, text="Pessoa Física", width=20, command=self.selecionar_pf).pack(pady=5)
        tk.Button(self, text="Pessoa Jurídica", width=20, command=self.selecionar_pj).pack(pady=5)

        self.transient(master)
        self.grab_set()
        self.wait_window()

    def selecionar_pf(self):
        from view.cliente_fisico_interface import ClienteFisicoInterface
        janela = ClienteFisicoInterface(self)
        cliente = janela.cliente_selecionado if hasattr(janela, 'cliente_selecionado') else None
        if cliente:
            self.resultado = {'id': cliente[0], 'nome': cliente[1], 'tipo': 'pf'}
        self.destroy()

    def selecionar_pj(self):
        from view.cliente_juridico_interface import ClienteJuridicoInterface
        janela = ClienteJuridicoInterface(self)
        cliente = janela.cliente_selecionado if hasattr(janela, 'cliente_selecionado') else None
        if cliente:
            self.resultado = {'id': cliente[0], 'nome': cliente[1], 'tipo': 'pj'}
        self.destroy()

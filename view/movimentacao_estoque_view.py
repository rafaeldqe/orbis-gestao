import tkinter as tk
from tkinter import messagebox
import control.produtos_controller as controller

class MovimentacaoEstoqueView(tk.Toplevel):
    def __init__(self, master, produto_id=None, atualizar_callback=None):
        super().__init__(master)
        self.title("Movimentação de Estoque")
        self.geometry("400x450")

        self.produto_id = produto_id
        self.atualizar_callback = atualizar_callback

        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # ID do Produto
        tk.Label(frame, text="ID do Produto:").grid(row=0, column=0, sticky="w")
        self.produto_id_entry = tk.Entry(frame, width=10)
        self.produto_id_entry.grid(row=0, column=1, padx=10, pady=5)

        # Nome do Produto
        tk.Label(frame, text="Nome do Produto:").grid(row=1, column=0, sticky="w")
        self.nome_produto_label = tk.Label(frame, text="", anchor="w", width=30)
        self.nome_produto_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        if self.produto_id:
            self.produto_id_entry.insert(0, str(self.produto_id))
            produto = controller.buscar_produto_por_id(self.produto_id)
            if produto:
                self.nome_produto_label.config(text=produto[1])

        # Quantidade
        tk.Label(frame, text="Quantidade:").grid(row=2, column=0, sticky="w")
        self.quantidade_entry = tk.Entry(frame, width=10)
        self.quantidade_entry.grid(row=2, column=1, padx=10, pady=5)

        # Observação
        tk.Label(frame, text="Observação:").grid(row=3, column=0, sticky="nw")
        self.obs_text = tk.Text(frame, width=40, height=5)
        self.obs_text.grid(row=3, column=1, padx=10, pady=5)

        # Botões
        entrada_btn = tk.Button(frame, text="📥 Entrada", width=15, command=self.entrada_estoque)
        entrada_btn.grid(row=4, column=0, pady=10)

        saida_btn = tk.Button(frame, text="📤 Saída", width=15, command=self.saida_estoque)
        saida_btn.grid(row=4, column=1, pady=10)

        fechar_btn = tk.Button(frame, text="Fechar", command=self.destroy)
        fechar_btn.grid(row=5, column=0, columnspan=2, pady=10)

    def entrada_estoque(self):
        self._movimentar_estoque("entrada")

    def saida_estoque(self):
        self._movimentar_estoque("saida")

    def _movimentar_estoque(self, tipo):
        try:
            produto_id = int(self.produto_id_entry.get())
            quantidade = int(self.quantidade_entry.get())
            observacao = self.obs_text.get("1.0", tk.END).strip()

            if quantidade <= 0:
                messagebox.showwarning("Aviso", "Quantidade deve ser maior que zero.", parent=self)
                return

            # ✅ Chamada corrigida para função existente
            controller.registrar_movimentacao(produto_id, tipo, quantidade, observacao)

            messagebox.showinfo("Sucesso", f"{tipo.capitalize()} registrada com sucesso!", parent=self)

            if self.atualizar_callback:
                self.atualizar_callback()

            self.destroy()

        except ValueError:
            messagebox.showerror("Erro", "ID e Quantidade devem ser números inteiros.", parent=self)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na movimentação: {e}", parent=self)

import tkinter as tk
from tkinter import ttk, messagebox
import control.vendas_controller as vendas_controller
import control.clientes_pf_controller as pf_controller
import control.clientes_pj_controller as pj_controller

class HistoricoVendasView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Histórico de Vendas")
        self.geometry("1000x600")

        self.clientes = self._carregar_clientes()
        self.clientes_dict = {str(c[0]): c[1] for c in self.clientes}

        self._montar_filtros()
        self._montar_tabela()
        self.carregar_vendas()

    def _montar_filtros(self):
        filtros = tk.Frame(self, pady=10)
        filtros.pack(fill="x", padx=20)

        tk.Label(filtros, text="Cliente:").pack(side="left")
        self.entrada_cliente = tk.Entry(filtros, width=30)
        self.entrada_cliente.pack(side="left", padx=5)

        tk.Label(filtros, text="Pedido #:").pack(side="left")
        self.entrada_id = tk.Entry(filtros, width=10)
        self.entrada_id.pack(side="left", padx=5)

        tk.Button(filtros, text="🔍 Buscar", command=self.carregar_vendas).pack(side="left", padx=10)

    def _montar_tabela(self):
        colunas = ("ID", "Data", "Cliente", "Total", "Pagamento", "Status")

        self.tabela = ttk.Treeview(self, columns=colunas, show="headings", height=20)
        for col in colunas:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, anchor="center", width=150)

        self.tabela.pack(fill="both", expand=True, padx=20, pady=10)

        botao = tk.Button(self, text="👁️ Ver Detalhes da Venda", command=self.visualizar_detalhes)
        botao.pack(pady=10)

    def _carregar_clientes(self):
        return pf_controller.listar_clientes() + pj_controller.listar_clientes()

    def carregar_vendas(self):
        nome_filtro = self.entrada_cliente.get().lower()
        id_filtro = self.entrada_id.get()

        vendas = vendas_controller.listar_vendas()
        self.tabela.delete(*self.tabela.get_children())

        for venda in vendas:
            venda_id, data, cliente_id, tipo, total, desconto, forma_pgto, status, operador = venda
            nome = self.clientes_dict.get(str(cliente_id), "Consumidor Final")

            if nome_filtro and nome_filtro not in nome.lower():
                continue
            if id_filtro and str(venda_id) != id_filtro:
                continue

            self.tabela.insert("", "end", values=(
                venda_id,
                data,
                nome,
                f"R$ {total:.2f}",
                forma_pgto,
                status
            ))

    def visualizar_detalhes(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showinfo("Aviso", "Selecione uma venda.")
            return

        venda_id = self.tabela.item(selecionado[0])["values"][0]
        venda, itens = vendas_controller.detalhar_venda(venda_id)

        texto = f"Detalhes da Venda #{venda_id}\n\n"
        texto += f"Forma de Pagamento: {venda[2]}\n"
        texto += f"Desconto: R$ {venda[0]:.2f}\n"
        texto += f"Total: R$ {venda[1]:.2f}\n\nItens:\n"

        for item in itens:
            nome, qtd, unit, sub, _ = item
            texto += f"- {nome} | {qtd} x R$ {unit:.2f} = R$ {sub:.2f}\n"

        messagebox.showinfo("Itens da Venda", texto)

import tkinter as tk
from view.produtos_view import ProdutosView
from view.movimentacoes_historico_view import HistoricoMovimentacoesView
from view.servicos_view import ServicosView
from view.cliente_fisico_interface import ClienteFisicoInterface
from view.cliente_juridico_interface import ClienteJuridicoInterface
from view.vendas_view import VendasView
from view.caixa_view import CaixaView
from view.abrir_caixa_tk import AbrirCaixaView
from view.contas_receber_view import ContasReceberView  # ✅ agora ok!
import control.produtos_controller as produtos_controller
import control.caixa_controller as caixa_controller
from view.historico_vendas_view import HistoricoVendasView

# ✅ Simulando usuário logado (substituir pelo login real depois)
USUARIO_LOGADO = "admin"

def abrir_tipo_cliente(root):
    janela = tk.Toplevel(root)
    janela.title("Tipo de Cliente")
    janela.geometry("300x150")

    tk.Label(janela, text="Selecione o tipo de cliente:", font=("Arial", 12)).pack(pady=10)

    tk.Button(janela, text="Pessoa Física", width=20,
              command=lambda: (janela.destroy(), ClienteFisicoInterface(root))).pack(pady=5)
    tk.Button(janela, text="Pessoa Jurídica", width=20,
              command=lambda: (janela.destroy(), ClienteJuridicoInterface(root))).pack(pady=5)

def abrir_caixa_ou_tela(root, operador):
    if caixa_controller.caixa_em_aberto_por_operador(operador):
        CaixaView(root)
    else:
        AbrirCaixaView(root, operador)

def abrir_dashboard():
    root = tk.Tk()
    root.title("Dashboard - Orbis Gestão")
    root.geometry("800x600")

    container = tk.Frame(root, padx=40, pady=40)
    container.pack(fill="both", expand=True)

    # 📊 Indicadores
    total_produtos = produtos_controller.contar_produtos()
    estoque_baixo = len(produtos_controller.listar_estoque_baixo())

    tk.Label(container, text=f"📊 Total de Produtos: {total_produtos}", font=("Arial", 14)).pack(pady=5)
    tk.Label(container, text=f"⚠️ Produtos com Estoque Baixo: {estoque_baixo}", font=("Arial", 14), fg="red").pack(pady=5)

    # Botões principais
    tk.Button(container, text="📦 Produtos", width=25, height=2, command=lambda: ProdutosView(root)).pack(pady=10)
    tk.Button(container, text="🛠️ Serviços", width=25, height=2, command=lambda: ServicosView(root)).pack(pady=10)
    tk.Button(container, text="👥 Clientes", width=25, height=2, command=lambda: abrir_tipo_cliente(root)).pack(pady=10)
    tk.Button(container, text="🛒 Vendas", width=25, height=2, command=lambda: VendasView(root)).pack(pady=10)
    tk.Button(container, text="🧾 Caixa", width=25, height=2, command=lambda: abrir_caixa_ou_tela(root, USUARIO_LOGADO)).pack(pady=10)
    tk.Button(container, text="💰 Contas a Receber", width=25, height=2, command=ContasReceberView).pack(pady=10)
    tk.Button(container, text="📑 Histórico de Vendas", width=25, height=2, command=HistoricoVendasView).pack(pady=10)
    tk.Button(container, text="Sair", width=25, height=2, command=root.destroy).pack(pady=20)

    root.mainloop()

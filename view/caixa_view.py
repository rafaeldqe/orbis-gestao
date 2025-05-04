import tkinter as tk
from tkinter import ttk, messagebox
import control.vendas_controller as controller
from control.nfe_controller import gerar_xml_nfe
from util.danfe import gerar_danfe_pdf
from control.fiscal_controller import autorizar_nf_e_simulada
import control.movimentacoes_controller as mov_controller
import os
import sqlite3
import subprocess  # usado para abrir o PDF

class CaixaView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Caixa - Orbis Gestão")
        self.geometry("1200x600")

        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Vendas Pendentes", font=("Arial", 16, "bold")).pack()

        self.tabela = ttk.Treeview(
            frame,
            columns=("ID", "Data", "Cliente", "Total", "Pagamento", "Status NF", "Chave"),
            show="headings",
            height=15
        )
        self.tabela.heading("ID", text="ID")
        self.tabela.heading("Data", text="Data")
        self.tabela.heading("Cliente", text="Cliente")
        self.tabela.heading("Total", text="Total (R$)")
        self.tabela.heading("Pagamento", text="Pagamento")
        self.tabela.heading("Status NF", text="Status NF-e")
        self.tabela.heading("Chave", text="Chave de Acesso")

        for col in ("ID", "Data", "Cliente", "Total", "Pagamento", "Status NF", "Chave"):
            self.tabela.column(col, anchor="center", width=160)

        self.tabela.pack(pady=10, fill="both", expand=True)

        botoes = tk.Frame(frame)
        botoes.pack(pady=10)

        tk.Button(botoes, text="🔄 Atualizar Lista", command=self.carregar_vendas_pendentes).pack(side="left", padx=10)
        tk.Button(botoes, text="🔍 Visualizar Venda", command=self.visualizar_venda).pack(side="left", padx=10)
        tk.Button(botoes, text="✅ Finalizar Venda", command=self.finalizar_venda).pack(side="left", padx=10)
        tk.Button(botoes, text="📄 Reimprimir DANFE", command=self.reimprimir_danfe).pack(side="left", padx=10)
        tk.Button(botoes, text="🚫 Cancelar NF-e", command=self.cancelar_nfe).pack(side="left", padx=10)
        tk.Button(botoes, text="📦 Fechar Caixa", command=self.abrir_fechamento_caixa).pack(side="left", padx=10)

        self.enviar_email_var = tk.BooleanVar(value=False)
        tk.Checkbutton(frame, text="📧 Enviar DANFE por e-mail ao finalizar", variable=self.enviar_email_var).pack(pady=5)

        self.carregar_vendas_pendentes()

    def carregar_vendas_pendentes(self):
        self.tabela.delete(*self.tabela.get_children())
        vendas = controller.listar_vendas()
        for venda in vendas:
            status_nf = venda[6] if len(venda) > 6 and venda[6] else "-"
            chave = venda[7] if len(venda) > 7 and venda[7] else "-"
            cliente = venda[2] if len(venda) > 2 and venda[2] else "Consumidor Final"
            self.tabela.insert("", "end", values=(venda[0], venda[1], cliente, venda[3], venda[4], status_nf, chave))

    def visualizar_venda(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Seleção", "Selecione uma venda.")
            return

        venda_id = self.tabela.item(selecionado)["values"][0]
        venda, itens = controller.detalhar_venda(venda_id)

        texto = f"Venda ID: {venda_id}\nForma de Pagamento: {venda[2]}\nDesconto: R$ {venda[0]:.2f}\nTotal: R$ {venda[1]:.2f}\n\nItens:\n"
        for i in itens:
            texto += f"- {i[0]} | {i[1]} x R$ {i[2]:.2f} = R$ {i[3]:.2f}\n"

        messagebox.showinfo("Detalhes da Venda", texto)

    def finalizar_venda(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Seleção", "Selecione uma venda.")
            return

        venda_id = self.tabela.item(selecionado)["values"][0]
        controller.finalizar_venda(venda_id)

        # Gerar XML e PDF do DANFE
        caminho_xml = gerar_xml_nfe(venda_id)
        enviar_email = self.enviar_email_var.get()

        # Gera e salva o PDF
        pdf_path = gerar_danfe_pdf(
            caminho_xml,
            email_destinatario="teste@cliente.com" if enviar_email else None
        )

        # Simula autorização da NF-e
        resposta = autorizar_nf_e_simulada(venda_id)

        # Registra saída no estoque
        _, itens = controller.detalhar_venda(venda_id)
        for item in itens:
            mov_controller.registrar_movimentacao(
                produto_id=item[4],
                tipo="saida",
                quantidade=item[1],
                observacao=f"Saída por NF-e da venda ID {venda_id}"
            )

        # Abrir o PDF no visualizador padrão do sistema
        try:
            if os.name == 'nt':
                subprocess.Popen(["start", "", pdf_path], shell=True)

            else:
                subprocess.Popen(["xdg-open", pdf_path])
        except Exception as e:
            print(f"Erro ao abrir PDF: {e}")
            messagebox.showwarning("Aviso", "PDF gerado, mas não foi possível abrir automaticamente.")

        # Pergunta se deseja imprimir
        deseja_imprimir = messagebox.askyesno("Impressão", "Deseja imprimir a DANFE agora?")
        if deseja_imprimir:
            try:
                if os.name == 'nt':
                    os.startfile(pdf_path, "print")
                else:
                    subprocess.Popen(["lp", pdf_path])
            except Exception as e:
                print(f"Erro ao imprimir DANFE: {e}")
                messagebox.showwarning("Erro", "Não foi possível enviar a DANFE para impressão.")

        messagebox.showinfo(
            "Sucesso",
            f"Venda {venda_id} finalizada e NF-e autorizada (simulada)!\n\n"
            f"Chave: {resposta['chave_acesso']}\nProtocolo: {resposta['protocolo']}"
        )

        self.carregar_vendas_pendentes()

    def reimprimir_danfe(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Seleção", "Selecione uma venda.")
            return

        venda_id = self.tabela.item(selecionado)["values"][0]
        xml_nome = f"NFe_{venda_id}"
        pasta = "notas_emitidas/xmls"

        for nome in os.listdir(pasta):
            if nome.startswith(xml_nome) and nome.endswith(".xml"):
                caminho = os.path.join(pasta, nome)
                gerar_danfe_pdf(caminho)
                return

        messagebox.showerror("Erro", f"XML da venda {venda_id} não encontrado para reimpressão.")

    def cancelar_nfe(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Seleção", "Selecione uma venda.")
            return

        venda_id = self.tabela.item(selecionado)["values"][0]
        status_nf = self.tabela.item(selecionado)["values"][5]

        if status_nf != "autorizado":
            messagebox.showinfo("Cancelamento", "A NF-e só pode ser cancelada se estiver autorizada.")
            return

        confirmar = messagebox.askyesno("Confirmação", f"Cancelar a NF-e da venda {venda_id}?")
        if not confirmar:
            return

        conn = controller.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE vendas SET
                status_nf = 'cancelada',
                protocolo = NULL,
                chave_acesso = NULL
            WHERE id = ?
        """, (venda_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("NF-e Cancelada", f"A NF-e da venda {venda_id} foi cancelada com sucesso.")
        self.carregar_vendas_pendentes()

    def abrir_fechamento_caixa(self):
        from view.fechamento_caixa_tk import FechamentoCaixaView
        FechamentoCaixaView(self, operador="admin")  # ajuste depois para operador logado

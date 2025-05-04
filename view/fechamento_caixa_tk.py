import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os
import subprocess
import sys
from util.db import conectar
import control.caixa_controller as caixa_controller

class FechamentoCaixaView(tk.Toplevel):
    def __init__(self, master, operador):
        super().__init__(master)
        self.title("Fechamento de Caixa")
        self.geometry("600x400")

        caixa = caixa_controller.buscar_caixa_aberto(operador)
        if not caixa:
            messagebox.showerror("Erro", "Nenhum caixa aberto encontrado para este operador.")
            self.destroy()
            return

        self.caixa_id = caixa[0]
        self.saldo_inicial = caixa[2]
        self.operador = operador

        tk.Label(self, text=f"Operador: {operador}", font=("Arial", 12)).pack(pady=5)
        tk.Label(self, text=f"Saldo Inicial: R$ {self.saldo_inicial:.2f}", font=("Arial", 12)).pack(pady=5)

        self.formas_pagamento, self.total_final = self.buscar_totais_por_forma()
        self.entradas = {}

        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="Forma de Pagamento", width=20, anchor="w", font=("Arial", 10, "bold")).grid(row=0, column=0)
        tk.Label(frame, text="Valor no Sistema (R$)", width=20, anchor="w", font=("Arial", 10, "bold")).grid(row=0, column=1)
        tk.Label(frame, text="Conferido (R$)", width=20, anchor="w", font=("Arial", 10, "bold")).grid(row=0, column=2)

        for i, (forma, valor) in enumerate(self.formas_pagamento.items(), start=1):
            tk.Label(frame, text=forma, width=20, anchor="w").grid(row=i, column=0)
            tk.Label(frame, text=f"{valor:.2f}", width=20, anchor="w").grid(row=i, column=1)
            entrada = tk.Entry(frame, width=20)
            entrada.grid(row=i, column=2)
            self.entradas[forma] = (valor, entrada)

        tk.Label(self, text=f"Total no Sistema: R$ {self.total_final:.2f}", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(self, text="✅ Confirmar Fechamento de Caixa", bg="green", fg="white",
                  font=("Arial", 12, "bold"), command=self.validar_conferencia).pack(pady=15)

    def buscar_totais_por_forma(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT data_abertura FROM caixa
            WHERE id = ? AND operador = ? AND status = 'aberto'
        ''', (self.caixa_id, self.operador))
        resultado = cursor.fetchone()
        if not resultado:
            return {}, 0.0

        data_hora_abertura = datetime.strptime(resultado[0], "%Y-%m-%d %H:%M:%S")
        agora = datetime.now()

        cursor.execute('''
            SELECT forma_pagamento, SUM(total)
            FROM vendas
            WHERE status = 'finalizada'
            AND datetime(data) BETWEEN ? AND ?
            GROUP BY forma_pagamento
        ''', (
            data_hora_abertura.strftime("%Y-%m-%d %H:%M:%S"),
            agora.strftime("%Y-%m-%d %H:%M:%S")
        ))

        totais = {}
        total_geral = 0
        for forma, soma in cursor.fetchall():
            totais[forma] = soma
            total_geral += soma

        conn.close()
        return totais, total_geral

    def validar_conferencia(self):
        total_digitado = 0
        diferencas = []
        totais_digitados = {}

        for forma, (valor_sistema, entrada) in self.entradas.items():
            valor_str = entrada.get().replace(",", ".").strip()
            try:
                valor_digitado = float(valor_str) if valor_str else 0.0
            except ValueError:
                messagebox.showerror("Erro", f"Valor inválido na forma de pagamento: {forma}")
                return

            totais_digitados[forma] = valor_digitado
            total_digitado += valor_digitado

            if abs(valor_sistema - valor_digitado) > 0.01:
                diferencas.append((forma, valor_sistema, valor_digitado))

        if diferencas:
            msg = "⚠️ Diferenças encontradas:\n\n"
            for forma, sistema, digitado in diferencas:
                msg += f"- {forma}: sistema R$ {sistema:.2f} | digitado R$ {digitado:.2f}\n"
            msg += f"\nTotal Digitado: R$ {total_digitado:.2f}\nDiferença Geral: R$ {total_digitado - self.total_final:.2f}"
            messagebox.showwarning("Diferenças Encontradas", msg)
        else:
            messagebox.showinfo("Fechamento OK", f"Todos os valores conferem!\nTotal Digitado: R$ {total_digitado:.2f}")

        if messagebox.askyesno("Confirmar", "Deseja realmente fechar o caixa com esses valores?"):
            caixa_controller.fechar_caixa(self.caixa_id, self.total_final)
            self.gerar_relatorio_pdf(totais_digitados, total_digitado)
            self.destroy()

    def gerar_relatorio_pdf(self, totais_digitados, total_digitado):
        pasta = "relatorios/fechamentos"
        os.makedirs(pasta, exist_ok=True)
        agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        caminho = f"{pasta}/fechamento_caixa_{self.caixa_id}_{agora}.pdf"

        c = canvas.Canvas(caminho, pagesize=A4)
        largura, altura = A4
        y = altura - 50

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "Relatório de Fechamento de Caixa")
        y -= 30
        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Operador: {self.operador}")
        y -= 20
        c.drawString(50, y, f"Caixa ID: {self.caixa_id}")
        y -= 20
        c.drawString(50, y, f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        y -= 30
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Saldo Inicial: R$ {self.saldo_inicial:.2f}")
        y -= 30

        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, "Forma")
        c.drawString(200, y, "Sistema")
        c.drawString(320, y, "Conferido")
        c.drawString(440, y, "Diferença")
        y -= 10
        c.line(50, y, 550, y)
        y -= 20

        c.setFont("Helvetica", 11)
        for forma in self.formas_pagamento:
            sistema = self.formas_pagamento[forma]
            conferido = totais_digitados.get(forma, 0.0)
            diferenca = conferido - sistema

            c.drawString(50, y, forma)
            c.drawString(200, y, f"R$ {sistema:.2f}")
            c.drawString(320, y, f"R$ {conferido:.2f}")
            c.drawString(440, y, f"R$ {diferenca:.2f}")
            y -= 20

            if y < 100:
                c.showPage()
                y = altura - 50

        y -= 10
        c.line(50, y, 550, y)
        y -= 30
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Total Sistema: R$ {self.total_final:.2f}")
        y -= 20
        c.drawString(50, y, f"Total Conferido: R$ {total_digitado:.2f}")
        y -= 20
        situacao = "✅ OK - Bateu" if abs(total_digitado - self.total_final) < 0.01 else "❌ Diferença Detectada"
        c.drawString(50, y, f"Situação: {situacao}")
        y -= 50
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(50, y, "Gerado por Orbis Gestão")

        c.save()
        print(f"📄 Relatório salvo: {caminho}")

        # Abrir o PDF após salvar
        try:
            if os.name == 'nt':
                os.startfile(caminho)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", caminho])
            else:
                subprocess.Popen(["xdg-open", caminho])
        except Exception as e:
            print(f"Erro ao abrir PDF: {e}")
            messagebox.showwarning("Erro", "O relatório foi gerado, mas não foi possível abrir automaticamente.")

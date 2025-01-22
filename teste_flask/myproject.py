#!/usr/bin/env python3

from flask import Flask, render_template, send_file, request
import matplotlib.pyplot as plt
import numpy as np
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Image
from reportlab.lib.units import inch
import sys
import io
import os

template_dir = os.path.join(os.getenv("SNAP"), "templates")

data_dir=""
sock_dir = os.getenv("SNAP_DATA") + "/package-run/testeflask/"
if not os.path.exists(sock_dir):
    os.makedirs(sock_dir)


def criarDiretorio():
    global data_dir
    data_dir = os.path.join(os.getenv("SNAP_COMMON"), "solutions", "activeConfiguration","DadosRelatorios")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

criarDiretorio()

def testeMatplot(x,y):
    global data_dir
    plt.plot(x,y)
    #plt.savefig(f"{data_dir}/teste.png",format="png")
    buffer = io.BytesIO()
    plt.savefig(buffer,format="png")
    return buffer

# Leitura do arquivo gerado pelo NodeRed com os dados lidos do PLC
def lerVariaveis(nomeArquivo):
    with open(f"{data_dir}/{nomeArquivo}.txt",'r') as f:
        a=f.readlines()
    return a

# Rodapé com bordas
def adicionar_rodape(canvas, doc):
    largura, altura = letter
    canvas.setStrokeColor(colors.black)
    canvas.setLineWidth(1)
    # Desenha as bordas
    canvas.rect(0, 0, largura, 50)
    # Adiciona o texto no rodapé
    canvas.setFont('Helvetica', 10)
    texto_rodape = "Relatório 1"
    canvas.drawString(largura - 100, 10, texto_rodape)

app=Flask(__name__, template_folder=template_dir)

@app.route('/testeflask')
def index():
    x=lerVariaveis()
    x_json = json.loads(x[0])
    x1=x_json['curva1_x']
    y1=x_json['curva1_y']
    testeMatplot(x1,y1)
    return x_json

@app.route('/testeflask/relatorio')
def relatorio():
    nomeArquivo = request.args.get("nome","x.pdf")
    x=lerVariaveis(nomeArquivo)
    x_json = json.loads(x[0])
    x1=x_json['curva1_x']
    y1=x_json['curva1_y']
    plt.plot(x1,y1)
    grafico_filename = io.BytesIO()
    plt.savefig(grafico_filename, format="png")
    plt.close()
    # Criando o arquivo PDF
    pdf_filename = f"{data_dir}/relatorio_completo.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    elements = []
    # Para inserir o gráfico como uma imagem no PDF, usamos o método `drawImage`
    grafico_img = Image(grafico_filename, width=400, height=300)
    elements.append(grafico_img)
    doc.build(elements, onFirstPage=adicionar_rodape, onLaterPages=adicionar_rodape)
    return render_template('index.html')
@app.route("/testeflask/pdf")
def serve_pdf():
    PDF_FILE_PATH = f"{data_dir}/relatorio_completo.pdf"
    return send_file(PDF_FILE_PATH, as_attachment=False)

if __name__=='__main__':
    #app.run('0.0.0.0',port=8080)
    app.run(host=f"unix:///{sock_dir}/web.sock")
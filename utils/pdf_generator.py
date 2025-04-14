from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfReader, PdfWriter
import io
import os

# Registrar a fonte Times New Roman (assumindo que está disponível no sistema)
def register_fonts():
    try:
        pdfmetrics.registerFont(TTFont('Times-Roman', 'Times-Roman'))
    except:
        # Fallback para a fonte padrão se Times New Roman não estiver disponível
        pass

def create_dispatch_pdf(text):
    """
    Cria um PDF de despacho com a formatação especificada.
    
    Args:
        text (str): Texto do despacho
        
    Returns:
        bytes: PDF gerado em bytes
    """
    register_fonts()
    
    # Criar buffer para o PDF
    buffer = io.BytesIO()
    
    # Configurar o tamanho da página e margens
    page_width, page_height = A4
    margin_top = 3 * cm
    margin_left = 3 * cm
    margin_right = 2 * cm
    margin_bottom = 2 * cm
    
    # Criar o canvas
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Adicionar cabeçalho
    header_path = "assets/niteroi_cabecalho.jpg"
    header_height = 0  # valor padrão caso a imagem não exista
    if os.path.exists(header_path):
        header_img = ImageReader(header_path)
        header_width = 8.02 * cm  # Largura de 8,02 cm
        header_height = 1.51 * cm  # Altura de 1,51 cm
        x_position = (page_width - header_width) / 2
        y_position = page_height - header_height - 1.2 * cm  # Adicionado espaço extra acima
        c.drawImage(header_img, x_position, y_position, 
                    width=header_width, height=header_height, preserveAspectRatio=True)
    else:
        # Se a imagem não estiver disponível, deixar um espaço para o cabeçalho
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(page_width / 2, page_height - margin_top / 2, "Secretaria da Fazenda de Niterói | SEREC")
    
    # Configurar fonte e tamanho para o corpo do texto
    try:
        c.setFont("Times-Roman", 14)
    except:
        c.setFont("Helvetica", 14)
    
    # Definir posição inicial para o texto
    text_top = page_height - margin_top - (header_height + 1.2 * cm if os.path.exists(header_path) else margin_top / 2) - 30
    text_width = page_width - margin_left - margin_right
    
    # Quebrar o texto em linhas
    lines = []
    for paragraph in text.split('\n'):
        if not paragraph:
            lines.append('')
        else:
            words = paragraph.split()
            line = ''
            for word in words:
                test_line = line + ' ' + word if line else word
                if c.stringWidth(test_line, "Times-Roman", 14) <= text_width:
                    line = test_line
                else:
                    lines.append(line)
                    line = word
            if line:
                lines.append(line)
    
    # Desenhar o texto
    y = text_top
    line_height = 20  # Ajustar conforme necessário
    for line in lines:
        if y < margin_bottom + 50:
            c.showPage()
            try:
                c.setFont("Times-Roman", 14)
            except:
                c.setFont("Helvetica", 14)
            y = page_height - margin_top - 30
        
        c.drawString(margin_left, y, line)
        y -= line_height
    
    # Adicionar rodapé
    footer_text = "Rua da Conceição, nº 100 – Centro – Niterói-RJ – CEP.: 24.020-084 Tel: (21) 2613-6617/2621-2990"
    try:
        c.setFont("Times-Roman", 9)
    except:
        c.setFont("Helvetica", 9)
    c.drawCentredString(page_width / 2, margin_bottom / 2, footer_text)
    
    # Finalizar o PDF
    c.save()
    
    # Retornar o buffer
    buffer.seek(0)
    return buffer.getvalue()

def merge_pdfs(pdf_paths, despacho_pdf):
    """
    Mescla vários PDFs e adiciona o despacho como a última página.
    
    Args:
        pdf_paths (list): Lista de caminhos para os PDFs a serem mesclados
        despacho_pdf (bytes): PDF do despacho em bytes
        
    Returns:
        bytes: PDF mesclado em bytes
    """
    merger = PdfWriter()
    
    # Adicionar os PDFs anexados
    for pdf_path in pdf_paths:
        pdf = PdfReader(open(pdf_path, 'rb'))
        for page in range(len(pdf.pages)):
            merger.add_page(pdf.pages[page])
    
    # Adicionar o PDF do despacho
    despacho_reader = PdfReader(io.BytesIO(despacho_pdf))
    for page in range(len(despacho_reader.pages)):
        merger.add_page(despacho_reader.pages[page])
    
    # Escrever o PDF final
    output = io.BytesIO()
    merger.write(output)
    output.seek(0)
    
    return output.getvalue()

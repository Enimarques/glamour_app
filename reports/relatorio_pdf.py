from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import os

class GeradorRelatorioPDF:
    """Classe para geração de relatórios em PDF."""
    
    def __init__(self, nome_arquivo: str):
        """
        Inicializa o gerador de relatórios.
        
        Args:
            nome_arquivo (str): Nome do arquivo PDF a ser gerado
        """
        # Cria diretório de relatórios se não existir
        diretorio = os.path.dirname(nome_arquivo)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)
            
        self.nome_arquivo = nome_arquivo
        self.doc = SimpleDocTemplate(nome_arquivo, pagesize=A4)
        self.story = []
        self.estilos = getSampleStyleSheet()
        
    def adicionar_titulo(self, titulo: str):
        """
        Adiciona um título ao relatório.
        
        Args:
            titulo (str): Texto do título
        """
        estilo_titulo = ParagraphStyle(
            'TituloCustomizado',
            parent=self.estilos['Heading1'],
            alignment=TA_CENTER,
            fontSize=18,
            spaceAfter=30
        )
        self.story.append(Paragraph(titulo, estilo_titulo))
        self.story.append(Spacer(1, 0.2*inch))
        
    def adicionar_subtitulo(self, subtitulo: str):
        """
        Adiciona um subtítulo ao relatório.
        
        Args:
            subtitulo (str): Texto do subtítulo
        """
        estilo_subtitulo = ParagraphStyle(
            'SubtituloCustomizado',
            parent=self.estilos['Heading2'],
            alignment=TA_LEFT,
            fontSize=14,
            spaceAfter=20
        )
        self.story.append(Paragraph(subtitulo, estilo_subtitulo))
        self.story.append(Spacer(1, 0.1*inch))
        
    def adicionar_paragrafo(self, texto: str):
        """
        Adiciona um parágrafo ao relatório.
        
        Args:
            texto (str): Texto do parágrafo
        """
        self.story.append(Paragraph(texto, self.estilos['Normal']))
        self.story.append(Spacer(1, 0.1*inch))
        
    def adicionar_tabela(self, dados: list, cabecalhos: list = None):
        """
        Adiciona uma tabela ao relatório.
        
        Args:
            dados (list): Lista de listas contendo os dados da tabela
            cabecalhos (list, opcional): Lista com os cabeçalhos da tabela
        """
        # Prepara os dados da tabela
        dados_tabela = []
        
        # Adiciona cabeçalhos se fornecidos
        if cabecalhos:
            dados_tabela.append(cabecalhos)
            
        # Adiciona os dados
        dados_tabela.extend(dados)
        
        # Cria a tabela
        tabela = Table(dados_tabela)
        
        # Define o estilo da tabela
        estilo_tabela = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        
        tabela.setStyle(estilo_tabela)
        
        # Adiciona a tabela ao documento
        self.story.append(tabela)
        self.story.append(Spacer(1, 0.2*inch))
        
    def adicionar_rodape(self):
        """Adiciona um rodapé com data e hora de geração."""
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        rodape = f"Relatório gerado em: {data_hora}"
        
        estilo_rodape = ParagraphStyle(
            'RodapeCustomizado',
            parent=self.estilos['Normal'],
            alignment=TA_CENTER,
            textColor=colors.grey,
            fontSize=10
        )
        
        self.story.append(Spacer(1, 0.5*inch))
        self.story.append(Paragraph(rodape, estilo_rodape))
        
    def gerar(self):
        """Gera o arquivo PDF."""
        self.doc.build(self.story)
        return self.nome_arquivo
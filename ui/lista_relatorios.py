from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMessageBox, QAbstractItemView, QLabel, QLineEdit,
                             QComboBox, QDateEdit, QSpacerItem, QSizePolicy,
                             QGroupBox, QTextEdit)
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtGui import QFont, QColor
from reports.relatorio_financeiro import RelatorioFinanceiro
from reports.catalogo_produtos import CatalogoProdutos
from datetime import datetime
import os

class ListaRelatorios(QWidget):
    """Widget para exibir e gerenciar a lista de relatórios."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.inicializar_ui()
        
    def inicializar_ui(self):
        """Inicializa a interface do usuário."""
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)
        
        # Título
        lbl_titulo = QLabel("Relatórios")
        lbl_titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 20px;
        """)
        layout_principal.addWidget(lbl_titulo)
        
        # Grupo de relatórios financeiros
        self.criar_grupo_relatorios_financeiros(layout_principal)
        
        # Grupo de catálogos de produtos
        self.criar_grupo_catalogos(layout_principal)
        
        # Área de visualização de status
        self.criar_area_status(layout_principal)
        
        # Aplicar estilo
        self.aplicar_estilo()
        
    def criar_grupo_relatorios_financeiros(self, layout_principal):
        """Cria o grupo de relatórios financeiros."""
        grupo_financeiro = QGroupBox("Relatórios Financeiros")
        layout_grupo = QVBoxLayout(grupo_financeiro)
        
        # Período
        layout_periodo = QHBoxLayout()
        layout_periodo.addWidget(QLabel("Período:"))
        
        self.data_inicio = QDateEdit()
        self.data_inicio.setDate(QDate.currentDate().addMonths(-1))  # Mês anterior
        self.data_inicio.setDisplayFormat("dd/MM/yyyy")
        layout_periodo.addWidget(self.data_inicio)
        
        layout_periodo.addWidget(QLabel("até"))
        
        self.data_fim = QDateEdit()
        self.data_fim.setDate(QDate.currentDate())  # Hoje
        self.data_fim.setDisplayFormat("dd/MM/yyyy")
        layout_periodo.addWidget(self.data_fim)
        
        layout_periodo.addStretch()
        layout_grupo.addLayout(layout_periodo)
        
        # Botões de relatórios financeiros
        layout_botoes = QHBoxLayout()
        
        self.btn_relatorio_detalhado = QPushButton("Relatório Financeiro Detalhado")
        self.btn_relatorio_detalhado.clicked.connect(self.gerar_relatorio_financeiro_detalhado)
        layout_botoes.addWidget(self.btn_relatorio_detalhado)
        
        self.btn_relatorio_simplificado = QPushButton("Relatório Financeiro Simplificado")
        self.btn_relatorio_simplificado.clicked.connect(self.gerar_relatorio_financeiro_simplificado)
        layout_botoes.addWidget(self.btn_relatorio_simplificado)
        
        layout_botoes.addStretch()
        layout_grupo.addLayout(layout_botoes)
        
        layout_principal.addWidget(grupo_financeiro)
        
    def criar_grupo_catalogos(self, layout_principal):
        """Cria o grupo de catálogos de produtos."""
        grupo_catalogos = QGroupBox("Catálogos de Produtos")
        layout_grupo = QVBoxLayout(grupo_catalogos)
        
        # Descrição
        lbl_descricao = QLabel("Gerar catálogos de produtos para distribuição.")
        lbl_descricao.setStyleSheet("color: #666666;")
        layout_grupo.addWidget(lbl_descricao)
        
        # Botões de catálogos
        layout_botoes = QHBoxLayout()
        
        self.btn_catalogo_detalhado = QPushButton("Catálogo Detalhado")
        self.btn_catalogo_detalhado.clicked.connect(self.gerar_catalogo_detalhado)
        layout_botoes.addWidget(self.btn_catalogo_detalhado)
        
        self.btn_catalogo_simples = QPushButton("Catálogo Simples")
        self.btn_catalogo_simples.clicked.connect(self.gerar_catalogo_simples)
        layout_botoes.addWidget(self.btn_catalogo_simples)
        
        layout_botoes.addStretch()
        layout_grupo.addLayout(layout_botoes)
        
        layout_principal.addWidget(grupo_catalogos)
        
    def criar_area_status(self, layout_principal):
        """Cria a área de visualização de status."""
        self.area_status = QTextEdit()
        self.area_status.setMaximumHeight(100)
        self.area_status.setReadOnly(True)
        self.area_status.setStyleSheet("""
            QTextEdit {
                background-color: #F8F9FA;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                padding: 10px;
                font-family: monospace;
            }
        """)
        self.area_status.setPlaceholderText("Status dos relatórios gerados aparecerá aqui...")
        layout_principal.addWidget(self.area_status)
        
    def aplicar_estilo(self):
        """Aplica o estilo moderno aos elementos."""
        estilo = """
        QGroupBox {
            font-weight: bold;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            margin-top: 1ex;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
            color: #4A90E2;
        }
        
        QPushButton {
            background-color: #4A90E2;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 6px;
            font-weight: 500;
            min-width: 120px;
        }
        
        QPushButton:hover {
            background-color: #357ABD;
        }
        
        QPushButton:pressed {
            background-color: #2E6DA4;
        }
        
        QDateEdit {
            padding: 8px;
            border: 1px solid #E0E0E0;
            border-radius: 6px;
            background-color: white;
            min-width: 120px;
        }
        
        QDateEdit::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid #E0E0E0;
        }
        """
        self.setStyleSheet(estilo)
        
    def gerar_relatorio_financeiro_detalhado(self):
        """Gera o relatório financeiro detalhado."""
        try:
            # Converter datas
            data_inicio = self.data_inicio.date().toPyDate()
            data_fim = self.data_fim.date().toPyDate()
            
            # Validar período
            if data_inicio > data_fim:
                QMessageBox.warning(self, "Período Inválido", 
                                  "A data de início deve ser anterior à data de fim.")
                return
                
            # Gerar relatório
            caminho_arquivo = "relatorios/relatorio_financeiro_detalhado.pdf"
            caminho_completo = RelatorioFinanceiro.gerar_relatorio_financeiro(
                periodo_inicio=data_inicio,
                periodo_fim=data_fim,
                caminho_arquivo=caminho_arquivo
            )
            
            # Mostrar mensagem de sucesso
            self.mostrar_status(f"✓ Relatório financeiro detalhado gerado com sucesso!\nSalvo em: {caminho_completo}")
            QMessageBox.information(self, "Sucesso", 
                                  f"Relatório gerado com sucesso!\n\nSalvo em: {caminho_completo}")
            
        except Exception as e:
            erro_msg = f"Erro ao gerar relatório: {str(e)}"
            self.mostrar_status(f"✗ {erro_msg}")
            QMessageBox.critical(self, "Erro", erro_msg)
            
    def gerar_relatorio_financeiro_simplificado(self):
        """Gera o relatório financeiro simplificado."""
        try:
            # Gerar relatório
            caminho_arquivo = "relatorios/relatorio_financeiro_simplificado.pdf"
            caminho_completo = RelatorioFinanceiro.gerar_relatorio_simplificado(
                caminho_arquivo=caminho_arquivo
            )
            
            # Mostrar mensagem de sucesso
            self.mostrar_status(f"✓ Relatório financeiro simplificado gerado com sucesso!\nSalvo em: {caminho_completo}")
            QMessageBox.information(self, "Sucesso", 
                                  f"Relatório gerado com sucesso!\n\nSalvo em: {caminho_completo}")
            
        except Exception as e:
            erro_msg = f"Erro ao gerar relatório: {str(e)}"
            self.mostrar_status(f"✗ {erro_msg}")
            QMessageBox.critical(self, "Erro", erro_msg)
            
    def gerar_catalogo_detalhado(self):
        """Gera o catálogo de produtos detalhado."""
        try:
            # Gerar catálogo
            caminho_arquivo = "relatorios/catalogo_produtos_detalhado.pdf"
            caminho_completo = CatalogoProdutos.gerar_catalogo(
                caminho_arquivo=caminho_arquivo
            )
            
            # Mostrar mensagem de sucesso
            self.mostrar_status(f"✓ Catálogo de produtos detalhado gerado com sucesso!\nSalvo em: {caminho_completo}")
            QMessageBox.information(self, "Sucesso", 
                                  f"Catálogo gerado com sucesso!\n\nSalvo em: {caminho_completo}")
            
        except Exception as e:
            erro_msg = f"Erro ao gerar catálogo: {str(e)}"
            self.mostrar_status(f"✗ {erro_msg}")
            QMessageBox.critical(self, "Erro", erro_msg)
            
    def gerar_catalogo_simples(self):
        """Gera o catálogo de produtos simples."""
        try:
            # Gerar catálogo
            caminho_arquivo = "relatorios/catalogo_produtos_simples.pdf"
            caminho_completo = CatalogoProdutos.gerar_catalogo_simples(
                caminho_arquivo=caminho_arquivo
            )
            
            # Mostrar mensagem de sucesso
            self.mostrar_status(f"✓ Catálogo de produtos simples gerado com sucesso!\nSalvo em: {caminho_completo}")
            QMessageBox.information(self, "Sucesso", 
                                  f"Catálogo gerado com sucesso!\n\nSalvo em: {caminho_completo}")
            
        except Exception as e:
            erro_msg = f"Erro ao gerar catálogo: {str(e)}"
            self.mostrar_status(f"✗ {erro_msg}")
            QMessageBox.critical(self, "Erro", erro_msg)
            
    def mostrar_status(self, mensagem):
        """Mostra uma mensagem na área de status."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        texto_atual = self.area_status.toPlainText()
        novo_texto = f"[{timestamp}] {mensagem}\n" + (texto_atual if texto_atual else "")
        self.area_status.setPlainText(novo_texto)
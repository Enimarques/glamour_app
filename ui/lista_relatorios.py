from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMessageBox, QAbstractItemView, QLabel, QLineEdit,
                             QComboBox, QDateEdit, QSpacerItem, QSizePolicy,
                             QGroupBox, QTextEdit, QFrame)
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
        self.total_gerados = 0
        self.total_erros = 0
        self.inicializar_ui()
        
    def inicializar_ui(self):
        """Inicializa a interface do usuário."""
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)
        
        # Cabeçalho da página
        self.criar_cabecalho_pagina(layout_principal)
        
        # Barra de ferramentas
        self.criar_barra_ferramentas(layout_principal)
        
        # Cards de resumo
        self.criar_cards_resumo(layout_principal)
        
        # Grupo de relatórios financeiros
        self.criar_grupo_relatorios_financeiros(layout_principal)
        
        # Grupo de catálogos de produtos
        self.criar_grupo_catalogos(layout_principal)
        
        # Área de visualização de status
        self.criar_area_status(layout_principal)
        
    def criar_cabecalho_pagina(self, layout_principal):
        """Cria o cabeçalho da página com título e breadcrumb."""
        layout_header = QHBoxLayout()
        
        # Layout para ícone + título
        layout_titulo = QHBoxLayout()
        
        lbl_icone = QLabel("📊")
        lbl_icone.setObjectName("breadcrumb_icon")
        layout_titulo.addWidget(lbl_icone)
        
        lbl_titulo = QLabel("Relatórios")
        lbl_titulo.setObjectName("page_title")
        layout_titulo.addWidget(lbl_titulo)
        
        layout_titulo.addStretch()
        layout_header.addLayout(layout_titulo)
        
        # Breadcrumb
        layout_breadcrumb = QHBoxLayout()
        layout_breadcrumb.addStretch()
        
        lbl_home = QLabel("🏠 Início")
        lbl_home.setObjectName("breadcrumb")
        lbl_home.setCursor(Qt.PointingHandCursor)
        layout_breadcrumb.addWidget(lbl_home)
        
        lbl_sep1 = QLabel(" › ")
        lbl_sep1.setObjectName("breadcrumb")
        layout_breadcrumb.addWidget(lbl_sep1)
        
        lbl_atual = QLabel("Relatórios")
        lbl_atual.setObjectName("breadcrumb")
        layout_breadcrumb.addWidget(lbl_atual)
        
        layout_header.addLayout(layout_breadcrumb)
        layout_principal.addLayout(layout_header)

    def criar_barra_ferramentas(self, layout_principal):
        """Cria a barra de ferramentas com ações e filtros."""
        frame_toolbar = QFrame()
        frame_toolbar.setObjectName("toolbar_header")
        layout_toolbar = QHBoxLayout(frame_toolbar)
        layout_toolbar.setContentsMargins(10, 10, 10, 10)
        layout_toolbar.setSpacing(15)
        
        # Botões de ação rápida
        btn_financeiro = QPushButton("💰 Resumo Financeiro")
        btn_financeiro.setObjectName("btn_adicionar")
        btn_financeiro.clicked.connect(self.gerar_relatorio_financeiro_simplificado)
        layout_toolbar.addWidget(btn_financeiro)
        
        btn_catalogo = QPushButton("📖 Catálogo Rápido")
        btn_catalogo.setObjectName("secondary")
        btn_catalogo.clicked.connect(self.gerar_catalogo_simples)
        layout_toolbar.addWidget(btn_catalogo)
        
        layout_toolbar.addStretch()
        
        # Botão limpar logs
        btn_limpar = QPushButton("🗑 Limpar Logs")
        btn_limpar.setObjectName("btn_action_delete")
        btn_limpar.setFixedWidth(120)
        btn_limpar.clicked.connect(lambda: self.area_status.clear())
        layout_toolbar.addWidget(btn_limpar)
        
        layout_principal.addWidget(frame_toolbar)

    def criar_cards_resumo(self, layout_principal):
        """Cria os cards de resumo."""
        layout_cards = QHBoxLayout()
        layout_cards.setSpacing(15)
        
        # Card Relatórios Gerados
        self.card_total = self.criar_card_resumo(
            "Relatórios Gerados", "0", "📄", "summary_card_total"
        )
        layout_cards.addWidget(self.card_total)
        
        # Card Último Relatório
        self.card_ultimo = self.criar_card_resumo(
            "Último Acesso", "--:--", "🕒", "summary_card_recebidos"
        )
        layout_cards.addWidget(self.card_ultimo)
        
        # Card Erros
        self.card_erros = self.criar_card_resumo(
            "Erros de Geração", "0", "⚠", "summary_card_vencem_hoje"
        )
        layout_cards.addWidget(self.card_erros)
        
        layout_principal.addLayout(layout_cards)

    def criar_card_resumo(self, titulo, valor, icone, object_name):
        """Cria um card de resumo."""
        frame = QFrame()
        frame.setObjectName(object_name)
        frame.setMinimumHeight(100)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Header
        layout_header = QHBoxLayout()
        
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setObjectName("summary_card_title")
        layout_header.addWidget(lbl_titulo)
        
        lbl_icone = QLabel(icone)
        lbl_icone.setObjectName("summary_card_icon")
        layout_header.addWidget(lbl_icone)
        
        layout.addLayout(layout_header)
        
        # Valor
        lbl_valor = QLabel(valor)
        lbl_valor.setObjectName("summary_card_value")
        layout.addWidget(lbl_valor)
        
        layout.addStretch()
        
        return frame
        
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
        self.btn_relatorio_detalhado.setObjectName("primary")
        self.btn_relatorio_detalhado.clicked.connect(self.gerar_relatorio_financeiro_detalhado)
        layout_botoes.addWidget(self.btn_relatorio_detalhado)
        
        self.btn_relatorio_simplificado = QPushButton("Relatório Financeiro Simplificado")
        self.btn_relatorio_simplificado.setObjectName("secondary")
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
        lbl_descricao.setObjectName("subtitulo")
        layout_grupo.addWidget(lbl_descricao)
        
        # Botões de catálogos
        layout_botoes = QHBoxLayout()
        
        self.btn_catalogo_detalhado = QPushButton("Catálogo Detalhado")
        self.btn_catalogo_detalhado.setObjectName("primary")
        self.btn_catalogo_detalhado.clicked.connect(self.gerar_catalogo_detalhado)
        layout_botoes.addWidget(self.btn_catalogo_detalhado)
        
        self.btn_catalogo_simples = QPushButton("Catálogo Simples")
        self.btn_catalogo_simples.setObjectName("secondary")
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
        self.area_status.setPlaceholderText("Status dos relatórios gerados aparecerá aqui...")
        layout_principal.addWidget(self.area_status)
        
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
        
        # Atualizar cards
        if "✓" in mensagem:
            self.total_gerados += 1
            self.atualizar_card_valor(self.card_total, str(self.total_gerados))
            self.atualizar_card_valor(self.card_ultimo, timestamp)
        elif "✗" in mensagem:
            self.total_erros += 1
            self.atualizar_card_valor(self.card_erros, str(self.total_erros))

    def atualizar_card_valor(self, card, valor):
        """Atualiza o valor em um card de resumo."""
        layout = card.layout()
        if layout and layout.count() >= 2:
            item_valor = layout.itemAt(1)
            if item_valor:
                lbl_valor = item_valor.widget()
                if lbl_valor:
                    lbl_valor.setText(valor)
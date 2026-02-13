from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMessageBox, QAbstractItemView, QLabel, QLineEdit,
                             QSpacerItem, QSizePolicy, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor
from controllers.consignacao_controller import ConsignacaoController
from ui.formulario_consignacao import FormularioConsignacao

class ListaConsignacoes(QWidget):
    """Widget para exibir e gerenciar a lista de consignações."""
    
    consignacoes_atualizadas = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.consignacoes = []
        self.consignacoes_filtradas = []
        self.inicializar_ui()
        self.carregar_consignacoes()
        
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
        
        # Tabela de consignações
        self.criar_tabela_consignacoes(layout_principal)
        
    def criar_cabecalho_pagina(self, layout_principal):
        """Cria o cabeçalho da página com título e breadcrumb."""
        layout_header = QHBoxLayout()
        
        # Layout para ícone + título
        layout_titulo = QHBoxLayout()
        
        lbl_icone = QLabel("📦")
        lbl_icone.setObjectName("breadcrumb_icon")
        layout_titulo.addWidget(lbl_icone)
        
        lbl_titulo = QLabel("Consignações")
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
        
        lbl_atual = QLabel("Consignações")
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
        
        # Botões de ação
        btn_nova = QPushButton("✚ Nova Consignação")
        btn_nova.setObjectName("btn_adicionar")
        btn_nova.clicked.connect(self.nova_consignacao)
        layout_toolbar.addWidget(btn_nova)
        
        btn_atualizar = QPushButton("🔄 Atualizar")
        btn_atualizar.setObjectName("btn_mais_acoes")
        btn_atualizar.clicked.connect(self.carregar_consignacoes)
        layout_toolbar.addWidget(btn_atualizar)
        
        layout_toolbar.addStretch()
        
        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("🔍 Buscar por revendedora...")
        self.campo_busca.setMinimumWidth(300)
        # self.campo_busca.textChanged.connect(self.filtrar_consignacoes) # To be implemented if needed
        layout_toolbar.addWidget(self.campo_busca)
        
        layout_principal.addWidget(frame_toolbar)

    def criar_cards_resumo(self, layout_principal):
        """Cria cards de resumo para as consignações."""
        layout_cards = QHBoxLayout()
        layout_cards.setSpacing(20)
        
        # Card Consignações Abertas
        self.card_abertas = self.criar_card_estilizado(
            "Consignações Abertas", "0", "🔓", "summary_card_a_vencer"
        )
        layout_cards.addWidget(self.card_abertas)
        
        # Card Total em Consignação
        self.card_total_consignado = self.criar_card_estilizado(
            "Total Consignado", "R$ 0,00", "💰", "summary_card_total"
        )
        layout_cards.addWidget(self.card_total_consignado)
        
        # Card Total Vendido
        self.card_total_vendido = self.criar_card_estilizado(
            "Total Vendido", "R$ 0,00", "📈", "summary_card_recebidos"
        )
        layout_cards.addWidget(self.card_total_vendido)
        
        layout_principal.addLayout(layout_cards)

    def criar_card_estilizado(self, titulo, valor, icone, object_name):
        """Auxiliar para criar cards de resumo estilizados."""
        frame = QFrame()
        frame.setObjectName(object_name)
        frame.setMinimumHeight(100)
        
        layout = QVBoxLayout(frame)
        
        # Linha superior (Ícone e Título)
        layout_top = QHBoxLayout()
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setObjectName("summary_card_title")
        layout_top.addWidget(lbl_titulo)
        
        layout_top.addStretch()
        
        lbl_icone = QLabel(icone)
        lbl_icone.setObjectName("summary_card_icon")
        layout_top.addWidget(lbl_icone)
        layout.addLayout(layout_top)
        
        # Valor
        lbl_valor = QLabel(valor)
        lbl_valor.setObjectName("summary_card_value")
        # Armazena a referência para atualização posterior
        if titulo == "Consignações Abertas": self.lbl_abertas = lbl_valor
        elif titulo == "Total Consignado": self.lbl_total_consignado = lbl_valor
        elif titulo == "Total Vendido": self.lbl_total_vendido = lbl_valor
        
        layout.addWidget(lbl_valor)
        
        return frame

    def criar_tabela_consignacoes(self, layout_principal):
        """Cria a tabela de consignações."""
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(7)
        self.tabela.setHorizontalHeaderLabels([
            "ID", "Revendedora", "Data Envio", "Status", "Total Vendido", "Total Líquido", "Ações"
        ])
        
        # Configurações da tabela
        self.tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabela.setAlternatingRowColors(True)
        self.tabela.setShowGrid(False)
        
        # Configurar cabeçalho
        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        
        # Altura das linhas
        self.tabela.verticalHeader().setDefaultSectionSize(50)
        
        layout_principal.addWidget(self.tabela)
        
    def carregar_consignacoes(self):
        """Carrega a lista de consignações do banco de dados."""
        try:
            self.consignacoes = ConsignacaoController.listar_consignacoes()
            self.atualizar_tabela()
            self.atualizar_cards_resumo()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar as consignações:\n{str(e)}")
            
    def atualizar_cards_resumo(self):
        """Atualiza os valores nos cards de resumo."""
        abertas = len([c for c in self.consignacoes if c.status == "Aberta"])
        total_vendido = sum(c.total_vendido for c in self.consignacoes)
        
        # Calcular total consignado (soma de itens de consignações abertas)
        total_consignado = 0
        for c in self.consignacoes:
            if c.status == "Aberta":
                for item in c.itens:
                    total_consignado += item.qtd_enviada * item.preco_unitario
        
        self.lbl_abertas.setText(str(abertas))
        self.lbl_total_consignado.setText(f"R$ {total_consignado:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        self.lbl_total_vendido.setText(f"R$ {total_vendido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    def atualizar_tabela(self):
        """Atualiza a tabela com as consignações."""
        self.tabela.setRowCount(len(self.consignacoes))
        
        for linha, consig in enumerate(self.consignacoes):
            # ID
            item_id = QTableWidgetItem(str(consig.id))
            item_id.setTextAlignment(Qt.AlignCenter)
            self.tabela.setItem(linha, 0, item_id)
            
            # Revendedora
            nome_cliente = consig.cliente.nome if consig.cliente else f"ID {consig.cliente_id}"
            self.tabela.setItem(linha, 1, QTableWidgetItem(nome_cliente))
            
            # Data Envio
            self.tabela.setItem(linha, 2, QTableWidgetItem(str(consig.data_envio)))
            
            # Status
            widget_status = QWidget()
            layout_status = QHBoxLayout(widget_status)
            layout_status.setContentsMargins(5, 5, 5, 5)
            
            lbl_status = QLabel(consig.status)
            lbl_status.setAlignment(Qt.AlignCenter)
            if consig.status == "Aberta":
                lbl_status.setObjectName("badge_em_aberto")
            elif consig.status == "Parcial":
                lbl_status.setObjectName("badge_pendente")
            elif consig.status == "Fechada":
                lbl_status.setObjectName("badge_confirmado")
            
            layout_status.addWidget(lbl_status)
            self.tabela.setCellWidget(linha, 3, widget_status)
            
            # Totais
            item_vendido = QTableWidgetItem(f"R$ {consig.total_vendido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            item_vendido.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tabela.setItem(linha, 4, item_vendido)
            
            item_liquido = QTableWidgetItem(f"R$ {consig.total_liquido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            item_liquido.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tabela.setItem(linha, 5, item_liquido)
            
            # Ações
            widget_acoes = QWidget()
            layout_acoes = QHBoxLayout(widget_acoes)
            layout_acoes.setContentsMargins(10, 5, 10, 5)
            layout_acoes.setSpacing(8)
            
            btn_ver = QPushButton("⚙️")
            btn_ver.setObjectName("btn_action_more")
            btn_ver.setToolTip("Gerenciar Consignação")
            btn_ver.clicked.connect(lambda checked, c=consig: self.ver_consignacao(c))
            layout_acoes.addWidget(btn_ver)
            
            layout_acoes.addStretch()
            self.tabela.setCellWidget(linha, 6, widget_acoes)
            
    def nova_consignacao(self):
        """Abre o formulário para criar uma nova consignação."""
        formulario = FormularioConsignacao(parent=self)
        formulario.consignacao_salva.connect(self.consignacao_criada)
        if formulario.exec_():
            self.carregar_consignacoes()
            
    def ver_consignacao(self, consignacao):
        """Abre o formulário para ver/editar uma consignação."""
        formulario = FormularioConsignacao(consignacao=consignacao, parent=self)
        formulario.consignacao_salva.connect(self.consignacao_atualizada)
        if formulario.exec_():
            self.carregar_consignacoes()
            
    def consignacao_criada(self):
        QMessageBox.information(self, "Sucesso", "Consignação criada com sucesso.")
        
    def consignacao_atualizada(self):
        QMessageBox.information(self, "Sucesso", "Consignação atualizada com sucesso.")

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMessageBox, QAbstractItemView, QLabel, QLineEdit,
                             QComboBox, QDateEdit, QSpacerItem, QSizePolicy,
                             QGroupBox, QFrame, QMenu)
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtGui import QFont, QColor
from models.venda import Venda
from controllers.venda_controller import VendaController
from ui.formulario_venda import FormularioVenda
from datetime import datetime, date

class ListaVendas(QWidget):
    """Widget para exibir e gerenciar a lista de vendas."""
    
    # Sinal emitido quando a lista de vendas é atualizada
    vendas_atualizadas = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vendas = []
        self.vendas_filtradas = []
        self.inicializar_ui()
        self.carregar_vendas()
        
    def inicializar_ui(self):
        """Inicializa a interface do usuário."""
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)
        
        # Cabeçalho da página
        self.criar_cabecalho_pagina(layout_principal)
        
        # Barra de ferramentas e filtros
        self.criar_barra_ferramentas(layout_principal)
        
        # Cards de resumo
        self.criar_cards_resumo(layout_principal)
        
        # Tabela de vendas
        self.criar_tabela_vendas(layout_principal)
        
    def criar_cabecalho_pagina(self, layout_principal):
        """Cria o cabeçalho da página."""
        layout_header = QHBoxLayout()
        
        layout_titulo = QHBoxLayout()
        
        lbl_icone = QLabel("🛒")
        lbl_icone.setObjectName("breadcrumb_icon")
        layout_titulo.addWidget(lbl_icone)
        
        lbl_titulo = QLabel("Vendas")
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
        
        lbl_atual = QLabel("Vendas")
        lbl_atual.setObjectName("breadcrumb")
        layout_breadcrumb.addWidget(lbl_atual)
        
        lbl_sep2 = QLabel(" › ")
        lbl_sep2.setObjectName("breadcrumb")
        layout_breadcrumb.addWidget(lbl_sep2)
        
        lbl_listar = QLabel("Listar")
        lbl_listar.setObjectName("breadcrumb")
        layout_breadcrumb.addWidget(lbl_listar)
        
        layout_header.addLayout(layout_breadcrumb)
        layout_principal.addLayout(layout_header)
        
    def criar_barra_ferramentas(self, layout_principal):
        """Cria a barra de ferramentas."""
        frame_toolbar = QFrame()
        frame_toolbar.setObjectName("toolbar_header")
        layout_toolbar = QHBoxLayout(frame_toolbar)
        layout_toolbar.setContentsMargins(10, 10, 10, 10)
        layout_toolbar.setSpacing(15)
        
        # Botões de ação
        btn_adicionar = QPushButton("✚ Registrar Venda")
        btn_adicionar.setObjectName("btn_adicionar")
        btn_adicionar.clicked.connect(self.registrar_venda)
        layout_toolbar.addWidget(btn_adicionar)
        
        btn_mais_acoes = QPushButton("⚙ Mais ações ▼")
        btn_mais_acoes.setObjectName("btn_mais_acoes")
        btn_mais_acoes.clicked.connect(self.mostrar_mais_acoes)
        layout_toolbar.addWidget(btn_mais_acoes)
        
        layout_toolbar.addStretch()
        
        # Filtros rápidos
        lbl_periodo = QLabel("Período:")
        layout_toolbar.addWidget(lbl_periodo)
        
        self.date_inicio = QDateEdit()
        self.date_inicio.setDisplayFormat("dd/MM/yyyy")
        self.date_inicio.setDate(QDate.currentDate().addDays(-30))
        self.date_inicio.setCalendarPopup(True)
        self.date_inicio.dateChanged.connect(self.filtrar_vendas)
        layout_toolbar.addWidget(self.date_inicio)
        
        lbl_ate = QLabel("até")
        layout_toolbar.addWidget(lbl_ate)
        
        self.date_fim = QDateEdit()
        self.date_fim.setDisplayFormat("dd/MM/yyyy")
        self.date_fim.setDate(QDate.currentDate())
        self.date_fim.setCalendarPopup(True)
        self.date_fim.dateChanged.connect(self.filtrar_vendas)
        layout_toolbar.addWidget(self.date_fim)
        
        # Status
        self.combo_status = QComboBox()
        self.combo_status.addItem("Todos", "")
        self.combo_status.addItem("Pago", "pago")
        self.combo_status.addItem("Pendente", "pendente")
        self.combo_status.currentIndexChanged.connect(self.filtrar_vendas)
        layout_toolbar.addWidget(self.combo_status)
        
        # Busca
        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("🔍 Buscar por cliente...")
        self.campo_busca.setMaximumWidth(250)
        self.campo_busca.textChanged.connect(self.filtrar_vendas)
        layout_toolbar.addWidget(self.campo_busca)
        
        # Botão atualizar
        btn_atualizar = QPushButton("↻ Atualizar")
        btn_atualizar.setObjectName("secondary")
        btn_atualizar.clicked.connect(self.carregar_vendas)
        layout_toolbar.addWidget(btn_atualizar)
        
        layout_principal.addWidget(frame_toolbar)
        
    def criar_cards_resumo(self, layout_principal):
        """Cria os cards de resumo."""
        layout_cards = QHBoxLayout()
        layout_cards.setSpacing(15)
        
        # Card Total de Vendas
        self.card_total = self.criar_card_resumo(
            "Total de Vendas", "0", "🛒", "summary_card_total"
        )
        layout_cards.addWidget(self.card_total)
        
        # Card Vendas Pagas
        self.card_pagas = self.criar_card_resumo(
            "Vendas Pagas", "R$ 0,00", "✓", "summary_card_recebidos"
        )
        layout_cards.addWidget(self.card_pagas)
        
        # Card Vendas Pendentes
        self.card_pendentes = self.criar_card_resumo(
            "Vendas Pendentes", "R$ 0,00", "⏳", "summary_card_vencem_hoje"
        )
        layout_cards.addWidget(self.card_pendentes)
        
        # Card Valor Total
        self.card_valor_total = self.criar_card_resumo(
            "Valor Total", "R$ 0,00", "💰", "summary_card_a_vencer"
        )
        layout_cards.addWidget(self.card_valor_total)
        
        layout_principal.addLayout(layout_cards)
        
    def criar_card_resumo(self, titulo, valor, icone, object_name):
        """Cria um card de resumo."""
        frame = QFrame()
        frame.setObjectName(object_name)
        frame.setMinimumHeight(100)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)
        
        layout_header = QHBoxLayout()
        
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setObjectName("summary_card_title")
        layout_header.addWidget(lbl_titulo)
        
        lbl_icone = QLabel(icone)
        lbl_icone.setObjectName("summary_card_icon")
        layout_header.addWidget(lbl_icone)
        
        layout.addLayout(layout_header)
        
        lbl_valor = QLabel(valor)
        lbl_valor.setObjectName("summary_card_value")
        layout.addWidget(lbl_valor)
        
        layout.addStretch()
        
        return frame
        
    def criar_tabela_vendas(self, layout_principal):
        """Cria a tabela de vendas."""
        container_tabela = QFrame()
        container_tabela.setObjectName("container_card")
        layout_container = QVBoxLayout(container_tabela)
        layout_container.setContentsMargins(20, 20, 20, 20)
        
        self.tabela_vendas = QTableWidget()
        self.tabela_vendas.setColumnCount(7)
        self.tabela_vendas.setHorizontalHeaderLabels([
            "Código", "Data", "Cliente", "Valor Total", "Tipo", "Status", "Ações"
        ])
        
        # Configurações
        self.tabela_vendas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela_vendas.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela_vendas.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabela_vendas.setAlternatingRowColors(True)
        self.tabela_vendas.setShowGrid(False)
        self.tabela_vendas.verticalHeader().setVisible(False)
        
        # Configurar cabeçalho
        header = self.tabela_vendas.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Código
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Data
        header.setSectionResizeMode(2, QHeaderView.Stretch)           # Cliente
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Valor
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Tipo
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Status
        header.setSectionResizeMode(6, QHeaderView.Fixed)             # Ações
        header.resizeSection(6, 180)
        
        self.tabela_vendas.verticalHeader().setDefaultSectionSize(60)
        
        layout_container.addWidget(self.tabela_vendas)
        layout_principal.addWidget(container_tabela)
        
    def carregar_vendas(self):
        """Carrega a lista de vendas."""
        try:
            self.vendas = VendaController.listar_vendas()
            self.vendas_filtradas = self.vendas.copy()
            self.filtrar_vendas()
            self.atualizar_resumo()
            self.vendas_atualizadas.emit()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar as vendas:\n{str(e)}")
            
    def atualizar_resumo(self):
        """Atualiza os cards de resumo."""
        try:
            total_vendas = len(self.vendas_filtradas)
            valor_pagas = sum(v.valor_total for v in self.vendas_filtradas if v.status == "pago")
            valor_pendentes = sum(v.valor_total for v in self.vendas_filtradas if v.status == "pendente")
            valor_total = sum(v.valor_total for v in self.vendas_filtradas)
            
            self.atualizar_card_valor(self.card_total, str(total_vendas))
            self.atualizar_card_valor(self.card_pagas, f"R$ {valor_pagas:,.2f}")
            self.atualizar_card_valor(self.card_pendentes, f"R$ {valor_pendentes:,.2f}")
            self.atualizar_card_valor(self.card_valor_total, f"R$ {valor_total:,.2f}")
        except Exception as e:
            print(f"Erro ao atualizar resumo: {e}")
            
    def atualizar_card_valor(self, card, valor):
        """Atualiza o valor em um card."""
        layout = card.layout()
        if layout and layout.count() >= 2:
            item_valor = layout.itemAt(1)
            if item_valor:
                lbl_valor = item_valor.widget()
                if lbl_valor:
                    lbl_valor.setText(valor)
            
    def filtrar_vendas(self):
        """Filtra as vendas."""
        try:
            data_inicio = self.date_inicio.date().toPyDate()
            data_fim = self.date_fim.date().toPyDate()
            status = self.combo_status.currentData()
            termo_busca = self.campo_busca.text().lower()
            
            self.vendas_filtradas = self.vendas.copy()
            
            # Filtrar por data
            self.vendas_filtradas = [
                v for v in self.vendas_filtradas 
                if v.data_venda.date() >= data_inicio and v.data_venda.date() <= data_fim
            ]
            
            # Filtrar por status
            if status:
                self.vendas_filtradas = [
                    v for v in self.vendas_filtradas 
                    if v.status == status
                ]
                
            # Filtrar por busca
            if termo_busca:
                self.vendas_filtradas = [
                    v for v in self.vendas_filtradas 
                    if (v.cliente and termo_busca in v.cliente.nome.lower())
                ]
                
            self.atualizar_tabela()
            self.atualizar_resumo()
        except Exception as e:
            print(f"Erro ao filtrar vendas: {e}")
        
    def atualizar_tabela(self):
        """Atualiza a tabela de vendas."""
        self.tabela_vendas.setRowCount(len(self.vendas_filtradas))
        
        for linha, venda in enumerate(self.vendas_filtradas):
            # Código
            item_id = QTableWidgetItem(str(venda.id))
            item_id.setTextAlignment(Qt.AlignCenter)
            self.tabela_vendas.setItem(linha, 0, item_id)
            
            # Data
            data_formatada = venda.data_venda.strftime("%d/%m/%Y")
            item_data = QTableWidgetItem(data_formatada)
            item_data.setTextAlignment(Qt.AlignCenter)
            self.tabela_vendas.setItem(linha, 1, item_data)
            
            # Cliente
            nome_cliente = venda.cliente.nome if venda.cliente else "Não informado"
            item_cliente = QTableWidgetItem(nome_cliente)
            self.tabela_vendas.setItem(linha, 2, item_cliente)
            
            # Valor Total
            item_valor = QTableWidgetItem(f"R$ {venda.valor_total:.2f}")
            item_valor.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tabela_vendas.setItem(linha, 3, item_valor)
            
            # Tipo
            tipo = "Fiado" if venda.tipo_pagamento == "fiado" else "À Vista"
            item_tipo = QTableWidgetItem(tipo)
            item_tipo.setTextAlignment(Qt.AlignCenter)
            self.tabela_vendas.setItem(linha, 4, item_tipo)
            
            # Status
            widget_status = self.criar_badge_status(venda)
            self.tabela_vendas.setCellWidget(linha, 5, widget_status)
            
            # Ações
            widget_acoes = self.criar_widget_acoes(venda)
            self.tabela_vendas.setCellWidget(linha, 6, widget_acoes)
            
    def criar_badge_status(self, venda):
        """Cria o badge de status."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        
        if venda.status == "pago":
            badge = QLabel("Pago")
            badge.setObjectName("badge_confirmado")
        else:
            badge = QLabel("Pendente")
            badge.setObjectName("badge_pendente")
        
        badge.setAlignment(Qt.AlignCenter)
        layout.addWidget(badge)
        
        return widget
        
    def criar_widget_acoes(self, venda):
        """Cria o widget de ações."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignCenter)
        
        # Botão Visualizar
        btn_view = QPushButton("👁")
        btn_view.setObjectName("btn_action_view")
        btn_view.setToolTip("Visualizar detalhes")
        btn_view.clicked.connect(lambda: self.visualizar_venda(venda))
        layout.addWidget(btn_view)
        
        # Botão Editar (só se pendente)
        if venda.status == "pendente":
            btn_edit = QPushButton("✏")
            btn_edit.setObjectName("btn_action_edit")
            btn_edit.setToolTip("Editar venda")
            btn_edit.clicked.connect(lambda: self.editar_venda(venda))
            layout.addWidget(btn_edit)
        
        # Botão Excluir
        btn_delete = QPushButton("✖")
        btn_delete.setObjectName("btn_action_delete")
        btn_delete.setToolTip("Excluir venda")
        btn_delete.clicked.connect(lambda: self.excluir_venda(venda))
        layout.addWidget(btn_delete)
        
        # Botão Mais
        btn_more = QPushButton("⋮")
        btn_more.setObjectName("btn_action_more")
        btn_more.setToolTip("Mais ações")
        btn_more.clicked.connect(lambda: self.mais_acoes_item(venda))
        layout.addWidget(btn_more)
        
        return widget
        
    def registrar_venda(self):
        """Registra uma nova venda."""
        try:
            formulario = FormularioVenda(parent=self)
            formulario.venda_registrada.connect(self.venda_adicionada)
            if formulario.exec_():
                self.carregar_vendas()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível abrir o formulário:\n{str(e)}")
            
    def visualizar_venda(self, venda):
        """Visualiza uma venda."""
        try:
            formulario = FormularioVenda(venda=venda, parent=self)
            formulario.setModal(True)
            formulario.show()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível visualizar a venda:\n{str(e)}")
            
    def editar_venda(self, venda):
        """Edita uma venda."""
        QMessageBox.information(self, "Editar", "Função de edição em desenvolvimento.")
        
    def excluir_venda(self, venda):
        """Exclui uma venda."""
        resposta = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            f"Deseja realmente excluir a venda #{venda.id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if resposta == QMessageBox.Yes:
            QMessageBox.information(self, "Excluir", "Função de exclusão em desenvolvimento.")
            
    def mostrar_mais_acoes(self):
        """Mostra menu de mais ações."""
        try:
            menu = QMenu(self)
            menu.addAction("📊 Exportar para Excel")
            menu.addAction("📄 Exportar para PDF")
            menu.addAction("🖨 Imprimir relatório")
            menu.addSeparator()
            menu.addAction("📈 Gráfico de vendas")
            menu.addAction("📊 Relatório por período")
            
            btn = self.sender()
            if btn:
                menu.exec_(btn.mapToGlobal(btn.rect().bottomLeft()))
        except Exception as e:
            QMessageBox.information(self, "Mais Ações", "Menu de ações em desenvolvimento.")
            
    def mais_acoes_item(self, venda):
        """Mostra mais ações para uma venda."""
        try:
            menu = QMenu(self)
            
            if venda.status == "pendente":
                action_pagar = menu.addAction("💵 Registrar Pagamento")
                action_pagar.triggered.connect(lambda: self.registrar_pagamento(venda))
                menu.addSeparator()
            
            menu.addAction("📄 Imprimir recibo")
            menu.addAction("📧 Enviar por email")
            
            btn = self.sender()
            if btn:
                menu.exec_(btn.mapToGlobal(btn.rect().bottomLeft()))
        except Exception as e:
            if venda.status == "pendente":
                self.registrar_pagamento(venda)
            
    def registrar_pagamento(self, venda):
        """Registra pagamento de uma venda."""
        QMessageBox.information(self, "Pagamento", "Função de registro de pagamento em desenvolvimento.")
        
    def venda_adicionada(self, venda):
        """Callback para venda adicionada."""
        QMessageBox.information(self, "Sucesso", f"✓ Venda registrada com sucesso!\nID: {venda.id}")
        self.carregar_vendas()

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMessageBox, QAbstractItemView, QLabel, QLineEdit,
                             QSpacerItem, QSizePolicy, QFrame, QMenu)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from models.cliente import Cliente
from controllers.cliente_controller import ClienteController
from ui.formulario_cliente import FormularioCliente

class ListaClientes(QWidget):
    """Widget para exibir e gerenciar a lista de clientes."""
    
    # Sinal emitido quando a lista de clientes é atualizada
    clientes_atualizados = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clientes = []
        self.clientes_filtrados = []
        self.inicializar_ui()
        self.carregar_clientes()
        
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
        
        # Tabela de clientes
        self.criar_tabela_clientes(layout_principal)
        
    def criar_cabecalho_pagina(self, layout_principal):
        """Cria o cabeçalho da página com título e breadcrumb."""
        layout_header = QHBoxLayout()
        
        # Layout para ícone + título
        layout_titulo = QHBoxLayout()
        
        lbl_icone = QLabel("👥")
        lbl_icone.setObjectName("breadcrumb_icon")
        layout_titulo.addWidget(lbl_icone)
        
        lbl_titulo = QLabel("Clientes")
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
        
        lbl_atual = QLabel("Clientes")
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
        """Cria a barra de ferramentas com ações e filtros."""
        frame_toolbar = QFrame()
        frame_toolbar.setObjectName("toolbar_header")
        layout_toolbar = QHBoxLayout(frame_toolbar)
        layout_toolbar.setContentsMargins(10, 10, 10, 10)
        layout_toolbar.setSpacing(15)
        
        # Botões de ação
        btn_adicionar = QPushButton("✚ Adicionar Cliente")
        btn_adicionar.setObjectName("btn_adicionar")
        btn_adicionar.clicked.connect(self.adicionar_cliente)
        layout_toolbar.addWidget(btn_adicionar)
        
        btn_mais_acoes = QPushButton("⚙ Mais ações ▼")
        btn_mais_acoes.setObjectName("btn_mais_acoes")
        btn_mais_acoes.clicked.connect(self.mostrar_mais_acoes)
        layout_toolbar.addWidget(btn_mais_acoes)
        
        layout_toolbar.addStretch()
        
        # Campo de busca
        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("🔍 Buscar por nome, telefone ou email...")
        self.campo_busca.setMinimumWidth(300)
        self.campo_busca.textChanged.connect(self.filtrar_clientes)
        layout_toolbar.addWidget(self.campo_busca)
        
        # Botão atualizar
        btn_atualizar = QPushButton("↻ Atualizar")
        btn_atualizar.setObjectName("secondary")
        btn_atualizar.clicked.connect(self.carregar_clientes)
        layout_toolbar.addWidget(btn_atualizar)
        
        layout_principal.addWidget(frame_toolbar)
        
    def criar_cards_resumo(self, layout_principal):
        """Cria os cards de resumo."""
        layout_cards = QHBoxLayout()
        layout_cards.setSpacing(15)
        
        # Card Total de Clientes
        self.card_total = self.criar_card_resumo(
            "Total de Clientes", "0", "👥", "summary_card_total"
        )
        layout_cards.addWidget(self.card_total)
        
        # Card Clientes Ativos
        self.card_ativos = self.criar_card_resumo(
            "Clientes Ativos", "0", "✓", "summary_card_recebidos"
        )
        layout_cards.addWidget(self.card_ativos)
        
        # Card Clientes com Dívidas
        self.card_dividas = self.criar_card_resumo(
            "Com Dívidas", "0", "⚠", "summary_card_vencem_hoje"
        )
        layout_cards.addWidget(self.card_dividas)
        
        # Card Novos (este mês)
        self.card_novos = self.criar_card_resumo(
            "Novos este Mês", "0", "⭐", "summary_card_a_vencer"
        )
        layout_cards.addWidget(self.card_novos)
        
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
        
    def criar_tabela_clientes(self, layout_principal):
        """Cria a tabela de clientes."""
        container_tabela = QFrame()
        container_tabela.setObjectName("container_card")
        layout_container = QVBoxLayout(container_tabela)
        layout_container.setContentsMargins(20, 20, 20, 20)
        
        # Tabela
        self.tabela_clientes = QTableWidget()
        self.tabela_clientes.setColumnCount(6)
        self.tabela_clientes.setHorizontalHeaderLabels([
            "Código", "Nome", "Telefone", "Email", "Status", "Ações"
        ])
        
        # Configurações
        self.tabela_clientes.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela_clientes.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela_clientes.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabela_clientes.setAlternatingRowColors(True)
        self.tabela_clientes.setShowGrid(False)
        self.tabela_clientes.verticalHeader().setVisible(False)
        
        # Configurar cabeçalho
        header = self.tabela_clientes.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Código
        header.setSectionResizeMode(1, QHeaderView.Stretch)           # Nome
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Telefone
        header.setSectionResizeMode(3, QHeaderView.Stretch)           # Email
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Status
        header.setSectionResizeMode(5, QHeaderView.Fixed)             # Ações
        header.resizeSection(5, 180)
        
        self.tabela_clientes.verticalHeader().setDefaultSectionSize(60)
        
        layout_container.addWidget(self.tabela_clientes)
        layout_principal.addWidget(container_tabela)
        
    def carregar_clientes(self):
        """Carrega a lista de clientes."""
        try:
            self.clientes = ClienteController.listar_clientes()
            self.clientes_filtrados = self.clientes.copy()
            self.atualizar_resumo()
            self.atualizar_tabela()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar os clientes:\n{str(e)}")
            
    def atualizar_resumo(self):
        """Atualiza os cards de resumo."""
        try:
            total = len(self.clientes)
            # Por enquanto, todos são considerados ativos
            ativos = total
            # Implementar lógica de dívidas se necessário
            dividas = 0
            # Novos este mês (simplificado)
            novos = 0
            
            self.atualizar_card_valor(self.card_total, str(total))
            self.atualizar_card_valor(self.card_ativos, str(ativos))
            self.atualizar_card_valor(self.card_dividas, str(dividas))
            self.atualizar_card_valor(self.card_novos, str(novos))
        except Exception as e:
            print(f"Erro ao atualizar resumo: {e}")
            
    def atualizar_card_valor(self, card, valor):
        """Atualiza o valor em um card de resumo."""
        layout = card.layout()
        if layout and layout.count() >= 2:
            item_valor = layout.itemAt(1)
            if item_valor:
                lbl_valor = item_valor.widget()
                if lbl_valor:
                    lbl_valor.setText(valor)
                    
    def atualizar_tabela(self):
        """Atualiza a tabela de clientes."""
        self.tabela_clientes.setRowCount(len(self.clientes_filtrados))
        
        for linha, cliente in enumerate(self.clientes_filtrados):
            # Código
            item_codigo = QTableWidgetItem(str(cliente.id))
            item_codigo.setTextAlignment(Qt.AlignCenter)
            self.tabela_clientes.setItem(linha, 0, item_codigo)
            
            # Nome
            item_nome = QTableWidgetItem(cliente.nome)
            self.tabela_clientes.setItem(linha, 1, item_nome)
            
            # Telefone
            item_telefone = QTableWidgetItem(cliente.telefone or "---")
            item_telefone.setTextAlignment(Qt.AlignCenter)
            self.tabela_clientes.setItem(linha, 2, item_telefone)
            
            # Email
            item_email = QTableWidgetItem(cliente.email or "---")
            self.tabela_clientes.setItem(linha, 3, item_email)
            
            # Status
            widget_status = self.criar_badge_status(cliente)
            self.tabela_clientes.setCellWidget(linha, 4, widget_status)
            
            # Ações
            widget_acoes = self.criar_widget_acoes(cliente)
            self.tabela_clientes.setCellWidget(linha, 5, widget_acoes)
            
    def criar_badge_status(self, cliente):
        """Cria o badge de status."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        
        badge = QLabel("Ativo")
        badge.setObjectName("badge_confirmado")
        badge.setAlignment(Qt.AlignCenter)
        layout.addWidget(badge)
        
        return widget
        
    def criar_widget_acoes(self, cliente):
        """Cria o widget com botões de ação."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignCenter)
        
        # Botão Visualizar
        btn_view = QPushButton("👁")
        btn_view.setObjectName("btn_action_view")
        btn_view.setToolTip("Visualizar detalhes")
        btn_view.clicked.connect(lambda: self.visualizar_cliente(cliente))
        layout.addWidget(btn_view)
        
        # Botão Editar
        btn_edit = QPushButton("✏")
        btn_edit.setObjectName("btn_action_edit")
        btn_edit.setToolTip("Editar cliente")
        btn_edit.clicked.connect(lambda: self.editar_cliente(cliente))
        layout.addWidget(btn_edit)
        
        # Botão Excluir
        btn_delete = QPushButton("✖")
        btn_delete.setObjectName("btn_action_delete")
        btn_delete.setToolTip("Excluir cliente")
        btn_delete.clicked.connect(lambda: self.excluir_cliente(cliente))
        layout.addWidget(btn_delete)
        
        # Botão Mais
        btn_more = QPushButton("⋮")
        btn_more.setObjectName("btn_action_more")
        btn_more.setToolTip("Mais ações")
        btn_more.clicked.connect(lambda: self.mais_acoes_item(cliente))
        layout.addWidget(btn_more)
        
        return widget
        
    def filtrar_clientes(self):
        """Filtra a lista de clientes."""
        texto_busca = self.campo_busca.text().lower()
        
        if not texto_busca:
            self.clientes_filtrados = self.clientes.copy()
        else:
            self.clientes_filtrados = [
                c for c in self.clientes
                if (texto_busca in c.nome.lower() or
                    (c.telefone and texto_busca in c.telefone.lower()) or
                    (c.email and texto_busca in c.email.lower()))
            ]
        
        self.atualizar_tabela()
        
    def adicionar_cliente(self):
        """Adiciona um novo cliente."""
        formulario = FormularioCliente(parent=self)
        if formulario.exec_():
            self.carregar_clientes()
            self.clientes_atualizados.emit()
            
    def visualizar_cliente(self, cliente):
        """Visualiza detalhes do cliente."""
        formulario = FormularioCliente(cliente, self)
        formulario.exec_()
        
    def editar_cliente(self, cliente):
        """Edita um cliente."""
        formulario = FormularioCliente(cliente, self)
        if formulario.exec_():
            self.carregar_clientes()
            self.clientes_atualizados.emit()
            
    def excluir_cliente(self, cliente):
        """Exclui um cliente."""
        resposta = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            f"Deseja realmente excluir o cliente '{cliente.nome}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if resposta == QMessageBox.Yes:
            try:
                ClienteController.excluir_cliente(cliente.id)
                QMessageBox.information(self, "Sucesso", "Cliente excluído com sucesso!")
                self.carregar_clientes()
                self.clientes_atualizados.emit()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Não foi possível excluir o cliente:\n{str(e)}")
                
    def mostrar_mais_acoes(self):
        """Mostra menu de mais ações."""
        try:
            menu = QMenu(self)
            menu.addAction("📊 Exportar para Excel")
            menu.addAction("📄 Exportar para PDF")
            menu.addAction("🖨 Imprimir lista")
            menu.addSeparator()
            menu.addAction("📧 Enviar email em massa")
            menu.addAction("💬 Enviar SMS em massa")
            
            btn = self.sender()
            if btn:
                menu.exec_(btn.mapToGlobal(btn.rect().bottomLeft()))
        except Exception as e:
            QMessageBox.information(self, "Mais Ações", "Menu de ações em desenvolvimento.")
            
    def mais_acoes_item(self, cliente):
        """Mostra mais ações para um cliente."""
        try:
            menu = QMenu(self)
            
            action_vendas = menu.addAction("🛒 Ver vendas")
            action_vendas.triggered.connect(lambda: self.ver_vendas_cliente(cliente))
            
            action_dividas = menu.addAction("💵 Ver dívidas")
            action_dividas.triggered.connect(lambda: self.ver_dividas_cliente(cliente))
            
            menu.addSeparator()
            menu.addAction("📧 Enviar email")
            menu.addAction("💬 Enviar SMS")
            
            btn = self.sender()
            if btn:
                menu.exec_(btn.mapToGlobal(btn.rect().bottomLeft()))
        except Exception as e:
            self.editar_cliente(cliente)
            
    def ver_vendas_cliente(self, cliente):
        """Mostra vendas do cliente."""
        try:
            janela = self.window()
            if hasattr(janela, "nav_list") and hasattr(janela, "lista_vendas"):
                janela.nav_list.setCurrentRow(3)
                vendas = janela.lista_vendas
                vendas.campo_busca.setText(cliente.nome)
                vendas.combo_status.setCurrentIndex(0)
                vendas.filtrar_vendas()
        except Exception:
            QMessageBox.information(self, "Vendas", f"Não foi possível abrir vendas para '{cliente.nome}'.")
        
    def ver_dividas_cliente(self, cliente):
        """Mostra dívidas do cliente."""
        try:
            janela = self.window()
            if hasattr(janela, "nav_list") and hasattr(janela, "lista_vendas"):
                janela.nav_list.setCurrentRow(3)
                vendas = janela.lista_vendas
                vendas.campo_busca.setText(cliente.nome)
                vendas.combo_status.setCurrentIndex(2)
                vendas.filtrar_vendas()
        except Exception:
            QMessageBox.information(self, "Dívidas", f"Não foi possível abrir dívidas para '{cliente.nome}'.")

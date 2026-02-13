from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMessageBox, QAbstractItemView, QLabel, QLineEdit,
                             QComboBox, QDateEdit, QSpacerItem, QSizePolicy,
                             QGroupBox, QTextEdit, QSpinBox, QProgressBar,
                             QTabWidget, QFrame, QScrollArea, QDialog, QFormLayout,
                             QDialogButtonBox, QDoubleSpinBox, QMenu)
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtGui import QFont, QColor, QBrush
from datetime import datetime, timedelta
from models.cliente import Cliente
from models.venda import Venda
from models.pagamento import Pagamento
from controllers.pagamento_controller import PagamentoController
from controllers.cliente_controller import ClienteController

class AbaCobrancas(QWidget):
    """Widget para exibir e gerenciar cobranças e dívidas pendentes."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dividas = []
        self.mes_atual = datetime.now().month
        self.ano_atual = datetime.now().year
        self.inicializar_ui()
        self.carregar_dividas()
        
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
        
        # Tabela de cobranças
        self.criar_tabela_cobrancas(layout_principal)
        
    def criar_cabecalho_pagina(self, layout_principal):
        """Cria o cabeçalho da página com título e breadcrumb."""
        layout_header = QHBoxLayout()
        
        # Layout vertical para ícone + título
        layout_titulo = QHBoxLayout()
        
        # Ícone (usando caractere Unicode)
        lbl_icone = QLabel("💰")
        lbl_icone.setObjectName("breadcrumb_icon")
        layout_titulo.addWidget(lbl_icone)
        
        # Título
        lbl_titulo = QLabel("Contas a receber")
        lbl_titulo.setObjectName("page_title")
        layout_titulo.addWidget(lbl_titulo)
        
        layout_titulo.addStretch()
        layout_header.addLayout(layout_titulo)
        
        # Breadcrumb/navegação
        layout_breadcrumb = QHBoxLayout()
        layout_breadcrumb.addStretch()
        
        lbl_home = QLabel("🏠 Início")
        lbl_home.setObjectName("breadcrumb")
        lbl_home.setCursor(Qt.PointingHandCursor)
        layout_breadcrumb.addWidget(lbl_home)
        
        lbl_sep1 = QLabel(" › ")
        lbl_sep1.setObjectName("breadcrumb")
        layout_breadcrumb.addWidget(lbl_sep1)
        
        lbl_atual = QLabel("Contas a receber")
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
        
        # Botões de ação à esquerda
        btn_adicionar = QPushButton("✚ Adicionar")
        btn_adicionar.setObjectName("btn_adicionar")
        btn_adicionar.clicked.connect(self.adicionar_cobranca)
        layout_toolbar.addWidget(btn_adicionar)
        
        btn_mais_acoes = QPushButton("⚙ Mais ações ▼")
        btn_mais_acoes.setObjectName("btn_mais_acoes")
        btn_mais_acoes.clicked.connect(self.mostrar_mais_acoes)
        layout_toolbar.addWidget(btn_mais_acoes)
        
        layout_toolbar.addStretch()
        
        # Seletor de mês
        self.combo_mes = QComboBox()
        self.combo_mes.setObjectName("month_selector")
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                 "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        for i, mes in enumerate(meses):
            self.combo_mes.addItem(f"{mes} de {self.ano_atual}", i + 1)
        self.combo_mes.setCurrentIndex(self.mes_atual - 1)
        self.combo_mes.currentIndexChanged.connect(self.filtrar_por_mes)
        layout_toolbar.addWidget(self.combo_mes)
        
        # Botão de busca avançada
        btn_busca = QPushButton("🔍 Busca avançada")
        btn_busca.setObjectName("btn_busca_avancada")
        btn_busca.clicked.connect(self.abrir_busca_avancada)
        layout_toolbar.addWidget(btn_busca)
        
        layout_principal.addWidget(frame_toolbar)
        
    def criar_cards_resumo(self, layout_principal):
        """Cria os cards de resumo das cobranças."""
        layout_cards = QHBoxLayout()
        layout_cards.setSpacing(15)
        
        # Card Vencidos
        self.card_vencidos = self.criar_card_resumo(
            "Vencidos", "0,00", "🔴", "summary_card_vencidos"
        )
        layout_cards.addWidget(self.card_vencidos)
        
        # Card Vencem Hoje
        self.card_vencem_hoje = self.criar_card_resumo(
            "Vencem hoje", "0,00", "🟠", "summary_card_vencem_hoje"
        )
        layout_cards.addWidget(self.card_vencem_hoje)
        
        # Card A Vencer
        self.card_a_vencer = self.criar_card_resumo(
            "A vencer", "0,00", "⚪", "summary_card_a_vencer"
        )
        layout_cards.addWidget(self.card_a_vencer)
        
        # Card Recebidos
        self.card_recebidos = self.criar_card_resumo(
            "Recebidos", "0,00", "🟢", "summary_card_recebidos"
        )
        layout_cards.addWidget(self.card_recebidos)
        
        # Card Total
        self.card_total = self.criar_card_resumo(
            "Total", "0,00", "💰", "summary_card_total"
        )
        layout_cards.addWidget(self.card_total)
        
        layout_principal.addLayout(layout_cards)
        
    def criar_card_resumo(self, titulo, valor, icone, object_name):
        """Cria um card de resumo."""
        frame = QFrame()
        frame.setObjectName(object_name)
        frame.setMinimumHeight(100)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Header com título e ícone externo
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
        
    def criar_tabela_cobrancas(self, layout_principal):
        """Cria a tabela de cobranças."""
        # Container para a tabela
        container_tabela = QFrame()
        container_tabela.setObjectName("container_card")
        layout_container = QVBoxLayout(container_tabela)
        layout_container.setContentsMargins(20, 20, 20, 20)
        
        # Tabela
        self.tabela_cobrancas = QTableWidget()
        self.tabela_cobrancas.setColumnCount(10)
        self.tabela_cobrancas.setHorizontalHeaderLabels([
            "Código", "Descrição", "Entidade", "Plano de contas", 
            "Pagamento", "Data", "Valor total", "Situação", "Loja", "Ações"
        ])
        
        # Configurações da tabela
        self.tabela_cobrancas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela_cobrancas.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela_cobrancas.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabela_cobrancas.setAlternatingRowColors(True)
        self.tabela_cobrancas.setShowGrid(False)
        self.tabela_cobrancas.verticalHeader().setVisible(False)
        
        # Configurar cabeçalho
        header = self.tabela_cobrancas.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Código
        header.setSectionResizeMode(1, QHeaderView.Stretch)           # Descrição
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Entidade
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Plano de contas
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Pagamento
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Data
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Valor total
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # Situação
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)  # Loja
        header.setSectionResizeMode(9, QHeaderView.Fixed)             # Ações
        header.resizeSection(9, 180)
        
        # Altura das linhas
        self.tabela_cobrancas.verticalHeader().setDefaultSectionSize(60)
        
        layout_container.addWidget(self.tabela_cobrancas)
        layout_principal.addWidget(container_tabela)
        
    def carregar_dividas(self):
        """Carrega as dívidas pendentes."""
        try:
            # Obter dívidas pendentes
            self.dividas = PagamentoController.obter_dividas_pendentes()
            
            # Atualizar resumo
            self.atualizar_resumo()
            
            # Atualizar tabela
            self.atualizar_tabela()
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar as cobranças:\n{str(e)}")
            
    def atualizar_resumo(self):
        """Atualiza os cards de resumo."""
        try:
            # Calcular totais
            total_vencidos = 0
            total_vencem_hoje = 0
            total_a_vencer = 0
            total_recebidos = 0
            total_geral = 0
            
            hoje = datetime.now().date()
            
            for divida in self.dividas:
                valor_pendente = divida['valor_pendente']
                data_vencimento = divida['data_vencimento']
                
                total_geral += divida['valor_total']
                total_recebidos += divida['valor_pago']
                
                if valor_pendente > 0 and data_vencimento:
                    # Converter para date se for datetime
                    if isinstance(data_vencimento, datetime):
                        data_vencimento = data_vencimento.date()
                    
                    if data_vencimento < hoje:
                        total_vencidos += valor_pendente
                    elif data_vencimento == hoje:
                        total_vencem_hoje += valor_pendente
                    else:
                        total_a_vencer += valor_pendente
            
            # Atualizar cards
            self.atualizar_card_valor(self.card_vencidos, f"{total_vencidos:,.2f}")
            self.atualizar_card_valor(self.card_vencem_hoje, f"{total_vencem_hoje:,.2f}")
            self.atualizar_card_valor(self.card_a_vencer, f"{total_a_vencer:,.2f}")
            self.atualizar_card_valor(self.card_recebidos, f"{total_recebidos:,.2f}")
            self.atualizar_card_valor(self.card_total, f"{total_geral:,.2f}")
            
        except Exception as e:
            print(f"Erro ao atualizar resumo: {e}")
            
    def atualizar_card_valor(self, card, valor):
        """Atualiza o valor em um card de resumo."""
        layout = card.layout()
        if layout and layout.count() >= 2:
            # O valor está no segundo item (índice 1)
            item_valor = layout.itemAt(1)
            if item_valor:
                lbl_valor = item_valor.widget()
                if lbl_valor:
                    lbl_valor.setText(valor)
                    
    def atualizar_tabela(self):
        """Atualiza a tabela com as dívidas."""
        self.tabela_cobrancas.setRowCount(len(self.dividas))
        
        for linha, divida in enumerate(self.dividas):
            # Código (Venda ID)
            item_codigo = QTableWidgetItem(str(divida['venda'].id))
            item_codigo.setTextAlignment(Qt.AlignCenter)
            self.tabela_cobrancas.setItem(linha, 0, item_codigo)
            
            # Descrição
            descricao = f"Venda nº {divida['venda'].id}"
            if divida['venda'].observacoes:
                descricao += f" 🛒"
            item_descricao = QTableWidgetItem(descricao)
            self.tabela_cobrancas.setItem(linha, 1, item_descricao)
            
            # Entidade (Cliente)
            nome_cliente = divida['cliente'].nome if divida['cliente'] else "---"
            item_entidade = QTableWidgetItem(nome_cliente)
            self.tabela_cobrancas.setItem(linha, 2, item_entidade)
            
            # Plano de contas
            item_plano = QTableWidgetItem("Vendas")
            item_plano.setTextAlignment(Qt.AlignCenter)
            self.tabela_cobrancas.setItem(linha, 3, item_plano)
            
            # Pagamento
            tipo_pag = divida['venda'].tipo_pagamento
            if "Boleto" in tipo_pag:
                tipo_display = "Boleto"
            elif "Promissória" in tipo_pag:
                tipo_display = "BB"
            else:
                tipo_display = tipo_pag
            item_pagamento = QTableWidgetItem(tipo_display)
            item_pagamento.setTextAlignment(Qt.AlignCenter)
            self.tabela_cobrancas.setItem(linha, 4, item_pagamento)
            
            # Data
            if divida['data_vencimento']:
                data_venc = divida['data_vencimento']
                # Converter para date se for datetime
                if isinstance(data_venc, datetime):
                    data_venc = data_venc.date()
                item_data = QTableWidgetItem(data_venc.strftime("%d/%m/%Y"))
            else:
                item_data = QTableWidgetItem("---")
            item_data.setTextAlignment(Qt.AlignCenter)
            self.tabela_cobrancas.setItem(linha, 5, item_data)
            
            # Valor total
            item_valor = QTableWidgetItem(f"{divida['valor_total']:,.2f}")
            item_valor.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tabela_cobrancas.setItem(linha, 6, item_valor)
            
            # Situação (Badge)
            widget_situacao = self.criar_badge_situacao(divida)
            self.tabela_cobrancas.setCellWidget(linha, 7, widget_situacao)
            
            # Loja
            item_loja = QTableWidgetItem("Savassi")
            item_loja.setTextAlignment(Qt.AlignCenter)
            self.tabela_cobrancas.setItem(linha, 8, item_loja)
            
            # Ações (botões)
            widget_acoes = self.criar_widget_acoes(divida)
            self.tabela_cobrancas.setCellWidget(linha, 9, widget_acoes)
            
    def criar_badge_situacao(self, divida):
        """Cria o badge de situação."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        
        # Determinar situação
        if divida['valor_pendente'] <= 0:
            badge = QLabel("Confirmado")
            badge.setObjectName("badge_confirmado")
        elif divida['dias_atraso'] > 0:
            badge = QLabel("Vencido")
            badge.setObjectName("badge_vencido")
        else:
            # Verificar se vence hoje
            data_venc = divida['data_vencimento']
            if data_venc:
                if isinstance(data_venc, datetime):
                    data_venc = data_venc.date()
                if data_venc == datetime.now().date():
                    badge = QLabel("Vence Hoje")
                    badge.setObjectName("badge_pendente")
                else:
                    badge = QLabel("Em aberto")
                    badge.setObjectName("badge_em_aberto")
            else:
                badge = QLabel("Em aberto")
                badge.setObjectName("badge_em_aberto")
        
        badge.setAlignment(Qt.AlignCenter)
        layout.addWidget(badge)
        
        return widget
        
    def criar_widget_acoes(self, divida):
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
        btn_view.clicked.connect(lambda: self.mostrar_detalhes(divida))
        layout.addWidget(btn_view)
        
        # Botão Editar
        btn_edit = QPushButton("✏")
        btn_edit.setObjectName("btn_action_edit")
        btn_edit.setToolTip("Editar cobrança")
        btn_edit.clicked.connect(lambda: self.editar_cobranca(divida))
        layout.addWidget(btn_edit)
        
        # Botão Excluir
        btn_delete = QPushButton("✖")
        btn_delete.setObjectName("btn_action_delete")
        btn_delete.setToolTip("Excluir cobrança")
        btn_delete.clicked.connect(lambda: self.excluir_cobranca(divida))
        layout.addWidget(btn_delete)
        
        # Botão Mais ações
        btn_more = QPushButton("⋮")
        btn_more.setObjectName("btn_action_more")
        btn_more.setToolTip("Mais ações")
        btn_more.clicked.connect(lambda: self.mais_acoes_item(divida))
        layout.addWidget(btn_more)
        
        return widget
        
    def filtrar_por_mes(self):
        """Filtra as cobranças por mês."""
        # Implementar filtro por mês
        self.carregar_dividas()
        
    def adicionar_cobranca(self):
        """Adiciona uma nova cobrança."""
        QMessageBox.information(self, "Adicionar", "Função de adicionar cobrança em desenvolvimento.")
        
    def mostrar_mais_acoes(self):
        """Mostra menu de mais ações."""
        try:
            from PyQt5.QtWidgets import QMenu
            menu = QMenu(self)
            menu.addAction("Exportar para Excel")
            menu.addAction("Exportar para PDF")
            menu.addAction("Imprimir relatório")
            menu.addSeparator()
            menu.addAction("Marcar todas como pagas")
            menu.addAction("Enviar lembretes")
            
            # Obter o botão que disparou
            btn = self.sender()
            if btn:
                menu.exec_(btn.mapToGlobal(btn.rect().bottomLeft()))
        except Exception as e:
            QMessageBox.information(self, "Mais Ações", "Menu de ações em desenvolvimento.")
        
    def abrir_busca_avancada(self):
        """Abre diálogo de busca avançada."""
        QMessageBox.information(self, "Busca Avançada", "Função de busca avançada em desenvolvimento.")
        
    def mostrar_detalhes(self, divida):
        """Mostra os detalhes de uma dívida."""
        dialog = DialogoDetalhesDivida(divida, self)
        dialog.exec_()
        
    def editar_cobranca(self, divida):
        """Edita uma cobrança."""
        QMessageBox.information(self, "Editar", f"Editar cobrança {divida['venda'].id} em desenvolvimento.")
        
    def excluir_cobranca(self, divida):
        """Exclui uma cobrança."""
        resposta = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            f"Deseja realmente excluir a cobrança #{divida['venda'].id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if resposta == QMessageBox.Yes:
            QMessageBox.information(self, "Excluir", "Função de exclusão em desenvolvimento.")
            
    def mais_acoes_item(self, divida):
        """Mostra mais ações para um item."""
        try:
            from PyQt5.QtWidgets import QMenu
            menu = QMenu(self)
            
            # Registrar pagamento
            action_pagar = menu.addAction("💵 Registrar Pagamento")
            action_pagar.triggered.connect(lambda: self.registrar_pagamento(divida['venda'].id))
            
            menu.addSeparator()
            menu.addAction("📧 Enviar lembrete")
            menu.addAction("📄 Gerar boleto")
            menu.addAction("🖨 Imprimir recibo")
            
            # Obter o botão que disparou
            btn = self.sender()
            if btn:
                menu.exec_(btn.mapToGlobal(btn.rect().bottomLeft()))
        except Exception as e:
            self.registrar_pagamento(divida['venda'].id)
        
    def registrar_pagamento(self, venda_id):
        """Abre o diálogo para registrar um pagamento."""
        dialog = DialogoRegistroPagamento(venda_id, self)
        if dialog.exec_():
            # Atualizar a lista de dívidas após o pagamento
            self.carregar_dividas()


class DialogoRegistroPagamento(QDialog):
    """Diálogo para registrar um pagamento de dívida."""
    
    def __init__(self, venda_id, parent=None):
        super().__init__(parent)
        self.venda_id = venda_id
        self.venda = Venda.obter_por_id(venda_id)
        self.pagamentos_existentes = Pagamento.obter_por_venda(venda_id)
        self.total_pago = sum(p.valor for p in self.pagamentos_existentes)
        
        self.inicializar_ui()
        
    def inicializar_ui(self):
        """Inicializa a interface do diálogo."""
        self.setWindowTitle("Registrar Pagamento")
        self.setModal(True)
        self.resize(500, 400)
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(25, 25, 25, 25)
        layout_principal.setSpacing(20)
        
        # Título
        lbl_titulo = QLabel("💵 Registrar Pagamento")
        lbl_titulo.setObjectName("titulo_secao")
        layout_principal.addWidget(lbl_titulo)
        
        # Informações da venda
        self.criar_grupo_informacoes_venda(layout_principal)
        
        # Formulário de pagamento
        self.criar_formulario_pagamento(layout_principal)
        
        # Botões
        self.criar_botoes(layout_principal)
        
    def criar_grupo_informacoes_venda(self, layout_principal):
        """Cria o grupo com informações da venda."""
        grupo_info = QGroupBox("Informações da Venda")
        layout_info = QFormLayout(grupo_info)
        layout_info.setSpacing(10)
        
        if self.venda:
            # Tipo de pagamento
            layout_info.addRow("Tipo de Pagamento:", QLabel(self.venda.tipo_pagamento))
            
            # Dia de vencimento (se aplicável)
            if self.venda.dia_vencimento:
                layout_info.addRow("Dia de Vencimento:", QLabel(str(self.venda.dia_vencimento)))
            
            # Valor total
            lbl_valor_total = QLabel(f"R$ {self.venda.valor_total:.2f}")
            lbl_valor_total.setObjectName("texto_destaque")
            layout_info.addRow("Valor Total:", lbl_valor_total)
            
            # Valor já pago
            lbl_valor_pago = QLabel(f"R$ {self.total_pago:.2f}")
            lbl_valor_pago.setObjectName("texto_sucesso")
            layout_info.addRow("Valor Já Pago:", lbl_valor_pago)
            
            # Valor pendente
            valor_pendente = self.venda.valor_total - self.total_pago
            lbl_valor_pendente = QLabel(f"R$ {valor_pendente:.2f}")
            lbl_valor_pendente.setObjectName("texto_perigo")
            layout_info.addRow("Valor Pendente:", lbl_valor_pendente)
            
            # Cliente
            if self.venda.cliente:
                layout_info.addRow("Cliente:", QLabel(self.venda.cliente.nome))
        
        layout_principal.addWidget(grupo_info)
        
    def criar_formulario_pagamento(self, layout_principal):
        """Cria o formulário para registro do pagamento."""
        grupo_pagamento = QGroupBox("Dados do Pagamento")
        layout_pagamento = QFormLayout(grupo_pagamento)
        layout_pagamento.setSpacing(10)
        
        # Valor do pagamento
        self.spin_valor = QDoubleSpinBox()
        self.spin_valor.setPrefix("R$ ")
        self.spin_valor.setMaximum(999999.99)
        self.spin_valor.setDecimals(2)
        valor_pendente = self.venda.valor_total - self.total_pago if self.venda else 0
        self.spin_valor.setValue(max(valor_pendente, 0))
        layout_pagamento.addRow("Valor do Pagamento:", self.spin_valor)
        
        # Data do pagamento
        self.date_pagamento = QDateEdit()
        self.date_pagamento.setDate(QDate.currentDate())
        self.date_pagamento.setDisplayFormat("dd/MM/yyyy")
        self.date_pagamento.setCalendarPopup(True)
        layout_pagamento.addRow("Data do Pagamento:", self.date_pagamento)
        
        # Observações
        self.txt_observacoes = QTextEdit()
        self.txt_observacoes.setMaximumHeight(80)
        self.txt_observacoes.setPlaceholderText("Observações sobre o pagamento (opcional)")
        layout_pagamento.addRow("Observações:", self.txt_observacoes)
        
        layout_principal.addWidget(grupo_pagamento)
        
    def criar_botoes(self, layout_principal):
        """Cria os botões do diálogo."""
        layout_botoes = QHBoxLayout()
        layout_botoes.addStretch()
        
        # Botão Cancelar
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setObjectName("secondary")
        btn_cancel.clicked.connect(self.reject)
        btn_cancel.setMinimumWidth(120)
        layout_botoes.addWidget(btn_cancel)
        
        # Botão Registrar
        btn_ok = QPushButton("✓ Registrar Pagamento")
        btn_ok.setObjectName("success")
        btn_ok.clicked.connect(self.aceitar)
        btn_ok.setMinimumWidth(180)
        layout_botoes.addWidget(btn_ok)
        
        layout_principal.addLayout(layout_botoes)
        
    def aceitar(self):
        """Registra o pagamento."""
        try:
            valor = self.spin_valor.value()
            if valor <= 0:
                QMessageBox.warning(self, "Aviso", "O valor do pagamento deve ser maior que zero.")
                return
                
            # Verificar se o valor não excede o pendente
            valor_pendente = self.venda.valor_total - self.total_pago
            if valor > valor_pendente:
                resposta = QMessageBox.question(
                    self,
                    "Confirmação",
                    f"O valor informado (R$ {valor:.2f}) é maior que o valor pendente (R$ {valor_pendente:.2f}).\nDeseja continuar?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if resposta == QMessageBox.No:
                    return
                    
            # Registrar o pagamento
            observacoes = self.txt_observacoes.toPlainText()
            pagamento = PagamentoController.registrar_pagamento(
                self.venda_id, valor, observacoes
            )
            
            if pagamento:
                QMessageBox.information(
                    self, 
                    "Sucesso", 
                    f"Pagamento registrado com sucesso!\nID: {pagamento.id}"
                )
                self.accept()
            else:
                QMessageBox.critical(
                    self, 
                    "Erro", 
                    "Não foi possível registrar o pagamento."
                )
                
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Erro", 
                f"Ocorreu um erro ao registrar o pagamento:\n{str(e)}"
            )


class DialogoDetalhesDivida(QDialog):
    """Diálogo para mostrar detalhes de uma dívida."""
    
    def __init__(self, divida, parent=None):
        super().__init__(parent)
        self.divida = divida
        self.inicializar_ui()
        
    def inicializar_ui(self):
        """Inicializa a interface do diálogo."""
        self.setWindowTitle("Detalhes da Dívida")
        self.setModal(True)
        self.resize(700, 550)
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(25, 25, 25, 25)
        layout_principal.setSpacing(20)
        
        # Título
        lbl_titulo = QLabel("📋 Detalhes da Dívida")
        lbl_titulo.setObjectName("titulo_secao")
        layout_principal.addWidget(lbl_titulo)
        
        # Informações gerais
        self.criar_grupo_informacoes_gerais(layout_principal)
        
        # Histórico de pagamentos
        self.criar_grupo_historico_pagamentos(layout_principal)
        
        # Botões
        self.criar_botoes(layout_principal)
        
    def criar_grupo_informacoes_gerais(self, layout_principal):
        """Cria o grupo com informações gerais da dívida."""
        grupo_info = QGroupBox("Informações Gerais")
        layout_info = QFormLayout(grupo_info)
        layout_info.setSpacing(10)
        
        # Cliente
        if self.divida['cliente']:
            layout_info.addRow("Cliente:", QLabel(self.divida['cliente'].nome))
            if self.divida['cliente'].telefone:
                layout_info.addRow("Telefone:", QLabel(self.divida['cliente'].telefone))
                
        # Venda
        layout_info.addRow("Venda ID:", QLabel(str(self.divida['venda'].id)))
        layout_info.addRow("Tipo de Pagamento:", QLabel(self.divida['venda'].tipo_pagamento))
        layout_info.addRow("Data da Venda:", QLabel(
            self.divida['venda'].data_venda.strftime("%d/%m/%Y") if self.divida['venda'].data_venda else "N/A"
        ))
        
        # Dia de vencimento (se aplicável)
        if self.divida['venda'].dia_vencimento:
            layout_info.addRow("Dia de Vencimento:", QLabel(str(self.divida['venda'].dia_vencimento)))
        
        # Valores
        layout_info.addRow("Valor Total:", QLabel(f"R$ {self.divida['valor_total']:.2f}"))
        layout_info.addRow("Valor Pago:", QLabel(f"R$ {self.divida['valor_pago']:.2f}"))
        
        lbl_pendente = QLabel(f"R$ {self.divida['valor_pendente']:.2f}")
        lbl_pendente.setObjectName("texto_perigo" if self.divida['valor_pendente'] > 0 else "texto_sucesso")
        layout_info.addRow("Valor Pendente:", lbl_pendente)
        
        # Vencimento
        if self.divida['data_vencimento']:
            layout_info.addRow("Data de Vencimento:", QLabel(
                self.divida['data_vencimento'].strftime("%d/%m/%Y")
            ))
            if self.divida['dias_atraso'] > 0:
                lbl_atraso = QLabel(f"{self.divida['dias_atraso']} dias")
                lbl_atraso.setObjectName("texto_perigo")
                layout_info.addRow("Dias de Atraso:", lbl_atraso)
            else:
                lbl_status = QLabel("Em dia")
                lbl_status.setObjectName("texto_sucesso")
                layout_info.addRow("Status:", lbl_status)
        
        layout_principal.addWidget(grupo_info)
        
    def criar_grupo_historico_pagamentos(self, layout_principal):
        """Cria o grupo com histórico de pagamentos."""
        grupo_pagamentos = QGroupBox("Histórico de Pagamentos")
        layout_pagamentos = QVBoxLayout(grupo_pagamentos)
        
        if self.divida['pagamentos']:
            # Tabela de pagamentos
            tabela = QTableWidget()
            tabela.setColumnCount(4)
            tabela.setHorizontalHeaderLabels(["Data", "Valor", "Observações", "ID"])
            tabela.setRowCount(len(self.divida['pagamentos']))
            
            # Configurações da tabela
            tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)
            tabela.setSelectionMode(QAbstractItemView.NoSelection)
            tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tabela.verticalHeader().setVisible(False)
            tabela.setAlternatingRowColors(True)
            
            for i, pagamento in enumerate(self.divida['pagamentos']):
                # Data
                item_data = QTableWidgetItem(
                    pagamento.data_pagamento.strftime("%d/%m/%Y") if pagamento.data_pagamento else "N/A"
                )
                tabela.setItem(i, 0, item_data)
                
                # Valor
                item_valor = QTableWidgetItem(f"R$ {pagamento.valor:.2f}")
                item_valor.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                tabela.setItem(i, 1, item_valor)
                
                # Observações
                item_obs = QTableWidgetItem(pagamento.observacoes or "---")
                tabela.setItem(i, 2, item_obs)
                
                # ID
                item_id = QTableWidgetItem(str(pagamento.id))
                item_id.setTextAlignment(Qt.AlignCenter)
                tabela.setItem(i, 3, item_id)
                
            layout_pagamentos.addWidget(tabela)
        else:
            lbl_sem_pagamentos = QLabel("Nenhum pagamento registrado para esta dívida.")
            lbl_sem_pagamentos.setStyleSheet("color: #95A5A6; font-style: italic; padding: 20px;")
            lbl_sem_pagamentos.setAlignment(Qt.AlignCenter)
            layout_pagamentos.addWidget(lbl_sem_pagamentos)
            
        layout_principal.addWidget(grupo_pagamentos)
        
    def criar_botoes(self, layout_principal):
        """Cria os botões do diálogo."""
        layout_botoes = QHBoxLayout()
        layout_botoes.addStretch()
        
        btn_fechar = QPushButton("Fechar")
        btn_fechar.setObjectName("secondary")
        btn_fechar.clicked.connect(self.accept)
        btn_fechar.setMinimumWidth(120)
        layout_botoes.addWidget(btn_fechar)
        
        layout_principal.addLayout(layout_botoes)

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMessageBox, QAbstractItemView, QLabel, QLineEdit,
                             QComboBox, QDateEdit, QSpacerItem, QSizePolicy,
                             QGroupBox, QTextEdit, QSpinBox, QProgressBar,
                             QTabWidget, QFrame, QScrollArea, QDialog, QFormLayout,
                             QDialogButtonBox, QDoubleSpinBox)
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
        self.inicializar_ui()
        self.carregar_dividas()
        
    def inicializar_ui(self):
        """Inicializa a interface do usuário."""
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(15)
        
        # Cabeçalho com resumo
        self.criar_cabecalho(layout_principal)
        
        # Filtros
        self.criar_filtros(layout_principal)
        
        # Conteúdo principal
        self.criar_conteudo_principal(layout_principal)
        
        # Aplicar estilo
        self.aplicar_estilo()
        
    def criar_cabecalho(self, layout_principal):
        """Cria o cabeçalho com resumo das cobranças."""
        # Grupo de resumo
        grupo_resumo = QGroupBox("Resumo de Cobranças")
        layout_resumo = QVBoxLayout(grupo_resumo)
        
        # Layout para os cards de resumo
        layout_cards = QHBoxLayout()
        
        # Card de total de dívidas
        self.card_total_dividas = self.criar_card_resumo("Total em Dívidas", "R$ 0,00", "#FF6B6B")
        layout_cards.addWidget(self.card_total_dividas)
        
        # Card de total pago
        self.card_total_pago = self.criar_card_resumo("Total Recebido", "R$ 0,00", "#28A745")
        layout_cards.addWidget(self.card_total_pago)
        
        # Card de total pendente
        self.card_total_pendente = self.criar_card_resumo("Total Pendente", "R$ 0,00", "#FFA500")
        layout_cards.addWidget(self.card_total_pendente)
        
        # Card de clientes devendo
        self.card_clientes_devendo = self.criar_card_resumo("Clientes Devendo", "0", "#4A90E2")
        layout_cards.addWidget(self.card_clientes_devendo)
        
        layout_resumo.addLayout(layout_cards)
        layout_principal.addWidget(grupo_resumo)
        
    def criar_card_resumo(self, titulo, valor, cor):
        """Cria um card de resumo."""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {cor};
                border-radius: 12px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(5)
        
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setStyleSheet("""
            color: white;
            font-size: 14px;
            font-weight: bold;
        """)
        layout.addWidget(lbl_titulo)
        
        lbl_valor = QLabel(valor)
        lbl_valor.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        layout.addWidget(lbl_valor)
        
        return frame
        
    def criar_filtros(self, layout_principal):
        """Cria os filtros para a lista de cobranças."""
        grupo_filtros = QGroupBox("Filtros")
        layout_filtros = QHBoxLayout(grupo_filtros)
        
        # Filtro por cliente
        layout_filtros.addWidget(QLabel("Cliente:"))
        self.combo_clientes = QComboBox()
        self.combo_clientes.addItem("Todos os clientes")
        layout_filtros.addWidget(self.combo_clientes)
        
        # Filtro por tipo de pagamento
        layout_filtros.addWidget(QLabel("Tipo:"))
        self.combo_tipo_pagamento = QComboBox()
        self.combo_tipo_pagamento.addItems([
            "Todos", 
            "Parcelado Boleto", 
            "Parcelado Promissória"
        ])
        layout_filtros.addWidget(self.combo_tipo_pagamento)
        
        # Campo de busca
        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("Buscar por cliente ou venda...")
        layout_filtros.addWidget(self.campo_busca)
        
        # Botão de atualizar
        self.btn_atualizar = QPushButton("Atualizar")
        self.btn_atualizar.clicked.connect(self.carregar_dividas)
        layout_filtros.addWidget(self.btn_atualizar)
        
        layout_principal.addWidget(grupo_filtros)
        
    def criar_conteudo_principal(self, layout_principal):
        """Cria o conteúdo principal com a tabela de cobranças."""
        # Tabela de cobranças
        self.tabela_cobrancas = QTableWidget()
        self.tabela_cobrancas.setColumnCount(9)
        self.tabela_cobrancas.setHorizontalHeaderLabels([
            "Cliente", "Venda ID", "Tipo", "Valor Total", "Valor Pago", 
            "Valor Pendente", "Vencimento", "Dias de Atraso", "Ações"
        ])
        
        # Configurações da tabela
        self.tabela_cobrancas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela_cobrancas.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela_cobrancas.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabela_cobrancas.setAlternatingRowColors(True)
        
        # Configurar cabeçalho
        header = self.tabela_cobrancas.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Venda ID
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Tipo
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Valor Total
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Valor Pago
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Valor Pendente
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Vencimento
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # Dias de Atraso
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)  # Ações
        
        # Altura das linhas
        self.tabela_cobrancas.verticalHeader().setDefaultSectionSize(50)
        
        layout_principal.addWidget(self.tabela_cobrancas)
        
    def aplicar_estilo(self):
        """Aplica o estilo moderno à interface."""
        estilo = """
        QWidget {
            background-color: #F8F9FA;
            font-family: Arial, sans-serif;
        }
        
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
        
        QComboBox {
            padding: 8px 12px;
            border: 1px solid #E0E0E0;
            border-radius: 6px;
            background-color: white;
            min-height: 20px;
        }
        
        QLineEdit {
            padding: 10px 12px;
            border: 1px solid #E0E0E0;
            border-radius: 6px;
            background-color: white;
            selection-background-color: #4A90E2;
        }
        
        QLineEdit:focus {
            border: 1px solid #4A90E2;
            outline: none;
        }
        
        QPushButton {
            background-color: #4A90E2;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 6px;
            font-weight: 500;
        }
        
        QPushButton:hover {
            background-color: #357ABD;
        }
        
        QPushButton:pressed {
            background-color: #2E6DA4;
        }
        
        QTableWidget {
            background-color: white;
            alternate-background-color: #FAFAFA;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            gridline-color: #F0F0F0;
            selection-background-color: #F0F5FF;
            selection-color: #333333;
        }
        
        QTableWidget::item {
            padding: 10px;
            border-bottom: 1px solid #F0F0F0;
        }
        
        QTableWidget::item:selected {
            background-color: #F0F5FF;
        }
        
        QHeaderView::section {
            background-color: #F5F5F5;
            color: #333333;
            padding: 12px;
            font-weight: 600;
            border: none;
            border-bottom: 1px solid #E0E0E0;
        }
        """
        self.setStyleSheet(estilo)
        
    def carregar_dividas(self):
        """Carrega as dívidas pendentes."""
        try:
            # Obter dívidas pendentes
            self.dividas = PagamentoController.obter_dividas_pendentes()
            
            # Aplicar filtros
            tipo_filtro = self.combo_tipo_pagamento.currentText()
            if tipo_filtro != "Todos":
                self.dividas = [d for d in self.dividas if d['venda'].tipo_pagamento == tipo_filtro]
            
            # Atualizar resumo
            self.atualizar_resumo()
            
            # Atualizar tabela
            self.atualizar_tabela()
            
            # Carregar clientes para o filtro
            self.carregar_clientes_filtro()
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar as cobranças:\n{str(e)}")
            
    def atualizar_resumo(self):
        """Atualiza os cards de resumo."""
        try:
            totais = PagamentoController.calcular_totais_dividas()
            
            # Atualizar cards
            self.atualizar_card_valor(self.card_total_dividas, f"R$ {totais['total_dividas']:.2f}")
            self.atualizar_card_valor(self.card_total_pago, f"R$ {totais['total_pago']:.2f}")
            self.atualizar_card_valor(self.card_total_pendente, f"R$ {totais['total_pendente']:.2f}")
            self.atualizar_card_valor(self.card_clientes_devendo, str(totais['numero_clientes_devendo']))
            
        except Exception as e:
            print(f"Erro ao atualizar resumo: {e}")
            
    def atualizar_card_valor(self, card, valor):
        """Atualiza o valor em um card de resumo."""
        layout = card.layout()
        if layout.count() >= 2:
            lbl_valor = layout.itemAt(1).widget()
            if lbl_valor:
                lbl_valor.setText(valor)
                
    def carregar_clientes_filtro(self):
        """Carrega a lista de clientes para o filtro."""
        try:
            clientes = ClienteController.listar_clientes()
            self.combo_clientes.clear()
            self.combo_clientes.addItem("Todos os clientes")
            for cliente in clientes:
                self.combo_clientes.addItem(f"{cliente.nome}", cliente.id)
        except Exception as e:
            print(f"Erro ao carregar clientes para filtro: {e}")
            
    def atualizar_tabela(self):
        """Atualiza a tabela com as dívidas."""
        self.tabela_cobrancas.setRowCount(len(self.dividas))
        
        for linha, divida in enumerate(self.dividas):
            # Cliente
            nome_cliente = divida['cliente'].nome if divida['cliente'] else "Cliente não identificado"
            item_cliente = QTableWidgetItem(nome_cliente)
            self.tabela_cobrancas.setItem(linha, 0, item_cliente)
            
            # Venda ID
            item_venda_id = QTableWidgetItem(str(divida['venda'].id))
            item_venda_id.setTextAlignment(Qt.AlignCenter)
            self.tabela_cobrancas.setItem(linha, 1, item_venda_id)
            
            # Tipo de pagamento
            item_tipo = QTableWidgetItem(divida['venda'].tipo_pagamento)
            item_tipo.setTextAlignment(Qt.AlignCenter)
            self.tabela_cobrancas.setItem(linha, 2, item_tipo)
            
            # Valor Total
            item_valor_total = QTableWidgetItem(f"R$ {divida['valor_total']:.2f}")
            item_valor_total.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tabela_cobrancas.setItem(linha, 3, item_valor_total)
            
            # Valor Pago
            item_valor_pago = QTableWidgetItem(f"R$ {divida['valor_pago']:.2f}")
            item_valor_pago.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tabela_cobrancas.setItem(linha, 4, item_valor_pago)
            
            # Valor Pendente
            item_valor_pendente = QTableWidgetItem(f"R$ {divida['valor_pendente']:.2f}")
            item_valor_pendente.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            # Colorir valor pendente em vermelho se houver dívida
            if divida['valor_pendente'] > 0:
                item_valor_pendente.setForeground(QBrush(QColor("#FF6B6B")))
                item_valor_pendente.setFont(QFont("", -1, QFont.Bold))
            self.tabela_cobrancas.setItem(linha, 5, item_valor_pendente)
            
            # Data de Vencimento
            data_vencimento = divida['data_vencimento']
            if data_vencimento:
                item_vencimento = QTableWidgetItem(data_vencimento.strftime("%d/%m/%Y"))
                item_vencimento.setTextAlignment(Qt.AlignCenter)
                # Colorir data de vencimento se estiver atrasada
                if divida['dias_atraso'] > 0:
                    item_vencimento.setForeground(QBrush(QColor("#FF6B6B")))
                    item_vencimento.setFont(QFont("", -1, QFont.Bold))
                self.tabela_cobrancas.setItem(linha, 6, item_vencimento)
            else:
                item_vencimento = QTableWidgetItem("N/A")
                item_vencimento.setTextAlignment(Qt.AlignCenter)
                self.tabela_cobrancas.setItem(linha, 6, item_vencimento)
            
            # Dias de Atraso
            dias_atraso = divida['dias_atraso']
            if dias_atraso > 0:
                item_atraso = QTableWidgetItem(f"{dias_atraso} dias")
                item_atraso.setTextAlignment(Qt.AlignCenter)
                item_atraso.setForeground(QBrush(QColor("#FF6B6B")))
                item_atraso.setFont(QFont("", -1, QFont.Bold))
                self.tabela_cobrancas.setItem(linha, 7, item_atraso)
            else:
                item_atraso = QTableWidgetItem("Em dia")
                item_atraso.setTextAlignment(Qt.AlignCenter)
                self.tabela_cobrancas.setItem(linha, 7, item_atraso)
            
            # Ações (botões)
            widget_acoes = QWidget()
            layout_acoes = QHBoxLayout(widget_acoes)
            layout_acoes.setContentsMargins(5, 5, 5, 5)
            layout_acoes.setSpacing(5)
            
            btn_registrar_pagamento = QPushButton("Registrar Pagamento")
            btn_registrar_pagamento.setStyleSheet("""
                QPushButton {
                    background-color: #28A745;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 5px 10px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #218838;
                }
            """)
            btn_registrar_pagamento.clicked.connect(
                lambda _, v=divida['venda'].id: self.registrar_pagamento(v)
            )
            layout_acoes.addWidget(btn_registrar_pagamento)
            
            btn_detalhes = QPushButton("Detalhes")
            btn_detalhes.setStyleSheet("""
                QPushButton {
                    background-color: #6C757D;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 5px 10px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #5A6268;
                }
            """)
            btn_detalhes.clicked.connect(
                lambda _, d=divida: self.mostrar_detalhes(d)
            )
            layout_acoes.addWidget(btn_detalhes)
            
            layout_acoes.addStretch()
            self.tabela_cobrancas.setCellWidget(linha, 8, widget_acoes)
            
        # Ajustar altura das linhas
        for i in range(self.tabela_cobrancas.rowCount()):
            self.tabela_cobrancas.setRowHeight(i, 50)
            
    def registrar_pagamento(self, venda_id):
        """Abre o diálogo para registrar um pagamento."""
        dialog = DialogoRegistroPagamento(venda_id, self)
        if dialog.exec_():
            # Atualizar a lista de dívidas após o pagamento
            self.carregar_dividas()
            
    def mostrar_detalhes(self, divida):
        """Mostra os detalhes de uma dívidas."""
        dialog = DialogoDetalhesDivida(divida, self)
        dialog.exec_()

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
        self.resize(400, 300)
        
        layout_principal = QVBoxLayout(self)
        
        # Título
        lbl_titulo = QLabel("Registrar Pagamento")
        lbl_titulo.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 20px;
        """)
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
        
        if self.venda:
            # Tipo de pagamento
            layout_info.addRow("Tipo de Pagamento:", QLabel(self.venda.tipo_pagamento))
            
            # Dia de vencimento (se aplicável)
            if self.venda.dia_vencimento:
                layout_info.addRow("Dia de Vencimento:", QLabel(str(self.venda.dia_vencimento)))
            
            # Valor total
            lbl_valor_total = QLabel(f"R$ {self.venda.valor_total:.2f}")
            lbl_valor_total.setStyleSheet("font-weight: bold;")
            layout_info.addRow("Valor Total:", lbl_valor_total)
            
            # Valor já pago
            lbl_valor_pago = QLabel(f"R$ {self.total_pago:.2f}")
            lbl_valor_pago.setStyleSheet("color: #28A745;")
            layout_info.addRow("Valor Já Pago:", lbl_valor_pago)
            
            # Valor pendente
            valor_pendente = self.venda.valor_total - self.total_pago
            lbl_valor_pendente = QLabel(f"R$ {valor_pendente:.2f}")
            lbl_valor_pendente.setStyleSheet("color: #FF6B6B; font-weight: bold;")
            layout_info.addRow("Valor Pendente:", lbl_valor_pendente)
            
            # Cliente
            if self.venda.cliente:
                layout_info.addRow("Cliente:", QLabel(self.venda.cliente.nome))
        
        layout_principal.addWidget(grupo_info)
        
    def criar_formulario_pagamento(self, layout_principal):
        """Cria o formulário para registro do pagamento."""
        grupo_pagamento = QGroupBox("Dados do Pagamento")
        layout_pagamento = QFormLayout(grupo_pagamento)
        
        # Valor do pagamento
        self.spin_valor = QDoubleSpinBox()
        self.spin_valor.setPrefix("R$ ")
        self.spin_valor.setMaximum(999999.99)
        self.spin_valor.setDecimals(2)
        valor_pendente = self.venda.valor_total - self.total_pago if self.venda else 0
        self.spin_valor.setValue(min(valor_pendente, 0))  # Valor padrão
        layout_pagamento.addRow("Valor do Pagamento:", self.spin_valor)
        
        # Data do pagamento
        self.date_pagamento = QDateEdit()
        self.date_pagamento.setDate(QDate.currentDate())
        self.date_pagamento.setDisplayFormat("dd/MM/yyyy")
        layout_pagamento.addRow("Data do Pagamento:", self.date_pagamento)
        
        # Observações
        self.txt_observacoes = QTextEdit()
        self.txt_observacoes.setMaximumHeight(80)
        layout_pagamento.addRow("Observações:", self.txt_observacoes)
        
        layout_principal.addWidget(grupo_pagamento)
        
    def criar_botoes(self, layout_principal):
        """Cria os botões do diálogo."""
        botoes = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        botoes.accepted.connect(self.aceitar)
        botoes.rejected.connect(self.reject)
        
        # Personalizar botões
        btn_ok = botoes.button(QDialogButtonBox.Ok)
        btn_ok.setText("Registrar Pagamento")
        btn_ok.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 6px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        btn_cancel = botoes.button(QDialogButtonBox.Cancel)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #6C757D;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 6px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #5A6268;
            }
        """)
        
        layout_principal.addWidget(botoes)
        
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
        self.resize(600, 500)
        
        layout_principal = QVBoxLayout(self)
        
        # Título
        lbl_titulo = QLabel("Detalhes da Dívida")
        lbl_titulo.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 20px;
        """)
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
        layout_info.addRow("Valor Pendente:", QLabel(f"R$ {self.divida['valor_pendente']:.2f}"))
        
        # Vencimento
        if self.divida['data_vencimento']:
            layout_info.addRow("Data de Vencimento:", QLabel(
                self.divida['data_vencimento'].strftime("%d/%m/%Y")
            ))
            if self.divida['dias_atraso'] > 0:
                layout_info.addRow("Dias de Atraso:", QLabel(
                    f"{self.divida['dias_atraso']} dias", 
                    styleSheet="color: #FF6B6B; font-weight: bold;"
                ))
            else:
                layout_info.addRow("Status:", QLabel("Em dia", styleSheet="color: #28A745;"))
        
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
                item_obs = QTableWidgetItem(pagamento.observacoes or "")
                tabela.setItem(i, 2, item_obs)
                
                # ID
                item_id = QTableWidgetItem(str(pagamento.id))
                item_id.setTextAlignment(Qt.AlignCenter)
                tabela.setItem(i, 3, item_id)
                
            layout_pagamentos.addWidget(tabela)
        else:
            lbl_sem_pagamentos = QLabel("Nenhum pagamento registrado para esta dívida.")
            lbl_sem_pagamentos.setStyleSheet("color: #666666; font-style: italic;")
            layout_pagamentos.addWidget(lbl_sem_pagamentos)
            
        layout_principal.addWidget(grupo_pagamentos)
        
    def criar_botoes(self, layout_principal):
        """Cria os botões do diálogo."""
        layout_botoes = QHBoxLayout()
        layout_botoes.addStretch()
        
        btn_fechar = QPushButton("Fechar")
        btn_fechar.clicked.connect(self.accept)
        layout_botoes.addWidget(btn_fechar)
        
        layout_principal.addLayout(layout_botoes)
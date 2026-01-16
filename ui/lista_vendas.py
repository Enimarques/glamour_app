from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMessageBox, QAbstractItemView, QLabel, QLineEdit,
                             QComboBox, QDateEdit, QSpacerItem, QSizePolicy,
                             QGroupBox)
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
        
        # Cabeçalho com filtros
        self.criar_cabecalho(layout_principal)
        
        # Tabela de vendas
        self.criar_tabela_vendas(layout_principal)
        
        # Aplicar estilo
        self.aplicar_estilo()
        
    def criar_cabecalho(self, layout_principal):
        """Cria o cabeçalho com título e filtros."""
        # Layout do cabeçalho
        layout_cabecalho = QVBoxLayout()
        
        # Título e botão
        layout_titulo = QHBoxLayout()
        lbl_titulo = QLabel("Lista de Vendas")
        lbl_titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333333;
        """)
        layout_titulo.addWidget(lbl_titulo)
        layout_titulo.addStretch()
        
        self.btn_atualizar = QPushButton("Atualizar")
        self.btn_atualizar.setObjectName("secondary")
        self.btn_atualizar.clicked.connect(self.carregar_vendas)
        layout_titulo.addWidget(self.btn_atualizar)
        
        self.btn_adicionar = QPushButton("Registrar Venda")
        self.btn_adicionar.clicked.connect(self.registrar_venda)
        layout_titulo.addWidget(self.btn_adicionar)
        
        layout_cabecalho.addLayout(layout_titulo)
        
        # Grupo de filtros
        grupo_filtros = QGroupBox("Filtros")
        layout_filtros = QHBoxLayout(grupo_filtros)
        layout_filtros.setContentsMargins(20, 20, 20, 20)
        layout_filtros.setSpacing(15)
        
        # Filtro por data
        lbl_data_inicio = QLabel("Data Início:")
        self.date_inicio = QDateEdit()
        self.date_inicio.setDisplayFormat("dd/MM/yyyy")
        self.date_inicio.setDate(QDate.currentDate().addDays(-30))
        self.date_inicio.dateChanged.connect(self.filtrar_vendas)
        layout_filtros.addWidget(lbl_data_inicio)
        layout_filtros.addWidget(self.date_inicio)
        
        lbl_data_fim = QLabel("Data Fim:")
        self.date_fim = QDateEdit()
        self.date_fim.setDisplayFormat("dd/MM/yyyy")
        self.date_fim.setDate(QDate.currentDate())
        self.date_fim.dateChanged.connect(self.filtrar_vendas)
        layout_filtros.addWidget(lbl_data_fim)
        layout_filtros.addWidget(self.date_fim)
        
        # Filtro por status
        lbl_status = QLabel("Status:")
        self.combo_status = QComboBox()
        self.combo_status.addItem("Todos", "")
        self.combo_status.addItem("Pago", "pago")
        self.combo_status.addItem("Pendente", "pendente")
        self.combo_status.currentIndexChanged.connect(self.filtrar_vendas)
        layout_filtros.addWidget(lbl_status)
        layout_filtros.addWidget(self.combo_status)
        
        # Campo de busca
        lbl_busca = QLabel("Buscar:")
        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("Buscar por cliente...")
        self.campo_busca.textChanged.connect(self.filtrar_vendas)
        layout_filtros.addWidget(lbl_busca)
        layout_filtros.addWidget(self.campo_busca)
        
        layout_cabecalho.addWidget(grupo_filtros)
        layout_principal.addLayout(layout_cabecalho)
        
    def criar_tabela_vendas(self, layout_principal):
        """Cria a tabela de vendas com estilo moderno."""
        self.tabela_vendas = QTableWidget()
        self.tabela_vendas.setColumnCount(7)
        self.tabela_vendas.setHorizontalHeaderLabels([
            "ID", "Data", "Cliente", "Valor Total", "Tipo", "Status", "Ações"
        ])
        
        # Configurações da tabela
        self.tabela_vendas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela_vendas.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela_vendas.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabela_vendas.setAlternatingRowColors(True)
        
        # Configurar cabeçalho
        header = self.tabela_vendas.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Data
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Valor
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Tipo
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Status
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Ações
        
        # Altura das linhas
        self.tabela_vendas.verticalHeader().setDefaultSectionSize(50)
        
        layout_principal.addWidget(self.tabela_vendas)
        
    def aplicar_estilo(self):
        """Aplica o estilo moderno à tabela."""
        estilo = """
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
        
        QComboBox, QDateEdit, QLineEdit {
            padding: 8px 12px;
            border: 1px solid #E0E0E0;
            border-radius: 6px;
            background-color: white;
            selection-background-color: #4A90E2;
            min-height: 20px;
        }
        
        QComboBox:focus, QDateEdit:focus, QLineEdit:focus {
            border: 1px solid #4A90E2;
            outline: none;
        }
        
        QDateEdit::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left-width: 1px;
            border-left-color: #E0E0E0;
            border-left-style: solid;
        }
        """
        self.tabela_vendas.setStyleSheet(estilo)
        
    def carregar_vendas(self):
        """Carrega a lista de vendas do banco de dados."""
        try:
            self.vendas = VendaController.listar_vendas()
            self.vendas_filtradas = self.vendas.copy()
            self.filtrar_vendas()
            self.vendas_atualizadas.emit()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar as vendas:\n{str(e)}")
            
    def filtrar_vendas(self):
        """Filtra as vendas com base nos critérios selecionados."""
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
            
        # Filtrar por termo de busca
        if termo_busca:
            self.vendas_filtradas = [
                v for v in self.vendas_filtradas 
                if (v.cliente and termo_busca in v.cliente.nome.lower())
            ]
            
        self.atualizar_tabela()
        
    def atualizar_tabela(self):
        """Atualiza a tabela com as vendas."""
        self.tabela_vendas.setRowCount(len(self.vendas_filtradas))
        
        for linha, venda in enumerate(self.vendas_filtradas):
            # Coluna ID
            item_id = QTableWidgetItem(str(venda.id))
            item_id.setTextAlignment(Qt.AlignCenter)
            item_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tabela_vendas.setItem(linha, 0, item_id)
            
            # Coluna Data
            data_formatada = venda.data_venda.strftime("%d/%m/%Y")
            item_data = QTableWidgetItem(data_formatada)
            item_data.setTextAlignment(Qt.AlignCenter)
            item_data.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tabela_vendas.setItem(linha, 1, item_data)
            
            # Coluna Cliente
            nome_cliente = venda.cliente.nome if venda.cliente else "Não informado"
            item_cliente = QTableWidgetItem(nome_cliente)
            item_cliente.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tabela_vendas.setItem(linha, 2, item_cliente)
            
            # Coluna Valor Total
            item_valor = QTableWidgetItem(f"R$ {venda.valor_total:.2f}")
            item_valor.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item_valor.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tabela_vendas.setItem(linha, 3, item_valor)
            
            # Coluna Tipo
            tipo = "Fiado" if venda.tipo_pagamento == "fiado" else "À Vista"
            item_tipo = QTableWidgetItem(tipo)
            item_tipo.setTextAlignment(Qt.AlignCenter)
            item_tipo.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tabela_vendas.setItem(linha, 4, item_tipo)
            
            # Coluna Status
            item_status = QTableWidgetItem(venda.status.capitalize())
            item_status.setTextAlignment(Qt.AlignCenter)
            item_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            
            # Colorir status
            if venda.status == "pago":
                item_status.setForeground(QColor("#50C878"))  # Verde
                item_status.setFont(QFont("", -1, QFont.Bold))
            else:
                item_status.setForeground(QColor("#FF6B6B"))  # Vermelho
                item_status.setFont(QFont("", -1, QFont.Bold))
                
            self.tabela_vendas.setItem(linha, 5, item_status)
            
            # Coluna Ações (botões)
            widget_acoes = QWidget()
            layout_acoes = QHBoxLayout(widget_acoes)
            layout_acoes.setContentsMargins(10, 5, 10, 5)
            layout_acoes.setSpacing(8)
            
            btn_visualizar = QPushButton("Visualizar")
            btn_visualizar.setObjectName("secondary")
            btn_visualizar.setFixedSize(100, 30)
            btn_visualizar.clicked.connect(lambda checked, v=venda: self.visualizar_venda(v))
            layout_acoes.addWidget(btn_visualizar)
            
            # Só mostrar botão de pagamento para vendas pendentes
            if venda.status == "pendente":
                btn_pagar = QPushButton("Registrar Pagamento")
                btn_pagar.setStyleSheet("""
                    QPushButton {
                        background-color: #50C878;
                        color: white;
                        border: none;
                        border-radius: 6px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #45B76A;
                    }
                """)
                btn_pagar.setFixedSize(140, 30)
                btn_pagar.clicked.connect(lambda checked, v=venda: self.registrar_pagamento(v))
                layout_acoes.addWidget(btn_pagar)
            
            layout_acoes.addStretch()
            self.tabela_vendas.setCellWidget(linha, 6, widget_acoes)
            
        # Ajustar altura das linhas
        for i in range(self.tabela_vendas.rowCount()):
            self.tabela_vendas.setRowHeight(i, 50)
            
    def registrar_venda(self):
        """Abre o formulário para registrar uma nova venda."""
        formulario = FormularioVenda(parent=self)
        formulario.venda_registrada.connect(self.venda_adicionada)
        
        if formulario.exec_():
            self.carregar_vendas()
            
    def visualizar_venda(self, venda: Venda):
        """Visualiza os detalhes de uma venda."""
        formulario = FormularioVenda(venda=venda, parent=self)
        formulario.setModal(True)
        formulario.show()
            
    def registrar_pagamento(self, venda: Venda):
        """Registra pagamento de uma venda fiado."""
        # TODO: Implementar formulário de registro de pagamento
        QMessageBox.information(self, "Informação", "Funcionalidade de registro de pagamento em desenvolvimento.")
        
    def venda_adicionada(self, venda: Venda):
        """Callback chamado quando uma venda é registrada."""
        QMessageBox.information(self, "Sucesso", f"Venda registrada com sucesso!\nID: {venda.id}")
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMessageBox, QAbstractItemView, QLabel, QLineEdit,
                             QSpacerItem, QSizePolicy)
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
        
        # Cabeçalho com filtros
        self.criar_cabecalho(layout_principal)
        
        # Tabela de clientes
        self.criar_tabela_clientes(layout_principal)
        
        # Aplicar estilo
        self.aplicar_estilo()
        
    def criar_cabecalho(self, layout_principal):
        """Cria o cabeçalho com título e filtros."""
        # Layout do cabeçalho
        layout_cabecalho = QHBoxLayout()
        
        # Título
        lbl_titulo = QLabel("Lista de Clientes")
        lbl_titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333333;
        """)
        layout_cabecalho.addWidget(lbl_titulo)
        
        # Espaçador
        layout_cabecalho.addStretch()
        
        # Campo de busca
        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("Buscar clientes...")
        self.campo_busca.setMinimumWidth(200)
        self.campo_busca.textChanged.connect(self.filtrar_clientes)
        layout_cabecalho.addWidget(self.campo_busca)
        
        # Botões
        self.btn_atualizar = QPushButton("Atualizar")
        self.btn_atualizar.setObjectName("secondary")
        self.btn_atualizar.clicked.connect(self.carregar_clientes)
        layout_cabecalho.addWidget(self.btn_atualizar)
        
        self.btn_adicionar = QPushButton("Adicionar Cliente")
        self.btn_adicionar.clicked.connect(self.adicionar_cliente)
        layout_cabecalho.addWidget(self.btn_adicionar)
        
        layout_principal.addLayout(layout_cabecalho)
        
    def criar_tabela_clientes(self, layout_principal):
        """Cria a tabela de clientes com estilo moderno."""
        self.tabela_clientes = QTableWidget()
        self.tabela_clientes.setColumnCount(5)
        self.tabela_clientes.setHorizontalHeaderLabels([
            "ID", "Nome", "Telefone", "Observações", "Ações"
        ])
        
        # Configurações da tabela
        self.tabela_clientes.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela_clientes.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela_clientes.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabela_clientes.setAlternatingRowColors(True)
        
        # Configurar cabeçalho
        header = self.tabela_clientes.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Nome
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Telefone
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Ações
        
        # Altura das linhas
        self.tabela_clientes.verticalHeader().setDefaultSectionSize(50)
        
        layout_principal.addWidget(self.tabela_clientes)
        
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
        """
        self.tabela_clientes.setStyleSheet(estilo)
        
    def carregar_clientes(self):
        """Carrega a lista de clientes do banco de dados."""
        try:
            self.clientes = ClienteController.listar_clientes()
            self.clientes_filtrados = self.clientes.copy()
            self.atualizar_tabela()
            self.clientes_atualizados.emit()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar os clientes:\n{str(e)}")
            
    def filtrar_clientes(self):
        """Filtra os clientes com base no termo de busca."""
        termo_busca = self.campo_busca.text().lower()
        
        self.clientes_filtrados = self.clientes.copy()
        
        # Filtrar por termo de busca
        if termo_busca:
            self.clientes_filtrados = [
                c for c in self.clientes_filtrados 
                if (termo_busca in c.nome.lower() or 
                    (c.telefone and termo_busca in c.telefone.lower()) or
                    (c.observacoes and termo_busca in c.observacoes.lower()))
            ]
            
        self.atualizar_tabela()
        
    def atualizar_tabela(self):
        """Atualiza a tabela com os clientes."""
        self.tabela_clientes.setRowCount(len(self.clientes_filtrados))
        
        for linha, cliente in enumerate(self.clientes_filtrados):
            # Coluna ID
            item_id = QTableWidgetItem(str(cliente.id))
            item_id.setTextAlignment(Qt.AlignCenter)
            item_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tabela_clientes.setItem(linha, 0, item_id)
            
            # Coluna Nome
            item_nome = QTableWidgetItem(cliente.nome)
            item_nome.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tabela_clientes.setItem(linha, 1, item_nome)
            
            # Coluna Telefone
            telefone = cliente.telefone if cliente.telefone else "-"
            item_telefone = QTableWidgetItem(telefone)
            item_telefone.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tabela_clientes.setItem(linha, 2, item_telefone)
            
            # Coluna Observações
            observacoes = cliente.observacoes if cliente.observacoes else "-"
            item_obs = QTableWidgetItem(observacoes)
            item_obs.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tabela_clientes.setItem(linha, 3, item_obs)
            
            # Coluna Ações (botões)
            widget_acoes = QWidget()
            layout_acoes = QHBoxLayout(widget_acoes)
            layout_acoes.setContentsMargins(10, 5, 10, 5)
            layout_acoes.setSpacing(8)
            
            btn_editar = QPushButton("Editar")
            btn_editar.setObjectName("secondary")
            btn_editar.setFixedSize(80, 30)
            btn_editar.clicked.connect(lambda checked, c=cliente: self.editar_cliente(c))
            layout_acoes.addWidget(btn_editar)
            
            btn_excluir = QPushButton("Excluir")
            btn_excluir.setStyleSheet("""
                QPushButton {
                    background-color: #FF6B6B;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #E55A5A;
                }
            """)
            btn_excluir.setFixedSize(80, 30)
            btn_excluir.clicked.connect(lambda checked, c=cliente: self.excluir_cliente(c))
            layout_acoes.addWidget(btn_excluir)
            
            layout_acoes.addStretch()
            self.tabela_clientes.setCellWidget(linha, 4, widget_acoes)
            
        # Ajustar altura das linhas
        for i in range(self.tabela_clientes.rowCount()):
            self.tabela_clientes.setRowHeight(i, 50)
            
    def adicionar_cliente(self):
        """Abre o formulário para adicionar um novo cliente."""
        formulario = FormularioCliente(parent=self)
        formulario.cliente_salvo.connect(self.cliente_adicionado)
        
        if formulario.exec_():
            self.carregar_clientes()
            
    def editar_cliente(self, cliente: Cliente):
        """Abre o formulário para editar um cliente."""
        formulario = FormularioCliente(cliente=cliente, parent=self)
        formulario.cliente_salvo.connect(self.cliente_atualizado)
        
        if formulario.exec_():
            self.carregar_clientes()
            
    def excluir_cliente(self, cliente: Cliente):
        """Exclui um cliente após confirmação."""
        resposta = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o cliente '{cliente.nome}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if resposta == QMessageBox.Yes:
            try:
                if ClienteController.excluir_cliente(cliente.id):
                    QMessageBox.information(self, "Sucesso", "Cliente excluído com sucesso.")
                    self.carregar_clientes()
                else:
                    QMessageBox.critical(self, "Erro", "Não foi possível excluir o cliente.")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao excluir o cliente:\n{str(e)}")
                
    def cliente_adicionado(self, cliente: Cliente):
        """Callback chamado quando um cliente é adicionado."""
        QMessageBox.information(self, "Sucesso", f"Cliente '{cliente.nome}' adicionado com sucesso.")
        
    def cliente_atualizado(self, cliente: Cliente):
        """Callback chamado quando um cliente é atualizado."""
        QMessageBox.information(self, "Sucesso", f"Cliente '{cliente.nome}' atualizado com sucesso.")
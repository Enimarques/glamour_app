from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMessageBox, QAbstractItemView, QLabel, QLineEdit,
                             QComboBox, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from models.produto import Produto
from controllers.produto_controller import ProdutoController
from ui.formulario_produto import FormularioProduto

class ListaProdutos(QWidget):
    """Widget para exibir e gerenciar a lista de produtos."""
    
    # Sinal emitido quando a lista de produtos é atualizada
    produtos_atualizados = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.produtos = []
        self.produtos_filtrados = []
        self.inicializar_ui()
        self.carregar_produtos()
        
    def inicializar_ui(self):
        """Inicializa a interface do usuário."""
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)
        
        # Cabeçalho com filtros
        self.criar_cabecalho(layout_principal)
        
        # Tabela de produtos
        self.criar_tabela_produtos(layout_principal)
        
        # Aplicar estilo
        self.aplicar_estilo()
        
    def criar_cabecalho(self, layout_principal):
        """Cria o cabeçalho com título e filtros."""
        # Layout do cabeçalho
        layout_cabecalho = QHBoxLayout()
        
        # Título
        lbl_titulo = QLabel("Lista de Produtos")
        lbl_titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333333;
        """)
        layout_cabecalho.addWidget(lbl_titulo)
        
        # Espaçador
        layout_cabecalho.addStretch()
        
        # Filtros
        self.combo_categoria = QComboBox()
        self.combo_categoria.addItem("Todas as categorias")
        self.combo_categoria.addItems(["Semijoias", "Relógios", "Acessórios", "Outros"])
        self.combo_categoria.setMinimumWidth(150)
        self.combo_categoria.currentTextChanged.connect(self.filtrar_produtos)
        layout_cabecalho.addWidget(self.combo_categoria)
        
        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("Buscar produtos...")
        self.campo_busca.setMinimumWidth(200)
        self.campo_busca.textChanged.connect(self.filtrar_produtos)
        layout_cabecalho.addWidget(self.campo_busca)
        
        # Botões
        self.btn_atualizar = QPushButton("Atualizar")
        self.btn_atualizar.setObjectName("secondary")
        self.btn_atualizar.clicked.connect(self.carregar_produtos)
        layout_cabecalho.addWidget(self.btn_atualizar)
        
        self.btn_adicionar = QPushButton("Adicionar Produto")
        self.btn_adicionar.clicked.connect(self.adicionar_produto)
        layout_cabecalho.addWidget(self.btn_adicionar)
        
        layout_principal.addLayout(layout_cabecalho)
        
    def criar_tabela_produtos(self, layout_principal):
        """Cria a tabela de produtos com estilo moderno."""
        self.tabela_produtos = QTableWidget()
        self.tabela_produtos.setColumnCount(7)
        self.tabela_produtos.setHorizontalHeaderLabels([
            "ID", "Nome", "Categoria", "Preço Custo", "Preço Venda", "Quantidade", "Ações"
        ])
        
        # Configurações da tabela
        self.tabela_produtos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela_produtos.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela_produtos.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabela_produtos.setAlternatingRowColors(True)
        
        # Configurar cabeçalho
        header = self.tabela_produtos.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Preço Custo
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Preço Venda
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Quantidade
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Ações
        
        # Altura das linhas
        self.tabela_produtos.verticalHeader().setDefaultSectionSize(50)
        
        layout_principal.addWidget(self.tabela_produtos)
        
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
        """
        self.tabela_produtos.setStyleSheet(estilo)
        
    def carregar_produtos(self):
        """Carrega a lista de produtos do banco de dados."""
        try:
            self.produtos = ProdutoController.listar_produtos()
            self.produtos_filtrados = self.produtos.copy()
            self.atualizar_tabela()
            self.produtos_atualizados.emit()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar os produtos:\n{str(e)}")
            
    def filtrar_produtos(self):
        """Filtra os produtos com base nos critérios selecionados."""
        termo_busca = self.campo_busca.text().lower()
        categoria = self.combo_categoria.currentText()
        
        self.produtos_filtrados = self.produtos.copy()
        
        # Filtrar por categoria
        if categoria != "Todas as categorias":
            self.produtos_filtrados = [
                p for p in self.produtos_filtrados 
                if p.categoria == categoria
            ]
            
        # Filtrar por termo de busca
        if termo_busca:
            self.produtos_filtrados = [
                p for p in self.produtos_filtrados 
                if termo_busca in p.nome.lower() or termo_busca in p.categoria.lower()
            ]
            
        self.atualizar_tabela()
        
    def atualizar_tabela(self):
        """Atualiza a tabela com os produtos."""
        self.tabela_produtos.setRowCount(len(self.produtos_filtrados))
        
        for linha, produto in enumerate(self.produtos_filtrados):
            # Coluna ID
            item_id = QTableWidgetItem(str(produto.id))
            item_id.setTextAlignment(Qt.AlignCenter)
            item_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tabela_produtos.setItem(linha, 0, item_id)
            
            # Coluna Nome
            item_nome = QTableWidgetItem(produto.nome)
            item_nome.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tabela_produtos.setItem(linha, 1, item_nome)
            
            # Coluna Categoria
            item_categoria = QTableWidgetItem(produto.categoria)
            item_categoria.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tabela_produtos.setItem(linha, 2, item_categoria)
            
            # Coluna Preço Custo
            item_custo = QTableWidgetItem(f"R$ {produto.preco_custo:.2f}")
            item_custo.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item_custo.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tabela_produtos.setItem(linha, 3, item_custo)
            
            # Coluna Preço Venda
            item_venda = QTableWidgetItem(f"R$ {produto.preco_venda:.2f}")
            item_venda.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item_venda.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tabela_produtos.setItem(linha, 4, item_venda)
            
            # Coluna Quantidade
            item_quantidade = QTableWidgetItem(str(produto.quantidade))
            item_quantidade.setTextAlignment(Qt.AlignCenter)
            item_quantidade.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            
            # Colorir quantidade baixa
            if produto.quantidade <= 5:
                item_quantidade.setForeground(QColor("#FF6B6B"))  # Vermelho
                item_quantidade.setFont(QFont("", -1, QFont.Bold))
                
            self.tabela_produtos.setItem(linha, 5, item_quantidade)
            
            # Coluna Ações (botões)
            widget_acoes = QWidget()
            layout_acoes = QHBoxLayout(widget_acoes)
            layout_acoes.setContentsMargins(10, 5, 10, 5)
            layout_acoes.setSpacing(8)
            
            btn_editar = QPushButton("Editar")
            btn_editar.setObjectName("secondary")
            btn_editar.setFixedSize(80, 30)
            btn_editar.clicked.connect(lambda checked, p=produto: self.editar_produto(p))
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
            btn_excluir.clicked.connect(lambda checked, p=produto: self.excluir_produto(p))
            layout_acoes.addWidget(btn_excluir)
            
            layout_acoes.addStretch()
            self.tabela_produtos.setCellWidget(linha, 6, widget_acoes)
            
        # Ajustar altura das linhas
        for i in range(self.tabela_produtos.rowCount()):
            self.tabela_produtos.setRowHeight(i, 50)
            
    def adicionar_produto(self):
        """Abre o formulário para adicionar um novo produto."""
        formulario = FormularioProduto(parent=self)
        formulario.produto_salvo.connect(self.produto_adicionado)
        
        if formulario.exec_():
            self.carregar_produtos()
            
    def editar_produto(self, produto: Produto):
        """Abre o formulário para editar um produto."""
        formulario = FormularioProduto(produto=produto, parent=self)
        formulario.produto_salvo.connect(self.produto_atualizado)
        
        if formulario.exec_():
            self.carregar_produtos()
            
    def excluir_produto(self, produto: Produto):
        """Exclui um produto após confirmação."""
        resposta = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o produto '{produto.nome}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if resposta == QMessageBox.Yes:
            try:
                if ProdutoController.excluir_produto(produto.id):
                    QMessageBox.information(self, "Sucesso", "Produto excluído com sucesso.")
                    self.carregar_produtos()
                else:
                    QMessageBox.critical(self, "Erro", "Não foi possível excluir o produto.")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao excluir o produto:\n{str(e)}")
                
    def produto_adicionado(self, produto: Produto):
        """Callback chamado quando um produto é adicionado."""
        QMessageBox.information(self, "Sucesso", f"Produto '{produto.nome}' adicionado com sucesso.")
        
    def produto_atualizado(self, produto: Produto):
        """Callback chamado quando um produto é atualizado."""
        QMessageBox.information(self, "Sucesso", f"Produto '{produto.nome}' atualizado com sucesso.")
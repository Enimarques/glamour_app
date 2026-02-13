from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMessageBox, QAbstractItemView, QLabel, QLineEdit,
                             QComboBox, QSpacerItem, QSizePolicy, QFrame)
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
        
        # Cabeçalho da página
        self.criar_cabecalho_pagina(layout_principal)
        
        # Barra de ferramentas
        self.criar_barra_ferramentas(layout_principal)
        
        # Cards de resumo
        self.criar_cards_resumo(layout_principal)
        
        # Tabela de produtos
        self.criar_tabela_produtos(layout_principal)
        
    def criar_cabecalho_pagina(self, layout_principal):
        """Cria o cabeçalho da página com título e breadcrumb."""
        layout_header = QHBoxLayout()
        
        # Layout para ícone + título
        layout_titulo = QHBoxLayout()
        
        lbl_icone = QLabel("💎")
        lbl_icone.setObjectName("breadcrumb_icon")
        layout_titulo.addWidget(lbl_icone)
        
        lbl_titulo = QLabel("Produtos")
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
        
        lbl_atual = QLabel("Produtos")
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
        btn_adicionar = QPushButton("✚ Adicionar Produto")
        btn_adicionar.setObjectName("btn_adicionar")
        btn_adicionar.clicked.connect(self.adicionar_produto)
        layout_toolbar.addWidget(btn_adicionar)
        
        btn_atualizar = QPushButton("🔄 Atualizar")
        btn_atualizar.setObjectName("btn_mais_acoes")
        btn_atualizar.clicked.connect(self.carregar_produtos)
        layout_toolbar.addWidget(btn_atualizar)
        
        layout_toolbar.addStretch()
        
        # Filtros
        self.combo_categoria = QComboBox()
        self.combo_categoria.addItem("Todas as categorias")
        self.combo_categoria.addItems(["Semijoias", "Relógios", "Acessórios", "Outros"])
        self.combo_categoria.setMinimumWidth(180)
        self.combo_categoria.currentTextChanged.connect(self.filtrar_produtos)
        layout_toolbar.addWidget(self.combo_categoria)
        
        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("🔍 Buscar produtos...")
        self.campo_busca.setMinimumWidth(250)
        self.campo_busca.textChanged.connect(self.filtrar_produtos)
        layout_toolbar.addWidget(self.campo_busca)
        
        layout_principal.addWidget(frame_toolbar)

    def criar_cards_resumo(self, layout_principal):
        """Cria cards de resumo para os produtos."""
        layout_cards = QHBoxLayout()
        layout_cards.setSpacing(20)
        
        # Card Total de Produtos
        self.card_total = self.criar_card_estilizado(
            "Total de Produtos", "0", "📦", "summary_card_total"
        )
        layout_cards.addWidget(self.card_total)
        
        # Card Estoque Baixo
        self.card_estoque_baixo = self.criar_card_estilizado(
            "Estoque Baixo", "0", "⚠️", "summary_card_vencidos"
        )
        layout_cards.addWidget(self.card_estoque_baixo)
        
        # Card Valor em Estoque
        self.card_valor_estoque = self.criar_card_estilizado(
            "Valor em Estoque", "R$ 0,00", "💰", "summary_card_recebidos"
        )
        layout_cards.addWidget(self.card_valor_estoque)
        
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
        if titulo == "Total de Produtos": self.lbl_total_produtos = lbl_valor
        elif titulo == "Estoque Baixo": self.lbl_estoque_baixo = lbl_valor
        elif titulo == "Valor em Estoque": self.lbl_valor_estoque = lbl_valor
        
        layout.addWidget(lbl_valor)
        
        return frame

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
        self.tabela_produtos.setShowGrid(False)  # Remove grades verticais para visual mais limpo
        
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
        
    def carregar_produtos(self):
        """Carrega a lista de produtos do banco de dados."""
        try:
            self.produtos = ProdutoController.listar_produtos()
            self.produtos_filtrados = self.produtos.copy()
            self.atualizar_tabela()
            self.atualizar_cards_resumo()
            self.produtos_atualizados.emit()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar os produtos:\n{str(e)}")
            
    def atualizar_cards_resumo(self):
        """Atualiza os valores nos cards de resumo."""
        total_produtos = len(self.produtos)
        estoque_baixo = len([p for p in self.produtos if p.quantidade <= 5])
        valor_estoque = sum(p.preco_custo * p.quantidade for p in self.produtos)
        
        self.lbl_total_produtos.setText(str(total_produtos))
        self.lbl_estoque_baixo.setText(str(estoque_baixo))
        self.lbl_valor_estoque.setText(f"R$ {valor_estoque:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

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
            
            btn_editar = QPushButton("✏️")
            btn_editar.setObjectName("btn_action_edit")
            btn_editar.setToolTip("Editar Produto")
            btn_editar.clicked.connect(lambda checked, p=produto: self.editar_produto(p))
            layout_acoes.addWidget(btn_editar)
            
            btn_excluir = QPushButton("🗑️")
            btn_excluir.setObjectName("btn_action_delete")
            btn_excluir.setToolTip("Excluir Produto")
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
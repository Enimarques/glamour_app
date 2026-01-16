from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QScrollArea, QFrame, QMessageBox, QLabel, QLineEdit,
                             QComboBox, QSpinBox, QGridLayout, QGroupBox,
                             QDialog, QListWidget, QTextEdit)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont, QColor
from models.produto import Produto
from models.cliente import Cliente
from models.carrinho import CarrinhoCompras, ItemCarrinho
from controllers.produto_controller import ProdutoController
from controllers.cliente_controller import ClienteController
from controllers.venda_controller import VendaController
from ui.formulario_produto import FormularioProduto
import os

class ListaProdutosMarketplace(QWidget):
    """Widget para exibir e gerenciar produtos em estilo marketplace com carrinho de compras."""
    
    # Sinal emitido quando a lista de produtos é atualizada
    produtos_atualizados = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.produtos = []
        self.produtos_filtrados = []
        self.carrinho = CarrinhoCompras()
        self.inicializar_ui()
        self.carregar_produtos()
        
    def inicializar_ui(self):
        """Inicializa a interface do usuário."""
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(15)
        
        # Cabeçalho com filtros e carrinho
        self.criar_cabecalho(layout_principal)
        
        # Conteúdo principal (produtos + carrinho)
        self.criar_conteudo_principal(layout_principal)
        
        # Aplicar estilo
        self.aplicar_estilo()
        
    def criar_cabecalho(self, layout_principal):
        """Cria o cabeçalho com título, filtros e carrinho."""
        # Layout do cabeçalho
        layout_cabecalho = QHBoxLayout()
        
        # Título
        lbl_titulo = QLabel("Marketplace de Produtos")
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
        
        # Barra do carrinho
        self.criar_barra_carrinho(layout_principal)
        
    def criar_barra_carrinho(self, layout_principal):
        """Cria a barra de informações do carrinho."""
        self.frame_carrinho = QFrame()
        self.frame_carrinho.setStyleSheet("""
            QFrame {
                background-color: #4A90E2;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        layout_carrinho = QHBoxLayout(self.frame_carrinho)
        
        self.lbl_info_carrinho = QLabel("Carrinho vazio")
        self.lbl_info_carrinho.setStyleSheet("""
            color: white;
            font-weight: bold;
            font-size: 16px;
        """)
        
        layout_carrinho.addWidget(self.lbl_info_carrinho)
        layout_carrinho.addStretch()
        
        self.btn_ver_carrinho = QPushButton("Ver Carrinho")
        self.btn_ver_carrinho.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #4A90E2;
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F0F5FF;
            }
        """)
        self.btn_ver_carrinho.clicked.connect(self.abrir_carrinho)
        layout_carrinho.addWidget(self.btn_ver_carrinho)
        
        layout_principal.addWidget(self.frame_carrinho)
        
    def criar_conteudo_principal(self, layout_principal):
        """Cria o conteúdo principal com grade de produtos."""
        # Área de rolagem para os produtos
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
            }
        """)
        
        # Widget container para os produtos
        self.container_produtos = QWidget()
        self.layout_grade_produtos = QGridLayout(self.container_produtos)
        self.layout_grade_produtos.setSpacing(20)
        self.layout_grade_produtos.setContentsMargins(10, 10, 10, 10)
        
        self.scroll_area.setWidget(self.container_produtos)
        layout_principal.addWidget(self.scroll_area)
        
    def aplicar_estilo(self):
        """Aplica o estilo moderno à interface."""
        estilo = """
        QWidget {
            background-color: #F8F9FA;
            font-family: Arial, sans-serif;
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
        
        QPushButton#secondary {
            background-color: #F8F9FA;
            color: #333333;
            border: 1px solid #E0E0E0;
        }
        
        QPushButton#secondary:hover {
            background-color: #E9ECEF;
        }
        """
        self.setStyleSheet(estilo)
        
    def carregar_produtos(self):
        """Carrega a lista de produtos do banco de dados."""
        try:
            self.produtos = ProdutoController.listar_produtos()
            self.produtos_filtrados = self.produtos.copy()
            self.atualizar_grade_produtos()
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
            
        self.atualizar_grade_produtos()
        
    def atualizar_grade_produtos(self):
        """Atualiza a grade de produtos com os produtos filtrados."""
        # Limpar layout existente
        for i in reversed(range(self.layout_grade_produtos.count())): 
            widget = self.layout_grade_produtos.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                
        # Adicionar produtos filtrados
        colunas = 4
        for index, produto in enumerate(self.produtos_filtrados):
            linha = index // colunas
            coluna = index % colunas
            widget_produto = self.criar_widget_produto(produto)
            self.layout_grade_produtos.addWidget(widget_produto, linha, coluna)
            
    def criar_widget_produto(self, produto: Produto) -> QWidget:
        """Cria um widget para exibir um produto."""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 12px;
                padding: 15px;
            }
            QFrame:hover {
                border: 1px solid #4A90E2;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        
        # Imagem do produto (placeholder)
        lbl_imagem = QLabel()
        lbl_imagem.setStyleSheet("""
            background-color: #F8F9FA;
            border-radius: 8px;
            min-height: 150px;
            max-height: 150px;
        """)
        lbl_imagem.setAlignment(Qt.AlignCenter)
        
        # Se tiver imagem, mostrar (por enquanto usando placeholder)
        if produto.caminho_imagem and os.path.exists(produto.caminho_imagem):
            pixmap = QPixmap(produto.caminho_imagem)
            lbl_imagem.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            lbl_imagem.setText("📷\nImagem")
            lbl_imagem.setStyleSheet("""
                background-color: #F8F9FA;
                border-radius: 8px;
                min-height: 150px;
                max-height: 150px;
                color: #666666;
                font-size: 14px;
            """)
            
        layout.addWidget(lbl_imagem)
        
        # Nome do produto
        lbl_nome = QLabel(produto.nome)
        lbl_nome.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #333333;
            margin-top: 5px;
        """)
        lbl_nome.setWordWrap(True)
        layout.addWidget(lbl_nome)
        
        # Categoria
        lbl_categoria = QLabel(produto.categoria)
        lbl_categoria.setStyleSheet("""
            font-size: 13px;
            color: #666666;
            margin-bottom: 5px;
        """)
        layout.addWidget(lbl_categoria)
        
        # Preço
        lbl_preco = QLabel(f"R$ {produto.preco_venda:.2f}")
        lbl_preco.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #4A90E2;
            margin: 5px 0;
        """)
        layout.addWidget(lbl_preco)
        
        # Estoque
        lbl_estoque = QLabel(f"Estoque: {produto.quantidade}")
        lbl_estoque.setStyleSheet("""
            font-size: 12px;
            color: #666666;
        """)
        layout.addWidget(lbl_estoque)
        
        # Botão de adicionar ao carrinho
        btn_adicionar = QPushButton("Adicionar ao Carrinho")
        btn_adicionar.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        btn_adicionar.clicked.connect(lambda _, p=produto: self.adicionar_ao_carrinho(p))
        layout.addWidget(btn_adicionar)
        
        return widget
        
    def adicionar_ao_carrinho(self, produto: Produto):
        """Adiciona um produto ao carrinho."""
        self.carrinho.adicionar_item(produto)
        self.atualizar_info_carrinho()
        QMessageBox.information(self, "Carrinho", f"{produto.nome} adicionado ao carrinho!")
        
    def atualizar_info_carrinho(self):
        """Atualiza as informações do carrinho na barra superior."""
        if self.carrinho.quantidade_itens > 0:
            self.lbl_info_carrinho.setText(
                f"Carrinho: {self.carrinho.quantidade_itens} itens - "
                f"Total: R$ {self.carrinho.total:.2f}"
            )
        else:
            self.lbl_info_carrinho.setText("Carrinho vazio")
            
    def abrir_carrinho(self):
        """Abre a janela do carrinho de compras."""
        dialog = DialogoCarrinho(self.carrinho, self)
        if dialog.exec_() == QDialog.Accepted:
            # Se o carrinho foi finalizado, limpar o carrinho
            self.carrinho.limpar()
            self.atualizar_info_carrinho()
            self.carregar_produtos()  # Atualizar estoque
            
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

class DialogoCarrinho(QDialog):
    """Diálogo para visualizar e finalizar o carrinho de compras."""
    
    def __init__(self, carrinho: CarrinhoCompras, parent=None):
        super().__init__(parent)
        self.carrinho = carrinho
        self.clientes = []
        self.inicializar_ui()
        self.carregar_clientes()
        
    def inicializar_ui(self):
        """Inicializa a interface do diálogo."""
        self.setWindowTitle("Carrinho de Compras")
        self.setGeometry(200, 200, 800, 600)
        
        layout_principal = QVBoxLayout(self)
        
        # Título
        lbl_titulo = QLabel("Carrinho de Compras")
        lbl_titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 20px;
        """)
        layout_principal.addWidget(lbl_titulo)
        
        # Conteúdo do carrinho
        self.criar_conteudo_carrinho(layout_principal)
        
        # Cliente e finalização
        self.criar_secao_finalizacao(layout_principal)
        
        # Botões
        self.criar_botoes(layout_principal)
        
    def criar_conteudo_carrinho(self, layout_principal):
        """Cria a seção com os itens do carrinho."""
        # Área de rolagem para os itens
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        # Container para os itens
        self.container_itens = QWidget()
        self.layout_itens = QVBoxLayout(self.container_itens)
        self.layout_itens.setSpacing(10)
        
        self.scroll_area.setWidget(self.container_itens)
        layout_principal.addWidget(self.scroll_area)
        
        # Atualizar itens do carrinho
        self.atualizar_itens_carrinho()
        
    def atualizar_itens_carrinho(self):
        """Atualiza a lista de itens no carrinho."""
        # Limpar layout existente
        for i in reversed(range(self.layout_itens.count())): 
            widget = self.layout_itens.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                
        # Adicionar itens do carrinho
        for item in self.carrinho.obter_itens():
            widget_item = self.criar_widget_item_carrinho(item)
            self.layout_itens.addWidget(widget_item)
            
        # Adicionar espaçador
        self.layout_itens.addStretch()
        
    def criar_widget_item_carrinho(self, item: ItemCarrinho) -> QWidget:
        """Cria um widget para exibir um item do carrinho."""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        layout = QHBoxLayout(widget)
        
        # Informações do produto
        layout_info = QVBoxLayout()
        
        lbl_nome = QLabel(item.produto.nome)
        lbl_nome.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout_info.addWidget(lbl_nome)
        
        lbl_categoria = QLabel(item.produto.categoria)
        lbl_categoria.setStyleSheet("color: #666666;")
        layout_info.addWidget(lbl_categoria)
        
        layout.addLayout(layout_info)
        
        # Preço unitário
        lbl_preco_unitario = QLabel(f"R$ {item.produto.preco_venda:.2f}")
        lbl_preco_unitario.setStyleSheet("font-size: 16px;")
        layout.addWidget(lbl_preco_unitario)
        
        # Quantidade
        spin_quantidade = QSpinBox()
        spin_quantidade.setRange(1, item.produto.quantidade)
        spin_quantidade.setValue(item.quantidade)
        spin_quantidade.valueChanged.connect(
            lambda value, pid=item.produto.id: self.atualizar_quantidade(pid, value)
        )
        layout.addWidget(spin_quantidade)
        
        # Subtotal
        lbl_subtotal = QLabel(f"R$ {item.subtotal:.2f}")
        lbl_subtotal.setStyleSheet("font-weight: bold; font-size: 16px; color: #4A90E2;")
        layout.addWidget(lbl_subtotal)
        
        # Botão remover
        btn_remover = QPushButton("Remover")
        btn_remover.setStyleSheet("""
            QPushButton {
                background-color: #FF6B6B;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #E55A5A;
            }
        """)
        btn_remover.clicked.connect(lambda _, pid=item.produto.id: self.remover_item(pid))
        layout.addWidget(btn_remover)
        
        return widget
        
    def atualizar_quantidade(self, produto_id: int, quantidade: int):
        """Atualiza a quantidade de um item no carrinho."""
        self.carrinho.atualizar_quantidade(produto_id, quantidade)
        self.atualizar_resumo()
        
    def remover_item(self, produto_id: int):
        """Remove um item do carrinho."""
        self.carrinho.remover_item(produto_id)
        self.atualizar_itens_carrinho()
        self.atualizar_resumo()
        
    def criar_secao_finalizacao(self, layout_principal):
        """Cria a seção para finalizar a compra."""
        # Grupo para seleção de cliente
        grupo_cliente = QGroupBox("Finalizar Compra")
        layout_grupo = QVBoxLayout(grupo_cliente)
        
        # Seleção de cliente
        layout_cliente = QHBoxLayout()
        layout_cliente.addWidget(QLabel("Cliente:"))
        
        self.combo_clientes = QComboBox()
        self.combo_clientes.addItem("Selecionar cliente...")
        layout_cliente.addWidget(self.combo_clientes)
        
        btn_novo_cliente = QPushButton("Novo Cliente")
        btn_novo_cliente.clicked.connect(self.adicionar_cliente)
        layout_cliente.addWidget(btn_novo_cliente)
        
        layout_grupo.addLayout(layout_cliente)
        
        # Resumo do pedido
        self.criar_resumo_pedido(layout_grupo)
        
        layout_principal.addWidget(grupo_cliente)
        
    def criar_resumo_pedido(self, layout_grupo):
        """Cria o resumo do pedido."""
        self.frame_resumo = QFrame()
        self.frame_resumo.setStyleSheet("""
            QFrame {
                background-color: #F8F9FA;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        layout_resumo = QVBoxLayout(self.frame_resumo)
        
        lbl_resumo_titulo = QLabel("Resumo do Pedido")
        lbl_resumo_titulo.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 10px;")
        layout_resumo.addWidget(lbl_resumo_titulo)
        
        self.lbl_resumo_itens = QLabel()
        layout_resumo.addWidget(self.lbl_resumo_itens)
        
        self.lbl_resumo_total = QLabel()
        self.lbl_resumo_total.setStyleSheet("font-weight: bold; font-size: 18px; color: #4A90E2;")
        layout_resumo.addWidget(self.lbl_resumo_total)
        
        layout_grupo.addWidget(self.frame_resumo)
        
        # Atualizar resumo inicial
        self.atualizar_resumo()
        
    def atualizar_resumo(self):
        """Atualiza o resumo do pedido."""
        self.lbl_resumo_itens.setText(f"Itens: {self.carrinho.quantidade_itens}")
        self.lbl_resumo_total.setText(f"Total: R$ {self.carrinho.total:.2f}")
        
    def criar_botoes(self, layout_principal):
        """Cria os botões do diálogo."""
        layout_botoes = QHBoxLayout()
        layout_botoes.addStretch()
        
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setObjectName("secondary")
        self.btn_cancelar.clicked.connect(self.reject)
        layout_botoes.addWidget(self.btn_cancelar)
        
        self.btn_finalizar = QPushButton("Finalizar Compra")
        self.btn_finalizar.clicked.connect(self.finalizar_compra)
        layout_botoes.addWidget(self.btn_finalizar)
        
        layout_principal.addLayout(layout_botoes)
        
    def carregar_clientes(self):
        """Carrega a lista de clientes."""
        try:
            self.clientes = ClienteController.listar_clientes()
            self.combo_clientes.clear()
            self.combo_clientes.addItem("Selecionar cliente...")
            for cliente in self.clientes:
                self.combo_clientes.addItem(f"{cliente.nome} ({cliente.telefone or 'Sem telefone'})", cliente.id)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar os clientes:\n{str(e)}")
            
    def adicionar_cliente(self):
        """Abre o formulário para adicionar um novo cliente."""
        # Para simplificar, vamos mostrar uma mensagem
        QMessageBox.information(self, "Informação", "Funcionalidade de adicionar cliente não implementada neste diálogo.")
        
    def finalizar_compra(self):
        """Finaliza a compra e registra a venda."""
        # Verificar se há itens no carrinho
        if self.carrinho.quantidade_itens == 0:
            QMessageBox.warning(self, "Aviso", "O carrinho está vazio.")
            return
            
        # Verificar se um cliente foi selecionado
        cliente_index = self.combo_clientes.currentIndex()
        if cliente_index <= 0:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione um cliente.")
            return
            
        cliente_id = self.combo_clientes.currentData()
        
        # Preparar itens para a venda
        itens_venda = []
        for item in self.carrinho.obter_itens():
            # Verificar estoque
            if item.quantidade > item.produto.quantidade:
                QMessageBox.warning(
                    self, 
                    "Estoque Insuficiente", 
                    f"Não há estoque suficiente para '{item.produto.nome}'. "
                    f"Disponível: {item.produto.quantidade}, Solicitado: {item.quantidade}"
                )
                return
                
            itens_venda.append({
                'produto_id': item.produto.id,
                'quantidade': item.quantidade,
                'preco_unitario': item.produto.preco_venda
            })
            
        # Registrar a venda
        try:
            venda = VendaController.criar_venda(
                cliente_id=cliente_id,
                itens=itens_venda,
                tipo_pagamento="avista"  # Por padrão, venda à vista
            )
            
            if venda:
                QMessageBox.information(
                    self, 
                    "Sucesso", 
                    f"Venda registrada com sucesso!\nID da venda: {venda.id}\nTotal: R$ {venda.valor_total:.2f}"
                )
                self.accept()  # Fechar o diálogo
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível registrar a venda.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao registrar a venda:\n{str(e)}")
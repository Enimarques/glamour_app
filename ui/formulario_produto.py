from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox,
                             QPushButton, QLabel, QFileDialog, QMessageBox,
                             QGroupBox, QWidget, QFrame)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QPixmap
from controllers.produto_controller import ProdutoController
from models.produto import Produto
import os

class FormularioProduto(QDialog):
    """Formulário para cadastro e edição de produtos."""
    
    # Sinal emitido quando um produto é salvo
    produto_salvo = pyqtSignal(Produto)
    
    def __init__(self, produto=None, parent=None):
        """
        Inicializa o formulário.
        
        Args:
            produto (Produto, opcional): Produto a ser editado. Se None, cria um novo.
            parent (QWidget, opcional): Widget pai.
        """
        super().__init__(parent)
        self.produto = produto
        self.caminho_imagem = None
        self.inicializar_ui()
        
    def inicializar_ui(self):
        """Inicializa a interface do usuário."""
        if self.produto:
            self.setWindowTitle(f"Editar Produto: {self.produto.nome}")
        else:
            self.setWindowTitle("Novo Produto")
            
        self.setModal(True)
        self.resize(500, 400)
        
        # Layout principal
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)
        
        # Título
        lbl_titulo = QLabel("Cadastro de Produto" if not self.produto else "Edição de Produto")
        lbl_titulo.setObjectName("titulo_pagina")
        layout_principal.addWidget(lbl_titulo)
        
        # Grupo de informações básicas
        self.criar_grupo_informacoes(layout_principal)
        
        # Grupo de precificação
        self.criar_grupo_precificacao(layout_principal)
        
        # Grupo de estoque
        self.criar_grupo_estoque(layout_principal)
        
        # Grupo de imagem
        self.criar_grupo_imagem(layout_principal)
        
        # Botões
        self.criar_botoes(layout_principal)
        
        # Preenche os campos se estiver editando um produto
        if self.produto:
            self.preencher_campos()
            
    def criar_grupo_informacoes(self, layout_principal):
        """Cria o grupo de informações básicas."""
        grupo_info = QGroupBox("Informações Básicas")
        layout_grupo = QFormLayout(grupo_info)
        layout_grupo.setContentsMargins(20, 20, 20, 20)
        layout_grupo.setSpacing(15)
        
        # Campo nome
        self.campo_nome = QLineEdit()
        self.campo_nome.setPlaceholderText("Digite o nome do produto")
        layout_grupo.addRow(QLabel("Nome:"), self.campo_nome)
        
        # Campo categoria
        self.campo_categoria = QComboBox()
        self.campo_categoria.addItems(["Semijoias", "Relógios", "Acessórios", "Outros"])
        layout_grupo.addRow(QLabel("Categoria:"), self.campo_categoria)
        
        layout_principal.addWidget(grupo_info)
        
    def criar_grupo_precificacao(self, layout_principal):
        """Cria o grupo de precificação."""
        grupo_preco = QGroupBox("Precificação")
        layout_grupo = QFormLayout(grupo_preco)
        layout_grupo.setContentsMargins(20, 20, 20, 20)
        layout_grupo.setSpacing(15)
        
        # Campo preço de custo
        self.campo_preco_custo = QDoubleSpinBox()
        self.campo_preco_custo.setRange(0, 999999.99)
        self.campo_preco_custo.setDecimals(2)
        self.campo_preco_custo.setPrefix("R$ ")
        self.campo_preco_custo.setMaximumWidth(150)
        layout_grupo.addRow(QLabel("Preço de Custo:"), self.campo_preco_custo)
        
        # Campo preço de venda
        self.campo_preco_venda = QDoubleSpinBox()
        self.campo_preco_venda.setRange(0, 999999.99)
        self.campo_preco_venda.setDecimals(2)
        self.campo_preco_venda.setPrefix("R$ ")
        self.campo_preco_venda.setMaximumWidth(150)
        layout_grupo.addRow(QLabel("Preço de Venda:"), self.campo_preco_venda)
        
        layout_principal.addWidget(grupo_preco)
        
    def criar_grupo_estoque(self, layout_principal):
        """Cria o grupo de estoque."""
        grupo_estoque = QGroupBox("Estoque")
        layout_grupo = QFormLayout(grupo_estoque)
        layout_grupo.setContentsMargins(20, 20, 20, 20)
        layout_grupo.setSpacing(15)
        
        # Campo quantidade
        self.campo_quantidade = QSpinBox()
        self.campo_quantidade.setRange(0, 999999)
        self.campo_quantidade.setMaximumWidth(150)
        layout_grupo.addRow(QLabel("Quantidade:"), self.campo_quantidade)
        
        layout_principal.addWidget(grupo_estoque)
        
    def criar_grupo_imagem(self, layout_principal):
        """Cria o grupo de imagem."""
        grupo_imagem = QGroupBox("Imagem do Produto")
        layout_grupo = QVBoxLayout(grupo_imagem)
        layout_grupo.setContentsMargins(20, 20, 20, 20)
        layout_grupo.setSpacing(15)
        
        # Campo de imagem
        layout_imagem = QHBoxLayout()
        self.campo_caminho_imagem = QLineEdit()
        self.campo_caminho_imagem.setPlaceholderText("Caminho da imagem (opcional)")
        self.campo_caminho_imagem.setReadOnly(True)
        btn_selecionar_imagem = QPushButton("Selecionar Imagem")
        btn_selecionar_imagem.setObjectName("secondary")
        btn_selecionar_imagem.clicked.connect(self.selecionar_imagem)
        layout_imagem.addWidget(self.campo_caminho_imagem)
        layout_imagem.addWidget(btn_selecionar_imagem)
        
        layout_grupo.addLayout(layout_imagem)
        
        layout_principal.addWidget(grupo_imagem)
        
    def criar_botoes(self, layout_principal):
        """Cria os botões do formulário."""
        layout_botoes = QHBoxLayout()
        layout_botoes.setSpacing(15)
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("secondary")
        btn_cancelar.clicked.connect(self.reject)
        layout_botoes.addWidget(btn_cancelar)
        
        btn_salvar = QPushButton("Salvar")
        btn_salvar.setObjectName("primary")
        btn_salvar.clicked.connect(self.salvar)
        btn_salvar.setDefault(True)
        layout_botoes.addWidget(btn_salvar)
        
        layout_principal.addLayout(layout_botoes)
        
    def preencher_campos(self):
        """Preenche os campos do formulário com os dados do produto."""
        self.campo_nome.setText(self.produto.nome)
        index_categoria = self.campo_categoria.findText(self.produto.categoria)
        if index_categoria >= 0:
            self.campo_categoria.setCurrentIndex(index_categoria)
        self.campo_preco_custo.setValue(self.produto.preco_custo)
        self.campo_preco_venda.setValue(self.produto.preco_venda)
        self.campo_quantidade.setValue(self.produto.quantidade)
        if self.produto.caminho_imagem:
            self.campo_caminho_imagem.setText(self.produto.caminho_imagem)
            self.caminho_imagem = self.produto.caminho_imagem
            
    def selecionar_imagem(self):
        """Abre diálogo para seleção de imagem."""
        caminho, _ = QFileDialog.getOpenFileName(
            self, 
            "Selecionar Imagem", 
            "", 
            "Imagens (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if caminho:
            self.campo_caminho_imagem.setText(os.path.basename(caminho))
            self.caminho_imagem = caminho
            
    def salvar(self):
        """Salva o produto."""
        nome = self.campo_nome.text().strip()
        categoria = self.campo_categoria.currentText()
        preco_custo = self.campo_preco_custo.value()
        preco_venda = self.campo_preco_venda.value()
        quantidade = self.campo_quantidade.value()
        
        # Validação básica
        if not nome:
            QMessageBox.warning(self, "Aviso", "Por favor, informe o nome do produto.")
            self.campo_nome.setFocus()
            return
            
        if preco_venda <= 0:
            QMessageBox.warning(self, "Aviso", "O preço de venda deve ser maior que zero.")
            self.campo_preco_venda.setFocus()
            return
            
        try:
            if self.produto:
                # Atualiza produto existente
                self.produto = ProdutoController.atualizar_produto(
                    self.produto.id,
                    nome=nome,
                    categoria=categoria,
                    preco_custo=preco_custo,
                    preco_venda=preco_venda,
                    quantidade=quantidade,
                    caminho_imagem=self.caminho_imagem
                )
            else:
                # Cria novo produto
                self.produto = ProdutoController.criar_produto(
                    nome=nome,
                    categoria=categoria,
                    preco_custo=preco_custo,
                    preco_venda=preco_venda,
                    quantidade=quantidade,
                    caminho_imagem=self.caminho_imagem
                )
                
            if self.produto:
                self.produto_salvo.emit(self.produto)
                self.accept()
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível salvar o produto.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao salvar o produto:\n{str(e)}")
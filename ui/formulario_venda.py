from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox,
                             QPushButton, QLabel, QMessageBox, QTableWidget,
                             QTableWidgetItem, QHeaderView, QAbstractItemView,
                             QGroupBox, QWidget, QDateEdit, QTextEdit, QCheckBox,
                             QStackedWidget, QFrame)
from PyQt5.QtCore import pyqtSignal, Qt, QDate
from PyQt5.QtGui import QFont
from controllers.venda_controller import VendaController
from controllers.produto_controller import ProdutoController
from controllers.cliente_controller import ClienteController
from models.venda import Venda
from models.produto import Produto
from models.cliente import Cliente
from datetime import datetime

class FormularioVenda(QDialog):
    """Formulário para registro e visualização de vendas."""
    
    # Sinal emitido quando uma venda é registrada
    venda_registrada = pyqtSignal(Venda)
    
    def __init__(self, venda: Venda = None, parent=None):
        super().__init__(parent)
        self.venda = venda
        self.clientes = []
        self.produtos = []
        self.itens_venda = []  # Lista de itens sendo adicionados à venda
        self.inicializar_ui()
        self.carregar_dados()
        
        if venda:
            self.preencher_campos_edicao()
            
    def inicializar_ui(self):
        """Inicializa a interface do usuário."""
        self.setWindowTitle("Registro de Venda" if not self.venda else "Edição de Venda")
        self.setModal(True)
        self.resize(800, 600)
        
        layout_principal = QVBoxLayout(self)
        
        # Abas para diferentes seções
        self.stacked_widget = QStackedWidget()
        
        # Aba de informações básicas
        self.criar_aba_informacoes_basicas()
        
        # Aba de itens da venda
        self.criar_aba_itens_venda()
        
        layout_principal.addWidget(self.stacked_widget)
        
        # Botões de navegação
        self.criar_botoes_navegacao(layout_principal)
        
        # Botões de ação
        self.criar_botoes_acao(layout_principal)
        
    def criar_aba_informacoes_basicas(self):
        """Cria a aba de informações básicas da venda."""
        widget_info = QWidget()
        layout_info = QVBoxLayout(widget_info)
        
        # Título
        lbl_titulo = QLabel("Informações Básicas da Venda")
        lbl_titulo.setObjectName("titulo_secao")
        layout_info.addWidget(lbl_titulo)
        
        # Grupo de cliente
        grupo_cliente = QGroupBox("Cliente")
        layout_cliente = QFormLayout(grupo_cliente)
        
        self.combo_clientes = QComboBox()
        self.combo_clientes.addItem("Selecionar cliente...")
        layout_cliente.addRow("Cliente:", self.combo_clientes)
        
        layout_info.addWidget(grupo_cliente)
        
        # Grupo de pagamento
        grupo_pagamento = QGroupBox("Pagamento")
        layout_pagamento = QFormLayout(grupo_pagamento)
        
        # Tipo de pagamento
        self.combo_tipo_pagamento = QComboBox()
        self.combo_tipo_pagamento.addItems([
            "Dinheiro", 
            "Cartão Crédito", 
            "Cartão Débito", 
            "PIX",
            "Parcelado Boleto",
            "Parcelado Promissória"
        ])
        self.combo_tipo_pagamento.currentTextChanged.connect(self.on_tipo_pagamento_changed)
        layout_pagamento.addRow("Tipo de Pagamento:", self.combo_tipo_pagamento)
        
        # Dia de vencimento (apenas para vendas parceladas)
        self.widget_dia_vencimento = QWidget()
        layout_dia_vencimento = QHBoxLayout(self.widget_dia_vencimento)
        
        self.spin_dia_vencimento = QSpinBox()
        self.spin_dia_vencimento.setRange(1, 31)
        self.spin_dia_vencimento.setValue(10)  # Valor padrão
        layout_dia_vencimento.addWidget(self.spin_dia_vencimento)
        
        lbl_dia_info = QLabel("(Dia do mês para vencimento)")
        layout_dia_vencimento.addWidget(lbl_dia_info)
        layout_dia_vencimento.addStretch()
        
        layout_pagamento.addRow("Dia de Vencimento:", self.widget_dia_vencimento)
        
        # Ocultar inicialmente o campo de dia de vencimento
        self.widget_dia_vencimento.setVisible(False)
        
        layout_info.addWidget(grupo_pagamento)
        
        # Grupo de data
        grupo_data = QGroupBox("Data da Venda")
        layout_data = QFormLayout(grupo_data)
        
        self.date_venda = QDateEdit()
        self.date_venda.setDate(QDate.currentDate())
        self.date_venda.setDisplayFormat("dd/MM/yyyy")
        layout_data.addRow("Data:", self.date_venda)
        
        layout_info.addWidget(grupo_data)
        
        layout_info.addStretch()
        self.stacked_widget.addWidget(widget_info)
        
    def criar_aba_itens_venda(self):
        """Cria a aba de itens da venda."""
        widget_itens = QWidget()
        layout_itens = QVBoxLayout(widget_itens)
        
        # Título
        lbl_titulo = QLabel("Itens da Venda")
        lbl_titulo.setObjectName("titulo_secao")
        layout_itens.addWidget(lbl_titulo)
        
        # Grupo para adicionar itens
        grupo_adicionar = QGroupBox("Adicionar Item")
        layout_adicionar = QHBoxLayout(grupo_adicionar)
        
        # Seleção de produto
        self.combo_produtos = QComboBox()
        layout_adicionar.addWidget(QLabel("Produto:"))
        layout_adicionar.addWidget(self.combo_produtos)
        
        # Quantidade
        self.spin_quantidade = QSpinBox()
        self.spin_quantidade.setRange(1, 999)
        self.spin_quantidade.setValue(1)
        layout_adicionar.addWidget(QLabel("Quantidade:"))
        layout_adicionar.addWidget(self.spin_quantidade)
        
        # Botão adicionar
        self.btn_adicionar_item = QPushButton("Adicionar Item")
        self.btn_adicionar_item.clicked.connect(self.adicionar_item_venda)
        layout_adicionar.addWidget(self.btn_adicionar_item)
        
        layout_itens.addWidget(grupo_adicionar)
        
        # Tabela de itens
        self.tabela_itens = QTableWidget()
        self.tabela_itens.setColumnCount(5)
        self.tabela_itens.setHorizontalHeaderLabels([
            "Produto", "Quantidade", "Preço Unitário", "Subtotal", "Ações"
        ])
        
        # Configurações da tabela
        self.tabela_itens.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela_itens.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela_itens.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # Configurar cabeçalho
        header = self.tabela_itens.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Quantidade
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Preço Unitário
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Subtotal
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Ações
        
        layout_itens.addWidget(self.tabela_itens)
        
        # Resumo da venda
        self.criar_resumo_venda(layout_itens)
        
        self.stacked_widget.addWidget(widget_itens)
        
    def criar_resumo_venda(self, layout_itens):
        """Cria o resumo da venda."""
        frame_resumo = QFrame()
        frame_resumo.setObjectName("container_card")
        
        layout_resumo = QHBoxLayout(frame_resumo)
        
        self.lbl_resumo_itens = QLabel("Itens: 0")
        layout_resumo.addWidget(self.lbl_resumo_itens)
        
        self.lbl_resumo_total = QLabel("Total: R$ 0,00")
        self.lbl_resumo_total.setObjectName("texto_destaque")
        layout_resumo.addWidget(self.lbl_resumo_total)
        
        layout_resumo.addStretch()
        
        layout_itens.addWidget(frame_resumo)
        
    def criar_botoes_navegacao(self, layout_principal):
        """Cria os botões de navegação entre abas."""
        layout_navegacao = QHBoxLayout()
        layout_navegacao.addStretch()
        
        self.btn_anterior = QPushButton("← Anterior")
        self.btn_anterior.clicked.connect(self.aba_anterior)
        self.btn_anterior.setEnabled(False)
        layout_navegacao.addWidget(self.btn_anterior)
        
        self.btn_proximo = QPushButton("Próximo →")
        self.btn_proximo.clicked.connect(self.proxima_aba)
        layout_navegacao.addWidget(self.btn_proximo)
        
        layout_navegacao.addStretch()
        layout_principal.addLayout(layout_navegacao)
        
    def criar_botoes_acao(self, layout_principal):
        """Cria os botões de ação."""
        layout_acao = QHBoxLayout()
        layout_acao.addStretch()
        
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.clicked.connect(self.reject)
        layout_acao.addWidget(self.btn_cancelar)
        
        self.btn_salvar = QPushButton("Salvar Venda")
        self.btn_salvar.clicked.connect(self.salvar_venda)
        layout_acao.addWidget(self.btn_salvar)
        
        layout_principal.addLayout(layout_acao)
        
    def on_tipo_pagamento_changed(self, texto):
        """Evento disparado quando o tipo de pagamento é alterado."""
        # Mostrar/ocultar campo de dia de vencimento conforme o tipo de pagamento
        is_parcelado = texto in ["Parcelado Boleto", "Parcelado Promissória"]
        self.widget_dia_vencimento.setVisible(is_parcelado)
        
    def aba_anterior(self):
        """Navega para a aba anterior."""
        indice_atual = self.stacked_widget.currentIndex()
        if indice_atual > 0:
            self.stacked_widget.setCurrentIndex(indice_atual - 1)
            self.atualizar_botoes_navegacao()
            
    def proxima_aba(self):
        """Navega para a próxima aba."""
        indice_atual = self.stacked_widget.currentIndex()
        if indice_atual < self.stacked_widget.count() - 1:
            self.stacked_widget.setCurrentIndex(indice_atual + 1)
            self.atualizar_botoes_navegacao()
            
    def atualizar_botoes_navegacao(self):
        """Atualiza o estado dos botões de navegação."""
        indice_atual = self.stacked_widget.currentIndex()
        total_abas = self.stacked_widget.count()
        
        self.btn_anterior.setEnabled(indice_atual > 0)
        self.btn_proximo.setEnabled(indice_atual < total_abas - 1)
        self.btn_proximo.setText("Concluir" if indice_atual == total_abas - 1 else "Próximo →")
        
    def carregar_dados(self):
        """Carrega clientes e produtos do banco de dados."""
        try:
            # Carregar clientes
            self.clientes = ClienteController.listar_clientes()
            self.combo_clientes.clear()
            self.combo_clientes.addItem("Selecionar cliente...")
            for cliente in self.clientes:
                self.combo_clientes.addItem(f"{cliente.nome} ({cliente.telefone or 'Sem telefone'})", cliente.id)
                
            # Carregar produtos
            self.produtos = ProdutoController.listar_produtos()
            self.combo_produtos.clear()
            for produto in self.produtos:
                self.combo_produtos.addItem(f"{produto.nome} (R$ {produto.preco_venda:.2f})", produto.id)
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar os dados:\n{str(e)}")
            
    def preencher_campos_edicao(self):
        """Preenche os campos do formulário com os dados da venda em edição."""
        if not self.venda:
            return
            
        # Selecionar cliente
        if self.venda.cliente_id:
            index = self.combo_clientes.findData(self.venda.cliente_id)
            if index >= 0:
                self.combo_clientes.setCurrentIndex(index)
                
        # Tipo de pagamento
        index = self.combo_tipo_pagamento.findText(self.venda.tipo_pagamento)
        if index >= 0:
            self.combo_tipo_pagamento.setCurrentIndex(index)
            
        # Dia de vencimento
        if self.venda.dia_vencimento:
            self.spin_dia_vencimento.setValue(self.venda.dia_vencimento)
            
        # Data da venda
        if self.venda.data_venda:
            self.date_venda.setDate(QDate.fromString(
                self.venda.data_venda.strftime("%Y-%m-%d"), "yyyy-MM-dd"))
                
        # Itens da venda
        self.itens_venda = [
            {
                'produto_id': item.produto_id,
                'quantidade': item.quantidade,
                'preco_unitario': item.preco_unitario
            }
            for item in self.venda.itens
        ]
        self.atualizar_tabela_itens()
        
    def adicionar_item_venda(self):
        """Adiciona um item à venda."""
        # Obter produto selecionado
        produto_index = self.combo_produtos.currentIndex()
        if produto_index < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um produto.")
            return
            
        produto_id = self.combo_produtos.currentData()
        produto = next((p for p in self.produtos if p.id == produto_id), None)
        
        if not produto:
            QMessageBox.warning(self, "Aviso", "Produto não encontrado.")
            return
            
        # Verificar estoque
        quantidade = self.spin_quantidade.value()
        if quantidade > produto.quantidade:
            QMessageBox.warning(
                self, 
                "Estoque Insuficiente", 
                f"Não há estoque suficiente para '{produto.nome}'.\nDisponível: {produto.quantidade}"
            )
            return
            
        # Adicionar item
        item = {
            'produto_id': produto_id,
            'quantidade': quantidade,
            'preco_unitario': produto.preco_venda
        }
        
        self.itens_venda.append(item)
        self.atualizar_tabela_itens()
        
        # Resetar campos
        self.spin_quantidade.setValue(1)
        
    def remover_item_venda(self, index):
        """Remove um item da venda."""
        if 0 <= index < len(self.itens_venda):
            del self.itens_venda[index]
            self.atualizar_tabela_itens()
            
    def atualizar_tabela_itens(self):
        """Atualiza a tabela de itens da venda."""
        self.tabela_itens.setRowCount(len(self.itens_venda))
        
        total = 0
        for linha, item in enumerate(self.itens_venda):
            # Obter produto
            produto = next((p for p in self.produtos if p.id == item['produto_id']), None)
            
            # Produto
            nome_produto = produto.nome if produto else "Produto não encontrado"
            self.tabela_itens.setItem(linha, 0, QTableWidgetItem(nome_produto))
            
            # Quantidade
            item_quantidade = QTableWidgetItem(str(item['quantidade']))
            item_quantidade.setTextAlignment(Qt.AlignCenter)
            self.tabela_itens.setItem(linha, 1, item_quantidade)
            
            # Preço unitário
            item_preco = QTableWidgetItem(f"R$ {item['preco_unitario']:.2f}")
            item_preco.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tabela_itens.setItem(linha, 2, item_preco)
            
            # Subtotal
            subtotal = item['quantidade'] * item['preco_unitario']
            total += subtotal
            item_subtotal = QTableWidgetItem(f"R$ {subtotal:.2f}")
            item_subtotal.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tabela_itens.setItem(linha, 3, item_subtotal)
            
            # Ações
            widget_acoes = QWidget()
            layout_acoes = QHBoxLayout(widget_acoes)
            layout_acoes.setContentsMargins(5, 5, 5, 5)
            layout_acoes.setSpacing(5)
            
            btn_remover = QPushButton("Remover")
            btn_remover.setObjectName("danger")
            btn_remover.clicked.connect(lambda _, i=linha: self.remover_item_venda(i))
            layout_acoes.addWidget(btn_remover)
            
            layout_acoes.addStretch()
            self.tabela_itens.setCellWidget(linha, 4, widget_acoes)
            
        # Atualizar resumo
        self.lbl_resumo_itens.setText(f"Itens: {len(self.itens_venda)}")
        self.lbl_resumo_total.setText(f"Total: R$ {total:.2f}")
        
    def salvar_venda(self):
        """Salva a venda."""
        try:
            # Validar dados
            if not self.itens_venda:
                QMessageBox.warning(self, "Aviso", "Adicione pelo menos um item à venda.")
                return
                
            # Obter cliente
            cliente_index = self.combo_clientes.currentIndex()
            cliente_id = self.combo_clientes.currentData() if cliente_index > 0 else None
            
            # Obter tipo de pagamento
            tipo_pagamento = self.combo_tipo_pagamento.currentText()
            
            # Obter dia de vencimento (apenas para vendas parceladas)
            dia_vencimento = None
            if tipo_pagamento in ["Parcelado Boleto", "Parcelado Promissória"]:
                dia_vencimento = self.spin_dia_vencimento.value()
                
            # Registrar a venda
            venda = VendaController.criar_venda(
                cliente_id=cliente_id,
                itens=self.itens_venda,
                tipo_pagamento=tipo_pagamento,
                dia_vencimento=dia_vencimento
            )
            
            if venda:
                QMessageBox.information(
                    self, 
                    "Sucesso", 
                    f"Venda registrada com sucesso!\nID da venda: {venda.id}\nTotal: R$ {venda.valor_total:.2f}"
                )
                self.venda_registrada.emit(venda)
                self.accept()
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível registrar a venda.")
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao registrar a venda:\n{str(e)}")
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QTextEdit, QPushButton, QLabel, QMessageBox,
                             QGroupBox, QWidget, QComboBox, QDoubleSpinBox, QTableWidget,
                             QTableWidgetItem, QAbstractItemView, QHeaderView, QSpinBox,
                             QScrollArea, QFrame, QSizePolicy)
from PyQt5.QtCore import pyqtSignal, Qt
from controllers.cliente_controller import ClienteController
from controllers.produto_controller import ProdutoController
from controllers.consignacao_controller import ConsignacaoController
from models.cliente import Cliente
from models.produto import Produto

class FormularioConsignacao(QDialog):
    """Formulário para criar e gerenciar consignações."""
    
    consignacao_salva = pyqtSignal()
    
    def __init__(self, consignacao=None, parent=None):
        super().__init__(parent)
        self.consignacao = consignacao
        self.novos_itens = [] # Lista de dicts para criação
        self.produtos_cache = [] # Cache de produtos para o combo
        self.clientes_cache = [] # Cache de clientes revendedoras
        self.item_widgets = []  # Cache de widgets por item (modo edi??o)
        
        self.inicializar_ui()
        
    def inicializar_ui(self):
        self.setWindowTitle("Nova Consignação" if not self.consignacao else f"Consignação #{self.consignacao.id}")
        self.resize(900, 700)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Cabeçalho
        self.criar_cabecalho(layout)
        
        # Área de Itens
        if not self.consignacao:
            self.criar_area_adicao_itens(layout)
            self.criar_tabela_novos_itens(layout)
        else:
            self.criar_tabela_gerenciamento_itens(layout)
            self.criar_resumo_totais(layout)
            self.atualizar_tabela_gerenciamento()
            
        # Botões finais
        self.criar_botoes_acao(layout)
        
        # Carregar dados iniciais
        self.carregar_dados()
        
    def criar_cabecalho(self, layout):
        grupo = QGroupBox("Dados da Consignação")
        form = QFormLayout(grupo)
        
        # Cliente
        self.combo_cliente = QComboBox()
        if self.consignacao:
            self.combo_cliente.setEnabled(False)
        else:
            self.combo_cliente.currentIndexChanged.connect(self.atualizar_comissao_padrao)
            
        form.addRow("Revendedora:", self.combo_cliente)
        
        # Observações
        self.txt_obs = QTextEdit()
        self.txt_obs.setMaximumHeight(60)
        if self.consignacao and self.consignacao.observacoes:
            self.txt_obs.setText(self.consignacao.observacoes)
        form.addRow("Observações:", self.txt_obs)
        
        layout.addWidget(grupo)
        
    def criar_area_adicao_itens(self, layout):
        grupo = QGroupBox("Adicionar Produtos")
        hbox = QHBoxLayout(grupo)
        
        # Produto
        self.combo_produto = QComboBox()
        self.combo_produto.setMinimumWidth(300)
        self.combo_produto.currentIndexChanged.connect(self.produto_selecionado)
        hbox.addWidget(QLabel("Produto:"))
        hbox.addWidget(self.combo_produto)
        
        # Qtd
        self.spin_qtd = QSpinBox()
        self.spin_qtd.setRange(1, 9999)
        self.spin_qtd.setValue(1)
        hbox.addWidget(QLabel("Qtd:"))
        hbox.addWidget(self.spin_qtd)
        
        # Preço (apenas visualização/ajuste)
        self.spin_preco = QDoubleSpinBox()
        self.spin_preco.setRange(0, 99999)
        self.spin_preco.setPrefix("R$ ")
        hbox.addWidget(QLabel("Preço:"))
        hbox.addWidget(self.spin_preco)
        
        # Comissão
        self.spin_comissao = QDoubleSpinBox()
        self.spin_comissao.setRange(0, 100)
        self.spin_comissao.setSuffix("%")
        hbox.addWidget(QLabel("Comissão:"))
        hbox.addWidget(self.spin_comissao)
        
        # Botão Adicionar
        btn_add = QPushButton("Adicionar")
        btn_add.clicked.connect(self.adicionar_item_lista)
        hbox.addWidget(btn_add)
        
        layout.addWidget(grupo)
        
    def criar_tabela_novos_itens(self, layout):
        self.tabela_itens = QTableWidget()
        self.tabela_itens.setColumnCount(5)
        self.tabela_itens.setHorizontalHeaderLabels(["Produto", "Qtd", "Preço Unit.", "Comissão %", "Ações"])
        header = self.tabela_itens.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        layout.addWidget(self.tabela_itens)
        
    def criar_tabela_gerenciamento_itens(self, layout):
        grupo = QGroupBox("Acerto com a Revendedora")
        vbox = QVBoxLayout(grupo)

        lbl_info = QLabel("Informe vendido e devolvido. O saldo mostra o que est? com a revendedora.")
        lbl_info.setObjectName("subtitulo")
        vbox.addWidget(lbl_info)

        self.scroll_itens = QScrollArea()
        self.scroll_itens.setWidgetResizable(True)
        self.scroll_itens.setObjectName("scroll_area_clean")

        self.itens_container = QWidget()
        self.itens_container.setObjectName("container_card")
        self.itens_layout = QVBoxLayout(self.itens_container)
        self.itens_layout.setSpacing(12)
        self.itens_layout.setContentsMargins(12, 12, 12, 12)
        self.itens_layout.addStretch()

        self.scroll_itens.setWidget(self.itens_container)
        vbox.addWidget(self.scroll_itens)
        layout.addWidget(grupo)

        # Preencher itens
        # self.atualizar_tabela_gerenciamento() - Movido para inicializar_ui para garantir que labels existam

    def criar_resumo_totais(self, layout):
        grupo = QGroupBox("Resumo Financeiro")
        form = QFormLayout(grupo)
        
        self.lbl_total_vendido = QLabel("R$ 0.00")
        self.lbl_total_comissao = QLabel("R$ 0.00")
        self.lbl_total_liquido = QLabel("R$ 0.00") # A receber pela loja
        
        form.addRow("Total Vendido:", self.lbl_total_vendido)
        form.addRow("Total Comissão Revendedora:", self.lbl_total_comissao)
        form.addRow("Total a Receber (Loja):", self.lbl_total_liquido)
        
        layout.addWidget(grupo)
        
    def criar_botoes_acao(self, layout):
        hbox = QHBoxLayout()
        hbox.addStretch()
        
        btn_cancelar = QPushButton("Fechar")
        btn_cancelar.clicked.connect(self.reject)
        hbox.addWidget(btn_cancelar)
        
        if not self.consignacao:
            btn_salvar = QPushButton("Criar Consignação")
            btn_salvar.setObjectName("primary")
            btn_salvar.clicked.connect(self.salvar_nova)
            hbox.addWidget(btn_salvar)
        else:
            if self.consignacao.status != "Fechada":
                btn_salvar = QPushButton("Salvar Acerto Parcial")
                btn_salvar.clicked.connect(lambda: self.salvar_acerto(finalizar=False))
                hbox.addWidget(btn_salvar)
                
                btn_finalizar = QPushButton("Finalizar Consignação")
                btn_finalizar.setObjectName("primary")
                btn_finalizar.clicked.connect(self.confirmar_finalizacao)
                hbox.addWidget(btn_finalizar)
            else:
                layout.addWidget(QLabel("Esta consignação está FECHADA."))
                
        layout.addLayout(hbox)
        
    def carregar_dados(self):
        # Carregar Clientes Revendedoras
        clientes = ClienteController.listar_clientes()
        self.clientes_cache = [c for c in clientes if getattr(c, 'tipo', 'Avulso') == 'Revendedora']
        
        self.combo_cliente.clear()
        for c in self.clientes_cache:
            self.combo_cliente.addItem(c.nome, c.id)
            
        if self.consignacao:
            index = self.combo_cliente.findData(self.consignacao.cliente_id)
            if index >= 0:
                self.combo_cliente.setCurrentIndex(index)
        
        # Carregar Produtos (apenas se criando)
        if not self.consignacao:
            try:
                # Preciso de um método para listar produtos no ProdutoController ou usar model direto
                # Usando Produto.obter_todos() se existir ou controller
                # Vou usar Produto.obter_todos() via hack ou adicionar no controller se não tiver
                # Verifiquei ProdutoController e não vi 'listar_produtos'. Vou checar Produto model.
                # Produto.obter_todos() não estava no snippet lido, mas geralmente existe.
                # Vou assumir que existe ou usar SQL direto se falhar.
                # Melhor: ler ProdutoController novamente ou assumir que existe algo similar.
                # Vou usar uma query direta aqui se necessário, mas melhor tentar ser limpo.
                from models.produto import Produto
                # Assumindo que eu possa adicionar obter_todos no Produto se não tiver
                pass
            except:
                pass
                
            # Popula combo produtos
            # (Simplificação: listar todos)
            # Na prática deveria ser paginado ou busca, mas ok para MVP
            pass
            
            # Vou popular produtos no showEvent ou timer para não travar init
            # Mas aqui vou chamar direto
            self.popular_produtos()

    def popular_produtos(self):
        # TODO: Implementar listagem eficiente
        # Por enquanto, vou tentar usar uma query direta ou adicionar metodo no controller
        # Vou usar query direta para garantir
        from database.db_manager import gerenciador_bd
        rows = gerenciador_bd.buscar_todos("SELECT * FROM produtos WHERE quantidade > 0 ORDER BY nome")
        self.produtos_cache = [Produto.from_row(row) for row in rows]
        
        self.combo_produto.clear()
        for p in self.produtos_cache:
            self.combo_produto.addItem(f"{p.nome} (Estoque: {p.quantidade})", p.id)
            
    def produto_selecionado(self, index):
        if index >= 0 and index < len(self.produtos_cache):
            produto = self.produtos_cache[index]
            self.spin_preco.setValue(produto.preco_venda)
            self.spin_qtd.setMaximum(produto.quantidade)
            
    def atualizar_comissao_padrao(self, index):
        if index >= 0 and index < len(self.clientes_cache):
            cliente = self.clientes_cache[index]
            comissao = getattr(cliente, 'comissao_padrao', 0.0)
            self.spin_comissao.setValue(comissao)

    def adicionar_item_lista(self):
        idx = self.combo_produto.currentIndex()
        if idx < 0: return
        
        produto = self.produtos_cache[idx]
        qtd = self.spin_qtd.value()
        preco = self.spin_preco.value()
        comissao = self.spin_comissao.value()
        
        # Verificar se já está na lista
        for item in self.novos_itens:
            if item['produto_id'] == produto.id:
                QMessageBox.warning(self, "Aviso", "Produto já adicionado à lista.")
                return

        self.novos_itens.append({
            'produto_id': produto.id,
            'produto_nome': produto.nome,
            'qtd': qtd,
            'preco': preco,
            'comissao': comissao
        })
        
        self.atualizar_tabela_novos_itens()
        
    def atualizar_tabela_novos_itens(self):
        self.tabela_itens.setRowCount(len(self.novos_itens))
        for i, item in enumerate(self.novos_itens):
            self.tabela_itens.setItem(i, 0, QTableWidgetItem(item['produto_nome']))
            self.tabela_itens.setItem(i, 1, QTableWidgetItem(str(item['qtd'])))
            self.tabela_itens.setItem(i, 2, QTableWidgetItem(f"R$ {item['preco']:.2f}"))
            self.tabela_itens.setItem(i, 3, QTableWidgetItem(f"{item['comissao']}%"))
            
            btn_del = QPushButton("Remover")
            btn_del.clicked.connect(lambda checked, idx=i: self.remover_item(idx))
            self.tabela_itens.setCellWidget(i, 4, btn_del)
            
    def remover_item(self, index):
        self.novos_itens.pop(index)
        self.atualizar_tabela_novos_itens()
        
    def salvar_nova(self):
        cliente_id = self.combo_cliente.currentData()
        if not cliente_id:
            QMessageBox.warning(self, "Erro", "Selecione uma revendedora.")
            return
            
        if not self.novos_itens:
            QMessageBox.warning(self, "Erro", "Adicione pelo menos um produto.")
            return
            
        obs = self.txt_obs.toPlainText()
        
        try:
            consig = ConsignacaoController.criar_consignacao(cliente_id, self.novos_itens, obs)
            if consig:
                self.consignacao_salva.emit()
                self.accept()
            else:
                QMessageBox.critical(self, "Erro", "Erro ao criar consignação.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro: {str(e)}")

    def atualizar_tabela_gerenciamento(self):
        if not self.consignacao: return

        # Limpar cards anteriores
        while self.itens_layout.count() > 1:
            item = self.itens_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.item_widgets = []
        total_v = 0
        total_c = 0

        for i, item in enumerate(self.consignacao.itens):
            card = self.criar_card_item(item, i)
            self.itens_layout.insertWidget(i, card)

            sub = item.qtd_vendida * item.preco_unitario
            total_v += sub
            total_c += sub * (item.comissao_percentual / 100)

            self.ajustar_limites_linha(i)

        self.atualizar_labels_totais(total_v, total_c)

    def criar_card_item(self, item, idx):
        card = QFrame()
        card.setObjectName("container_card")
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        nome = item.produto_nome if hasattr(item, 'produto_nome') else f"ID {item.produto_id}"
        lbl_nome = QLabel(nome)
        lbl_nome.setObjectName("titulo_secao")
        layout.addWidget(lbl_nome)

        linha1 = QHBoxLayout()
        linha1.setSpacing(12)

        linha1.addWidget(QLabel(f"Enviado: {item.qtd_enviada}"))

        spin_vendida = QSpinBox()
        spin_vendida.setRange(0, item.qtd_enviada)
        spin_vendida.setValue(item.qtd_vendida)
        spin_vendida.valueChanged.connect(lambda val, i=idx: self.calcular_totais_linha(i))
        linha1.addWidget(QLabel("Vendido:"))
        linha1.addWidget(spin_vendida)

        spin_devolvida = QSpinBox()
        spin_devolvida.setRange(0, item.qtd_enviada)
        spin_devolvida.setValue(item.qtd_devolvida)
        spin_devolvida.valueChanged.connect(lambda val, i=idx: self.calcular_totais_linha(i))
        linha1.addWidget(QLabel("Devolvido:"))
        linha1.addWidget(spin_devolvida)

        qtd_com_revendedora = item.qtd_enviada - item.qtd_vendida - item.qtd_devolvida
        lbl_com = QLabel(str(max(0, qtd_com_revendedora)))
        lbl_com.setObjectName("texto_destaque")
        linha1.addWidget(QLabel("Com revendedora:"))
        linha1.addWidget(lbl_com)

        linha1.addStretch()
        layout.addLayout(linha1)

        linha2 = QHBoxLayout()
        linha2.setSpacing(12)
        linha2.addWidget(QLabel(f"Pre?o unit.: R$ {item.preco_unitario:.2f}"))
        linha2.addWidget(QLabel(f"Comiss?o: {item.comissao_percentual}%"))

        sub = item.qtd_vendida * item.preco_unitario
        lbl_subtotal = QLabel(f"Subtotal vendido: R$ {sub:.2f}")
        lbl_subtotal.setObjectName("texto_sucesso")
        linha2.addWidget(lbl_subtotal)

        linha2.addStretch()
        layout.addLayout(linha2)

        self.item_widgets.append({
            "spin_vendida": spin_vendida,
            "spin_devolvida": spin_devolvida,
            "lbl_com": lbl_com,
            "lbl_subtotal": lbl_subtotal
        })

        return card

    def ajustar_limites_linha(self, row_idx):
        if not self.consignacao:
            return
        item = self.consignacao.itens[row_idx]
        widgets = self.item_widgets[row_idx]
        spin_vendida = widgets["spin_vendida"]
        spin_devolvida = widgets["spin_devolvida"]
        if not spin_vendida or not spin_devolvida:
            return

        max_vendida = max(0, item.qtd_enviada - spin_devolvida.value())
        max_devolvida = max(0, item.qtd_enviada - spin_vendida.value())

        spin_vendida.blockSignals(True)
        spin_devolvida.blockSignals(True)

        spin_vendida.setMaximum(max_vendida)
        if spin_vendida.value() > max_vendida:
            spin_vendida.setValue(max_vendida)

        spin_devolvida.setMaximum(max_devolvida)
        if spin_devolvida.value() > max_devolvida:
            spin_devolvida.setValue(max_devolvida)

        spin_vendida.blockSignals(False)
        spin_devolvida.blockSignals(False)

    def calcular_totais_linha(self, row_idx):
        # Atualiza a linha e recalcula totais gerais
        self.ajustar_limites_linha(row_idx)

        widgets = self.item_widgets[row_idx]
        spin_vendida = widgets["spin_vendida"]
        spin_devolvida = widgets["spin_devolvida"]
        qtd_vendida = spin_vendida.value()
        qtd_devolvida = spin_devolvida.value()

        item = self.consignacao.itens[row_idx]
        qtd_com_revendedora = item.qtd_enviada - qtd_vendida - qtd_devolvida

        # Atualiza label com revendedora
        widgets["lbl_com"].setText(str(max(0, qtd_com_revendedora)))

        # Atualiza subtotal
        sub = qtd_vendida * item.preco_unitario
        widgets["lbl_subtotal"].setText(f"Subtotal vendido: R$ {sub:.2f}")

        # Recalcula geral
        self.recalcular_totais_gerais()

    def recalcular_totais_gerais(self):
        total_v = 0
        total_c = 0
        
        for i, item in enumerate(self.consignacao.itens):
            widgets = self.item_widgets[i]
            qtd_vendida = widgets["spin_vendida"].value()
            
            sub = qtd_vendida * item.preco_unitario
            comissao = sub * (item.comissao_percentual / 100)
            
            total_v += sub
            total_c += comissao
            
        self.atualizar_labels_totais(total_v, total_c)
        
    def atualizar_labels_totais(self, total_vendido, total_comissao):
        self.lbl_total_vendido.setText(f"R$ {total_vendido:.2f}")
        self.lbl_total_comissao.setText(f"R$ {total_comissao:.2f}")
        self.lbl_total_liquido.setText(f"R$ {total_vendido - total_comissao:.2f}")

    def confirmar_finalizacao(self):
        reply = QMessageBox.question(self, 'Confirmar Finalização',
                                     "Tem certeza que deseja finalizar esta consignação?\n\n"
                                     "Os produtos NÃO vendidos serão devolvidos ao estoque principal.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.salvar_acerto(finalizar=True)

    def salvar_acerto(self, finalizar=False):
        itens_atualizados = []
        for i, item in enumerate(self.consignacao.itens):
            widgets = self.item_widgets[i]
            qtd_vendida = widgets["spin_vendida"].value()
            qtd_devolvida = widgets["spin_devolvida"].value()
            
            itens_atualizados.append({
                'item_id': item.id,
                'qtd_vendida': qtd_vendida,
                'qtd_devolvida': qtd_devolvida
            })
            
        success = ConsignacaoController.registrar_acerto(self.consignacao.id, itens_atualizados, finalizar)
        
        if success:
            msg = "Consignação finalizada com sucesso!" if finalizar else "Acerto salvo com sucesso!"
            QMessageBox.information(self, "Sucesso", msg)
            self.consignacao_salva.emit()
            self.accept()
        else:
            QMessageBox.critical(self, "Erro", "Erro ao salvar acerto.")

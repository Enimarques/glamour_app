from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QScrollArea, QFrame, QMessageBox, QLabel, QLineEdit,
                             QComboBox, QSpinBox, QGridLayout, QGroupBox,
                             QDialog, QListWidget, QTextEdit, QSizePolicy, QFileDialog)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QFont, QColor, QPainter, QPainterPath
from PyQt5.QtPrintSupport import QPrinter
from models.produto import Produto
from models.cliente import Cliente
from models.carrinho import CarrinhoCompras, ItemCarrinho
from controllers.produto_controller import ProdutoController
from controllers.cliente_controller import ClienteController
from controllers.venda_controller import VendaController
from ui.formulario_produto import FormularioProduto
import os

class ProdutoCard(QFrame):
    """Componente customizado para exibir um produto com design moderno."""
    
    adicionado_ao_carrinho = pyqtSignal(object)
    selecionado_alterado = pyqtSignal(object, bool)
    
    def __init__(self, produto, parent=None):
        super().__init__(parent)
        self.produto = produto
        self.setObjectName("card_produto_moderno")
        self.setFixedSize(300, 420)
        self.selecionado = False
        self.inicializar_ui()
        
    def inicializar_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        self.lbl_imagem = QLabel()
        self.lbl_imagem.setFixedSize(260, 190)
        self.lbl_imagem.setObjectName("placeholder_imagem_moderna")
        self.lbl_imagem.setAlignment(Qt.AlignCenter)
        if getattr(self.produto, "caminho_imagem", None) and os.path.exists(self.produto.caminho_imagem):
            pix = QPixmap(self.produto.caminho_imagem).scaled(260, 190, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.lbl_imagem.setPixmap(pix)
        else:
            self.lbl_imagem.setText("💎")
            self.lbl_imagem.setStyleSheet("background-color: #F8F9FA; border-radius: 12px; font-size: 60px; color: #BDC3C7;")
        layout.addWidget(self.lbl_imagem)
        
        # Informações
        lbl_categoria = QLabel(self.produto.categoria.upper() if self.produto.categoria else "GERAL")
        lbl_categoria.setStyleSheet("color: #27AE60; font-weight: bold; font-size: 10px; letter-spacing: 1px;")
        layout.addWidget(lbl_categoria)
        
        lbl_nome = QLabel(self.produto.nome)
        lbl_nome.setObjectName("produto_nome_moderno")
        lbl_nome.setWordWrap(True)
        lbl_nome.setStyleSheet("font-size: 16px; font-weight: bold; color: #34495E;")
        layout.addWidget(lbl_nome)
        
        lbl_ref = QLabel(f"REF: {self.produto.id:04d}")
        lbl_ref.setStyleSheet("color: #95A5A6; font-size: 11px;")
        layout.addWidget(lbl_ref)
        
        layout.addStretch()
        
        h_layout = QHBoxLayout()
        lbl_preco = QLabel(f"R$ {self.produto.preco_venda:,.2f}")
        lbl_preco.setStyleSheet("font-size: 20px; font-weight: 800; color: #2C3E50;")
        h_layout.addWidget(lbl_preco)

        btn_edit = QPushButton("✏")
        btn_edit.setFixedSize(40, 40)
        btn_edit.setObjectName("btn_action_edit")
        btn_edit.clicked.connect(self.editar_produto)
        h_layout.addWidget(btn_edit)
        
        layout.addLayout(h_layout)
        
        btn_add_full = QPushButton("Adicionar à sacola")
        btn_add_full.setObjectName("primary")
        btn_add_full.setMinimumHeight(40)
        btn_add_full.clicked.connect(lambda: self.adicionado_ao_carrinho.emit(self.produto))
        layout.addWidget(btn_add_full)
    
    def toggle_selecao(self):
        self.selecionado = not self.selecionado
        self.setStyleSheet("border: 2px solid #2ECC71;" if self.selecionado else "")
        self.selecionado_alterado.emit(self.produto, self.selecionado)
    
    def editar_produto(self):
        try:
            formulario = FormularioProduto(produto=self.produto, parent=self)
            if formulario.exec_():
                self.parent().parent().parent().carregar_produtos()
        except Exception:
            pass

class ListaProdutosMarketplace(QWidget):
    """Aba de Produtos padronizada com o novo Design System."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.produtos = []
        self.carrinho = CarrinhoCompras()
        self.selecionados = []
        self.inicializar_ui()
        self.carregar_produtos()
        
    def inicializar_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(30)
        
        # Header
        header = QHBoxLayout()
        title_box = QVBoxLayout()
        lbl_title = QLabel("Gestão de Produtos")
        lbl_title.setObjectName("page_title")
        lbl_breadcrumb = QLabel("Início › Produtos › Marketplace")
        lbl_breadcrumb.setObjectName("breadcrumb")
        title_box.addWidget(lbl_title)
        title_box.addWidget(lbl_breadcrumb)
        header.addLayout(title_box)
        header.addStretch()
        
        self.btn_novo = QPushButton("+ Novo Produto")
        self.btn_novo.setObjectName("btn_adicionar")
        self.btn_novo.setMinimumHeight(45)
        self.btn_novo.clicked.connect(self.adicionar_produto)
        header.addWidget(self.btn_novo)
        layout_principal.addLayout(header)
        
        # Toolbar (Filtros)
        frame_toolbar = QFrame()
        frame_toolbar.setObjectName("toolbar_header")
        layout_toolbar = QHBoxLayout(frame_toolbar)
        
        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("🔍 Pesquisar por nome ou referência...")
        self.campo_busca.setMinimumWidth(400)
        self.campo_busca.textChanged.connect(self.filtrar_produtos)
        layout_toolbar.addWidget(self.campo_busca)
        
        self.combo_cat = QComboBox()
        self.combo_cat.addItems(["Todas as Categorias", "Anéis", "Brincos", "Colares", "Relógios"])
        self.combo_cat.setMinimumWidth(200)
        layout_toolbar.addWidget(self.combo_cat)
        
        layout_toolbar.addStretch()
        layout_principal.addWidget(frame_toolbar)
        
        frame_actions = QFrame()
        frame_actions.setObjectName("toolbar_header")
        layout_actions = QHBoxLayout(frame_actions)
        layout_actions.setContentsMargins(10, 10, 10, 10)
        layout_actions.setSpacing(15)
        
        self.lbl_selecionados = QLabel("Selecionados: 0")
        layout_actions.addWidget(self.lbl_selecionados)
        
        btn_sel_all = QPushButton("Selecionar tudo")
        btn_sel_all.setObjectName("secondary")
        btn_sel_all.clicked.connect(self.selecionar_todos)
        layout_actions.addWidget(btn_sel_all)
        
        btn_clear = QPushButton("Limpar seleção")
        btn_clear.setObjectName("secondary")
        btn_clear.clicked.connect(self.limpar_selecao)
        layout_actions.addWidget(btn_clear)
        
        btn_pdf = QPushButton("Exportar PDF")
        btn_pdf.setObjectName("btn_mais_acoes")
        btn_pdf.clicked.connect(self.exportar_pdf)
        layout_actions.addWidget(btn_pdf)
        
        layout_actions.addStretch()
        
        btn_vender = QPushButton("Mandar pra vender")
        btn_vender.setObjectName("primary")
        btn_vender.clicked.connect(self.mandar_para_vender)
        layout_actions.addWidget(btn_vender)
        
        btn_consignar = QPushButton("Consignar")
        btn_consignar.setObjectName("primary")
        btn_consignar.clicked.connect(self.consignar_selecionados)
        layout_actions.addWidget(btn_consignar)
        
        layout_principal.addWidget(frame_actions)
        
        # Área de Scroll dos Cards
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName("scroll_area_clean")
        self.scroll.setStyleSheet("background: transparent; border: none;")
        
        self.widget_cards = QWidget()
        self.layout_grid = QGridLayout(self.widget_cards)
        self.layout_grid.setSpacing(20)
        self.layout_grid.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        self.scroll.setWidget(self.widget_cards)
        layout_principal.addWidget(self.scroll)
        
        barra = QFrame()
        barra.setObjectName("toolbar_header")
        hbar = QHBoxLayout(barra)
        hbar.setContentsMargins(10, 10, 10, 10)
        hbar.setSpacing(15)
        self.lbl_carrinho = QLabel("Sacola: 0 itens • Total: R$ 0,00")
        hbar.addWidget(self.lbl_carrinho)
        hbar.addStretch()
        btn_final_venda = QPushButton("Finalizar venda")
        btn_final_venda.setObjectName("primary")
        btn_final_venda.clicked.connect(self.finalizar_venda_carrinho)
        hbar.addWidget(btn_final_venda)
        btn_final_consig = QPushButton("Consignar seleção")
        btn_final_consig.setObjectName("primary")
        btn_final_consig.clicked.connect(self.finalizar_consignacao_carrinho)
        hbar.addWidget(btn_final_consig)
        btn_limpar = QPushButton("Limpar sacola")
        btn_limpar.setObjectName("secondary")
        btn_limpar.clicked.connect(self.limpar_carrinho)
        hbar.addWidget(btn_limpar)
        layout_principal.addWidget(barra)
        
    def carregar_produtos(self):
        """Busca produtos no banco e preenche a grid."""
        try:
            self.produtos = ProdutoController.listar_produtos()
            self.atualizar_grid(self.produtos)
        except Exception as e:
            print(f"Erro ao carregar produtos: {e}")
            
    def atualizar_grid(self, lista_produtos):
        """Limpa e preenche a grid de cards."""
        # Limpar grid atual
        for i in reversed(range(self.layout_grid.count())): 
            self.layout_grid.itemAt(i).widget().setParent(None)
            
        colunas = 4
        for index, prod in enumerate(lista_produtos):
            card = ProdutoCard(prod)
            card.adicionado_ao_carrinho.connect(self.adicionar_item_carrinho)
            card.selecionado_alterado.connect(self.atualizar_selecao)
            self.layout_grid.addWidget(card, index // colunas, index % colunas)
            
    def filtrar_produtos(self):
        termo = self.campo_busca.text().lower()
        cat = self.combo_cat.currentText()
        filtrados = [p for p in self.produtos if termo in p.nome.lower()]
        if cat and cat != "Todas as Categorias":
            filtrados = [p for p in filtrados if (p.categoria or "").lower() == cat.lower()]
        self.atualizar_grid(filtrados)

    def adicionar_produto(self):
        formulario = FormularioProduto(parent=self)
        if formulario.exec_():
            self.carregar_produtos()
    
    def atualizar_selecao(self, produto, selecionado):
        if selecionado:
            if produto not in self.selecionados:
                self.selecionados.append(produto)
        else:
            self.selecionados = [p for p in self.selecionados if p.id != produto.id]
        self.lbl_selecionados.setText(f"Selecionados: {len(self.selecionados)}")
    
    def selecionar_todos(self):
        for i in range(self.layout_grid.count()):
            w = self.layout_grid.itemAt(i).widget()
            if isinstance(w, ProdutoCard) and not w.selecionado:
                w.toggle_selecao()
    
    def limpar_selecao(self):
        for i in range(self.layout_grid.count()):
            w = self.layout_grid.itemAt(i).widget()
            if isinstance(w, ProdutoCard) and w.selecionado:
                w.toggle_selecao()
        self.selecionados = []
        self.lbl_selecionados.setText("Selecionados: 0")
    
    def adicionar_item_carrinho(self, produto):
        self.carrinho.adicionar_item(produto, 1)
        self.atualizar_barra_carrinho()
    
    def atualizar_barra_carrinho(self):
        self.lbl_carrinho.setText(f"Sacola: {self.carrinho.quantidade_itens} itens • Total: R$ {self.carrinho.total:.2f}")
    
    def limpar_carrinho(self):
        self.carrinho.limpar()
        self.atualizar_barra_carrinho()
    
    def exportar_pdf(self):
        try:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(os.path.join(os.getcwd(), "mostruario_produtos.pdf"))
            painter = QPainter(printer)
            margem = 50
            x = margem
            y = margem
            largura = printer.pageRect().width() - 2*margem
            linha_altura = 120
            itens = self.selecionados if self.selecionados else self.produtos
            for p in itens:
                painter.drawText(x, y, f"{p.nome}  •  R$ {p.preco_venda:.2f}  •  REF {p.id:04d}")
                if getattr(p, "caminho_imagem", None) and os.path.exists(p.caminho_imagem):
                    pix = QPixmap(p.caminho_imagem).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    painter.drawPixmap(x + largura - 120, y - 20, pix)
                y += linha_altura
                if y + linha_altura > printer.pageRect().height() - margem:
                    printer.newPage()
                    y = margem
            painter.end()
            QMessageBox.information(self, "Exportar", "PDF gerado: mostruario_produtos.pdf")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao exportar PDF:\n{str(e)}")
    
    def mandar_para_vender(self):
        try:
            from ui.formulario_venda import FormularioVenda
            formulario = FormularioVenda(parent=self)
            formulario.carregar_dados()
            itens = [{'produto_id': item.produto.id, 'quantidade': item.quantidade, 'preco_unitario': item.produto.preco_venda} for item in self.carrinho.obter_itens()]
            formulario.itens_venda = itens
            formulario.atualizar_tabela_itens()
            if formulario.exec_():
                self.limpar_carrinho()
                self.carregar_produtos()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao abrir venda:\n{str(e)}")
    
    def consignar_selecionados(self):
        try:
            from ui.formulario_consignacao import FormularioConsignacao
            formulario = FormularioConsignacao(parent=self)
            formulario.carregar_dados()
            itens = [{'produto_id': item.produto.id, 'produto_nome': item.produto.nome, 'qtd': item.quantidade, 'preco': item.produto.preco_venda, 'comissao': 0.0} for item in self.carrinho.obter_itens()]
            formulario.novos_itens = itens
            formulario.atualizar_tabela_novos_itens()
            if formulario.exec_():
                self.limpar_carrinho()
                self.carregar_produtos()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao abrir consignação:\n{str(e)}")
    
    def finalizar_venda_carrinho(self):
        self.mandar_para_vender()
    
    def finalizar_consignacao_carrinho(self):
        self.consignar_selecionados()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    # Mock para teste
    class MockProd:
        def __init__(self, i):
            self.id = i
            self.nome = f"Produto Exemplo {i}"
            self.categoria = "Semijoias"
            self.preco_venda = 150.0 * i
    
    w = ListaProdutosMarketplace()
    w.produtos = [MockProd(i) for i in range(1, 10)]
    w.atualizar_grid(w.produtos)
    w.show()
    sys.exit(app.exec_())

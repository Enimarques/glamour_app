import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, qApp, 
                             QToolBar, QStatusBar, QDockWidget, QTextEdit, 
                             QTabWidget, QVBoxLayout, QWidget, QLabel, 
                             QPushButton, QHBoxLayout, QFrame, QSizePolicy,
                             QListWidget, QStackedWidget, QListWidgetItem)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QPixmap, QColor, QPalette
from ui.lista_produtos_marketplace import ListaProdutosMarketplace
from ui.lista_clientes import ListaClientes
from ui.lista_consignacoes import ListaConsignacoes
from ui.lista_vendas import ListaVendas
from ui.lista_relatorios import ListaRelatorios
from ui.lista_configuracoes import ListaConfiguracoes
from ui.aba_cobrancas import AbaCobrancas

class JanelaPrincipal(QMainWindow):
    """Janela principal da aplicação com novo design integrado."""
    
    def __init__(self):
        super().__init__()
        self.inicializar_ui()
        
    def inicializar_ui(self):
        """Inicializa a interface do usuário."""
        self.setWindowTitle("JOIA SYSTEM - Gestão de Semijoias")
        self.setGeometry(100, 100, 1280, 850)
        
        # Widget Central com Layout Horizontal (Sidebar + Conteúdo)
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.layout_principal = QHBoxLayout(self.widget_central)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)
        
        # Criar componentes da UI
        self.criar_sidebar()
        self.criar_stacked_widget()
        self.criar_barra_status()
        
    def criar_sidebar(self):
        """Cria a sidebar de navegação integrada."""
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        layout_sidebar = QVBoxLayout(self.sidebar)
        layout_sidebar.setContentsMargins(0, 0, 0, 0)
        layout_sidebar.setSpacing(0)
        
        # Logo/Title Container
        self.container_logo = QFrame()
        layout_logo = QVBoxLayout(self.container_logo)
        layout_logo.setContentsMargins(15, 10, 15, 10)
        lbl_logo = QLabel("💎 JOIA SYSTEM")
        lbl_logo.setObjectName("logo_label")
        lbl_logo.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout_logo.addWidget(lbl_logo)
        layout_sidebar.addWidget(self.container_logo)
        
        # Lista de navegação com Ícones
        self.nav_list = QListWidget()
        self.nav_list.setObjectName("nav_list")
        self.nav_list.setIconSize(QSize(18, 18))
        
        # Itens do Menu
        menus = [
            ("Dashboard", "🏠"),
            ("Produtos", "📦"),
            ("Clientes", "👥"),
            ("Vendas", "🛒"),
            ("Consignações", "📄"),
            ("Cobranças", "💳"),
            ("Relatórios", "📊"),
            ("Configurações", "⚙")
        ]
        
        for nome, icone in menus:
            item = QListWidgetItem(f"{icone}  {nome}")
            self.nav_list.addItem(item)
            
        self.nav_list.currentRowChanged.connect(self.mudar_aba)
        layout_sidebar.addWidget(self.nav_list)
        
        # Espaçador e Rodapé do Menu
        layout_sidebar.addStretch()
        
        lbl_versao = QLabel("v2.0.0 Stable")
        lbl_versao.setStyleSheet("color: #A0AEC0; padding: 15px; font-size: 10px; font-weight: 600;")
        layout_sidebar.addWidget(lbl_versao)
        
        self.layout_principal.addWidget(self.sidebar)
        
    def criar_stacked_widget(self):
        """Cria o widget empilhado para as diferentes abas."""
        self.stacked_widget = QStackedWidget()
        
        # Criar widgets para cada aba
        self.criar_widget_dashboard()
        self.criar_widget_produtos()
        self.criar_widget_clientes()
        self.criar_widget_vendas()
        self.criar_widget_consignacoes()
        self.criar_widget_cobrancas()
        self.criar_widget_relatorios()
        self.criar_widget_configuracoes()
        
        self.layout_principal.addWidget(self.stacked_widget)
        self.nav_list.setCurrentRow(0) # Iniciar no Dashboard
        
    def criar_widget_dashboard(self):
        """Cria o widget do dashboard moderno."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        
        # Header
        header = QHBoxLayout()
        title_box = QVBoxLayout()
        lbl_title = QLabel("Painel de Controle")
        lbl_title.setObjectName("page_title")
        lbl_breadcrumb = QLabel("Início › Dashboard")
        lbl_breadcrumb.setObjectName("breadcrumb")
        title_box.addWidget(lbl_title)
        title_box.addWidget(lbl_breadcrumb)
        header.addLayout(title_box)
        header.addStretch()
        
        btn_novo = QPushButton("+ Novo Registro")
        btn_novo.setObjectName("btn_adicionar")
        btn_novo.setMinimumHeight(45)
        header.addWidget(btn_novo)
        layout.addLayout(header)
        
        # Cards de Resumo
        layout_cards = QHBoxLayout()
        layout_cards.setSpacing(20)
        
        cards = [
            ("Vendas Hoje", "R$ 0,00", "📈", "summary_card_total"),
            ("Clientes", "0", "👥", "summary_card_recebidos"),
            ("Pendentes", "0", "⏳", "summary_card_vencem_hoje"),
            ("Estoque", "0", "📦", "summary_card_a_vencer")
        ]
        
        for t, v, i, obj in cards:
            card = self.criar_card_dashboard(t, v, i, obj)
            layout_cards.addWidget(card)
            
        layout.addLayout(layout_cards)
        
        # Área Central (Empty State por enquanto)
        container = QFrame()
        container.setObjectName("container_card")
        layout_cont = QVBoxLayout(container)
        layout_cont.setContentsMargins(100, 100, 100, 100)
        
        lbl_welcome = QLabel("Bem-vindo ao Novo JOIA SYSTEM")
        lbl_welcome.setStyleSheet("font-size: 22px; font-weight: bold; color: #34495E;")
        lbl_welcome.setAlignment(Qt.AlignCenter)
        
        lbl_desc = QLabel("Seu ambiente de trabalho foi atualizado para uma experiência mais clean e produtiva.\nUse o menu lateral para navegar entre as funções.")
        lbl_desc.setStyleSheet("color: #7F8C8D; font-size: 15px; margin-top: 10px;")
        lbl_desc.setAlignment(Qt.AlignCenter)
        
        layout_cont.addWidget(lbl_welcome)
        layout_cont.addWidget(lbl_desc)
        layout.addWidget(container)
        
        layout.addStretch()
        self.stacked_widget.addWidget(widget)

    def criar_card_dashboard(self, titulo, valor, icone, object_name):
        """Cria um card de resumo para o dashboard."""
        frame = QFrame()
        frame.setObjectName(object_name)
        frame.setMinimumHeight(130)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(25, 25, 25, 25)
        
        h_layout = QHBoxLayout()
        lbl_t = QLabel(titulo)
        lbl_t.setObjectName("summary_card_title")
        lbl_i = QLabel(icone)
        lbl_i.setObjectName("summary_card_icon")
        h_layout.addWidget(lbl_t)
        h_layout.addWidget(lbl_i)
        layout.addLayout(h_layout)
        
        lbl_v = QLabel(valor)
        lbl_v.setObjectName("summary_card_value")
        layout.addWidget(lbl_v)
        
        return frame
        
    def criar_widget_produtos(self):
        """Cria o widget de produtos."""
        self.lista_produtos = ListaProdutosMarketplace()
        self.stacked_widget.addWidget(self.lista_produtos)
        
    def criar_widget_clientes(self):
        """Cria o widget de clientes."""
        self.lista_clientes = ListaClientes()
        self.stacked_widget.addWidget(self.lista_clientes)
        
    def criar_widget_vendas(self):
        """Cria o widget de vendas."""
        self.lista_vendas = ListaVendas()
        self.stacked_widget.addWidget(self.lista_vendas)
        
    def criar_widget_consignacoes(self):
        """Cria o widget de consignações."""
        self.lista_consignacoes = ListaConsignacoes()
        self.stacked_widget.addWidget(self.lista_consignacoes)
        
    def criar_widget_cobrancas(self):
        """Cria o widget de cobranças."""
        self.aba_cobrancas = AbaCobrancas()
        self.stacked_widget.addWidget(self.aba_cobrancas)
        
    def criar_widget_relatorios(self):
        """Cria o widget de relatórios."""
        self.lista_relatorios = ListaRelatorios()
        self.stacked_widget.addWidget(self.lista_relatorios)
        
    def criar_widget_configuracoes(self):
        """Cria o widget de configurações."""
        self.lista_configuracoes = ListaConfiguracoes()
        self.stacked_widget.addWidget(self.lista_configuracoes)
        
    def mudar_aba(self, index):
        """Muda a aba exibida conforme a seleção na sidebar."""
        self.stacked_widget.setCurrentIndex(index)
        
    def criar_barra_status(self):
        """Cria a barra de status."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("background: white; border-top: 1px solid #E1E8ED; color: #7F8C8D;")
        self.status_bar.showMessage("Sistema pronto para uso")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Supondo que o estilo global já é aplicado no main.py, mas para teste local:
    from ui.styles import GLOBAL_STYLESHEET
    app.setStyleSheet(GLOBAL_STYLESHEET)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec_())

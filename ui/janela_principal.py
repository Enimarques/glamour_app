import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, qApp, 
                             QToolBar, QStatusBar, QDockWidget, QTextEdit, 
                             QTabWidget, QVBoxLayout, QWidget, QLabel, 
                             QPushButton, QHBoxLayout, QFrame, QSizePolicy,
                             QListWidget, QStackedWidget)
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
    """Janela principal da aplicação de gerenciamento de loja de semijoias."""
    
    def __init__(self):
        super().__init__()
        self.inicializar_ui()
        
    def inicializar_ui(self):
        """Inicializa a interface do usuário."""
        self.setWindowTitle("Sistema de Gerenciamento de Loja de Semijoias")
        self.setGeometry(100, 100, 1200, 800)
        
        # Criar componentes da UI
        self.criar_sidebar()
        self.criar_stacked_widget()
        self.criar_barra_status()
        
    def criar_sidebar(self):
        """Cria a sidebar de navegação."""
        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(280)
        # Style is now handled globally in styles.py
        
        # Layout da sidebar
        layout_sidebar = QVBoxLayout(self.sidebar)
        layout_sidebar.setContentsMargins(0, 30, 0, 30)
        layout_sidebar.setSpacing(10)
        
        # Logo/Title
        lbl_logo = QLabel("JOIA SYSTEM")
        lbl_logo.setObjectName("logo_label")
        lbl_logo.setAlignment(Qt.AlignCenter)
        layout_sidebar.addWidget(lbl_logo)
        
        # Lista de navegação
        self.lista_navegacao = QListWidget()
        self.lista_navegacao.setObjectName("nav_list")
        self.lista_navegacao.addItems([
            "Dashboard",
            "Produtos", 
            "Clientes",
            "Vendas",
            "Consignações",
            "Cobranças",
            "Relatórios",
            "Configurações"
        ])
        # Style is now handled globally in styles.py
        
        self.lista_navegacao.currentRowChanged.connect(self.mudar_aba)
        layout_sidebar.addWidget(self.lista_navegacao)
        
        # Adicionar sidebar ao layout
        self.setCentralWidget(QWidget())
        layout_principal = QHBoxLayout(self.centralWidget())
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)
        layout_principal.addWidget(self.sidebar)
        
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
        
        # Adicionar ao layout principal
        self.centralWidget().layout().addWidget(self.stacked_widget)
        
    def criar_widget_dashboard(self):
        """Cria o widget do dashboard."""
        widget_dashboard = QWidget()
        layout_dashboard = QVBoxLayout(widget_dashboard)
        layout_dashboard.setContentsMargins(30, 30, 30, 30)
        layout_dashboard.setSpacing(20)
        
        # Cabeçalho da página
        layout_header = QHBoxLayout()
        
        # Layout para ícone + título
        layout_titulo = QHBoxLayout()
        lbl_icone = QLabel("🏠")
        lbl_icone.setObjectName("breadcrumb_icon")
        layout_titulo.addWidget(lbl_icone)
        
        lbl_titulo = QLabel("Dashboard")
        lbl_titulo.setObjectName("page_title")
        layout_titulo.addWidget(lbl_titulo)
        layout_titulo.addStretch()
        layout_header.addLayout(layout_titulo)
        
        # Breadcrumb
        layout_breadcrumb = QHBoxLayout()
        layout_breadcrumb.addStretch()
        lbl_home = QLabel("🏠 Início")
        lbl_home.setObjectName("breadcrumb")
        layout_breadcrumb.addWidget(lbl_home)
        
        lbl_sep1 = QLabel(" › ")
        lbl_sep1.setObjectName("breadcrumb")
        layout_breadcrumb.addWidget(lbl_sep1)
        
        lbl_atual = QLabel("Dashboard")
        lbl_atual.setObjectName("breadcrumb")
        layout_breadcrumb.addWidget(lbl_atual)
        layout_header.addLayout(layout_breadcrumb)
        
        layout_dashboard.addLayout(layout_header)
        
        # Cards de resumo
        layout_cards = QHBoxLayout()
        layout_cards.setSpacing(15)
        
        card_vendas = self.criar_card_dashboard("Vendas do Mês", "R$ 0,00", "💰", "summary_card_total")
        card_clientes = self.criar_card_dashboard("Novos Clientes", "0", "👥", "summary_card_recebidos")
        card_estoque = self.criar_card_dashboard("Produtos em Estoque", "0", "📦", "summary_card_a_vencer")
        card_alertas = self.criar_card_dashboard("Alertas", "0", "⚠", "summary_card_vencem_hoje")
        
        layout_cards.addWidget(card_vendas)
        layout_cards.addWidget(card_clientes)
        layout_cards.addWidget(card_estoque)
        layout_cards.addWidget(card_alertas)
        
        layout_dashboard.addLayout(layout_cards)
        
        # Área de Conteúdo Central
        container_msg = QFrame()
        container_msg.setObjectName("container_card")
        layout_msg = QVBoxLayout(container_msg)
        layout_msg.setContentsMargins(50, 50, 50, 50)
        
        lbl_mensagem = QLabel("Bem-vindo ao JOIA SYSTEM\n\nO seu painel de controle central está sendo preparado.\nAqui você verá gráficos de vendas, metas e indicadores de desempenho.")
        lbl_mensagem.setStyleSheet("color: #6B6B6B; font-size: 16px; line-height: 1.5;")
        lbl_mensagem.setAlignment(Qt.AlignCenter)
        
        layout_msg.addWidget(lbl_mensagem)
        layout_dashboard.addWidget(container_msg)
        
        layout_dashboard.addStretch()
        
        self.stacked_widget.addWidget(widget_dashboard)

    def criar_card_dashboard(self, titulo, valor, icone, object_name):
        """Cria um card de resumo para o dashboard."""
        frame = QFrame()
        frame.setObjectName(object_name)
        frame.setMinimumHeight(120)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        layout_header = QHBoxLayout()
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setObjectName("summary_card_title")
        layout_header.addWidget(lbl_titulo)
        
        lbl_icone = QLabel(icone)
        lbl_icone.setObjectName("summary_card_icon")
        layout_header.addWidget(lbl_icone)
        layout.addLayout(layout_header)
        
        lbl_valor = QLabel(valor)
        lbl_valor.setObjectName("summary_card_value")
        lbl_valor.setStyleSheet("font-size: 24px;")
        layout.addWidget(lbl_valor)
        
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
        
    def mudar_aba(self, item):
        """Muda a aba exibida conforme a seleção na sidebar."""
        self.stacked_widget.setCurrentIndex(item)
        
    def criar_barra_status(self):
        """Cria a barra de status."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Sistema pronto para uso")
        
    def mostrar_lista_produtos(self):
        """Mostra a aba de lista de produtos."""
        self.lista_navegacao.setCurrentRow(1)  # Produtos
        self.stacked_widget.setCurrentIndex(1)  # Widget de produtos

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec_())
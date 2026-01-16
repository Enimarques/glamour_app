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
        
        # Aplicar estilo moderno
        self.aplicar_estilo()
        
    def criar_sidebar(self):
        """Cria a sidebar de navegação."""
        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet("""
            QFrame {
                background-color: #2C3E50;
                border-right: 1px solid #34495E;
            }
        """)
        
        # Layout da sidebar
        layout_sidebar = QVBoxLayout(self.sidebar)
        layout_sidebar.setContentsMargins(0, 20, 0, 20)
        layout_sidebar.setSpacing(0)
        
        # Logo/Title
        lbl_logo = QLabel("JOIA SYSTEM")
        lbl_logo.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 20px;
            border-bottom: 1px solid #34495E;
        """)
        lbl_logo.setAlignment(Qt.AlignCenter)
        layout_sidebar.addWidget(lbl_logo)
        
        # Lista de navegação
        self.lista_navegacao = QListWidget()
        self.lista_navegacao.addItems([
            "Dashboard",
            "Produtos", 
            "Clientes",
            "Vendas",
            "Cobranças",
            "Relatórios",
            "Configurações"
        ])
        self.lista_navegacao.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                color: #ECF0F1;
                font-size: 16px;
                padding: 10px 0;
            }
            
            QListWidget::item {
                padding: 15px 30px;
                border-bottom: 1px solid #34495E;
            }
            
            QListWidget::item:selected {
                background-color: #3498DB;
                color: white;
                border-left: 4px solid #1ABC9C;
            }
            
            QListWidget::item:hover {
                background-color: #34495E;
            }
        """)
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
        
        # Título
        lbl_titulo = QLabel("Dashboard")
        lbl_titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 20px;
        """)
        layout_dashboard.addWidget(lbl_titulo)
        
        # Mensagem de funcionalidade em desenvolvimento
        lbl_mensagem = QLabel("Dashboard em desenvolvimento.\nAqui serão exibidas métricas e indicadores importantes.")
        lbl_mensagem.setStyleSheet("""
            font-size: 16px;
            color: #666666;
            background-color: #F8F9FA;
            padding: 40px;
            border-radius: 8px;
            border: 1px dashed #E0E0E0;
            text-align: center;
        """)
        lbl_mensagem.setAlignment(Qt.AlignCenter)
        layout_dashboard.addWidget(lbl_mensagem)
        
        layout_dashboard.addStretch()
        
        self.stacked_widget.addWidget(widget_dashboard)
        
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
        
    def aplicar_estilo(self):
        """Aplica o estilo moderno à aplicação."""
        estilo = """
        QMainWindow {
            background-color: #F8F9FA;
        }
        
        QStatusBar {
            background-color: #2C3E50;
            color: white;
            border-top: 1px solid #34495E;
        }
        """
        self.setStyleSheet(estilo)
        
    def mostrar_lista_produtos(self):
        """Mostra a aba de lista de produtos."""
        self.lista_navegacao.setCurrentRow(1)  # Produtos
        self.stacked_widget.setCurrentIndex(1)  # Widget de produtos

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec_())
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QTextEdit,
                             QPushButton, QLabel, QMessageBox,
                             QGroupBox, QWidget)
from PyQt5.QtCore import pyqtSignal, Qt
from controllers.cliente_controller import ClienteController
from models.cliente import Cliente

class FormularioCliente(QDialog):
    """Formulário para cadastro e edição de clientes."""
    
    # Sinal emitido quando um cliente é salvo
    cliente_salvo = pyqtSignal(Cliente)
    
    def __init__(self, cliente=None, parent=None):
        """
        Inicializa o formulário.
        
        Args:
            cliente (Cliente, opcional): Cliente a ser editado. Se None, cria um novo.
            parent (QWidget, opcional): Widget pai.
        """
        super().__init__(parent)
        self.cliente = cliente
        self.inicializar_ui()
        
    def inicializar_ui(self):
        """Inicializa a interface do usuário."""
        if self.cliente:
            self.setWindowTitle(f"Editar Cliente: {self.cliente.nome}")
        else:
            self.setWindowTitle("Novo Cliente")
            
        self.setModal(True)
        self.resize(500, 400)
        
        # Aplicar estilo
        self.aplicar_estilo()
        
        # Layout principal
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)
        
        # Título
        lbl_titulo = QLabel("Cadastro de Cliente" if not self.cliente else "Edição de Cliente")
        lbl_titulo.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 10px;
        """)
        layout_principal.addWidget(lbl_titulo)
        
        # Grupo de informações básicas
        self.criar_grupo_informacoes(layout_principal)
        
        # Grupo de observações
        self.criar_grupo_observacoes(layout_principal)
        
        # Botões
        self.criar_botoes(layout_principal)
        
        # Preenche os campos se estiver editando um cliente
        if self.cliente:
            self.preencher_campos()
            
    def aplicar_estilo(self):
        """Aplica o estilo moderno ao formulário."""
        estilo = """
        QDialog {
            background-color: #FFFFFF;
        }
        
        QLabel {
            color: #333333;
            font-family: "Segoe UI", "Roboto", Arial, sans-serif;
        }
        
        QLineEdit, QTextEdit {
            padding: 10px 12px;
            border: 1px solid #E0E0E0;
            border-radius: 6px;
            background-color: white;
            selection-background-color: #4A90E2;
            font-size: 14px;
        }
        
        QLineEdit:focus, QTextEdit:focus {
            border: 1px solid #4A90E2;
            outline: none;
        }
        
        QGroupBox {
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            margin-top: 15px;
            padding-top: 20px;
            font-weight: bold;
            color: #4A90E2;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 15px;
            padding: 0 10px;
            background-color: white;
        }
        
        QPushButton {
            background-color: #4A90E2;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 500;
            min-width: 100px;
        }
        
        QPushButton:hover {
            background-color: #357ABD;
        }
        
        QPushButton:pressed {
            background-color: #2E6DA4;
        }
        
        QPushButton#secondary {
            background-color: transparent;
            color: #4A90E2;
            border: 1px solid #4A90E2;
        }
        
        QPushButton#secondary:hover {
            background-color: #F0F5FF;
        }
        """
        self.setStyleSheet(estilo)
        
    def criar_grupo_informacoes(self, layout_principal):
        """Cria o grupo de informações básicas."""
        grupo_info = QGroupBox("Informações Básicas")
        layout_grupo = QFormLayout(grupo_info)
        layout_grupo.setContentsMargins(20, 20, 20, 20)
        layout_grupo.setSpacing(15)
        
        # Campo nome
        self.campo_nome = QLineEdit()
        self.campo_nome.setPlaceholderText("Digite o nome completo do cliente")
        layout_grupo.addRow(QLabel("Nome:"), self.campo_nome)
        
        # Campo telefone
        self.campo_telefone = QLineEdit()
        self.campo_telefone.setPlaceholderText("(00) 00000-0000")
        layout_grupo.addRow(QLabel("Telefone:"), self.campo_telefone)
        
        layout_principal.addWidget(grupo_info)
        
    def criar_grupo_observacoes(self, layout_principal):
        """Cria o grupo de observações."""
        grupo_obs = QGroupBox("Observações")
        layout_grupo = QVBoxLayout(grupo_obs)
        layout_grupo.setContentsMargins(20, 20, 20, 20)
        layout_grupo.setSpacing(15)
        
        # Campo observações
        self.campo_observacoes = QTextEdit()
        self.campo_observacoes.setPlaceholderText("Adicione observações sobre o cliente (preferências, histórico, etc.)")
        self.campo_observacoes.setMaximumHeight(100)
        layout_grupo.addWidget(self.campo_observacoes)
        
        layout_principal.addWidget(grupo_obs)
        
    def criar_botoes(self, layout_principal):
        """Cria os botões do formulário."""
        layout_botoes = QHBoxLayout()
        layout_botoes.setSpacing(15)
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("secondary")
        btn_cancelar.clicked.connect(self.reject)
        layout_botoes.addWidget(btn_cancelar)
        
        btn_salvar = QPushButton("Salvar")
        btn_salvar.clicked.connect(self.salvar)
        btn_salvar.setDefault(True)
        layout_botoes.addWidget(btn_salvar)
        
        layout_principal.addLayout(layout_botoes)
        
    def preencher_campos(self):
        """Preenche os campos do formulário com os dados do cliente."""
        self.campo_nome.setText(self.cliente.nome)
        if self.cliente.telefone:
            self.campo_telefone.setText(self.cliente.telefone)
        if self.cliente.observacoes:
            self.campo_observacoes.setPlainText(self.cliente.observacoes)
            
    def salvar(self):
        """Salva o cliente."""
        nome = self.campo_nome.text().strip()
        telefone = self.campo_telefone.text().strip()
        observacoes = self.campo_observacoes.toPlainText().strip()
        
        # Validação básica
        if not nome:
            QMessageBox.warning(self, "Aviso", "Por favor, informe o nome do cliente.")
            self.campo_nome.setFocus()
            return
            
        try:
            if self.cliente:
                # Atualiza cliente existente
                self.cliente = ClienteController.atualizar_cliente(
                    self.cliente.id,
                    nome=nome,
                    telefone=telefone if telefone else None,
                    observacoes=observacoes if observacoes else None
                )
            else:
                # Cria novo cliente
                self.cliente = ClienteController.criar_cliente(
                    nome=nome,
                    telefone=telefone if telefone else None,
                    observacoes=observacoes if observacoes else None
                )
                
            if self.cliente:
                self.cliente_salvo.emit(self.cliente)
                self.accept()
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível salvar o cliente.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao salvar o cliente:\n{str(e)}")
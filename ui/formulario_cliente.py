from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QTextEdit,
                             QPushButton, QLabel, QMessageBox,
                             QGroupBox, QWidget, QComboBox, QDoubleSpinBox)
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
        
        # Layout principal
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)
        
        # Título
        lbl_titulo = QLabel("Cadastro de Cliente" if not self.cliente else "Edição de Cliente")
        lbl_titulo.setObjectName("titulo_pagina")
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

        # Campo Tipo de Cliente
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Avulso", "Revendedora"])
        self.combo_tipo.currentTextChanged.connect(self.alternar_campo_comissao)
        layout_grupo.addRow(QLabel("Tipo de Cliente:"), self.combo_tipo)

        # Campo Comissão Padrão
        self.campo_comissao = QDoubleSpinBox()
        self.campo_comissao.setRange(0, 100)
        self.campo_comissao.setSuffix("%")
        self.campo_comissao.setDecimals(1)
        self.campo_comissao.setEnabled(False)  # Desabilitado por padrão (Avulso)
        layout_grupo.addRow(QLabel("Comissão Padrão:"), self.campo_comissao)
        
        layout_principal.addWidget(grupo_info)

    def alternar_campo_comissao(self, texto):
        """Habilita ou desabilita o campo de comissão baseado no tipo de cliente."""
        is_revendedora = texto == "Revendedora"
        self.campo_comissao.setEnabled(is_revendedora)
        if not is_revendedora:
            self.campo_comissao.setValue(0.0)
        
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
        btn_salvar.setObjectName("primary")
        btn_salvar.clicked.connect(self.salvar)
        btn_salvar.setDefault(True)
        layout_botoes.addWidget(btn_salvar)
        
        layout_principal.addLayout(layout_botoes)
        
    def preencher_campos(self):
        """Preenche os campos do formulário com os dados do cliente."""
        self.campo_nome.setText(self.cliente.nome)
        if self.cliente.telefone:
            self.campo_telefone.setText(self.cliente.telefone)
        
        # Preencher tipo e comissão
        tipo = getattr(self.cliente, 'tipo', 'Avulso')
        index_tipo = self.combo_tipo.findText(tipo)
        if index_tipo >= 0:
            self.combo_tipo.setCurrentIndex(index_tipo)
            
        comissao = getattr(self.cliente, 'comissao_padrao', 0.0)
        self.campo_comissao.setValue(comissao)
        
        if self.cliente.observacoes:
            self.campo_observacoes.setPlainText(self.cliente.observacoes)
            
    def salvar(self):
        """Salva o cliente."""
        nome = self.campo_nome.text().strip()
        telefone = self.campo_telefone.text().strip()
        tipo = self.combo_tipo.currentText()
        comissao = self.campo_comissao.value()
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
                    tipo=tipo,
                    comissao_padrao=comissao,
                    observacoes=observacoes if observacoes else None
                )
            else:
                # Cria novo cliente
                self.cliente = ClienteController.criar_cliente(
                    nome=nome,
                    telefone=telefone if telefone else None,
                    tipo=tipo,
                    comissao_padrao=comissao,
                    observacoes=observacoes if observacoes else None
                )
                
            if self.cliente:
                self.cliente_salvo.emit(self.cliente)
                self.accept()
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível salvar o cliente.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao salvar o cliente:\n{str(e)}")
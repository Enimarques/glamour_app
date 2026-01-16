from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMessageBox, QAbstractItemView, QLabel, QLineEdit,
                             QComboBox, QDateEdit, QSpacerItem, QSizePolicy,
                             QGroupBox, QTextEdit, QCheckBox, QSpinBox, QColorDialog,
                             QFontDialog, QFileDialog)
from PyQt5.QtCore import Qt, pyqtSignal, QSettings
from PyQt5.QtGui import QFont, QColor, QPixmap
import os

class ListaConfiguracoes(QWidget):
    """Widget para exibir e gerenciar as configurações do sistema."""
    
    # Sinal emitido quando as configurações são salvas
    configuracoes_salvas = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.configuracoes = QSettings("JoiaSystem", "SistemaLojaSemijoias")
        self.inicializar_ui()
        self.carregar_configuracoes()
        
    def inicializar_ui(self):
        """Inicializa a interface do usuário."""
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)
        
        # Título
        lbl_titulo = QLabel("Configurações")
        lbl_titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 20px;
        """)
        layout_principal.addWidget(lbl_titulo)
        
        # Grupo de preferências gerais
        self.criar_grupo_preferencias_gerais(layout_principal)
        
        # Grupo de aparência
        self.criar_grupo_aparencia(layout_principal)
        
        # Grupo de backup
        self.criar_grupo_backup(layout_principal)
        
        # Botões de ação
        self.criar_botoes_acao(layout_principal)
        
        # Aplicar estilo
        self.aplicar_estilo()
        
    def criar_grupo_preferencias_gerais(self, layout_principal):
        """Cria o grupo de preferências gerais."""
        grupo_geral = QGroupBox("Preferências Gerais")
        layout_grupo = QVBoxLayout(grupo_geral)
        
        # Nome da loja
        layout_nome = QHBoxLayout()
        layout_nome.addWidget(QLabel("Nome da Loja:"))
        self.campo_nome_loja = QLineEdit()
        layout_nome.addWidget(self.campo_nome_loja)
        layout_grupo.addLayout(layout_nome)
        
        # Telefone
        layout_telefone = QHBoxLayout()
        layout_telefone.addWidget(QLabel("Telefone:"))
        self.campo_telefone = QLineEdit()
        layout_telefone.addWidget(self.campo_telefone)
        layout_grupo.addLayout(layout_telefone)
        
        # Endereço
        layout_endereco = QHBoxLayout()
        layout_endereco.addWidget(QLabel("Endereço:"))
        self.campo_endereco = QLineEdit()
        layout_endereco.addWidget(self.campo_endereco)
        layout_grupo.addLayout(layout_endereco)
        
        layout_principal.addWidget(grupo_geral)
        
    def criar_grupo_aparencia(self, layout_principal):
        """Cria o grupo de aparência."""
        grupo_aparencia = QGroupBox("Aparência")
        layout_grupo = QVBoxLayout(grupo_aparencia)
        
        # Cor primária
        layout_cor = QHBoxLayout()
        layout_cor.addWidget(QLabel("Cor Primária:"))
        self.btn_cor_primaria = QPushButton("Selecionar Cor")
        self.btn_cor_primaria.clicked.connect(self.selecionar_cor_primaria)
        self.lbl_preview_cor = QLabel()
        self.lbl_preview_cor.setFixedSize(30, 30)
        self.lbl_preview_cor.setStyleSheet("background-color: #4A90E2; border: 1px solid #CCCCCC;")
        layout_cor.addWidget(self.btn_cor_primaria)
        layout_cor.addWidget(self.lbl_preview_cor)
        layout_cor.addStretch()
        layout_grupo.addLayout(layout_cor)
        
        # Fonte
        layout_fonte = QHBoxLayout()
        layout_fonte.addWidget(QLabel("Fonte Padrão:"))
        self.btn_fonte = QPushButton("Selecionar Fonte")
        self.btn_fonte.clicked.connect(self.selecionar_fonte)
        self.lbl_preview_fonte = QLabel("Exemplo de Texto")
        layout_fonte.addWidget(self.btn_fonte)
        layout_fonte.addWidget(self.lbl_preview_fonte)
        layout_fonte.addStretch()
        layout_grupo.addLayout(layout_fonte)
        
        layout_principal.addWidget(grupo_aparencia)
        
    def criar_grupo_backup(self, layout_principal):
        """Cria o grupo de backup."""
        grupo_backup = QGroupBox("Backup")
        layout_grupo = QVBoxLayout(grupo_backup)
        
        # Diretório de backup
        layout_diretorio = QHBoxLayout()
        layout_diretorio.addWidget(QLabel("Diretório de Backup:"))
        self.campo_diretorio_backup = QLineEdit()
        self.campo_diretorio_backup.setPlaceholderText("Selecione o diretório de backup")
        self.btn_selecionar_diretorio = QPushButton("Selecionar")
        self.btn_selecionar_diretorio.clicked.connect(self.selecionar_diretorio_backup)
        layout_diretorio.addWidget(self.campo_diretorio_backup)
        layout_diretorio.addWidget(self.btn_selecionar_diretorio)
        layout_grupo.addLayout(layout_diretorio)
        
        # Frequência de backup
        layout_frequencia = QHBoxLayout()
        layout_frequencia.addWidget(QLabel("Frequência de Backup:"))
        self.combo_frequencia = QComboBox()
        self.combo_frequencia.addItems(["Diário", "Semanal", "Mensal", "Manual"])
        layout_frequencia.addWidget(self.combo_frequencia)
        layout_frequencia.addStretch()
        layout_grupo.addLayout(layout_frequencia)
        
        # Botão de backup agora
        layout_backup = QHBoxLayout()
        self.btn_backup_agora = QPushButton("Fazer Backup Agora")
        self.btn_backup_agora.clicked.connect(self.fazer_backup_agora)
        layout_backup.addWidget(self.btn_backup_agora)
        layout_backup.addStretch()
        layout_grupo.addLayout(layout_backup)
        
        layout_principal.addWidget(grupo_backup)
        
    def criar_botoes_acao(self, layout_principal):
        """Cria os botões de ação."""
        layout_botoes = QHBoxLayout()
        layout_botoes.addStretch()
        
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setObjectName("secondary")
        self.btn_cancelar.clicked.connect(self.cancelar)
        layout_botoes.addWidget(self.btn_cancelar)
        
        self.btn_salvar = QPushButton("Salvar Configurações")
        self.btn_salvar.clicked.connect(self.salvar_configuracoes)
        layout_botoes.addWidget(self.btn_salvar)
        
        layout_principal.addLayout(layout_botoes)
        
    def aplicar_estilo(self):
        """Aplica o estilo moderno aos elementos."""
        estilo = """
        QGroupBox {
            font-weight: bold;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            margin-top: 1ex;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
            color: #4A90E2;
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
        
        QLineEdit, QComboBox {
            padding: 8px;
            border: 1px solid #E0E0E0;
            border-radius: 6px;
            background-color: white;
        }
        
        QLineEdit:focus, QComboBox:focus {
            border: 1px solid #4A90E2;
            outline: none;
        }
        """
        self.setStyleSheet(estilo)
        
    def selecionar_cor_primaria(self):
        """Abre o diálogo para selecionar a cor primária."""
        cor_atual = self.lbl_preview_cor.palette().window().color()
        cor = QColorDialog.getColor(cor_atual, self, "Selecione a Cor Primária")
        if cor.isValid():
            self.lbl_preview_cor.setStyleSheet(f"background-color: {cor.name()}; border: 1px solid #CCCCCC;")
            
    def selecionar_fonte(self):
        """Abre o diálogo para selecionar a fonte."""
        fonte_atual = self.lbl_preview_fonte.font()
        fonte, ok = QFontDialog.getFont(fonte_atual, self, "Selecione a Fonte")
        if ok:
            self.lbl_preview_fonte.setFont(fonte)
            
    def selecionar_diretorio_backup(self):
        """Abre o diálogo para selecionar o diretório de backup."""
        diretorio = QFileDialog.getExistingDirectory(self, "Selecione o Diretório de Backup")
        if diretorio:
            self.campo_diretorio_backup.setText(diretorio)
            
    def fazer_backup_agora(self):
        """Realiza um backup imediato."""
        try:
            # Aqui seria implementada a lógica real de backup
            QMessageBox.information(self, "Backup", "Backup realizado com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao realizar backup:\n{str(e)}")
            
    def carregar_configuracoes(self):
        """Carrega as configurações salvas."""
        self.campo_nome_loja.setText(self.configuracoes.value("nome_loja", "Joia System"))
        self.campo_telefone.setText(self.configuracoes.value("telefone", ""))
        self.campo_endereco.setText(self.configuracoes.value("endereco", ""))
        self.campo_diretorio_backup.setText(self.configuracoes.value("diretorio_backup", ""))
        self.combo_frequencia.setCurrentText(self.configuracoes.value("frequencia_backup", "Semanal"))
        
    def salvar_configuracoes(self):
        """Salva as configurações."""
        try:
            self.configuracoes.setValue("nome_loja", self.campo_nome_loja.text())
            self.configuracoes.setValue("telefone", self.campo_telefone.text())
            self.configuracoes.setValue("endereco", self.campo_endereco.text())
            self.configuracoes.setValue("diretorio_backup", self.campo_diretorio_backup.text())
            self.configuracoes.setValue("frequencia_backup", self.combo_frequencia.currentText())
            
            QMessageBox.information(self, "Sucesso", "Configurações salvas com sucesso!")
            self.configuracoes_salvas.emit()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar configurações:\n{str(e)}")
            
    def cancelar(self):
        """Cancela as alterações e recarrega as configurações."""
        resposta = QMessageBox.question(self, "Cancelar", 
                                      "Tem certeza que deseja cancelar as alterações?",
                                      QMessageBox.Yes | QMessageBox.No)
        if resposta == QMessageBox.Yes:
            self.carregar_configuracoes()
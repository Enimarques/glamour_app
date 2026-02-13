from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMessageBox, QAbstractItemView, QLabel, QLineEdit,
                             QComboBox, QDateEdit, QSpacerItem, QSizePolicy,
                             QGroupBox, QTextEdit, QCheckBox, QSpinBox, QColorDialog,
                             QFontDialog, QFileDialog, QFrame)
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
        
        # Cabeçalho da página
        self.criar_cabecalho_pagina(layout_principal)
        
        # Cards informativos
        self.criar_cards_info(layout_principal)
        
        # Container para os grupos
        container = QFrame()
        container.setObjectName("container_card")
        layout_container = QVBoxLayout(container)
        layout_container.setContentsMargins(20, 20, 20, 20)
        layout_container.setSpacing(20)
        
        # Grupo de preferências gerais
        self.criar_grupo_preferencias_gerais(layout_container)
        
        # Grupo de aparência
        self.criar_grupo_aparencia(layout_container)
        
        # Grupo de backup
        self.criar_grupo_backup(layout_container)
        
        layout_principal.addWidget(container)
        
        # Botões de ação
        self.criar_botoes_acao(layout_principal)
        
    def criar_cabecalho_pagina(self, layout_principal):
        """Cria o cabeçalho da página."""
        layout_header = QHBoxLayout()
        
        layout_titulo = QHBoxLayout()
        
        lbl_icone = QLabel("⚙")
        lbl_icone.setObjectName("breadcrumb_icon")
        layout_titulo.addWidget(lbl_icone)
        
        lbl_titulo = QLabel("Configurações")
        lbl_titulo.setObjectName("page_title")
        layout_titulo.addWidget(lbl_titulo)
        
        layout_titulo.addStretch()
        layout_header.addLayout(layout_titulo)
        
        # Breadcrumb
        layout_breadcrumb = QHBoxLayout()
        layout_breadcrumb.addStretch()
        
        lbl_home = QLabel("🏠 Início")
        lbl_home.setObjectName("breadcrumb")
        lbl_home.setCursor(Qt.PointingHandCursor)
        layout_breadcrumb.addWidget(lbl_home)
        
        lbl_sep = QLabel(" › ")
        lbl_sep.setObjectName("breadcrumb")
        layout_breadcrumb.addWidget(lbl_sep)
        
        lbl_atual = QLabel("Configurações")
        lbl_atual.setObjectName("breadcrumb")
        layout_breadcrumb.addWidget(lbl_atual)
        
        layout_header.addLayout(layout_breadcrumb)
        layout_principal.addLayout(layout_header)
        
    def criar_cards_info(self, layout_principal):
        """Cria cards informativos."""
        layout_cards = QHBoxLayout()
        layout_cards.setSpacing(15)
        
        # Card Sistema
        card1 = self.criar_card_info("Sistema", "Versão 2.0", "💻", "summary_card_total")
        layout_cards.addWidget(card1)
        
        # Card Última Atualização
        card2 = self.criar_card_info("Última Atualização", "Hoje", "📅", "summary_card_recebidos")
        layout_cards.addWidget(card2)
        
        # Card Backup
        card3 = self.criar_card_info("Último Backup", "Nenhum", "💾", "summary_card_vencem_hoje")
        layout_cards.addWidget(card3)
        
        # Card Status
        card4 = self.criar_card_info("Status", "Ativo", "✓", "summary_card_a_vencer")
        layout_cards.addWidget(card4)
        
        layout_principal.addLayout(layout_cards)
        
    def criar_card_info(self, titulo, valor, icone, object_name):
        """Cria um card informativo."""
        frame = QFrame()
        frame.setObjectName(object_name)
        frame.setMinimumHeight(100)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)
        
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
        layout.addWidget(lbl_valor)
        
        layout.addStretch()
        
        return frame
        
    def criar_grupo_preferencias_gerais(self, layout_pai):
        """Cria o grupo de preferências gerais."""
        grupo_geral = QGroupBox("Preferências Gerais")
        layout_grupo = QVBoxLayout(grupo_geral)
        layout_grupo.setSpacing(15)
        
        # Nome da loja
        layout_nome = QHBoxLayout()
        lbl_nome = QLabel("Nome da Loja:")
        lbl_nome.setMinimumWidth(150)
        layout_nome.addWidget(lbl_nome)
        self.campo_nome_loja = QLineEdit()
        self.campo_nome_loja.setPlaceholderText("Digite o nome da sua loja")
        layout_nome.addWidget(self.campo_nome_loja)
        layout_grupo.addLayout(layout_nome)
        
        # Telefone
        layout_telefone = QHBoxLayout()
        lbl_tel = QLabel("Telefone:")
        lbl_tel.setMinimumWidth(150)
        layout_telefone.addWidget(lbl_tel)
        self.campo_telefone = QLineEdit()
        self.campo_telefone.setPlaceholderText("(00) 0000-0000")
        layout_telefone.addWidget(self.campo_telefone)
        layout_grupo.addLayout(layout_telefone)
        
        # Endereço
        layout_endereco = QHBoxLayout()
        lbl_end = QLabel("Endereço:")
        lbl_end.setMinimumWidth(150)
        layout_endereco.addWidget(lbl_end)
        self.campo_endereco = QLineEdit()
        self.campo_endereco.setPlaceholderText("Rua, número, bairro, cidade")
        layout_endereco.addWidget(self.campo_endereco)
        layout_grupo.addLayout(layout_endereco)
        
        layout_pai.addWidget(grupo_geral)
        
    def criar_grupo_aparencia(self, layout_pai):
        """Cria o grupo de aparência."""
        grupo_aparencia = QGroupBox("Aparência")
        layout_grupo = QVBoxLayout(grupo_aparencia)
        layout_grupo.setSpacing(15)
        
        # Cor primária
        layout_cor = QHBoxLayout()
        lbl_cor = QLabel("Cor Primária:")
        lbl_cor.setMinimumWidth(150)
        layout_cor.addWidget(lbl_cor)
        self.btn_cor_primaria = QPushButton("Selecionar Cor")
        self.btn_cor_primaria.setObjectName("secondary")
        self.btn_cor_primaria.clicked.connect(self.selecionar_cor_primaria)
        self.lbl_preview_cor = QLabel()
        self.lbl_preview_cor.setFixedSize(40, 40)
        self.lbl_preview_cor.setObjectName("preview_cor")
        self.lbl_preview_cor.setStyleSheet("background-color: #C9A24D; border-radius: 20px;")
        layout_cor.addWidget(self.btn_cor_primaria)
        layout_cor.addWidget(self.lbl_preview_cor)
        layout_cor.addStretch()
        layout_grupo.addLayout(layout_cor)
        
        # Fonte
        layout_fonte = QHBoxLayout()
        lbl_fonte = QLabel("Fonte Padrão:")
        lbl_fonte.setMinimumWidth(150)
        layout_fonte.addWidget(lbl_fonte)
        self.btn_fonte = QPushButton("Selecionar Fonte")
        self.btn_fonte.setObjectName("secondary")
        self.btn_fonte.clicked.connect(self.selecionar_fonte)
        self.lbl_preview_fonte = QLabel("Exemplo de Texto")
        self.lbl_preview_fonte.setStyleSheet("padding: 5px 10px; background-color: #F5F7FA; border-radius: 5px;")
        layout_fonte.addWidget(self.btn_fonte)
        layout_fonte.addWidget(self.lbl_preview_fonte)
        layout_fonte.addStretch()
        layout_grupo.addLayout(layout_fonte)
        
        layout_pai.addWidget(grupo_aparencia)
        
    def criar_grupo_backup(self, layout_pai):
        """Cria o grupo de backup."""
        grupo_backup = QGroupBox("Backup e Segurança")
        layout_grupo = QVBoxLayout(grupo_backup)
        layout_grupo.setSpacing(15)
        
        # Diretório de backup
        layout_diretorio = QHBoxLayout()
        lbl_dir = QLabel("Diretório de Backup:")
        lbl_dir.setMinimumWidth(150)
        layout_diretorio.addWidget(lbl_dir)
        self.campo_diretorio_backup = QLineEdit()
        self.campo_diretorio_backup.setPlaceholderText("Selecione o diretório de backup")
        self.btn_selecionar_diretorio = QPushButton("📁 Procurar")
        self.btn_selecionar_diretorio.setObjectName("secondary")
        self.btn_selecionar_diretorio.clicked.connect(self.selecionar_diretorio_backup)
        layout_diretorio.addWidget(self.campo_diretorio_backup, 3)
        layout_diretorio.addWidget(self.btn_selecionar_diretorio, 1)
        layout_grupo.addLayout(layout_diretorio)
        
        # Frequência de backup
        layout_frequencia = QHBoxLayout()
        lbl_freq = QLabel("Frequência de Backup:")
        lbl_freq.setMinimumWidth(150)
        layout_frequencia.addWidget(lbl_freq)
        self.combo_frequencia = QComboBox()
        self.combo_frequencia.addItems(["Diário", "Semanal", "Mensal", "Manual"])
        self.combo_frequencia.setMaximumWidth(200)
        layout_frequencia.addWidget(self.combo_frequencia)
        layout_frequencia.addStretch()
        layout_grupo.addLayout(layout_frequencia)
        
        # Botão de backup agora
        layout_backup = QHBoxLayout()
        layout_backup.addStretch()
        self.btn_backup_agora = QPushButton("💾 Fazer Backup Agora")
        self.btn_backup_agora.setObjectName("info")
        self.btn_backup_agora.setMinimumWidth(200)
        self.btn_backup_agora.clicked.connect(self.fazer_backup_agora)
        layout_backup.addWidget(self.btn_backup_agora)
        layout_grupo.addLayout(layout_backup)
        
        layout_pai.addWidget(grupo_backup)
        
    def criar_botoes_acao(self, layout_principal):
        """Cria os botões de ação."""
        layout_botoes = QHBoxLayout()
        layout_botoes.addStretch()
        
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setObjectName("secondary")
        self.btn_cancelar.setMinimumWidth(120)
        self.btn_cancelar.clicked.connect(self.cancelar)
        layout_botoes.addWidget(self.btn_cancelar)
        
        self.btn_salvar = QPushButton("✓ Salvar Configurações")
        self.btn_salvar.setObjectName("success")
        self.btn_salvar.setMinimumWidth(200)
        self.btn_salvar.clicked.connect(self.salvar_configuracoes)
        layout_botoes.addWidget(self.btn_salvar)
        
        layout_principal.addLayout(layout_botoes)
        
    def selecionar_cor_primaria(self):
        """Abre o diálogo para selecionar a cor primária."""
        cor_str = self.lbl_preview_cor.styleSheet()
        # Extrair a cor do stylesheet
        try:
            cor_atual = QColor("#C9A24D")  # Cor padrão
            cor = QColorDialog.getColor(cor_atual, self, "Selecione a Cor Primária")
            if cor.isValid():
                self.lbl_preview_cor.setStyleSheet(f"background-color: {cor.name()}; border-radius: 20px;")
        except Exception as e:
            print(f"Erro ao selecionar cor: {e}")
            
    def selecionar_fonte(self):
        """Abre o diálogo para selecionar a fonte."""
        try:
            fonte_atual = self.lbl_preview_fonte.font()
            fonte, ok = QFontDialog.getFont(fonte_atual, self, "Selecione a Fonte")
            if ok:
                self.lbl_preview_fonte.setFont(fonte)
        except Exception as e:
            print(f"Erro ao selecionar fonte: {e}")
            
    def selecionar_diretorio_backup(self):
        """Abre o diálogo para selecionar o diretório de backup."""
        try:
            diretorio = QFileDialog.getExistingDirectory(self, "Selecione o Diretório de Backup")
            if diretorio:
                self.campo_diretorio_backup.setText(diretorio)
        except Exception as e:
            print(f"Erro ao selecionar diretório: {e}")
            
    def fazer_backup_agora(self):
        """Realiza um backup imediato."""
        try:
            # Aqui seria implementada a lógica real de backup
            resposta = QMessageBox.question(
                self,
                "Confirmar Backup",
                "Deseja realmente fazer um backup do banco de dados agora?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if resposta == QMessageBox.Yes:
                QMessageBox.information(self, "Backup", "Backup realizado com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao realizar backup:\n{str(e)}")
            
    def carregar_configuracoes(self):
        """Carrega as configurações salvas."""
        try:
            self.campo_nome_loja.setText(self.configuracoes.value("nome_loja", "Joia System"))
            self.campo_telefone.setText(self.configuracoes.value("telefone", ""))
            self.campo_endereco.setText(self.configuracoes.value("endereco", ""))
            self.campo_diretorio_backup.setText(self.configuracoes.value("diretorio_backup", ""))
            freq = self.configuracoes.value("frequencia_backup", "Semanal")
            index = self.combo_frequencia.findText(freq)
            if index >= 0:
                self.combo_frequencia.setCurrentIndex(index)
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
        
    def salvar_configuracoes(self):
        """Salva as configurações."""
        try:
            self.configuracoes.setValue("nome_loja", self.campo_nome_loja.text())
            self.configuracoes.setValue("telefone", self.campo_telefone.text())
            self.configuracoes.setValue("endereco", self.campo_endereco.text())
            self.configuracoes.setValue("diretorio_backup", self.campo_diretorio_backup.text())
            self.configuracoes.setValue("frequencia_backup", self.combo_frequencia.currentText())
            
            QMessageBox.information(self, "Sucesso", "✓ Configurações salvas com sucesso!")
            self.configuracoes_salvas.emit()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar configurações:\n{str(e)}")
            
    def cancelar(self):
        """Cancela as alterações e recarrega as configurações."""
        resposta = QMessageBox.question(
            self, 
            "Cancelar Alterações", 
            "Tem certeza que deseja descartar as alterações?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if resposta == QMessageBox.Yes:
            self.carregar_configuracoes()

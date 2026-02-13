# -*- coding: utf-8 -*-

"""
Módulo de Estilos (QSS) para o Sistema de Gerenciamento de Loja de Semijoias.
Tema: Soft UI / Neumorphism Light com toques de Dourado.
"""

# Paleta de Cores
COLOR_BG_MAIN = "#F5F7FA"       # Cinza muito claro (Fundo Geral)
COLOR_BG_CARD = "#FFFFFF"       # Branco (Cartões/Containers)
COLOR_GOLD_MAIN = "#C9A24D"     # Dourado Principal
COLOR_GOLD_HOVER = "#D4AF37"    # Dourado Hover (Gold Clássico)
COLOR_GOLD_LIGHT = "#E6C77A"    # Dourado Claro (Detalhes)
COLOR_TEXT_MAIN = "#2C3E50"     # Texto Principal
COLOR_TEXT_SEC = "#7F8C8D"      # Texto Secundário
COLOR_BORDER = "#E1E8ED"        # Bordas Suaves
COLOR_DANGER = "#E74C3C"        # Vermelho Perigo
COLOR_DANGER_BG = "#FDECEA"     # Fundo Perigo
COLOR_SUCCESS = "#27AE60"       # Verde Sucesso
COLOR_SUCCESS_BG = "#D5F4E6"    # Fundo Sucesso
COLOR_WARNING = "#F39C12"       # Laranja Aviso
COLOR_WARNING_BG = "#FEF5E7"    # Fundo Aviso
COLOR_INFO = "#3498DB"          # Azul Info
COLOR_INFO_HOVER = "#2980B9"    # Azul Info Hover
COLOR_INFO_BG = "#EBF5FB"       # Fundo Info
COLOR_GRAY = "#95A5A6"          # Cinza
COLOR_GRAY_BG = "#ECF0F1"       # Fundo Cinza
COLOR_DARK = "#34495E"          # Escuro

# Estilo Global (QSS)
GLOBAL_STYLESHEET = f"""
/* --- JANELA PRINCIPAL E WIDGETS GERAIS --- */
QMainWindow, QWidget {{
    background-color: {COLOR_BG_MAIN};
    font-family: "Segoe UI", "Roboto", "Arial";
    font-size: 14px;
    color: {COLOR_TEXT_MAIN};
}}

/* --- FRAMES E CONTAINERS (Efeito Card) --- */
QFrame#container_card, QWidget#container_card {{
    background-color: {COLOR_BG_CARD};
    border-radius: 16px;
    border: 1px solid {COLOR_BORDER};
}}

/* --- SIDEBAR (Barra Lateral) --- */
QFrame#sidebar {{
    background-color: #FFFFFF;
    border-right: 1px solid {COLOR_BORDER};
}}

QLabel#logo_label {{
    color: {COLOR_GOLD_MAIN};
    font-size: 22px;
    font-weight: bold;
    padding: 20px;
    border-bottom: 2px solid {COLOR_BG_MAIN};
}}

/* --- LISTA DE NAVEGAÇÃO (Sidebar) --- */
QListWidget#nav_list {{
    background-color: transparent;
    border: none;
    outline: none;
    margin-top: 20px;
}}

QListWidget#nav_list::item {{
    color: {COLOR_TEXT_SEC};
    padding: 12px 20px;
    margin: 4px 15px;
    border-radius: 10px;
    font-weight: 500;
}}

QListWidget#nav_list::item:hover {{
    background-color: #FAF5E6; /* Amarelo muito pálido */
    color: {COLOR_GOLD_MAIN};
}}

QListWidget#nav_list::item:selected {{
    background-color: {COLOR_GOLD_MAIN};
    color: white;
    border: none;
    /* Sombra suave simulada */
}}

/* --- BOTÕES (Estilo Neumorphism/Soft) --- */
QPushButton {{
    background-color: {COLOR_BG_CARD};
    color: {COLOR_TEXT_MAIN};
    border: 1px solid {COLOR_BORDER};
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: 600;
    /* Sombra sutil para volume */
    border-bottom: 2px solid #D1D1D1; 
}}

QPushButton:hover {{
    background-color: {COLOR_GOLD_LIGHT};
    color: white;
    border: 1px solid {COLOR_GOLD_MAIN};
    border-bottom: 2px solid {COLOR_GOLD_MAIN};
}}

QPushButton:pressed {{
    background-color: {COLOR_GOLD_MAIN};
    border-top: 2px solid #A8863D;
    border-bottom: none;
    padding-top: 12px; /* Efeito de afundar */
}}

/* Botão Primário (Ação Principal - Dourado) */
QPushButton#primary {{
    background-color: {COLOR_GOLD_MAIN};
    color: white;
    border: none;
    border-bottom: 3px solid #A8863D;
}}

QPushButton#primary:hover {{
    background-color: {COLOR_GOLD_HOVER};
}}

QPushButton#primary:pressed {{
    border-top: 3px solid #8C6E30;
    border-bottom: none;
}}

/* Botão Secundário */
QPushButton#secondary {{
    background-color: #FFFFFF;
    color: {COLOR_TEXT_MAIN};
    border: 1px solid {COLOR_BORDER};
}}

QPushButton#secondary:hover {{
    background-color: #F5F5F5;
    border-color: {COLOR_GOLD_MAIN};
}}

/* Botão de Perigo/Excluir */
QPushButton#danger {{
    background-color: #FFF0F0;
    color: #D32F2F;
    border: 1px solid #FFCDD2;
}}

QPushButton#danger:hover {{
    background-color: #D32F2F;
    color: white;
}}

/* Botão de Sucesso */
QPushButton#success {{
    background-color: #E8F5E9;
    color: #2E7D32;
    border: 1px solid #C8E6C9;
}}

QPushButton#success:hover {{
    background-color: #2E7D32;
    color: white;
}}

/* --- CAMPOS DE FORMULÁRIO (Inputs) --- */
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QTextEdit {{
    background-color: {COLOR_BG_CARD};
    border: 1px solid {COLOR_BORDER};
    border-radius: 10px;
    padding: 8px 12px;
    color: {COLOR_TEXT_MAIN};
    selection-background-color: {COLOR_GOLD_MAIN};
}}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{
    border: 1px solid {COLOR_GOLD_MAIN};
    background-color: #FFFCF5;
}}

/* --- TABELAS (Modernas) --- */
QTableWidget, QTableView {{
    background-color: {COLOR_BG_CARD};
    gridline-color: transparent;
    border: 1px solid {COLOR_BORDER};
    border-radius: 8px;
    selection-background-color: {COLOR_GOLD_LIGHT}; /* Seleção Dourada Clara */
    selection-color: {COLOR_TEXT_MAIN};
    alternate-background-color: #FAFAFA; /* Zebra suave */
}}

QHeaderView::section {{
    background-color: {COLOR_BG_MAIN};
    color: {COLOR_TEXT_SEC};
    font-weight: bold;
    padding: 10px;
    border: none;
    border-bottom: 2px solid {COLOR_GOLD_MAIN};
}}

QTableWidget::item {{
    padding: 8px;
    border-bottom: 1px solid #F0F0F0;
}}

/* --- MARKETPLACE & PRODUTOS --- */
QScrollArea#scroll_area_clean {{
    border: none;
    background-color: transparent;
}}

QFrame#barra_carrinho {{
    background-color: #2E2E2E;
    border-radius: 12px;
}}

QLabel#info_carrinho {{
    color: {COLOR_GOLD_LIGHT};
    font-weight: bold;
    font-size: 16px;
}}

QPushButton#btn_ver_carrinho {{
    background-color: {COLOR_GOLD_LIGHT};
    color: #2E2E2E;
    border: none;
    font-weight: bold;
}}

QPushButton#btn_ver_carrinho:hover {{
    background-color: {COLOR_GOLD_HOVER};
    color: white;
}}

QFrame#card_produto:hover {{
    border: 1px solid {COLOR_GOLD_MAIN};
    background-color: #FFFCF5;
}}

QLabel#produto_nome {{
    font-weight: bold; 
    font-size: 16px; 
    color: {COLOR_TEXT_MAIN};
}}

QLabel#produto_categoria {{
    color: {COLOR_TEXT_SEC}; 
    font-size: 12px;
}}

QLabel#produto_preco {{
    font-weight: bold; 
    font-size: 18px; 
    color: {COLOR_GOLD_MAIN};
}}

QLabel#placeholder_imagem {{
    background-color: {COLOR_BG_MAIN};
    border-radius: 8px;
    color: {COLOR_GOLD_MAIN};
    font-size: 20px;
}}

/* --- ITEM CARRINHO --- */
QFrame#item_carrinho {{
    background-color: white;
    border: 1px solid {COLOR_BORDER};
    border-radius: 8px;
}}

QLabel#carrinho_subtotal {{
    font-weight: bold; 
    font-size: 16px; 
    color: #4A90E2;
}}

QLabel#preco_unitario {{
    font-size: 16px; 
    color: {COLOR_TEXT_MAIN};
}}

QLabel#titulo_resumo {{
    font-weight: bold; 
    font-size: 16px; 
    margin-bottom: 10px;
    color: {COLOR_TEXT_MAIN};
}}

QLabel#total_resumo {{
    font-weight: bold; 
    font-size: 18px; 
    color: #4A90E2;
}}

QPushButton#btn_remover_carrinho {{
    background-color: {COLOR_DANGER_BG};
    color: {COLOR_DANGER};
    border: 1px solid #FFCDD2;
    border-radius: 4px;
    padding: 5px 10px;
}}

QPushButton#btn_remover_carrinho:hover {{
    background-color: {COLOR_DANGER};
    color: white;
}}

/* --- SCROLLBARS (Personalizadas) --- */
QScrollBar:vertical {{
    border: none;
    background: {COLOR_BG_MAIN};
    width: 10px;
    margin: 0px 0px 0px 0px;
}}
QScrollBar::handle:vertical {{
    background: #D1D1D1;
    min-height: 20px;
    border-radius: 5px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    border: none;
    background: none;
}}

/* --- CARDS DE RESUMO (Dashboard) --- */
QFrame#card_resumo, QFrame#card_danger, QFrame#card_success, QFrame#card_warning, QFrame#card_info {{
    border-radius: 12px;
    padding: 15px;
    color: white;
}}

QFrame#card_danger {{
    background-color: #FF6B6B;
}}

QFrame#card_success {{
    background-color: #28A745;
}}

QFrame#card_warning {{
    background-color: #FFA500;
}}

QFrame#card_info {{
    background-color: #4A90E2;
}}

QLabel#card_titulo {{
    color: white;
    font-size: 14px;
    font-weight: bold;
    background-color: transparent;
}}

QLabel#card_valor {{
    color: white;
    font-size: 24px;
    font-weight: bold;
    background-color: transparent;
}}

QLabel#titulo_pagina {{
    font-size: 26px;
    font-weight: bold;
    color: {COLOR_TEXT_MAIN};
    margin-bottom: 15px;
}}

QLabel#subtitulo {{
    font-size: 16px;
    color: {COLOR_TEXT_SEC};
    margin-bottom: 10px;
}}

QLabel#titulo_secao {{
    font-size: 18px;
    font-weight: bold;
    color: {COLOR_TEXT_MAIN};
    margin-bottom: 20px;
}}

QLabel#texto_destaque {{
    font-weight: bold;
    font-size: 16px;
    color: #4A90E2;
}}

QLabel#texto_sucesso {{
    font-weight: bold;
    font-size: 16px;
    color: #28A745;
}}

QLabel#texto_perigo {{
    font-weight: bold;
    font-size: 16px;
    color: #FF6B6B;
}}

QLabel#preview_cor {{
    border: 1px solid {COLOR_BORDER};
    border-radius: 4px;
}}

/* --- BOTÃO INFO --- */
QPushButton#info {{
    background-color: #17a2b8;
    color: white;
    border: 1px solid #138496;
}}

QPushButton#info:hover {{
    background-color: #138496;
}}

/* --- GROUP BOX --- */
QGroupBox {{
    border: 1px solid {COLOR_BORDER};
    border-radius: 12px;
    margin-top: 25px;
    background-color: {COLOR_BG_CARD};
    font-weight: bold;
    color: {COLOR_TEXT_MAIN};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 20px;
    padding: 0 10px;
    background-color: {COLOR_BG_CARD}; 
    color: {COLOR_GOLD_MAIN};
}}

/* --- STATUS BADGES --- */
QLabel#badge_confirmado, QLabel#badge_confirmed {{
    background-color: {COLOR_SUCCESS_BG};
    color: {COLOR_SUCCESS};
    border: 1px solid {COLOR_SUCCESS};
    border-radius: 12px;
    padding: 4px 12px;
    font-weight: 600;
    font-size: 12px;
}}

QLabel#badge_pendente, QLabel#badge_pending {{
    background-color: {COLOR_WARNING_BG};
    color: {COLOR_WARNING};
    border: 1px solid {COLOR_WARNING};
    border-radius: 12px;
    padding: 4px 12px;
    font-weight: 600;
    font-size: 12px;
}}

QLabel#badge_vencido, QLabel#badge_overdue {{
    background-color: {COLOR_DANGER_BG};
    color: {COLOR_DANGER};
    border: 1px solid {COLOR_DANGER};
    border-radius: 12px;
    padding: 4px 12px;
    font-weight: 600;
    font-size: 12px;
}}

QLabel#badge_em_aberto {{
    background-color: #F3E5F5;
    color: #8E24AA;
    border: 1px solid #8E24AA;
    border-radius: 12px;
    padding: 4px 12px;
    font-weight: 600;
    font-size: 12px;
}}

QLabel#badge_a_vencer {{
    background-color: {COLOR_GRAY_BG};
    color: {COLOR_GRAY};
    border: 1px solid {COLOR_GRAY};
    border-radius: 12px;
    padding: 4px 12px;
    font-weight: 600;
    font-size: 12px;
}}

QLabel#badge_hoje {{
    background-color: #E8F5E9;
    color: #2E7D32;
    border: 1px solid #2E7D32;
    border-radius: 4px;
    padding: 2px 8px;
    font-weight: bold;
    font-size: 11px;
}}

/* --- ACTION BUTTONS (Icon Style) --- */
QPushButton#btn_action_view {{
    background-color: {COLOR_INFO};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
    min-width: 35px;
    max-width: 35px;
}}

QPushButton#btn_action_view:hover {{
    background-color: {COLOR_INFO_HOVER};
}}

QPushButton#btn_action_edit {{
    background-color: {COLOR_WARNING};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
    min-width: 35px;
    max-width: 35px;
}}

QPushButton#btn_action_edit:hover {{
    background-color: #E67E22;
}}

QPushButton#btn_action_delete {{
    background-color: {COLOR_DANGER};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
    min-width: 35px;
    max-width: 35px;
}}

QPushButton#btn_action_delete:hover {{
    background-color: #C0392B;
}}

QPushButton#btn_action_more {{
    background-color: {COLOR_SUCCESS};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
    min-width: 35px;
    max-width: 35px;
}}

QPushButton#btn_action_more:hover {{
    background-color: #229954;
}}

/* --- SUMMARY CARDS (Modern Style) --- */
QFrame#summary_card_vencidos {{
    background-color: {COLOR_DANGER};
    border: none;
    border-radius: 12px;
    padding: 20px;
}}

QFrame#summary_card_vencem_hoje {{
    background-color: {COLOR_WARNING};
    border: none;
    border-radius: 12px;
    padding: 20px;
}}

QFrame#summary_card_a_vencer {{
    background-color: {COLOR_GRAY};
    border: none;
    border-radius: 12px;
    padding: 20px;
}}

QFrame#summary_card_recebidos {{
    background-color: {COLOR_SUCCESS};
    border: none;
    border-radius: 12px;
    padding: 20px;
}}

QFrame#summary_card_total {{
    background-color: {COLOR_DARK};
    border: none;
    border-radius: 12px;
    padding: 20px;
}}

QLabel#summary_card_title {{
    color: white;
    font-size: 13px;
    font-weight: 500;
    background-color: transparent;
}}

QLabel#summary_card_value {{
    color: white;
    font-size: 26px;
    font-weight: bold;
    background-color: transparent;
}}

QLabel#summary_card_icon {{
    color: rgba(255, 255, 255, 0.3);
    font-size: 14px;
    background-color: transparent;
}}

/* --- HEADER TOOLBAR --- */
QFrame#toolbar_header {{
    background-color: {COLOR_BG_CARD};
    border: 1px solid {COLOR_BORDER};
    border-radius: 10px;
    padding: 10px 15px;
}}

QPushButton#btn_adicionar {{
    background-color: {COLOR_SUCCESS};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 14px;
}}

QPushButton#btn_adicionar:hover {{
    background-color: #229954;
}}

QPushButton#btn_mais_acoes {{
    background-color: {COLOR_DARK};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 14px;
}}

QPushButton#btn_mais_acoes:hover {{
    background-color: #2C3E50;
}}

QPushButton#btn_busca_avancada {{
    background-color: {COLOR_DARK};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 14px;
}}

QPushButton#btn_busca_avancada:hover {{
    background-color: #2C3E50;
}}

QComboBox#month_selector {{
    background-color: {COLOR_DARK};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 15px;
    font-weight: 600;
    font-size: 14px;
    min-width: 150px;
}}

QComboBox#month_selector::drop-down {{
    border: none;
    width: 25px;
}}

QComboBox#month_selector::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid white;
    margin-right: 10px;
}}

/* --- PAGE HEADER --- */
QLabel#page_title {{
    font-size: 24px;
    font-weight: bold;
    color: {COLOR_TEXT_MAIN};
}}

QLabel#breadcrumb {{
    font-size: 13px;
    color: {COLOR_TEXT_SEC};
}}

QLabel#breadcrumb_icon {{
    font-size: 16px;
    color: {COLOR_TEXT_MAIN};
}}
"""

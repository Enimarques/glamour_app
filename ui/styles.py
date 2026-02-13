# -*- coding: utf-8 -*-

"""
Módulo de Estilos (QSS) para o Sistema de Gerenciamento de Loja de Semijoias.
Design System Refinado: Cores Pastéis e Layout Compacto.
"""

# Paleta de Cores Suaves (Pastéis)
COLOR_BG_MAIN = "#F8FAFC"       # Fundo Geral Neutro
COLOR_BG_CARD = "#FFFFFF"       # Branco Puro para Cards
COLOR_PRIMARY = "#48BB78"       # Verde Pastel (Ação Principal)
COLOR_PRIMARY_LIGHT = "#D5F4E6" # Fundo Verde Suave
COLOR_DARK = "#2D3748"          # Dark Blue/Gray (Menu e Títulos)
COLOR_TEXT_MAIN = "#2D3748"     # Texto Principal
COLOR_TEXT_SEC = "#718096"      # Texto Secundário
COLOR_BORDER = "#E2E8F0"        # Bordas Sutis e Claras

# Estilo Global (QSS)
GLOBAL_STYLESHEET = f"""
/* --- JANELA PRINCIPAL --- */
QMainWindow, QWidget {{
    background-color: {COLOR_BG_MAIN};
    font-family: "Segoe UI", "Inter", "Roboto", "Arial";
    font-size: 13px;
    color: {COLOR_TEXT_MAIN};
}}

/* --- SIDEBAR (COMPACTA E INTEGRADA - IMAGE-1) --- */
QFrame#sidebar {{
    background-color: #FFFFFF;
    border-right: 1px solid {COLOR_BORDER};
    min-width: 240px;
    max-width: 240px;
}}

QLabel#logo_label {{
    color: {COLOR_DARK};
    font-size: 16px;
    font-weight: 800;
    padding: 25px 15px;
    letter-spacing: 0.5px;
}}

QListWidget#nav_list {{
    background-color: transparent;
    border: none;
    outline: none;
    padding: 5px;
}}

QListWidget#nav_list::item {{
    color: {COLOR_TEXT_SEC};
    padding: 10px 15px;
    margin-bottom: 2px;
    border-radius: 6px;
    font-weight: 500;
}}

QListWidget#nav_list::item:hover {{
    background-color: #F7FAFC;
    color: {COLOR_DARK};
}}

QListWidget#nav_list::item:selected {{
    background-color: #EDF2F7;
    color: {COLOR_PRIMARY};
    border-left: 3px solid {COLOR_PRIMARY};
    font-weight: 600;
}}

/* --- COMPONENTES DE FORMULÁRIO (ESTILO IMAGE-2) --- */
QLineEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox, QTextEdit {{
    background-color: #FFFFFF;
    border: 1px solid {COLOR_BORDER};
    border-radius: 6px;
    padding: 8px 12px;
    color: {COLOR_TEXT_MAIN};
    min-height: 35px;
}}

QLineEdit:focus, QComboBox:focus, QDateEdit:focus {{
    border: 1px solid {COLOR_PRIMARY};
    background-color: #FFFFFF;
}}

QComboBox::drop-down, QDateEdit::drop-down {{
    border: none;
    width: 20px;
}}

QComboBox::down-arrow, QDateEdit::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {COLOR_TEXT_SEC};
    margin-right: 8px;
}}

/* --- BOTÕES (ESTILO CLEAN IMAGE-2) --- */
QPushButton {{
    background-color: #FFFFFF;
    border: 1px solid {COLOR_BORDER};
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
    color: {COLOR_DARK};
}}

QPushButton:hover {{
    background-color: #F7FAFC;
    border-color: #CBD5E0;
}}

QPushButton#btn_adicionar, QPushButton#primary {{
    background-color: {COLOR_PRIMARY};
    color: white;
    border: none;
}}

QPushButton#btn_adicionar:hover, QPushButton#primary:hover {{
    background-color: #38A169;
}}

QPushButton#btn_mais_acoes, QPushButton#secondary {{
    background-color: #FFFFFF;
    color: {COLOR_DARK};
    border: 1px solid {COLOR_BORDER};
}}

/* --- CARDS DE RESUMO (DESTACADOS COM CORES PASTÉIS) --- */
QFrame#summary_card_vencidos {{
    background-color: #FFF5F5;
    border: 1px solid #FEB2B2;
    border-radius: 10px;
}}

QFrame#summary_card_vencem_hoje {{
    background-color: #FFFBEB;
    border: 1px solid #F6E05E;
    border-radius: 10px;
}}

QFrame#summary_card_a_vencer {{
    background-color: #EBF8FF;
    border: 1px solid #90CDF4;
    border-radius: 10px;
}}

QFrame#summary_card_recebidos {{
    background-color: #F0FFF4;
    border: 1px solid #9AE6B4;
    border-radius: 10px;
}}

QFrame#summary_card_total {{
    background-color: #F7FAFC;
    border: 1px solid #CBD5E0;
    border-radius: 10px;
}}

QLabel#summary_card_title {{
    color: #4A5568;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    background: transparent;
}}

QLabel#summary_card_value {{
    color: {COLOR_DARK};
    font-size: 22px;
    font-weight: 800;
    margin-top: 2px;
    background: transparent;
}}

QLabel#summary_card_icon {{
    font-size: 20px;
    background: transparent;
}}

/* --- TABELAS --- */
QFrame#container_card {{
    background-color: #FFFFFF;
    border: 1px solid {COLOR_BORDER};
    border-radius: 10px;
}}

QTableWidget, QTableView {{
    background-color: #FFFFFF;
    gridline-color: transparent;
    border: none;
    outline: none;
}}

QHeaderView::section {{
    background-color: #F8FAFC;
    color: {COLOR_TEXT_SEC};
    padding: 12px;
    border: none;
    border-bottom: 1px solid {COLOR_BORDER};
    font-weight: 700;
    text-transform: uppercase;
    font-size: 10px;
}}

QTableWidget::item {{
    padding: 12px;
    border-bottom: 1px solid #F1F5F9;
}}

/* --- BADGES --- */
QLabel#badge_success {{ background-color: #D5F4E6; color: #27AE60; border-radius: 12px; padding: 4px 10px; font-weight: 700; font-size: 11px; }}
QLabel#badge_warning {{ background-color: #FEF5E7; color: #F39C12; border-radius: 12px; padding: 4px 10px; font-weight: 700; font-size: 11px; }}
QLabel#badge_info {{ background-color: #EBF5FB; color: #3498DB; border-radius: 12px; padding: 4px 10px; font-weight: 700; font-size: 11px; }}

/* --- MARKETPLACE & PRODUTOS --- */
QFrame#card_produto_moderno {{
    background-color: #FFFFFF;
    border: 1px solid {COLOR_BORDER};
    border-radius: 12px;
}}

QFrame#card_produto_moderno:hover {{
    border: 1px solid {COLOR_PRIMARY};
    background-color: #FFFFFF;
}}

QLabel#placeholder_imagem_moderna {{
    background-color: #F8FAFC;
    border-radius: 8px;
}}
"""

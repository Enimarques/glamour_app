#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ponto de entrada principal para o Sistema de Gerenciamento de Loja de Semijoias
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from ui.janela_principal import JanelaPrincipal

def main():
    """Função principal da aplicação."""
    # Cria a aplicação Qt
    app = QApplication(sys.argv)
    app.setApplicationName("Sistema de Gerenciamento de Loja de Semijoias")
    app.setApplicationVersion("1.0.0")
    
    # Cria e mostra a janela principal
    janela = JanelaPrincipal()
    janela.show()
    
    # Executa o loop de eventos da aplicação
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
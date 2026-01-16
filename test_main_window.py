#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple test script to verify the main window works correctly.
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.janela_principal import JanelaPrincipal

def main():
    """Main function to test the main window."""
    print("Creating QApplication...")
    app = QApplication(sys.argv)
    print("QApplication created successfully")
    
    print("Creating main window...")
    janela = JanelaPrincipal()
    print("Main window created successfully")
    
    print("Showing main window...")
    janela.show()
    print("Main window shown successfully")
    
    print("Starting event loop...")
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
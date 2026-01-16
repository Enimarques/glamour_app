#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de teste para verificar se os componentes de UI foram implementados corretamente.
"""

import sys
import os

def test_ui_components():
    """Testa se todos os componentes de UI podem ser importados corretamente."""
    print("=== Testando Componentes de UI ===")
    
    try:
        from ui.janela_principal import JanelaPrincipal
        print("✓ Janela principal importada com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar janela principal: {e}")
        return False
        
    try:
        from ui.lista_produtos import ListaProdutos
        print("✓ Lista de produtos importada com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar lista de produtos: {e}")
        return False
        
    try:
        from ui.formulario_produto import FormularioProduto
        print("✓ Formulário de produto importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar formulário de produto: {e}")
        return False
        
    try:
        from ui.lista_clientes import ListaClientes
        print("✓ Lista de clientes importada com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar lista de clientes: {e}")
        return False
        
    try:
        from ui.formulario_cliente import FormularioCliente
        print("✓ Formulário de cliente importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar formulário de cliente: {e}")
        return False
        
    return True

def main():
    """Função principal de teste."""
    print("=== Teste de Componentes de UI ===\n")
    
    success = test_ui_components()
    
    if success:
        print("\n🎉 Todos os componentes de UI foram importados com sucesso!")
        print("A interface foi atualizada com sucesso.")
        return 0
    else:
        print("\n❌ Alguns componentes de UI falharam ao ser importados.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
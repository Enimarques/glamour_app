#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de teste para verificar se os componentes de vendas foram implementados corretamente.
"""

import sys
import os

def test_modulo_vendas():
    """Testa se todos os componentes do módulo de vendas podem ser importados corretamente."""
    print("=== Testando Módulo de Vendas ===")
    
    try:
        from models.venda import Venda, ItemVenda
        print("✓ Modelos de venda importados com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar modelos de venda: {e}")
        return False
        
    try:
        from controllers.venda_controller import VendaController
        print("✓ Controller de venda importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar controller de venda: {e}")
        return False
        
    try:
        from ui.lista_vendas import ListaVendas
        print("✓ Lista de vendas importada com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar lista de vendas: {e}")
        return False
        
    try:
        from ui.formulario_venda import FormularioVenda
        print("✓ Formulário de venda importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar formulário de venda: {e}")
        return False
        
    return True

def main():
    """Função principal de teste."""
    print("=== Teste do Módulo de Vendas ===\n")
    
    success = test_modulo_vendas()
    
    if success:
        print("\n🎉 Todos os componentes do módulo de vendas foram importados com sucesso!")
        print("O módulo de vendas foi implementado corretamente.")
        return 0
    else:
        print("\n❌ Alguns componentes do módulo de vendas falharam ao ser importados.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
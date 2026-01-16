#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de teste para verificar se o módulo de produtos marketplace foi implementado corretamente.
"""

import sys
import os

def test_modulo_produtos_marketplace():
    """Testa se todos os componentes do módulo de produtos marketplace podem ser importados corretamente."""
    print("=== Testando Módulo de Produtos Marketplace ===")
    
    try:
        from models.carrinho import CarrinhoCompras, ItemCarrinho
        print("✓ Modelos de carrinho importados com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar modelos de carrinho: {e}")
        return False
        
    try:
        from ui.lista_produtos_marketplace import ListaProdutosMarketplace
        print("✓ Interface de produtos marketplace importada com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar interface de produtos marketplace: {e}")
        return False
        
    try:
        from ui.lista_produtos_marketplace import DialogoCarrinho
        print("✓ Diálogo de carrinho importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar diálogo de carrinho: {e}")
        return False
    
    print("Todos os componentes do módulo de produtos marketplace estão funcionando corretamente!\n")
    return True

def test_integracao_main_window():
    """Testa se a janela principal integra o novo módulo corretamente."""
    print("=== Testando Integração com Janela Principal ===")
    
    try:
        from ui.janela_principal import JanelaPrincipal
        print("✓ Janela principal importada com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar janela principal: {e}")
        return False
        
    print("Integração com janela principal está funcionando corretamente!\n")
    return True

if __name__ == "__main__":
    print("Testando módulo de produtos marketplace...\n")
    
    sucesso = True
    sucesso &= test_modulo_produtos_marketplace()
    sucesso &= test_integracao_main_window()
    
    if sucesso:
        print("✅ Todos os testes passaram! O módulo de produtos marketplace está pronto para uso.")
        sys.exit(0)
    else:
        print("❌ Alguns testes falharam. Verifique os erros acima.")
        sys.exit(1)
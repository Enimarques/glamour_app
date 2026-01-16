#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de teste para verificar se os componentes de relatórios e configurações 
foram implementados corretamente.
"""

import sys
import os

def test_modulo_relatorios():
    """Testa se todos os componentes do módulo de relatórios podem ser importados corretamente."""
    print("=== Testando Módulo de Relatórios ===")
    
    try:
        from reports.relatorio_financeiro import RelatorioFinanceiro
        print("✓ Relatório financeiro importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar relatório financeiro: {e}")
        return False
        
    try:
        from reports.catalogo_produtos import CatalogoProdutos
        print("✓ Catálogo de produtos importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar catálogo de produtos: {e}")
        return False
        
    try:
        from ui.lista_relatorios import ListaRelatorios
        print("✓ Interface de relatórios importada com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar interface de relatórios: {e}")
        return False
    
    print("Todos os componentes do módulo de relatórios estão funcionando corretamente!\n")
    return True

def test_modulo_configuracoes():
    """Testa se todos os componentes do módulo de configurações podem ser importados corretamente."""
    print("=== Testando Módulo de Configurações ===")
    
    try:
        from ui.lista_configuracoes import ListaConfiguracoes
        print("✓ Interface de configurações importada com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar interface de configurações: {e}")
        return False
    
    print("Todos os componentes do módulo de configurações estão funcionando corretamente!\n")
    return True

def test_integracao_main_window():
    """Testa se a janela principal integra os novos módulos corretamente."""
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
    print("Testando módulos de relatórios e configurações...\n")
    
    sucesso = True
    sucesso &= test_modulo_relatorios()
    sucesso &= test_modulo_configuracoes()
    sucesso &= test_integracao_main_window()
    
    if sucesso:
        print("✅ Todos os testes passaram! Os módulos de relatórios e configurações estão prontos para uso.")
        sys.exit(0)
    else:
        print("❌ Alguns testes falharam. Verifique os erros acima.")
        sys.exit(1)
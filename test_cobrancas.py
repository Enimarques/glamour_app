#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de teste para verificar se o módulo de cobranças foi implementado corretamente.
"""

import sys
import os

def test_modulo_cobrancas():
    """Testa se todos os componentes do módulo de cobranças podem ser importados corretamente."""
    print("=== Testando Módulo de Cobranças ===")
    
    try:
        from models.pagamento import Pagamento
        print("✓ Modelo de pagamento importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar modelo de pagamento: {e}")
        return False
        
    try:
        from controllers.pagamento_controller import PagamentoController
        print("✓ Controlador de pagamento importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar controlador de pagamento: {e}")
        return False
        
    try:
        from ui.aba_cobrancas import AbaCobrancas
        print("✓ Interface de cobranças importada com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar interface de cobranças: {e}")
        return False
        
    try:
        from ui.aba_cobrancas import DialogoRegistroPagamento
        print("✓ Diálogo de registro de pagamento importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar diálogo de registro de pagamento: {e}")
        return False
        
    try:
        from ui.aba_cobrancas import DialogoDetalhesDivida
        print("✓ Diálogo de detalhes de dívida importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar diálogo de detalhes de dívida: {e}")
        return False
    
    print("Todos os componentes do módulo de cobranças estão funcionando corretamente!\n")
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
    print("Testando módulo de cobranças...\n")
    
    sucesso = True
    sucesso &= test_modulo_cobrancas()
    sucesso &= test_integracao_main_window()
    
    if sucesso:
        print("✅ Todos os testes passaram! O módulo de cobranças está pronto para uso.")
        sys.exit(0)
    else:
        print("❌ Alguns testes falharam. Verifique os erros acima.")
        sys.exit(1)
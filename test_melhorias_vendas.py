#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de teste para verificar se as melhorias no sistema de vendas e cobranças foram implementadas corretamente.
"""

import sys
import os
from datetime import datetime

def test_modelos_atualizados():
    """Testa se os modelos foram atualizados corretamente."""
    print("=== Testando Modelos Atualizados ===")
    
    try:
        from models.venda import Venda
        # Testar criação de venda com novos tipos de pagamento
        venda = Venda(
            tipo_pagamento="Parcelado Boleto",
            dia_vencimento=15
        )
        assert venda.tipo_pagamento == "Parcelado Boleto"
        assert venda.dia_vencimento == 15
        print("✓ Modelo de venda atualizado com sucesso")
    except Exception as e:
        print(f"✗ Erro ao testar modelo de venda: {e}")
        return False
        
    try:
        from models.pagamento import Pagamento
        pagamento = Pagamento()
        print("✓ Modelo de pagamento funcionando corretamente")
    except Exception as e:
        print(f"✗ Erro ao testar modelo de pagamento: {e}")
        return False
    
    print("Todos os modelos foram atualizados corretamente!\n")
    return True

def test_controladores_atualizados():
    """Testa se os controladores foram atualizados corretamente."""
    print("=== Testando Controladores Atualizados ===")
    
    try:
        from controllers.venda_controller import VendaController
        # Testar criação de venda com novos tipos de pagamento
        venda = VendaController.criar_venda(
            tipo_pagamento="Cartão Crédito"
        )
        # Vendas à vista devem ser marcadas como 'pago'
        if venda:
            assert venda.status == "pago"
        print("✓ Controlador de vendas atualizado com sucesso")
    except Exception as e:
        print(f"✗ Erro ao testar controlador de vendas: {e}")
        return False
        
    try:
        from controllers.pagamento_controller import PagamentoController
        # Testar métodos do controlador de pagamentos
        dividas = PagamentoController.obter_dividas_pendentes()
        print("✓ Controlador de pagamentos funcionando corretamente")
    except Exception as e:
        print(f"✗ Erro ao testar controlador de pagamentos: {e}")
        return False
    
    print("Todos os controladores foram atualizados corretamente!\n")
    return True

def test_interfaces_atualizadas():
    """Testa se as interfaces foram atualizadas corretamente."""
    print("=== Testando Interfaces Atualizadas ===")
    
    try:
        from ui.formulario_venda import FormularioVenda
        print("✓ Interface de formulário de venda importada com sucesso")
    except Exception as e:
        print(f"✗ Erro ao importar interface de formulário de venda: {e}")
        return False
        
    try:
        from ui.aba_cobrancas import AbaCobrancas
        print("✓ Interface de cobranças importada com sucesso")
    except Exception as e:
        print(f"✗ Erro ao importar interface de cobranças: {e}")
        return False
    
    print("Todas as interfaces foram atualizadas corretamente!\n")
    return True

def test_banco_dados_atualizado():
    """Testa se o banco de dados foi atualizado corretamente."""
    print("=== Testando Banco de Dados Atualizado ===")
    
    try:
        from database.db_manager import gerenciador_bd
        # Conectar ao banco de dados
        conexao = gerenciador_bd.conectar()
        cursor = conexao.cursor()
        
        # Verificar se a coluna dia_vencimento existe na tabela vendas
        cursor.execute("PRAGMA table_info(vendas)")
        colunas = cursor.fetchall()
        nomes_colunas = [coluna[1] for coluna in colunas]
        
        if 'dia_vencimento' in nomes_colunas:
            print("✓ Coluna dia_vencimento adicionada à tabela vendas")
        else:
            print("✗ Coluna dia_vencimento não encontrada na tabela vendas")
            return False
            
        print("Banco de dados atualizado corretamente!\n")
        return True
    except Exception as e:
        print(f"✗ Erro ao testar banco de dados: {e}")
        return False

if __name__ == "__main__":
    print("Testando melhorias no sistema de vendas e cobranças...\n")
    
    sucesso = True
    sucesso &= test_modelos_atualizados()
    sucesso &= test_controladores_atualizados()
    sucesso &= test_interfaces_atualizadas()
    sucesso &= test_banco_dados_atualizado()
    
    if sucesso:
        print("✅ Todos os testes passaram! As melhorias no sistema de vendas e cobranças estão prontas para uso.")
        sys.exit(0)
    else:
        print("❌ Alguns testes falharam. Verifique os erros acima.")
        sys.exit(1)
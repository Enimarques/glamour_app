#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de teste para verificar se todos os componentes da aplicação estão funcionando corretamente.
"""

import sys
import os

def test_imports():
    """Testa se todos os módulos podem ser importados corretamente."""
    print("=== Testando Importações ===")
    
    try:
        from database.db_manager import gerenciador_bd
        print("✓ Gerenciador de banco de dados importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar gerenciador de banco de dados: {e}")
        return False
        
    try:
        from models.produto import Produto
        print("✓ Modelo de Produto importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar modelo de Produto: {e}")
        return False
        
    try:
        from models.cliente import Cliente
        print("✓ Modelo de Cliente importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar modelo de Cliente: {e}")
        return False
        
    try:
        from models.venda import Venda, ItemVenda
        print("✓ Modelos de Venda e ItemVenda importados com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar modelos de Venda: {e}")
        return False
        
    try:
        from controllers.produto_controller import ProdutoController
        print("✓ Controller de Produto importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar controller de Produto: {e}")
        return False
        
    try:
        from controllers.cliente_controller import ClienteController
        print("✓ Controller de Cliente importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar controller de Cliente: {e}")
        return False
        
    try:
        from controllers.venda_controller import VendaController
        print("✓ Controller de Venda importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar controller de Venda: {e}")
        return False
        
    try:
        from ui.janela_principal import JanelaPrincipal
        print("✓ Interface principal importada com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar interface principal: {e}")
        return False
        
    try:
        from reports.catalogo_produtos import CatalogoProdutos
        print("✓ Relatório de catálogo importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar relatório de catálogo: {e}")
        return False
        
    try:
        from reports.relatorio_financeiro import RelatorioFinanceiro
        print("✓ Relatório financeiro importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar relatório financeiro: {e}")
        return False
        
    return True

def test_database_connection():
    """Testa a conexão com o banco de dados."""
    print("\n=== Testando Conexão com Banco de Dados ===")
    
    try:
        from database.db_manager import gerenciador_bd
        conexao = gerenciador_bd.conectar()
        print("✓ Conexão com banco de dados estabelecida com sucesso")
        
        # Testa uma consulta simples
        cursor = gerenciador_bd.executar_consulta("SELECT 1")
        resultado = cursor.fetchone()
        if resultado:
            print("✓ Consulta ao banco de dados executada com sucesso")
        else:
            print("✗ Falha ao executar consulta no banco de dados")
            return False
            
        return True
    except Exception as e:
        print(f"✗ Erro ao conectar com banco de dados: {e}")
        return False

def test_basic_operations():
    """Testa operações básicas de CRUD."""
    print("\n=== Testando Operações Básicas ===")
    
    try:
        from controllers.produto_controller import ProdutoController
        from controllers.cliente_controller import ClienteController
        
        # Testa criação de produto
        produto = ProdutoController.criar_produto(
            nome="Produto de Teste",
            categoria="Teste",
            preco_custo=10.0,
            preco_venda=20.0,
            quantidade=5
        )
        print(f"✓ Produto criado com sucesso (ID: {produto.id})")
        
        # Testa atualização de produto
        produto_atualizado = ProdutoController.atualizar_produto(
            produto.id,
            quantidade=10
        )
        if produto_atualizado and produto_atualizado.quantidade == 10:
            print("✓ Produto atualizado com sucesso")
        else:
            print("✗ Falha ao atualizar produto")
            return False
            
        # Testa criação de cliente
        cliente = ClienteController.criar_cliente(
            nome="Cliente de Teste",
            telefone="(11) 99999-9999",
            observacoes="Cliente para testes"
        )
        print(f"✓ Cliente criado com sucesso (ID: {cliente.id})")
        
        # Testa listagem
        produtos = ProdutoController.listar_produtos()
        clientes = ClienteController.listar_clientes()
        print(f"✓ Listagem realizada com sucesso ({len(produtos)} produtos, {len(clientes)} clientes)")
        
        # Testa exclusão
        if ProdutoController.excluir_produto(produto.id):
            print("✓ Produto excluído com sucesso")
        else:
            print("✗ Falha ao excluir produto")
            return False
            
        if ClienteController.excluir_cliente(cliente.id):
            print("✓ Cliente excluído com sucesso")
        else:
            print("✗ Falha ao excluir cliente")
            return False
            
        return True
    except Exception as e:
        print(f"✗ Erro ao executar operações básicas: {e}")
        return False

def main():
    """Função principal de teste."""
    print("=== Teste da Aplicação de Gerenciamento de Loja de Semijoias ===\n")
    
    # Executa todos os testes
    tests = [
        ("Importações", test_imports),
        ("Conexão com Banco de Dados", test_database_connection),
        ("Operações Básicas", test_basic_operations)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Erro inesperado no teste {test_name}: {e}")
            results.append((test_name, False))
    
    # Mostra resultados
    print("\n=== Resultados dos Testes ===")
    all_passed = True
    for test_name, result in results:
        status = "PASSOU" if result else "FALHOU"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 Todos os testes passaram! A aplicação está funcionando corretamente.")
        return 0
    else:
        print("\n❌ Alguns testes falharam. Verifique os erros acima.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
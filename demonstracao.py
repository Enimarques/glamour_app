#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demonstração das funcionalidades principais do Sistema de Gerenciamento de Loja de Semijoias.
"""

from controllers.produto_controller import ProdutoController
from controllers.cliente_controller import ClienteController
from controllers.venda_controller import VendaController
from reports.catalogo_produtos import CatalogoProdutos
from reports.relatorio_financeiro import RelatorioFinanceiro
import os

def demonstrar_cadastro_produtos():
    """Demonstra o cadastro e gerenciamento de produtos."""
    print("=== Demonstração: Cadastro de Produtos ===")
    
    # Criar alguns produtos
    produto1 = ProdutoController.criar_produto(
        nome="Colar de Pérolas",
        categoria="Semijoias",
        preco_custo=35.00,
        preco_venda=79.90,
        quantidade=10
    )
    print(f"✓ Produto criado: {produto1.nome} (ID: {produto1.id})")
    
    produto2 = ProdutoController.criar_produto(
        nome="Relógio de Pulso Feminino",
        categoria="Relógios",
        preco_custo=120.00,
        preco_venda=249.90,
        quantidade=5
    )
    print(f"✓ Produto criado: {produto2.nome} (ID: {produto2.id})")
    
    # Listar produtos
    produtos = ProdutoController.listar_produtos()
    print(f"\nLista de produtos ({len(produtos)} itens):")
    for produto in produtos[-2:]:  # Mostrar apenas os dois últimos
        print(f"  - {produto.nome} (R$ {produto.preco_venda:.2f}) - Estoque: {produto.quantidade}")
    
    # Atualizar um produto
    produto_atualizado = ProdutoController.atualizar_produto(
        produto1.id,
        quantidade=15  # Aumentar o estoque
    )
    print(f"\n✓ Estoque atualizado: {produto_atualizado.nome} agora tem {produto_atualizado.quantidade} unidades")
    
    # Verificar estoque baixo
    produtos_baixo = ProdutoController.verificar_estoque_baixo(limite=6)
    if produtos_baixo:
        print(f"\n⚠ Produtos com estoque baixo (< 6 unidades):")
        for produto in produtos_baixo:
            print(f"  - {produto.nome}: {produto.quantidade} unidades")
    else:
        print(f"\n✓ Nenhum produto com estoque baixo.")

def demonstrar_cadastro_clientes():
    """Demonstra o cadastro e gerenciamento de clientes."""
    print("\n=== Demonstração: Cadastro de Clientes ===")
    
    # Criar alguns clientes
    cliente1 = ClienteController.criar_cliente(
        nome="Carlos Mendes",
        telefone="(11) 98765-1234",
        observacoes="Cliente VIP, compra mensalmente"
    )
    print(f"✓ Cliente criado: {cliente1.nome} (ID: {cliente1.id})")
    
    cliente2 = ClienteController.criar_cliente(
        nome="Fernanda Costa",
        telefone="(11) 99876-5432",
        observacoes="Interessada em semijoias"
    )
    print(f"✓ Cliente criado: {cliente2.nome} (ID: {cliente2.id})")
    
    # Listar clientes
    clientes = ClienteController.listar_clientes()
    print(f"\nLista de clientes ({len(clientes)} cadastrados):")
    for cliente in clientes[-2:]:  # Mostrar apenas os dois últimos
        print(f"  - {cliente.nome} ({cliente.telefone})")
    
    # Buscar cliente por nome
    clientes_encontrados = ClienteController.buscar_clientes("Carlos")
    if clientes_encontrados:
        print(f"\n🔍 Cliente encontrado na busca por 'Carlos':")
        for cliente in clientes_encontrados:
            print(f"  - {cliente.nome}")

def demonstrar_registro_vendas():
    """Demonstra o registro de vendas."""
    print("\n=== Demonstração: Registro de Vendas ===")
    
    # Obter produtos e clientes para a venda
    produtos = ProdutoController.listar_produtos()
    clientes = ClienteController.listar_clientes()
    
    if len(produtos) >= 2 and len(clientes) >= 1:
        # Criar uma venda de exemplo
        itens_venda = [
            {
                "produto_id": produtos[-1].id,  # Último produto cadastrado
                "quantidade": 1,
                "preco_unitario": produtos[-1].preco_venda
            },
            {
                "produto_id": produtos[-2].id,  # Penúltimo produto cadastrado
                "quantidade": 2,
                "preco_unitario": produtos[-2].preco_venda
            }
        ]
        
        venda = VendaController.criar_venda(
            cliente_id=clientes[-1].id,  # Último cliente cadastrado
            itens=itens_venda,
            tipo_pagamento="avista"
        )
        
        if venda:
            print(f"✓ Venda registrada com sucesso (ID: {venda.id})")
            if venda.cliente:
                print(f"  Cliente: {venda.cliente.nome}")
            else:
                print(f"  Cliente: Não especificado")
            print(f"  Valor total: R$ {venda.valor_total:.2f}")
            print(f"  Status: {venda.status}")
            
            # Mostrar itens da venda
            print("  Itens:")
            for item in venda.itens:
                if item.produto:
                    print(f"    - {item.produto.nome}: {item.quantidade} x R$ {item.preco_unitario:.2f}")
                else:
                    print(f"    - Produto ID {item.produto_id}: {item.quantidade} x R$ {item.preco_unitario:.2f}")
        else:
            print("✗ Falha ao registrar venda")
    else:
        print("✗ Não há produtos ou clientes suficientes para registrar uma venda")

def demonstrar_relatorios():
    """Demonstra a geração de relatórios."""
    print("\n=== Demonstração: Geração de Relatórios ===")
    
    # Gerar catálogo de produtos
    try:
        caminho_catalogo = CatalogoProdutos.gerar_catalogo("relatorios/catalogo_demo.pdf")
        print(f"✓ Catálogo de produtos gerado: {caminho_catalogo}")
    except Exception as e:
        print(f"✗ Erro ao gerar catálogo: {e}")
    
    # Gerar relatório financeiro
    try:
        caminho_relatorio = RelatorioFinanceiro.gerar_relatorio_simplificado("relatorios/financeiro_demo.pdf")
        print(f"✓ Relatório financeiro gerado: {caminho_relatorio}")
    except Exception as e:
        print(f"✗ Erro ao gerar relatório financeiro: {e}")
    
    # Mostrar informações financeiras
    dados_financeiros = VendaController.calcular_financeiro()
    print(f"\nResumo Financeiro:")
    print(f"  Total Recebido: R$ {dados_financeiros['total_recebido']:.2f}")
    print(f"  Total a Receber: R$ {dados_financeiros['total_a_receber']:.2f}")
    print(f"  Número de Vendas: {dados_financeiros['numero_vendas']}")
    print(f"  Clientes Inadimplentes: {len(dados_financeiros['clientes_inadimplentes'])}")

def main():
    """Função principal da demonstração."""
    print("=== Demonstração do Sistema de Gerenciamento de Loja de Semijoias ===\n")
    
    try:
        demonstrar_cadastro_produtos()
        demonstrar_cadastro_clientes()
        demonstrar_registro_vendas()
        demonstrar_relatorios()
        
        print("\n=== Demonstração Concluída ===")
        print(" Todas as funcionalidades foram demonstradas com sucesso!")
        print("\nVocê pode agora:")
        print("1. Executar 'python main.py' para abrir a interface gráfica")
        print("2. Ver os relatórios gerados na pasta 'relatorios/'")
        print("3. Consultar o banco de dados 'loja_semijoias.db'")
        
    except Exception as e:
        print(f"\n❌ Erro durante a demonstração: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
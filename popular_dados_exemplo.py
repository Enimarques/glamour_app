#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para popular o banco de dados com dados de exemplo para testes.
"""

from models.produto import Produto
from models.cliente import Cliente
from controllers.produto_controller import ProdutoController
from controllers.cliente_controller import ClienteController
# VendaController will be imported when needed

def popular_produtos_exemplo():
    """Popula o banco de dados com produtos de exemplo."""
    print("Inserindo produtos de exemplo...")
    
    # Produtos de exemplo
    produtos_exemplo = [
        {
            "nome": "Colar de Prata com Pedras",
            "categoria": "Semijoias",
            "preco_custo": 45.00,
            "preco_venda": 89.90,
            "quantidade": 15
        },
        {
            "nome": "Brinco de Argola Média",
            "categoria": "Semijoias",
            "preco_custo": 22.50,
            "preco_venda": 45.00,
            "quantidade": 8
        },
        {
            "nome": "Pulseira de Couro Feminina",
            "categoria": "Acessórios",
            "preco_custo": 30.00,
            "preco_venda": 59.90,
            "quantidade": 12
        },
        {
            "nome": "Relógio Digital Esportivo",
            "categoria": "Relógios",
            "preco_custo": 85.00,
            "preco_venda": 149.90,
            "quantidade": 5
        },
        {
            "nome": "Anel de Prata com Zircônia",
            "categoria": "Semijoias",
            "preco_custo": 38.00,
            "preco_venda": 75.00,
            "quantidade": 3
        }
    ]
    
    # Insere os produtos
    for dados_produto in produtos_exemplo:
        produto = ProdutoController.criar_produto(**dados_produto)
        print(f"Produto inserido: {produto.nome} (ID: {produto.id})")
        
def popular_clientes_exemplo():
    """Popula o banco de dados com clientes de exemplo."""
    print("\nInserindo clientes de exemplo...")
    
    # Clientes de exemplo
    clientes_exemplo = [
        {
            "nome": "Maria Silva",
            "telefone": "(11) 98765-4321",
            "observacoes": "Cliente frequente, prefere semijoias"
        },
        {
            "nome": "João Santos",
            "telefone": "(11) 91234-5678",
            "observacoes": "Comprou relógio recentemente"
        },
        {
            "nome": "Ana Oliveira",
            "telefone": "(11) 99876-5432",
            "observacoes": "Interesse em pulseiras"
        }
    ]
    
    # Insere os clientes
    for dados_cliente in clientes_exemplo:
        cliente = ClienteController.criar_cliente(**dados_cliente)
        print(f"Cliente inserido: {cliente.nome} (ID: {cliente.id})")
        
def popular_vendas_exemplo():
    """Popula o banco de dados com vendas de exemplo."""
    print("\nInserindo vendas de exemplo...")
    
    # Para esta demonstração, vamos apenas mostrar como seria feito
    # Na prática, você precisaria obter os IDs reais dos produtos e clientes
    print("Exemplo de como registrar uma venda:")
    print("- Obter IDs dos produtos e clientes")
    print("- Criar itens da venda")
    print("- Registrar a venda através do VendaController")

def main():
    """Função principal."""
    print("=== Script para Popular Dados de Exemplo ===\n")
    
    try:
        popular_produtos_exemplo()
        popular_clientes_exemplo()
        popular_vendas_exemplo()
        
        print("\n=== Finalizado ===")
        print("Dados de exemplo inseridos com sucesso!")
        
    except Exception as e:
        print(f"\nErro ao inserir dados de exemplo: {e}")

if __name__ == "__main__":
    main()
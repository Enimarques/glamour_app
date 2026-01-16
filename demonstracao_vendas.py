#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demonstração das funcionalidades do módulo de vendas.
"""

from controllers.venda_controller import VendaController
from controllers.produto_controller import ProdutoController
from controllers.cliente_controller import ClienteController
import sys

def demonstrar_registro_venda():
    """Demonstra o registro de uma venda."""
    print("=== Demonstração: Registro de Venda ===")
    
    try:
        # Obter produtos e clientes existentes
        produtos = ProdutoController.listar_produtos()
        clientes = ClienteController.listar_clientes()
        
        if not produtos:
            print("⚠ Nenhum produto cadastrado. Criando produtos de exemplo...")
            # Criar alguns produtos de exemplo
            produto1 = ProdutoController.criar_produto(
                nome="Colar de Prata",
                categoria="Semijoias",
                preco_custo=45.00,
                preco_venda=89.90,
                quantidade=10
            )
            produto2 = ProdutoController.criar_produto(
                nome="Brinco de Ouro",
                categoria="Semijoias",
                preco_custo=35.00,
                preco_venda=69.90,
                quantidade=5
            )
            produtos = [produto1, produto2]
            print(f"✓ Produtos criados: {produto1.nome}, {produto2.nome}")
            
        if not clientes:
            print("⚠ Nenhum cliente cadastrado. Criando cliente de exemplo...")
            # Criar um cliente de exemplo
            cliente = ClienteController.criar_cliente(
                nome="Cliente Exemplo",
                telefone="(11) 99999-9999",
                observacoes="Cliente para demonstração"
            )
            clientes = [cliente]
            print(f"✓ Cliente criado: {cliente.nome}")
            
        # Preparar itens para a venda
        itens_venda = [
            {
                "produto_id": produtos[0].id,
                "quantidade": 2,
                "preco_unitario": produtos[0].preco_venda
            }
        ]
        
        if len(produtos) > 1:
            itens_venda.append({
                "produto_id": produtos[1].id,
                "quantidade": 1,
                "preco_unitario": produtos[1].preco_venda
            })
        
        # Registrar venda à vista
        venda_avista = VendaController.criar_venda(
            cliente_id=clientes[0].id if clientes else None,
            itens=itens_venda,
            tipo_pagamento="avista"
        )
        
        if venda_avista:
            print(f"✓ Venda à vista registrada com sucesso (ID: {venda_avista.id})")
            print(f"  Valor total: R$ {venda_avista.valor_total:.2f}")
            print(f"  Status: {venda_avista.status}")
            print("  Itens:")
            for item in venda_avista.itens:
                produto = ProdutoController.obter_produto(item.produto_id)
                if produto:
                    print(f"    - {produto.nome}: {item.quantidade} x R$ {item.preco_unitario:.2f}")
        else:
            print("✗ Falha ao registrar venda à vista")
            
        # Registrar venda fiado
        venda_fiado = VendaController.criar_venda(
            cliente_id=clientes[0].id if clientes else None,
            itens=[itens_venda[0]],  # Apenas o primeiro item
            tipo_pagamento="fiado"
        )
        
        if venda_fiado:
            print(f"\n✓ Venda fiado registrada com sucesso (ID: {venda_fiado.id})")
            print(f"  Valor total: R$ {venda_fiado.valor_total:.2f}")
            print(f"  Status: {venda_fiado.status}")
            print("  Itens:")
            for item in venda_fiado.itens:
                produto = ProdutoController.obter_produto(item.produto_id)
                if produto:
                    print(f"    - {produto.nome}: {item.quantidade} x R$ {item.preco_unitario:.2f}")
        else:
            print("✗ Falha ao registrar venda fiado")
            
    except Exception as e:
        print(f"✗ Erro durante o registro de venda: {e}")
        import traceback
        traceback.print_exc()

def demonstrar_listagem_vendas():
    """Demonstra a listagem de vendas."""
    print("\n=== Demonstração: Listagem de Vendas ===")
    
    try:
        vendas = VendaController.listar_vendas()
        print(f"✓ Total de vendas registradas: {len(vendas)}")
        
        if vendas:
            print("\nÚltimas 3 vendas:")
            for venda in vendas[:3]:
                cliente_nome = venda.cliente.nome if venda.cliente else "Não informado"
                tipo = "Fiado" if venda.tipo_pagamento == "fiado" else "À Vista"
                print(f"  ID: {venda.id} | Cliente: {cliente_nome} | "
                      f"Valor: R$ {venda.valor_total:.2f} | Tipo: {tipo} | "
                      f"Status: {venda.status}")
        else:
            print("Nenhuma venda registrada.")
            
    except Exception as e:
        print(f"✗ Erro ao listar vendas: {e}")

def demonstrar_calculo_financeiro():
    """Demonstra o cálculo financeiro."""
    print("\n=== Demonstração: Cálculo Financeiro ===")
    
    try:
        dados_financeiros = VendaController.calcular_financeiro()
        print("✓ Cálculo financeiro realizado com sucesso")
        print(f"  Total Recebido: R$ {dados_financeiros['total_recebido']:.2f}")
        print(f"  Total a Receber: R$ {dados_financeiros['total_a_receber']:.2f}")
        print(f"  Número de Vendas: {dados_financeiros['numero_vendas']}")
        print(f"  Clientes Inadimplentes: {len(dados_financeiros['clientes_inadimplentes'])}")
        
    except Exception as e:
        print(f"✗ Erro no cálculo financeiro: {e}")

def main():
    """Função principal da demonstração."""
    print("=== Demonstração do Módulo de Vendas ===\n")
    
    try:
        demonstrar_registro_venda()
        demonstrar_listagem_vendas()
        demonstrar_calculo_financeiro()
        
        print("\n=== Demonstração Concluída ===")
        print("Todas as funcionalidades do módulo de vendas foram demonstradas com sucesso!")
        print("\nVocê pode agora:")
        print("1. Executar 'python main.py' para abrir a interface gráfica")
        print("2. Navegar até a aba 'Vendas' para usar a interface completa")
        
    except Exception as e:
        print(f"\n❌ Erro durante a demonstração: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
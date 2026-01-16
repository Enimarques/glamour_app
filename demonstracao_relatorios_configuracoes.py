#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demonstração das funcionalidades dos módulos de relatórios e configurações.
"""

import sys
import os
from datetime import datetime, timedelta

def demonstrar_relatorios():
    """Demonstra a geração de relatórios."""
    print("=== Demonstração: Geração de Relatórios ===")
    
    try:
        from reports.relatorio_financeiro import RelatorioFinanceiro
        from reports.catalogo_produtos import CatalogoProdutos
        
        # Criar diretório de relatórios se não existir
        if not os.path.exists("relatorios"):
            os.makedirs("relatorios")
        
        # Gerar relatório financeiro simplificado
        print("Gerando relatório financeiro simplificado...")
        caminho_relatorio = RelatorioFinanceiro.gerar_relatorio_simplificado(
            "relatorios/demonstracao_financeiro_simples.pdf"
        )
        print(f"✓ Relatório financeiro simplificado gerado: {caminho_relatorio}")
        
        # Gerar catálogo de produtos
        print("Gerando catálogo de produtos...")
        caminho_catalogo = CatalogoProdutos.gerar_catalogo_simples(
            "relatorios/demonstracao_catalogo_simples.pdf"
        )
        print(f"✓ Catálogo de produtos gerado: {caminho_catalogo}")
        
        print("\n✅ Demonstração de relatórios concluída com sucesso!\n")
        
    except Exception as e:
        print(f"✗ Erro na demonstração de relatórios: {str(e)}\n")
        
def demonstrar_configuracoes():
    """Demonstra o funcionamento das configurações."""
    print("=== Demonstração: Configurações do Sistema ===")
    
    try:
        from PyQt5.QtCore import QSettings
        
        # Criar configurações de exemplo
        configuracoes = QSettings("JoiaSystem", "SistemaLojaSemijoias")
        
        # Salvar algumas configurações de exemplo
        configuracoes.setValue("nome_loja", "Joia System Demo")
        configuracoes.setValue("telefone", "(11) 99999-9999")
        configuracoes.setValue("endereco", "Rua Exemplo, 123 - São Paulo/SP")
        configuracoes.setValue("diretorio_backup", "./backups")
        configuracoes.setValue("frequencia_backup", "Semanal")
        
        print("✓ Configurações de exemplo salvas com sucesso")
        
        # Ler as configurações salvas
        nome_loja = configuracoes.value("nome_loja", "Não definido")
        telefone = configuracoes.value("telefone", "Não definido")
        endereco = configuracoes.value("endereco", "Não definido")
        
        print(f"Nome da loja: {nome_loja}")
        print(f"Telefone: {telefone}")
        print(f"Endereço: {endereco}")
        
        print("\n✅ Demonstração de configurações concluída com sucesso!\n")
        
    except Exception as e:
        print(f"✗ Erro na demonstração de configurações: {str(e)}\n")

def main():
    """Função principal de demonstração."""
    print("Sistema de Gerenciamento de Loja de Semijoias")
    print("=" * 50)
    print("Demonstração dos módulos de relatórios e configurações\n")
    
    demonstrar_relatorios()
    demonstrar_configuracoes()
    
    print("🎉 Todas as demonstrações foram concluídas!")
    print("\nOs módulos de relatórios e configurações estão prontos para uso no sistema.")

if __name__ == "__main__":
    main()
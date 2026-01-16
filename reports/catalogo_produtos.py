from reports.relatorio_pdf import GeradorRelatorioPDF
from models.produto import Produto
from controllers.produto_controller import ProdutoController
import os

class CatalogoProdutos:
    """Classe para geração do catálogo de produtos em PDF."""
    
    @staticmethod
    def gerar_catalogo(caminho_arquivo: str = "relatorios/catalogo_produtos.pdf") -> str:
        """
        Gera o catálogo de produtos em PDF.
        
        Args:
            caminho_arquivo (str): Caminho onde o arquivo PDF será salvo
            
        Returns:
            str: Caminho do arquivo PDF gerado
        """
        # Certifica-se de que o diretório existe
        diretorio = os.path.dirname(caminho_arquivo)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)
            
        # Cria o gerador de PDF
        pdf = GeradorRelatorioPDF(caminho_arquivo)
        
        # Adiciona título
        pdf.adicionar_titulo("CATÁLOGO DE PRODUTOS")
        
        # Obtém todos os produtos
        produtos = ProdutoController.listar_produtos()
        
        if not produtos:
            pdf.adicionar_paragrafo("Nenhum produto cadastrado.")
        else:
            # Cria tabela com os produtos
            cabecalhos = ["Código", "Nome", "Categoria", "Preço"]
            dados = []
            
            for produto in produtos:
                linha = [
                    str(produto.id),
                    produto.nome,
                    produto.categoria,
                    f"R$ {produto.preco_venda:.2f}"
                ]
                dados.append(linha)
                
            pdf.adicionar_tabela(dados, cabecalhos)
            
        # Adiciona rodapé
        pdf.adicionar_rodape()
        
        # Gera o PDF
        return pdf.gerar()
        
    @staticmethod
    def gerar_catalogo_simples(caminho_arquivo: str = "relatorios/catalogo_simples.pdf") -> str:
        """
        Gera um catálogo simples de produtos em PDF (sem formatação de tabela).
        
        Args:
            caminho_arquivo (str): Caminho onde o arquivo PDF será salvo
            
        Returns:
            str: Caminho do arquivo PDF gerado
        """
        # Certifica-se de que o diretório existe
        diretorio = os.path.dirname(caminho_arquivo)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)
            
        # Cria o gerador de PDF
        pdf = GeradorRelatorioPDF(caminho_arquivo)
        
        # Adiciona título
        pdf.adicionar_titulo("CATÁLOGO DE PRODUTOS")
        
        # Obtém todos os produtos
        produtos = ProdutoController.listar_produtos()
        
        if not produtos:
            pdf.adicionar_paragrafo("Nenhum produto cadastrado.")
        else:
            # Adiciona cada produto como um parágrafo
            for i, produto in enumerate(produtos, 1):
                texto_produto = (
                    f"{i}. {produto.nome} ({produto.categoria}) - "
                    f"R$ {produto.preco_venda:.2f}"
                )
                pdf.adicionar_paragrafo(texto_produto)
                
        # Adiciona rodapé
        pdf.adicionar_rodape()
        
        # Gera o PDF
        return pdf.gerar()
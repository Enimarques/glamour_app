from typing import List, Optional
from models.produto import Produto

class ProdutoController:
    """Controlador para gerenciar operações relacionadas a produtos."""
    
    @staticmethod
    def criar_produto(nome: str, categoria: str, preco_custo: float, 
                     preco_venda: float, quantidade: int, caminho_imagem: str = None) -> Produto:
        """
        Cria um novo produto.
        
        Args:
            nome (str): Nome do produto
            categoria (str): Categoria do produto
            preco_custo (float): Preço de custo
            preco_venda (float): Preço de venda
            quantidade (int): Quantidade em estoque
            caminho_imagem (str, opcional): Caminho para a imagem do produto
            
        Returns:
            Produto: Produto criado
        """
        produto = Produto(
            nome=nome,
            categoria=categoria,
            preco_custo=preco_custo,
            preco_venda=preco_venda,
            quantidade=quantidade,
            caminho_imagem=caminho_imagem
        )
        produto.salvar()
        return produto
    
    @staticmethod
    def atualizar_produto(produto_id: int, nome: str = None, categoria: str = None,
                         preco_custo: float = None, preco_venda: float = None,
                         quantidade: int = None, caminho_imagem: str = None) -> Optional[Produto]:
        """
        Atualiza um produto existente.
        
        Args:
            produto_id (int): ID do produto a ser atualizado
            nome (str, opcional): Novo nome do produto
            categoria (str, opcional): Nova categoria do produto
            preco_custo (float, opcional): Novo preço de custo
            preco_venda (float, opcional): Novo preço de venda
            quantidade (int, opcional): Nova quantidade em estoque
            caminho_imagem (str, opcional): Novo caminho para a imagem do produto
            
        Returns:
            Produto ou None: Produto atualizado ou None se não encontrado
        """
        produto = Produto.obter_por_id(produto_id)
        if not produto:
            return None
            
        if nome is not None:
            produto.nome = nome
        if categoria is not None:
            produto.categoria = categoria
        if preco_custo is not None:
            produto.preco_custo = preco_custo
        if preco_venda is not None:
            produto.preco_venda = preco_venda
        if quantidade is not None:
            produto.quantidade = quantidade
        if caminho_imagem is not None:
            produto.caminho_imagem = caminho_imagem
            
        produto.salvar()
        return produto
    
    @staticmethod
    def excluir_produto(produto_id: int) -> bool:
        """
        Exclui um produto.
        
        Args:
            produto_id (int): ID do produto a ser excluído
            
        Returns:
            bool: True se bem sucedido, False caso contrário
        """
        produto = Produto.obter_por_id(produto_id)
        if not produto:
            return False
        return produto.excluir()
    
    @staticmethod
    def obter_produto(produto_id: int) -> Optional[Produto]:
        """
        Obtém um produto pelo ID.
        
        Args:
            produto_id (int): ID do produto
            
        Returns:
            Produto ou None: Produto encontrado ou None se não encontrado
        """
        return Produto.obter_por_id(produto_id)
    
    @staticmethod
    def listar_produtos() -> List[Produto]:
        """
        Lista todos os produtos.
        
        Returns:
            List[Produto]: Lista de todos os produtos
        """
        return Produto.obter_todos()
    
    @staticmethod
    def buscar_produtos(nome: str) -> List[Produto]:
        """
        Busca produtos pelo nome.
        
        Args:
            nome (str): Nome ou parte do nome do produto
            
        Returns:
            List[Produto]: Lista de produtos encontrados
        """
        return Produto.buscar_por_nome(nome)
    
    @staticmethod
    def verificar_estoque_baixo(limite: int = 5) -> List[Produto]:
        """
        Verifica produtos com estoque baixo.
        
        Args:
            limite (int): Limite de quantidade para considerar estoque baixo
            
        Returns:
            List[Produto]: Lista de produtos com estoque baixo
        """
        todos_produtos = Produto.obter_todos()
        return [produto for produto in todos_produtos if produto.quantidade <= limite]
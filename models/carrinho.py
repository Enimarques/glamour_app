from dataclasses import dataclass
from typing import Dict
from models.produto import Produto

@dataclass
class ItemCarrinho:
    """Representa um item no carrinho de compras."""
    produto: Produto
    quantidade: int
    
    @property
    def subtotal(self) -> float:
        """Calcula o subtotal do item."""
        return self.produto.preco_venda * self.quantidade

class CarrinhoCompras:
    """Representa um carrinho de compras."""
    
    def __init__(self):
        self.itens: Dict[int, ItemCarrinho] = {}  # produto_id -> ItemCarrinho
    
    def adicionar_item(self, produto: Produto, quantidade: int = 1):
        """Adiciona um item ao carrinho."""
        if produto.id in self.itens:
            self.itens[produto.id].quantidade += quantidade
        else:
            self.itens[produto.id] = ItemCarrinho(produto, quantidade)
    
    def remover_item(self, produto_id: int):
        """Remove um item do carrinho."""
        if produto_id in self.itens:
            del self.itens[produto_id]
    
    def atualizar_quantidade(self, produto_id: int, quantidade: int):
        """Atualiza a quantidade de um item no carrinho."""
        if quantidade <= 0:
            self.remover_item(produto_id)
        elif produto_id in self.itens:
            self.itens[produto_id].quantidade = quantidade
    
    def limpar(self):
        """Limpa o carrinho."""
        self.itens.clear()
    
    @property
    def total(self) -> float:
        """Calcula o total do carrinho."""
        return sum(item.subtotal for item in self.itens.values())
    
    @property
    def quantidade_itens(self) -> int:
        """Retorna a quantidade total de itens no carrinho."""
        return sum(item.quantidade for item in self.itens.values())
    
    def obter_itens(self) -> list[ItemCarrinho]:
        """Retorna uma lista com todos os itens do carrinho."""
        return list(self.itens.values())
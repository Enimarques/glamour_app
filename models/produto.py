from dataclasses import dataclass
from typing import Optional
import sqlite3
from database.db_manager import gerenciador_bd

@dataclass
class Produto:
    """Representa um produto na loja de semijoias."""
    id: Optional[int] = None
    nome: str = ""
    categoria: str = ""
    preco_custo: float = 0.0
    preco_venda: float = 0.0
    quantidade: int = 0
    caminho_imagem: Optional[str] = None
    
    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'Produto':
        """Cria uma instância de Produto a partir de uma linha do banco de dados."""
        return cls(
            id=row['id'],
            nome=row['nome'],
            categoria=row['categoria'],
            preco_custo=row['preco_custo'],
            preco_venda=row['preco_venda'],
            quantidade=row['quantidade'],
            caminho_imagem=row['caminho_imagem']
        )
    
    def salvar(self) -> bool:
        """
        Salva o produto no banco de dados.
        
        Returns:
            bool: True se bem sucedido, False caso contrário
        """
        try:
            if self.id is None:
                # Insere novo produto
                consulta = '''
                    INSERT INTO produtos (nome, categoria, preco_custo, preco_venda, quantidade, caminho_imagem)
                    VALUES (?, ?, ?, ?, ?, ?)
                '''
                cursor = gerenciador_bd.executar_consulta(consulta, (
                    self.nome, self.categoria, self.preco_custo, 
                    self.preco_venda, self.quantidade, self.caminho_imagem
                ))
                self.id = cursor.lastrowid
            else:
                # Atualiza produto existente
                consulta = '''
                    UPDATE produtos 
                    SET nome=?, categoria=?, preco_custo=?, preco_venda=?, quantidade=?, caminho_imagem=?, atualizado_em=CURRENT_TIMESTAMP
                    WHERE id=?
                '''
                gerenciador_bd.executar_consulta(consulta, (
                    self.nome, self.categoria, self.preco_custo, 
                    self.preco_venda, self.quantidade, self.caminho_imagem, self.id
                ))
            return True
        except Exception as e:
            print(f"Erro ao salvar produto: {e}")
            return False
    
    def excluir(self) -> bool:
        """
        Exclui o produto do banco de dados.
        
        Returns:
            bool: True se bem sucedido, False caso contrário
        """
        try:
            if self.id is not None:
                consulta = "DELETE FROM produtos WHERE id=?"
                gerenciador_bd.executar_consulta(consulta, (self.id,))
                self.id = None
                return True
            return False
        except Exception as e:
            print(f"Erro ao excluir produto: {e}")
            return False
    
    @staticmethod
    def obter_por_id(produto_id: int) -> Optional['Produto']:
        """
        Recupera um produto pelo seu ID.
        
        Args:
            produto_id (int): O ID do produto
            
        Returns:
            Produto ou None: Instância de Produto ou None se não encontrado
        """
        consulta = "SELECT * FROM produtos WHERE id=?"
        row = gerenciador_bd.buscar_um(consulta, (produto_id,))
        if row:
            return Produto.from_row(row)
        return None
    
    @staticmethod
    def obter_todos() -> list['Produto']:
        """
        Recupera todos os produtos.
        
        Returns:
            list[Produto]: Lista de todos os produtos
        """
        consulta = "SELECT * FROM produtos ORDER BY nome"
        rows = gerenciador_bd.buscar_todos(consulta)
        return [Produto.from_row(row) for row in rows]
    
    @staticmethod
    def buscar_por_nome(nome: str) -> list['Produto']:
        """
        Busca produtos pelo nome.
        
        Args:
            nome (str): Nome do produto a ser buscado
            
        Returns:
            list[Produto]: Lista de produtos correspondentes
        """
        consulta = "SELECT * FROM produtos WHERE nome LIKE ? ORDER BY nome"
        rows = gerenciador_bd.buscar_todos(consulta, (f"%{nome}%",))
        return [Produto.from_row(row) for row in rows]
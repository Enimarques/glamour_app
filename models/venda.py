from dataclasses import dataclass
from typing import Optional, List
import sqlite3
from datetime import datetime
from database.db_manager import gerenciador_bd
from models.produto import Produto
from models.cliente import Cliente

@dataclass
class ItemVenda:
    """Representa um item em uma venda."""
    id: Optional[int] = None
    venda_id: Optional[int] = None
    produto_id: int = 0
    quantidade: int = 0
    preco_unitario: float = 0.0
    produto: Optional[Produto] = None  # Para conveniência, não armazenado no BD
    
    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'ItemVenda':
        """Cria uma instância de ItemVenda a partir de uma linha do banco de dados."""
        return cls(
            id=row['id'],
            venda_id=row['venda_id'],
            produto_id=row['produto_id'],
            quantidade=row['quantidade'],
            preco_unitario=row['preco_unitario']
        )

@dataclass
class Venda:
    """Representa uma transação de venda na loja de semijoias."""
    id: Optional[int] = None
    cliente_id: Optional[int] = None
    valor_total: float = 0.0
    tipo_pagamento: str = "Dinheiro"  # Tipos: 'Dinheiro', 'Cartão Crédito', 'Cartão Débito', 'PIX', 'Parcelado Boleto', 'Parcelado Promissória'
    status: str = "pago"  # 'pago' ou 'pendente'
    data_venda: Optional[datetime] = None
    dia_vencimento: Optional[int] = None  # Dia do mês para vencimento (para vendas parceladas)
    observacoes: Optional[str] = None
    itens: List[ItemVenda] = None
    cliente: Optional[Cliente] = None  # Para conveniência, não armazenado no BD
    
    def __post_init__(self):
        if self.itens is None:
            self.itens = []
        if self.data_venda is None:
            self.data_venda = datetime.now()
    
    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'Venda':
        """Cria uma instância de Venda a partir de uma linha do banco de dados."""
        data_venda = datetime.fromisoformat(row['data_venda']) if row['data_venda'] else None
        # Obter dia de vencimento e observações se existirem
        keys = row.keys()
        dia_vencimento = row['dia_vencimento'] if 'dia_vencimento' in keys and row['dia_vencimento'] else None
        observacoes = row['observacoes'] if 'observacoes' in keys else None
        
        return cls(
            id=row['id'],
            cliente_id=row['cliente_id'],
            valor_total=row['valor_total'],
            tipo_pagamento=row['tipo_pagamento'],
            status=row['status'],
            data_venda=data_venda,
            dia_vencimento=dia_vencimento,
            observacoes=observacoes
        )
    
    def salvar(self) -> bool:
        """
        Salva a venda no banco de dados.
        
        Returns:
            bool: True se bem sucedido, False caso contrário
        """
        try:
            if self.id is None:
                # Insere nova venda
                query = '''
                    INSERT INTO vendas (cliente_id, valor_total, tipo_pagamento, status, data_venda, dia_vencimento, observacoes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                '''
                cursor = gerenciador_bd.executar_consulta(query, (
                    self.cliente_id, self.valor_total, self.tipo_pagamento, 
                    self.status, self.data_venda.isoformat(), self.dia_vencimento, self.observacoes
                ))
                self.id = cursor.lastrowid
                
                # Salva itens da venda
                for item in self.itens:
                    item.venda_id = self.id
                    self._salvar_item_venda(item)
            else:
                # Atualiza venda existente
                query = '''
                    UPDATE vendas 
                    SET cliente_id=?, valor_total=?, tipo_pagamento=?, status=?, data_venda=?, dia_vencimento=?, observacoes=?
                    WHERE id=?
                '''
                gerenciador_bd.executar_consulta(query, (
                    self.cliente_id, self.valor_total, self.tipo_pagamento, 
                    self.status, self.data_venda.isoformat(), self.dia_vencimento, self.observacoes, self.id
                ))
                
                # Para simplificar neste MVP, não atualizaremos os itens da venda
                # Numa implementação completa, trataríamos atualizações/exclusões adequadamente
            return True
        except Exception as e:
            print(f"Erro ao salvar venda: {e}")
            return False
    
    def _salvar_item_venda(self, item: ItemVenda) -> bool:
        """
        Salva um item de venda no banco de dados.
        
        Args:
            item (ItemVenda): O item de venda a ser salvo
            
        Returns:
            bool: True se bem sucedido, False caso contrário
        """
        try:
            query = '''
                INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario)
                VALUES (?, ?, ?, ?)
            '''
            cursor = gerenciador_bd.executar_consulta(query, (
                item.venda_id, item.produto_id, item.quantidade, item.preco_unitario
            ))
            item.id = cursor.lastrowid
            return True
        except Exception as e:
            print(f"Erro ao salvar item de venda: {e}")
            return False
    
    def excluir(self) -> bool:
        """
        Exclui a venda do banco de dados.
        
        Returns:
            bool: True se bem sucedido, False caso contrário
        """
        try:
            if self.id is not None:
                # Exclui itens da venda primeiro
                query = "DELETE FROM itens_venda WHERE venda_id=?"
                gerenciador_bd.executar_consulta(query, (self.id,))
                
                # Exclui a venda
                query = "DELETE FROM vendas WHERE id=?"
                gerenciador_bd.executar_consulta(query, (self.id,))
                self.id = None
                return True
            return False
        except Exception as e:
            print(f"Erro ao excluir venda: {e}")
            return False
    
    @staticmethod
    def obter_por_id(venda_id: int) -> Optional['Venda']:
        """
        Recupera uma venda pelo seu ID.
        
        Args:
            venda_id (int): O ID da venda
            
        Returns:
            Venda ou None: Instância de Venda ou None se não encontrado
        """
        query = "SELECT * FROM vendas WHERE id=?"
        row = gerenciador_bd.buscar_um(query, (venda_id,))
        if row:
            venda = Venda.from_row(row)
            # Carrega itens associados
            venda.itens = Venda.obter_itens_venda(venda_id)
            # Carrega cliente associado se existir
            if venda.cliente_id:
                venda.cliente = Cliente.obter_por_id(venda.cliente_id)
            return venda
        return None
    
    @staticmethod
    def obter_itens_venda(venda_id: int) -> List[ItemVenda]:
        """
        Recupera todos os itens de uma venda.
        
        Args:
            venda_id (int): O ID da venda
            
        Returns:
            List[ItemVenda]: Lista de itens da venda
        """
        query = "SELECT * FROM itens_venda WHERE venda_id=?"
        rows = gerenciador_bd.buscar_todos(query, (venda_id,))
        itens = [ItemVenda.from_row(row) for row in rows]
        
        # Carrega informações do produto para cada item
        for item in itens:
            item.produto = Produto.obter_por_id(item.produto_id)
            
        return itens
    
    @staticmethod
    def obter_todas() -> list['Venda']:
        """
        Recupera todas as vendas.
        
        Returns:
            list[Venda]: Lista de todas as vendas
        """
        query = "SELECT * FROM vendas ORDER BY data_venda DESC"
        rows = gerenciador_bd.buscar_todos(query)
        vendas = [Venda.from_row(row) for row in rows]
        
        # Carrega itens e clientes associados
        for venda in vendas:
            venda.itens = Venda.obter_itens_venda(venda.id)
            if venda.cliente_id:
                venda.cliente = Cliente.obter_por_id(venda.cliente_id)
                
        return vendas
    
    @staticmethod
    def obter_vendas_pendentes() -> list['Venda']:
        """
        Recupera todas as vendas pendentes (vendas parceladas ainda não pagas).
        
        Returns:
            list[Venda]: Lista de vendas pendentes
        """
        query = "SELECT * FROM vendas WHERE status='pendente' ORDER BY data_venda DESC"
        rows = gerenciador_bd.buscar_todos(query)
        vendas = [Venda.from_row(row) for row in rows]
        
        # Carrega itens e clientes associados
        for venda in vendas:
            venda.itens = Venda.obter_itens_venda(venda.id)
            if venda.cliente_id:
                venda.cliente = Cliente.obter_por_id(venda.cliente_id)
                
        return vendas
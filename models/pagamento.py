from dataclasses import dataclass
from typing import Optional, List
import sqlite3
from datetime import datetime
from database.db_manager import gerenciador_bd
from models.venda import Venda

@dataclass
class Pagamento:
    """Representa um pagamento de uma venda fiado."""
    id: Optional[int] = None
    venda_id: int = 0
    valor: float = 0.0
    data_pagamento: Optional[datetime] = None
    observacoes: Optional[str] = None
    venda: Optional[Venda] = None  # Para conveniência, não armazenado no BD
    
    def __post_init__(self):
        if self.data_pagamento is None:
            self.data_pagamento = datetime.now()
    
    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'Pagamento':
        """Cria uma instância de Pagamento a partir de uma linha do banco de dados."""
        data_pagamento = datetime.fromisoformat(row['data_pagamento']) if row['data_pagamento'] else None
        return cls(
            id=row['id'],
            venda_id=row['venda_id'],
            valor=row['valor'],
            data_pagamento=data_pagamento,
            observacoes=row['observacoes']
        )
    
    def salvar(self) -> bool:
        """
        Salva o pagamento no banco de dados.
        
        Returns:
            bool: True se bem sucedido, False caso contrário
        """
        try:
            if self.id is None:
                # Insere novo pagamento
                query = '''
                    INSERT INTO pagamentos (venda_id, valor, data_pagamento, observacoes)
                    VALUES (?, ?, ?, ?)
                '''
                cursor = gerenciador_bd.executar_consulta(query, (
                    self.venda_id, self.valor, 
                    self.data_pagamento.isoformat(), self.observacoes
                ))
                self.id = cursor.lastrowid
            else:
                # Atualiza pagamento existente
                query = '''
                    UPDATE pagamentos 
                    SET venda_id=?, valor=?, data_pagamento=?, observacoes=?
                    WHERE id=?
                '''
                gerenciador_bd.executar_consulta(query, (
                    self.venda_id, self.valor, 
                    self.data_pagamento.isoformat(), self.observacoes, self.id
                ))
            return True
        except Exception as e:
            print(f"Erro ao salvar pagamento: {e}")
            return False
    
    def excluir(self) -> bool:
        """
        Exclui o pagamento do banco de dados.
        
        Returns:
            bool: True se bem sucedido, False caso contrário
        """
        try:
            if self.id is not None:
                query = "DELETE FROM pagamentos WHERE id=?"
                gerenciador_bd.executar_consulta(query, (self.id,))
                self.id = None
                return True
            return False
        except Exception as e:
            print(f"Erro ao excluir pagamento: {e}")
            return False
    
    @staticmethod
    def obter_por_id(pagamento_id: int) -> Optional['Pagamento']:
        """
        Recupera um pagamento pelo seu ID.
        
        Args:
            pagamento_id (int): O ID do pagamento
            
        Returns:
            Pagamento ou None: Instância de Pagamento ou None se não encontrado
        """
        query = "SELECT * FROM pagamentos WHERE id=?"
        row = gerenciador_bd.buscar_um(query, (pagamento_id,))
        if row:
            pagamento = Pagamento.from_row(row)
            # Carrega venda associada se existir
            if pagamento.venda_id:
                pagamento.venda = Venda.obter_por_id(pagamento.venda_id)
            return pagamento
        return None
    
    @staticmethod
    def obter_por_venda(venda_id: int) -> List['Pagamento']:
        """
        Recupera todos os pagamentos de uma venda.
        
        Args:
            venda_id (int): O ID da venda
            
        Returns:
            List[Pagamento]: Lista de pagamentos da venda
        """
        query = "SELECT * FROM pagamentos WHERE venda_id=? ORDER BY data_pagamento DESC"
        rows = gerenciador_bd.buscar_todos(query, (venda_id,))
        pagamentos = [Pagamento.from_row(row) for row in rows]
        
        # Carrega venda associada para cada pagamento
        for pagamento in pagamentos:
            if pagamento.venda_id:
                pagamento.venda = Venda.obter_por_id(pagamento.venda_id)
                
        return pagamentos
    
    @staticmethod
    def obter_todos() -> List['Pagamento']:
        """
        Recupera todos os pagamentos.
        
        Returns:
            List[Pagamento]: Lista de todos os pagamentos
        """
        query = "SELECT * FROM pagamentos ORDER BY data_pagamento DESC"
        rows = gerenciador_bd.buscar_todos(query)
        pagamentos = [Pagamento.from_row(row) for row in rows]
        
        # Carrega vendas associadas
        for pagamento in pagamentos:
            if pagamento.venda_id:
                pagamento.venda = Venda.obter_por_id(pagamento.venda_id)
                
        return pagamentos
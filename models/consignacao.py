from dataclasses import dataclass, field
from typing import Optional, List
import sqlite3
from database.db_manager import gerenciador_bd
from models.cliente import Cliente

@dataclass
class ItemConsignacao:
    """Representa um item de uma consignação."""
    id: Optional[int] = None
    consignacao_id: Optional[int] = None
    produto_id: int = 0
    qtd_enviada: int = 0
    qtd_vendida: int = 0
    qtd_devolvida: int = 0
    preco_unitario: float = 0.0
    comissao_percentual: float = 0.0
    
    # Propriedades calculadas/auxiliares
    produto_nome: str = ""  # Para exibição
    
    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'ItemConsignacao':
        item = cls(
            id=row['id'],
            consignacao_id=row['consignacao_id'],
            produto_id=row['produto_id'],
            qtd_enviada=row['qtd_enviada'],
            qtd_vendida=row['qtd_vendida'],
            qtd_devolvida=row['qtd_devolvida'],
            preco_unitario=row['preco_unitario'],
            comissao_percentual=row['comissao_percentual']
        )
        # Se a query fez JOIN com produtos, pega o nome
        keys = row.keys()
        if 'produto_nome' in keys:
            item.produto_nome = row['produto_nome']
        return item

    def salvar(self) -> bool:
        try:
            if self.id is None:
                consulta = '''
                    INSERT INTO itens_consignacao 
                    (consignacao_id, produto_id, qtd_enviada, qtd_vendida, qtd_devolvida, preco_unitario, comissao_percentual)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                '''
                cursor = gerenciador_bd.executar_consulta(consulta, (
                    self.consignacao_id, self.produto_id, self.qtd_enviada, 
                    self.qtd_vendida, self.qtd_devolvida, self.preco_unitario, self.comissao_percentual
                ))
                self.id = cursor.lastrowid
            else:
                consulta = '''
                    UPDATE itens_consignacao 
                    SET qtd_enviada=?, qtd_vendida=?, qtd_devolvida=?, preco_unitario=?, comissao_percentual=?
                    WHERE id=?
                '''
                gerenciador_bd.executar_consulta(consulta, (
                    self.qtd_enviada, self.qtd_vendida, self.qtd_devolvida, 
                    self.preco_unitario, self.comissao_percentual, self.id
                ))
            return True
        except Exception as e:
            print(f"Erro ao salvar item de consignação: {e}")
            return False

@dataclass
class Consignacao:
    """Representa uma consignação para revendedora."""
    id: Optional[int] = None
    cliente_id: int = 0
    data_envio: str = "" # Timestamp string
    status: str = "Aberta"
    data_fechamento: Optional[str] = None
    total_vendido: float = 0.0
    total_comissao: float = 0.0
    total_liquido: float = 0.0
    observacoes: Optional[str] = None
    
    # Relações
    itens: List[ItemConsignacao] = field(default_factory=list)
    cliente: Optional[Cliente] = None
    
    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'Consignacao':
        consig = cls(
            id=row['id'],
            cliente_id=row['cliente_id'],
            data_envio=row['data_envio'],
            status=row['status'],
            data_fechamento=row['data_fechamento'],
            total_vendido=row['total_vendido'],
            total_comissao=row['total_comissao'],
            total_liquido=row['total_liquido'],
            observacoes=row['observacoes']
        )
        keys = row.keys()
        if 'cliente_nome' in keys:
             # Cria objeto cliente parcial se houver dados do join
             consig.cliente = Cliente(id=row['cliente_id'], nome=row['cliente_nome'])
        return consig

    def salvar(self) -> bool:
        try:
            if self.id is None:
                consulta = '''
                    INSERT INTO consignacoes 
                    (cliente_id, data_envio, status, total_vendido, total_comissao, total_liquido, observacoes)
                    VALUES (?, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?)
                '''
                cursor = gerenciador_bd.executar_consulta(consulta, (
                    self.cliente_id, self.status, self.total_vendido, 
                    self.total_comissao, self.total_liquido, self.observacoes
                ))
                self.id = cursor.lastrowid
                
                # Salvar itens
                for item in self.itens:
                    item.consignacao_id = self.id
                    item.salvar()
            else:
                consulta = '''
                    UPDATE consignacoes 
                    SET status=?, data_fechamento=?, total_vendido=?, total_comissao=?, total_liquido=?, observacoes=?, atualizado_em=CURRENT_TIMESTAMP
                    WHERE id=?
                '''
                gerenciador_bd.executar_consulta(consulta, (
                    self.status, self.data_fechamento, self.total_vendido, 
                    self.total_comissao, self.total_liquido, self.observacoes, self.id
                ))
                # Itens devem ser salvos separadamente ou via controller para evitar duplicação/inconsistência
            return True
        except Exception as e:
            print(f"Erro ao salvar consignação: {e}")
            return False
            
    def carregar_itens(self):
        """Carrega os itens desta consignação."""
        if self.id:
            consulta = '''
                SELECT i.*, p.nome as produto_nome 
                FROM itens_consignacao i
                JOIN produtos p ON i.produto_id = p.id
                WHERE i.consignacao_id = ?
            '''
            rows = gerenciador_bd.buscar_todos(consulta, (self.id,))
            self.itens = [ItemConsignacao.from_row(row) for row in rows]

    @staticmethod
    def obter_todas() -> List['Consignacao']:
        consulta = '''
            SELECT c.*, cl.nome as cliente_nome 
            FROM consignacoes c
            JOIN clientes cl ON c.cliente_id = cl.id
            ORDER BY c.data_envio DESC
        '''
        rows = gerenciador_bd.buscar_todos(consulta)
        return [Consignacao.from_row(row) for row in rows]
        
    @staticmethod
    def obter_por_id(id: int) -> Optional['Consignacao']:
        consulta = '''
            SELECT c.*, cl.nome as cliente_nome 
            FROM consignacoes c
            JOIN clientes cl ON c.cliente_id = cl.id
            WHERE c.id = ?
        '''
        row = gerenciador_bd.buscar_um(consulta, (id,))
        if row:
            consig = Consignacao.from_row(row)
            consig.carregar_itens()
            return consig
        return None

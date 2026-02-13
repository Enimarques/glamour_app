from dataclasses import dataclass
from typing import Optional
import sqlite3
from database.db_manager import gerenciador_bd

@dataclass
class Cliente:
    """Representa um cliente na loja de semijoias."""
    id: Optional[int] = None
    nome: str = ""
    telefone: Optional[str] = None
    email: Optional[str] = None
    tipo: str = "Avulso"
    comissao_padrao: float = 0.0
    observacoes: Optional[str] = None
    
    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'Cliente':
        """Cria uma instância de Cliente a partir de uma linha do banco de dados."""
        # Verifica se as colunas novas existem na row (para compatibilidade)
        keys = row.keys()
        tipo = row['tipo'] if 'tipo' in keys else 'Avulso'
        comissao = row['comissao_padrao'] if 'comissao_padrao' in keys else 0.0
        email = row['email'] if 'email' in keys else None
        
        return cls(
            id=row['id'],
            nome=row['nome'],
            telefone=row['telefone'],
            email=email,
            tipo=tipo,
            comissao_padrao=comissao,
            observacoes=row['observacoes']
        )
    
    def salvar(self) -> bool:
        """
        Salva o cliente no banco de dados.
        
        Returns:
            bool: True se bem sucedido, False caso contrário
        """
        try:
            if self.id is None:
                # Insere novo cliente
                consulta = '''
                    INSERT INTO clientes (nome, telefone, email, tipo, comissao_padrao, observacoes)
                    VALUES (?, ?, ?, ?, ?, ?)
                '''
                cursor = gerenciador_bd.executar_consulta(consulta, (
                    self.nome, self.telefone, self.email, self.tipo, self.comissao_padrao, self.observacoes
                ))
                self.id = cursor.lastrowid
            else:
                # Atualiza cliente existente
                consulta = '''
                    UPDATE clientes 
                    SET nome=?, telefone=?, email=?, tipo=?, comissao_padrao=?, observacoes=?, atualizado_em=CURRENT_TIMESTAMP
                    WHERE id=?
                '''
                gerenciador_bd.executar_consulta(consulta, (
                    self.nome, self.telefone, self.email, self.tipo, self.comissao_padrao, self.observacoes, self.id
                ))
            return True
        except Exception as e:
            print(f"Erro ao salvar cliente: {e}")
            return False
    
    def excluir(self) -> bool:
        """
        Exclui o cliente do banco de dados.
        
        Returns:
            bool: True se bem sucedido, False caso contrário
        """
        try:
            if self.id is not None:
                consulta = "DELETE FROM clientes WHERE id=?"
                gerenciador_bd.executar_consulta(consulta, (self.id,))
                self.id = None
                return True
            return False
        except Exception as e:
            print(f"Erro ao excluir cliente: {e}")
            return False
    
    @staticmethod
    def obter_por_id(cliente_id: int) -> Optional['Cliente']:
        """
        Recupera um cliente pelo seu ID.
        
        Args:
            cliente_id (int): O ID do cliente
            
        Returns:
            Cliente ou None: Instância de Cliente ou None se não encontrado
        """
        consulta = "SELECT * FROM clientes WHERE id=?"
        row = gerenciador_bd.buscar_um(consulta, (cliente_id,))
        if row:
            return Cliente.from_row(row)
        return None
    
    @staticmethod
    def obter_todos() -> list['Cliente']:
        """
        Recupera todos os clientes.
        
        Returns:
            list[Cliente]: Lista de todos os clientes
        """
        consulta = "SELECT * FROM clientes ORDER BY nome"
        rows = gerenciador_bd.buscar_todos(consulta)
        return [Cliente.from_row(row) for row in rows]
    
    @staticmethod
    def buscar_por_nome(nome: str) -> list['Cliente']:
        """
        Busca clientes pelo nome.
        
        Args:
            nome (str): Nome do cliente a ser buscado
            
        Returns:
            list[Cliente]: Lista de clientes correspondentes
        """
        consulta = "SELECT * FROM clientes WHERE nome LIKE ? ORDER BY nome"
        rows = gerenciador_bd.buscar_todos(consulta, (f"%{nome}%",))
        return [Cliente.from_row(row) for row in rows]
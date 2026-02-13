from typing import List, Optional
from models.cliente import Cliente

class ClienteController:
    """Controlador para gerenciar operações relacionadas a clientes."""
    
    @staticmethod
    def criar_cliente(nome: str, telefone: str = None, tipo: str = "Avulso", 
                      comissao_padrao: float = 0.0, observacoes: str = None) -> Cliente:
        """
        Cria um novo cliente.
        
        Args:
            nome (str): Nome do cliente
            telefone (str, opcional): Telefone do cliente
            tipo (str, opcional): Tipo do cliente ('Avulso' ou 'Revendedora')
            comissao_padrao (float, opcional): Comissão padrão para revendedoras
            observacoes (str, opcional): Observações sobre o cliente
            
        Returns:
            Cliente: Cliente criado
        """
        cliente = Cliente(
            nome=nome,
            telefone=telefone,
            tipo=tipo,
            comissao_padrao=comissao_padrao,
            observacoes=observacoes
        )
        cliente.salvar()
        return cliente
    
    @staticmethod
    def atualizar_cliente(cliente_id: int, nome: str = None, telefone: str = None,
                         tipo: str = None, comissao_padrao: float = None,
                         observacoes: str = None) -> Optional[Cliente]:
        """
        Atualiza um cliente existente.
        
        Args:
            cliente_id (int): ID do cliente a ser atualizado
            nome (str, opcional): Novo nome do cliente
            telefone (str, opcional): Novo telefone do cliente
            tipo (str, opcional): Novo tipo do cliente
            comissao_padrao (float, opcional): Nova comissão padrão
            observacoes (str, opcional): Novas observações sobre o cliente
            
        Returns:
            Cliente ou None: Cliente atualizado ou None se não encontrado
        """
        cliente = Cliente.obter_por_id(cliente_id)
        if not cliente:
            return None
            
        if nome is not None:
            cliente.nome = nome
        if telefone is not None:
            cliente.telefone = telefone
        if tipo is not None:
            cliente.tipo = tipo
        if comissao_padrao is not None:
            cliente.comissao_padrao = comissao_padrao
        if observacoes is not None:
            cliente.observacoes = observacoes
            
        cliente.salvar()
        return cliente
    
    @staticmethod
    def excluir_cliente(cliente_id: int) -> bool:
        """
        Exclui um cliente.
        
        Args:
            cliente_id (int): ID do cliente a ser excluído
            
        Returns:
            bool: True se bem sucedido, False caso contrário
        """
        cliente = Cliente.obter_por_id(cliente_id)
        if not cliente:
            return False
        return cliente.excluir()
    
    @staticmethod
    def obter_cliente(cliente_id: int) -> Optional[Cliente]:
        """
        Obtém um cliente pelo ID.
        
        Args:
            cliente_id (int): ID do cliente
            
        Returns:
            Cliente ou None: Cliente encontrado ou None se não encontrado
        """
        return Cliente.obter_por_id(cliente_id)
    
    @staticmethod
    def listar_clientes() -> List[Cliente]:
        """
        Lista todos os clientes.
        
        Returns:
            List[Cliente]: Lista de todos os clientes
        """
        return Cliente.obter_todos()
    
    @staticmethod
    def buscar_clientes(nome: str) -> List[Cliente]:
        """
        Busca clientes pelo nome.
        
        Args:
            nome (str): Nome ou parte do nome do cliente
            
        Returns:
            List[Cliente]: Lista de clientes encontrados
        """
        return Cliente.buscar_por_nome(nome)
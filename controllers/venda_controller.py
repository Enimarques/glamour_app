from typing import List, Optional
from datetime import datetime
from models.venda import Venda, ItemVenda
from models.produto import Produto
from models.cliente import Cliente

class VendaController:
    """Controlador para gerenciar operações relacionadas a vendas."""
    
    @staticmethod
    def criar_venda(cliente_id: int = None, itens: List[dict] = None, 
                   tipo_pagamento: str = "Dinheiro", dia_vencimento: int = None) -> Optional[Venda]:
        """
        Cria uma nova venda.
        
        Args:
            cliente_id (int, opcional): ID do cliente
            itens (List[dict]): Lista de itens da venda, cada item com 'produto_id', 'quantidade' e 'preco_unitario'
            tipo_pagamento (str): Tipo de pagamento ('Dinheiro', 'Cartão Crédito', 'Cartão Débito', 'PIX', 'Parcelado Boleto', 'Parcelado Promissória')
            dia_vencimento (int, opcional): Dia do mês para vencimento (para vendas parceladas)
            
        Returns:
            Venda ou None: Venda criada ou None se erro
        """
        if itens is None:
            itens = []
            
        # Calcular o valor total
        valor_total = sum(item['quantidade'] * item['preco_unitario'] for item in itens)
        
        # Definir o status baseado no tipo de pagamento
        # Pagamentos à vista são marcados como 'pago' imediatamente
        # Pagamentos parcelados são marcados como 'pendente' até serem totalmente pagos
        status = "pendente" if tipo_pagamento in ["Parcelado Boleto", "Parcelado Promissória"] else "pago"
        
        # Criar a venda
        venda = Venda(
            cliente_id=cliente_id,
            valor_total=valor_total,
            tipo_pagamento=tipo_pagamento,
            status=status,
            dia_vencimento=dia_vencimento
        )
        
        # Adicionar os itens
        for item_data in itens:
            item = ItemVenda(
                produto_id=item_data['produto_id'],
                quantidade=item_data['quantidade'],
                preco_unitario=item_data['preco_unitario']
            )
            venda.itens.append(item)
        
        # Salvar a venda
        if venda.salvar():
            # Atualizar o estoque dos produtos
            for item in venda.itens:
                produto = Produto.obter_por_id(item.produto_id)
                if produto:
                    produto.quantidade -= item.quantidade
                    produto.salvar()
            return venda
        return None
    
    @staticmethod
    def registrar_pagamento(venda_id: int, valor: float, observacoes: str = None) -> bool:
        """
        Registra um pagamento para uma venda parcelada.
        
        Args:
            venda_id (int): ID da venda
            valor (float): Valor do pagamento
            observacoes (str, opcional): Observações sobre o pagamento
            
        Returns:
            bool: True se bem sucedido, False caso contrário
        """
        venda = Venda.obter_por_id(venda_id)
        if not venda:
            return False
            
        # Verificar se é uma venda parcelada
        if venda.tipo_pagamento not in ["Parcelado Boleto", "Parcelado Promissória"]:
            return False
            
        # TODO: Implementar registro de pagamento na tabela pagamentos
        # Por enquanto, apenas atualizamos o status se o valor pago cobrir o total
        if valor >= venda.valor_total:
            venda.status = "pago"
            return venda.salvar()
            
        return False
    
    @staticmethod
    def obter_venda(venda_id: int) -> Optional[Venda]:
        """
        Obtém uma venda pelo ID.
        
        Args:
            venda_id (int): ID da venda
            
        Returns:
            Venda ou None: Venda encontrada ou None se não encontrada
        """
        return Venda.obter_por_id(venda_id)
    
    @staticmethod
    def listar_vendas() -> List[Venda]:
        """
        Lista todas as vendas.
        
        Returns:
            List[Venda]: Lista de todas as vendas
        """
        return Venda.obter_todas()
    
    @staticmethod
    def listar_vendas_pendentes() -> List[Venda]:
        """
        Lista todas as vendas pendentes (parceladas).
        
        Returns:
            List[Venda]: Lista de vendas pendentes
        """
        return Venda.obter_vendas_pendentes()
    
    @staticmethod
    def calcular_financeiro(periodo_inicio: datetime = None, periodo_fim: datetime = None) -> dict:
        """
        Calcula informações financeiras para um período.
        
        Args:
            periodo_inicio (datetime, opcional): Data de início do período
            periodo_fim (datetime, opcional): Data de fim do período
            
        Returns:
            dict: Informações financeiras
        """
        todas_vendas = Venda.obter_todas()
        
        # Filtrar por período se especificado
        if periodo_inicio or periodo_fim:
            vendas_filtradas = []
            for venda in todas_vendas:
                if periodo_inicio and venda.data_venda < periodo_inicio:
                    continue
                if periodo_fim and venda.data_venda > periodo_fim:
                    continue
                vendas_filtradas.append(venda)
        else:
            vendas_filtradas = todas_vendas
            
        # Calcular totais
        total_recebido = sum(venda.valor_total for venda in vendas_filtradas if venda.status == "pago")
        total_a_receber = sum(venda.valor_total for venda in vendas_filtradas if venda.status == "pendente")
        
        # Clientes inadimplentes (com vendas parceladas pendentes)
        clientes_inadimplentes = []
        for venda in Venda.obter_vendas_pendentes():
            if venda.cliente_id:
                cliente = Cliente.obter_por_id(venda.cliente_id)
                if cliente and cliente not in clientes_inadimplentes:
                    clientes_inadimplentes.append(cliente)
        
        return {
            "total_recebido": total_recebido,
            "total_a_receber": total_a_receber,
            "clientes_inadimplentes": clientes_inadimplentes,
            "numero_vendas": len(vendas_filtradas)
        }
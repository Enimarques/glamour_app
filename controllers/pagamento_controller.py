from typing import List, Optional
from datetime import datetime, timedelta
from models.pagamento import Pagamento
from models.venda import Venda, ItemVenda
from models.cliente import Cliente

class PagamentoController:
    """Controlador para gerenciar operações relacionadas a pagamentos."""
    
    @staticmethod
    def registrar_pagamento(venda_id: int, valor: float, observacoes: str = None) -> Optional[Pagamento]:
        """
        Registra um pagamento para uma venda fiado.
        
        Args:
            venda_id (int): ID da venda
            valor (float): Valor do pagamento
            observacoes (str, opcional): Observações sobre o pagamento
            
        Returns:
            Pagamento ou None: Pagamento registrado ou None se erro
        """
        try:
            # Verificar se a venda existe e é fiado
            venda = Venda.obter_por_id(venda_id)
            if not venda:
                raise ValueError("Venda não encontrada")
                
            if venda.tipo_pagamento not in ["Parcelado Boleto", "Parcelado Promissória"]:
                raise ValueError("A venda não é do tipo parcelado")
                
            # Criar o pagamento
            pagamento = Pagamento(
                venda_id=venda_id,
                valor=valor,
                observacoes=observacoes
            )
            
            # Salvar o pagamento
            if pagamento.salvar():
                # Verificar se o pagamento quitou a dívida
                pagamentos_existentes = Pagamento.obter_por_venda(venda_id)
                total_pago = sum(p.valor for p in pagamentos_existentes) + valor
                
                # Se o total pago cobrir o valor da venda, atualizar o status
                if total_pago >= venda.valor_total:
                    venda.status = "pago"
                    venda.salvar()
                    
                return pagamento
            return None
        except Exception as e:
            print(f"Erro ao registrar pagamento: {e}")
            return None
    
    @staticmethod
    def obter_pagamento(pagamento_id: int) -> Optional[Pagamento]:
        """
        Obtém um pagamento pelo ID.
        
        Args:
            pagamento_id (int): ID do pagamento
            
        Returns:
            Pagamento ou None: Pagamento encontrado ou None se não encontrado
        """
        return Pagamento.obter_por_id(pagamento_id)
    
    @staticmethod
    def listar_pagamentos() -> List[Pagamento]:
        """
        Lista todos os pagamentos.
        
        Returns:
            List[Pagamento]: Lista de todos os pagamentos
        """
        return Pagamento.obter_todos()
    
    @staticmethod
    def listar_pagamentos_por_venda(venda_id: int) -> List[Pagamento]:
        """
        Lista todos os pagamentos de uma venda específica.
        
        Args:
            venda_id (int): ID da venda
            
        Returns:
            List[Pagamento]: Lista de pagamentos da venda
        """
        return Pagamento.obter_por_venda(venda_id)
    
    @staticmethod
    def obter_dividas_pendentes() -> List[dict]:
        """
        Obtém todas as dívidas pendentes com informações detalhadas.
        
        Returns:
            List[dict]: Lista de dívidas pendentes com informações do cliente, venda e valores
        """
        # Obter todas as vendas pendentes (apenas parceladas)
        vendas_pendentes = Venda.obter_vendas_pendentes()
        # Filtrar apenas vendas parceladas (boleto ou promissória)
        vendas_pendentes = [v for v in vendas_pendentes 
                           if v.tipo_pagamento in ["Parcelado Boleto", "Parcelado Promissória"]]
        
        dividas = []
        for venda in vendas_pendentes:
            # Obter pagamentos já realizados para esta venda
            pagamentos = Pagamento.obter_por_venda(venda.id)
            total_pago = sum(p.valor for p in pagamentos)
            
            # Calcular valores pendentes
            valor_total = venda.valor_total
            valor_pago = total_pago
            valor_pendente = valor_total - valor_pago
            
            # Obter informações do cliente
            cliente = venda.cliente
            if not cliente:
                cliente = Cliente.obter_por_id(venda.cliente_id) if venda.cliente_id else None
            
            # Calcular data de vencimento
            data_vencimento = None
            dias_atraso = 0
            
            if venda.data_venda:
                # Para vendas parceladas, usar o dia do vencimento configurado na venda
                # Se não houver dia configurado, usar 30 dias após a venda
                if hasattr(venda, 'dia_vencimento') and venda.dia_vencimento:
                    try:
                        # Criar data de vencimento com base no dia configurado
                        mes_vencimento = venda.data_venda.month
                        ano_vencimento = venda.data_venda.year
                        
                        # Se o dia da venda for depois do dia de vencimento, usar próximo mês
                        if venda.data_venda.day > venda.dia_vencimento:
                            if mes_vencimento == 12:
                                mes_vencimento = 1
                                ano_vencimento += 1
                            else:
                                mes_vencimento += 1
                        
                        # Tratar meses com menos dias (fevereiro, etc)
                        max_day = 28
                        if mes_vencimento in [1, 3, 5, 7, 8, 10, 12]:
                            max_day = 31
                        elif mes_vencimento in [4, 6, 9, 11]:
                            max_day = 30
                        else:  # fevereiro
                            # Verificar se é ano bissexto
                            if (ano_vencimento % 4 == 0 and ano_vencimento % 100 != 0) or (ano_vencimento % 400 == 0):
                                max_day = 29
                            else:
                                max_day = 28
                        
                        dia_vencimento = min(venda.dia_vencimento, max_day)
                        data_vencimento = datetime(ano_vencimento, mes_vencimento, dia_vencimento)
                    except ValueError:
                        # Em caso de erro, usar 30 dias após a venda
                        data_vencimento = venda.data_venda + timedelta(days=30)
                else:
                    # Padrão: 30 dias após a venda
                    data_vencimento = venda.data_venda + timedelta(days=30)
                
                # Calcular dias de atraso
                if datetime.now().date() > data_vencimento.date():
                    dias_atraso = (datetime.now().date() - data_vencimento.date()).days
            
            divida_info = {
                'venda': venda,
                'cliente': cliente,
                'valor_total': valor_total,
                'valor_pago': valor_pago,
                'valor_pendente': valor_pendente,
                'data_vencimento': data_vencimento,
                'dias_atraso': dias_atraso,
                'pagamentos': pagamentos
            }
            
            dividas.append(divida_info)
            
        return dividas
    
    @staticmethod
    def calcular_totais_dividas() -> dict:
        """
        Calcula totais das dívidas pendentes.
        
        Returns:
            dict: Totais das dívidas
        """
        dividas = PagamentoController.obter_dividas_pendentes()
        
        total_dividas = sum(d['valor_total'] for d in dividas)
        total_pago = sum(d['valor_pago'] for d in dividas)
        total_pendente = sum(d['valor_pendente'] for d in dividas)
        
        return {
            'total_dividas': total_dividas,
            'total_pago': total_pago,
            'total_pendente': total_pendente,
            'numero_clientes_devendo': len(set(d['cliente'].id for d in dividas if d['cliente']))
        }
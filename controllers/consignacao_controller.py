from typing import List, Optional, Dict
import datetime
from models.consignacao import Consignacao, ItemConsignacao
from models.produto import Produto
from database.db_manager import gerenciador_bd

class ConsignacaoController:
    """Controlador para gerenciar operações de consignação."""
    
    @staticmethod
    def criar_consignacao(cliente_id: int, itens: List[Dict], observacoes: str = None) -> Optional[Consignacao]:
        """
        Cria uma nova consignação.
        
        Args:
            cliente_id (int): ID da revendedora
            itens (list): Lista de dicionários com dados dos itens:
                          {'produto_id': int, 'qtd': int, 'preco': float, 'comissao': float}
            observacoes (str): Observações
            
        Returns:
            Consignacao: A consignação criada ou None em caso de erro
        """
        try:
            # Validar estoque
            for item_data in itens:
                produto = Produto.obter_por_id(item_data['produto_id'])
                if not produto:
                    raise ValueError(f"Produto {item_data['produto_id']} não encontrado")
                if produto.quantidade < item_data['qtd']:
                    raise ValueError(f"Estoque insuficiente para produto '{produto.nome}'. Disponível: {produto.quantidade}")
            
            # Criar consignação
            consignacao = Consignacao(
                cliente_id=cliente_id,
                observacoes=observacoes,
                status="Aberta"
            )
            
            # Criar itens (em memória)
            for item_data in itens:
                item = ItemConsignacao(
                    produto_id=item_data['produto_id'],
                    qtd_enviada=item_data['qtd'],
                    preco_unitario=item_data['preco'],
                    comissao_percentual=item_data['comissao']
                )
                consignacao.itens.append(item)
                
            # Salvar (isso salva a consignação e os itens)
            if consignacao.salvar():
                # Atualizar estoque e registrar movimentação
                for item in consignacao.itens:
                    produto = Produto.obter_por_id(item.produto_id)
                    if produto:
                        produto.quantidade -= item.qtd_enviada
                        produto.salvar()
                        
                        # Registrar movimentação
                        consulta_mov = '''
                            INSERT INTO movimentacoes_estoque 
                            (produto_id, tipo_movimentacao, quantidade, observacoes)
                            VALUES (?, 'saida', ?, ?)
                        '''
                        gerenciador_bd.executar_consulta(consulta_mov, (
                            produto.id, item.qtd_enviada, f"Consignação #{consignacao.id}"
                        ))
                return consignacao
            return None
        except Exception as e:
            print(f"Erro ao criar consignação: {e}")
            raise e # Re-raise para a UI tratar

    @staticmethod
    def registrar_acerto(consignacao_id: int, itens_atualizados: List[Dict], finalizar: bool = False) -> bool:
        """
        Registra acerto de contas (vendas parciais ou totais).
        
        Args:
            consignacao_id (int): ID da consignação
            itens_atualizados (list): Lista com {'item_id': int, 'qtd_vendida': int, 'qtd_devolvida': int}
            finalizar (bool): Se True, fecha a consignação
        """
        consignacao = Consignacao.obter_por_id(consignacao_id)
        if not consignacao:
            return False
            
        try:
            total_vendido = 0.0
            total_comissao = 0.0
            
            itens_por_id = {item.id: item for item in consignacao.itens}
            
            # Atualizar itens
            for dados in itens_atualizados:
                item = itens_por_id.get(dados['item_id'])
                if not item:
                    continue

                qtd_vendida = dados.get('qtd_vendida', 0)
                qtd_devolvida = dados.get('qtd_devolvida', 0)

                if qtd_vendida + qtd_devolvida > item.qtd_enviada:
                    raise ValueError("Quantidade vendida + devolvida não pode exceder a quantidade enviada.")

                devolvida_anterior = item.qtd_devolvida
                item.qtd_vendida = qtd_vendida
                item.qtd_devolvida = qtd_devolvida
                item.salvar()
                
                valor_item = item.qtd_vendida * item.preco_unitario
                comissao_item = valor_item * (item.comissao_percentual / 100)
                
                total_vendido += valor_item
                total_comissao += comissao_item
                
                # Ajustar estoque pelo delta de devolução
                delta_devolucao = item.qtd_devolvida - devolvida_anterior
                if delta_devolucao != 0:
                    produto = Produto.obter_por_id(item.produto_id)
                    if not produto:
                        raise ValueError("Produto não encontrado para ajuste de estoque.")

                    if delta_devolucao > 0:
                        produto.quantidade += delta_devolucao
                        produto.salvar()
                        
                        consulta_mov = '''
                            INSERT INTO movimentacoes_estoque 
                            (produto_id, tipo_movimentacao, quantidade, observacoes)
                            VALUES (?, 'entrada', ?, ?)
                        '''
                        gerenciador_bd.executar_consulta(consulta_mov, (
                            produto.id, delta_devolucao, f"Devolução Consignação #{consignacao.id}"
                        ))
                    else:
                        # Reverte devolução (ajuste para manter consistência)
                        if produto.quantidade + delta_devolucao < 0:
                            raise ValueError(f"Estoque insuficiente para ajuste do produto '{produto.nome}'.")
                        produto.quantidade += delta_devolucao
                        produto.salvar()
                        
                        consulta_mov = '''
                            INSERT INTO movimentacoes_estoque 
                            (produto_id, tipo_movimentacao, quantidade, observacoes)
                            VALUES (?, 'saida', ?, ?)
                        '''
                        gerenciador_bd.executar_consulta(consulta_mov, (
                            produto.id, abs(delta_devolucao), f"Ajuste devolução Consignação #{consignacao.id}"
                        ))
            
            # Recalcular totais gerais (iterando sobre todos os itens para garantir consistência)
            total_vendido_geral = 0.0
            total_comissao_geral = 0.0
            
            for item in consignacao.itens:
                 v = item.qtd_vendida * item.preco_unitario
                 c = v * (item.comissao_percentual / 100)
                 total_vendido_geral += v
                 total_comissao_geral += c
            
            consignacao.total_vendido = total_vendido_geral
            consignacao.total_comissao = total_comissao_geral
            consignacao.total_liquido = total_vendido_geral - total_comissao_geral
            
            if finalizar:
                consignacao.status = "Fechada"
                consignacao.data_fechamento = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Devolver produtos ao estoque
                for item in consignacao.itens:
                    qtd_restante = item.qtd_enviada - item.qtd_vendida - item.qtd_devolvida
                    if qtd_restante > 0:
                        produto = Produto.obter_por_id(item.produto_id)
                        if produto:
                            produto.quantidade += qtd_restante
                            produto.salvar()
                            
                            consulta_mov = '''
                                INSERT INTO movimentacoes_estoque 
                                (produto_id, tipo_movimentacao, quantidade, observacoes)
                                VALUES (?, 'entrada', ?, ?)
                            '''
                            gerenciador_bd.executar_consulta(consulta_mov, (
                                produto.id, qtd_restante, f"Retorno Consignação #{consignacao.id}"
                            ))
                            
                            item.qtd_devolvida += qtd_restante
                            item.salvar()
            else:
                consignacao.status = "Parcial"
                
            consignacao.salvar()
            return True
            
        except Exception as e:
            print(f"Erro ao registrar acerto: {e}")
            return False

    @staticmethod
    def listar_consignacoes() -> List[Consignacao]:
        return Consignacao.obter_todas()
        
    @staticmethod
    def obter_consignacao(id: int) -> Optional[Consignacao]:
        return Consignacao.obter_por_id(id)

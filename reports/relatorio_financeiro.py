from reports.relatorio_pdf import GeradorRelatorioPDF
from controllers.venda_controller import VendaController
from datetime import datetime
import os

class RelatorioFinanceiro:
    """Classe para geração de relatórios financeiros em PDF."""
    
    @staticmethod
    def gerar_relatorio_financeiro(periodo_inicio: datetime = None, 
                                 periodo_fim: datetime = None,
                                 caminho_arquivo: str = "relatorios/relatorio_financeiro.pdf") -> str:
        """
        Gera o relatório financeiro em PDF.
        
        Args:
            periodo_inicio (datetime, opcional): Data de início do período
            periodo_fim (datetime, opcional): Data de fim do período
            caminho_arquivo (str): Caminho onde o arquivo PDF será salvo
            
        Returns:
            str: Caminho do arquivo PDF gerado
        """
        # Certifica-se de que o diretório existe
        diretorio = os.path.dirname(caminho_arquivo)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)
            
        # Cria o gerador de PDF
        pdf = GeradorRelatorioPDF(caminho_arquivo)
        
        # Adiciona título
        pdf.adicionar_titulo("RELATÓRIO FINANCEIRO")
        
        # Adiciona informações do período
        if periodo_inicio and periodo_fim:
            periodo_texto = f"Período: {periodo_inicio.strftime('%d/%m/%Y')} a {periodo_fim.strftime('%d/%m/%Y')}"
        elif periodo_inicio:
            periodo_texto = f"A partir de: {periodo_inicio.strftime('%d/%m/%Y')}"
        elif periodo_fim:
            periodo_texto = f"Até: {periodo_fim.strftime('%d/%m/%Y')}"
        else:
            periodo_texto = "Período: Todo o histórico"
            
        pdf.adicionar_subtitulo(periodo_texto)
        
        # Calcula informações financeiras
        dados_financeiros = VendaController.calcular_financeiro(periodo_inicio, periodo_fim)
        
        # Adiciona resumo financeiro
        pdf.adicionar_subtitulo("Resumo Financeiro")
        
        resumo_dados = [
            ["Total Recebido", f"R$ {dados_financeiros['total_recebido']:.2f}"],
            ["Total a Receber", f"R$ {dados_financeiros['total_a_receber']:.2f}"],
            ["Número de Vendas", str(dados_financeiros['numero_vendas'])],
            ["Clientes Inadimplentes", str(len(dados_financeiros['clientes_inadimplentes']))]
        ]
        
        pdf.adicionar_tabela(resumo_dados)
        
        # Adiciona informações sobre clientes inadimplentes
        if dados_financeiros['clientes_inadimplentes']:
            pdf.adicionar_subtitulo("Clientes Inadimplentes")
            
            cabecalhos_clientes = ["ID", "Nome", "Telefone"]
            dados_clientes = []
            
            for cliente in dados_financeiros['clientes_inadimplentes']:
                linha = [
                    str(cliente.id),
                    cliente.nome,
                    cliente.telefone or "N/A"
                ]
                dados_clientes.append(linha)
                
            pdf.adicionar_tabela(dados_clientes, cabecalhos_clientes)
        else:
            pdf.adicionar_paragrafo("Nenhum cliente inadimplente encontrado.")
            
        # Adiciona rodapé
        pdf.adicionar_rodape()
        
        # Gera o PDF
        return pdf.gerar()
        
    @staticmethod
    def gerar_relatorio_simplificado(caminho_arquivo: str = "relatorios/relatorio_simplificado.pdf") -> str:
        """
        Gera um relatório financeiro simplificado em PDF.
        
        Args:
            caminho_arquivo (str): Caminho onde o arquivo PDF será salvo
            
        Returns:
            str: Caminho do arquivo PDF gerado
        """
        # Certifica-se de que o diretório existe
        diretorio = os.path.dirname(caminho_arquivo)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)
            
        # Cria o gerador de PDF
        pdf = GeradorRelatorioPDF(caminho_arquivo)
        
        # Adiciona título
        pdf.adicionar_titulo("RELATÓRIO FINANCEIRO SIMPLIFICADO")
        
        # Calcula informações financeiras
        dados_financeiros = VendaController.calcular_financeiro()
        
        # Adiciona informações principais
        pdf.adicionar_paragrafo(
            f"Total Recebido: R$ {dados_financeiros['total_recebido']:.2f}"
        )
        pdf.adicionar_paragrafo(
            f"Total a Receber: R$ {dados_financeiros['total_a_receber']:.2f}"
        )
        pdf.adicionar_paragrafo(
            f"Número de Vendas: {dados_financeiros['numero_vendas']}"
        )
        pdf.adicionar_paragrafo(
            f"Clientes Inadimplentes: {len(dados_financeiros['clientes_inadimplentes'])}"
        )
            
        # Adiciona rodapé
        pdf.adicionar_rodape()
        
        # Gera o PDF
        return pdf.gerar()
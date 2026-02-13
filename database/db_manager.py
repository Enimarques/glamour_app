import sqlite3
import os
from typing import Optional
import logging

class GerenciadorBancoDados:
    """Gerencia conexões e operações com o banco de dados para o sistema da loja de semijoias."""
    
    def __init__(self, caminho_banco: str = None):
        """
        Inicializa o gerenciador de banco de dados.
        
        Args:
            caminho_banco (str): Caminho para o arquivo do banco de dados SQLite
        """
        if caminho_banco is None:
            # Define o caminho padrão relativo ao diretório do aplicativo (glamour_app)
            # db_manager.py está em glamour_app/database/
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            caminho_banco = os.path.join(base_dir, "loja_semijoias.db")
            
        self.caminho_banco = caminho_banco
        self.conexao: Optional[sqlite3.Connection] = None
        
    def conectar(self) -> sqlite3.Connection:
        """
        Estabelece uma conexão com o banco de dados.
        
        Returns:
            sqlite3.Connection: Objeto de conexão com o banco de dados
        """
        if self.conexao is None:
            # Cria diretório se não existir
            diretorio_banco = os.path.dirname(self.caminho_banco)
            if diretorio_banco and not os.path.exists(diretorio_banco):
                os.makedirs(diretorio_banco)
                
            self.conexao = sqlite3.connect(self.caminho_banco)
            self.conexao.row_factory = sqlite3.Row  # Permite acesso às colunas pelo nome
            self._inicializar_tabelas()
            self._atualizar_esquema()  # Atualizar esquema se necessário
            
        return self.conexao
    
    def desconectar(self):
        """Fecha a conexão com o banco de dados."""
        if self.conexao:
            self.conexao.close()
            self.conexao = None
    
    def _inicializar_tabelas(self):
        """Cria as tabelas se elas não existirem."""
        conexao = self.conectar()
        cursor = conexao.cursor()
        
        # Tabela de produtos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                preco_custo REAL NOT NULL,
                preco_venda REAL NOT NULL,
                quantidade INTEGER NOT NULL DEFAULT 0,
                caminho_imagem TEXT,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT,
                email TEXT,
                tipo TEXT DEFAULT 'Avulso', -- 'Avulso' ou 'Revendedora'
                comissao_padrao REAL DEFAULT 0.0,
                observacoes TEXT,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de vendas (versão inicial sem dia_vencimento)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                valor_total REAL NOT NULL,
                tipo_pagamento TEXT NOT NULL, -- 'Dinheiro', 'Cartão Crédito', 'Cartão Débito', 'PIX', 'Parcelado Boleto', 'Parcelado Promissória'
                status TEXT NOT NULL, -- 'pago' ou 'pendente'
                data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                observacoes TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        ''')
        
        # Tabela de itens de venda (produtos em uma venda)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS itens_venda (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venda_id INTEGER NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_unitario REAL NOT NULL,
                FOREIGN KEY (venda_id) REFERENCES vendas (id),
                FOREIGN KEY (produto_id) REFERENCES produtos (id)
            )
        ''')
        
        # Tabela de pagamentos (para vendas parceladas)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pagamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venda_id INTEGER NOT NULL,
                valor REAL NOT NULL,
                data_pagamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                observacoes TEXT,
                FOREIGN KEY (venda_id) REFERENCES vendas (id)
            )
        ''')
        
        # Tabela de movimentações de estoque
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                tipo_movimentacao TEXT NOT NULL, -- 'entrada' ou 'saida'
                quantidade INTEGER NOT NULL,
                observacoes TEXT,
                data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (produto_id) REFERENCES produtos (id)
            )
        ''')

        # Tabela de consignações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consignacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'Aberta', -- 'Aberta', 'Parcial', 'Fechada'
                data_fechamento TIMESTAMP,
                total_vendido REAL DEFAULT 0.0,
                total_comissao REAL DEFAULT 0.0,
                total_liquido REAL DEFAULT 0.0,
                observacoes TEXT,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        ''')

        # Tabela de itens de consignação
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS itens_consignacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                consignacao_id INTEGER NOT NULL,
                produto_id INTEGER NOT NULL,
                qtd_enviada INTEGER NOT NULL,
                qtd_vendida INTEGER DEFAULT 0,
                qtd_devolvida INTEGER DEFAULT 0,
                preco_unitario REAL NOT NULL,
                comissao_percentual REAL NOT NULL,
                FOREIGN KEY (consignacao_id) REFERENCES consignacoes (id),
                FOREIGN KEY (produto_id) REFERENCES produtos (id)
            )
        ''')
        
        conexao.commit()
    
    def _atualizar_esquema(self):
        """Atualiza o esquema do banco de dados para versões mais recentes."""
        conexao = self.conectar()
        cursor = conexao.cursor()
        
        # Verificar se a coluna dia_vencimento existe na tabela vendas
        cursor.execute("PRAGMA table_info(vendas)")
        colunas_vendas = cursor.fetchall()
        nomes_colunas_vendas = [coluna[1] for coluna in colunas_vendas]
        
        # Se a coluna dia_vencimento não existir, adicioná-la
        if 'dia_vencimento' not in nomes_colunas_vendas:
            try:
                cursor.execute("ALTER TABLE vendas ADD COLUMN dia_vencimento INTEGER")
                conexao.commit()
                print("Coluna dia_vencimento adicionada à tabela vendas")
            except Exception as e:
                print(f"Erro ao adicionar coluna dia_vencimento: {e}")

        # Se a coluna observacoes não existir em vendas, adicioná-la
        if 'observacoes' not in nomes_colunas_vendas:
            try:
                cursor.execute("ALTER TABLE vendas ADD COLUMN observacoes TEXT")
                conexao.commit()
                print("Coluna observacoes adicionada à tabela vendas")
            except Exception as e:
                print(f"Erro ao adicionar coluna observacoes em vendas: {e}")

        # Atualizar tabela clientes com novos campos
        cursor.execute("PRAGMA table_info(clientes)")
        colunas_clientes = cursor.fetchall()
        nomes_colunas_clientes = [coluna[1] for coluna in colunas_clientes]

        if 'email' not in nomes_colunas_clientes:
            try:
                cursor.execute("ALTER TABLE clientes ADD COLUMN email TEXT")
                conexao.commit()
                print("Coluna email adicionada à tabela clientes")
            except Exception as e:
                print(f"Erro ao adicionar coluna email: {e}")

        if 'tipo' not in nomes_colunas_clientes:
            try:
                cursor.execute("ALTER TABLE clientes ADD COLUMN tipo TEXT DEFAULT 'Avulso'")
                cursor.execute("UPDATE clientes SET tipo = 'Avulso' WHERE tipo IS NULL")
                conexao.commit()
                print("Coluna tipo adicionada à tabela clientes")
            except Exception as e:
                print(f"Erro ao adicionar coluna tipo: {e}")

        if 'comissao_padrao' not in nomes_colunas_clientes:
            try:
                cursor.execute("ALTER TABLE clientes ADD COLUMN comissao_padrao REAL DEFAULT 0.0")
                conexao.commit()
                print("Coluna comissao_padrao adicionada à tabela clientes")
            except Exception as e:
                print(f"Erro ao adicionar coluna comissao_padrao: {e}")
                
        # Garantir que as tabelas de consignação existam (caso o DB já existisse mas sem elas)
        self._inicializar_tabelas()
    
    def executar_consulta(self, consulta: str, parametros: tuple = ()) -> sqlite3.Cursor:
        """
        Executa uma consulta e retorna o cursor.
        
        Args:
            consulta (str): Consulta SQL a ser executada
            parametros (tuple): Parâmetros da consulta
            
        Returns:
            sqlite3.Cursor: Cursor com os resultados da consulta
        """
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute(consulta, parametros)
        conexao.commit()
        return cursor
    
    def buscar_todos(self, consulta: str, parametros: tuple = ()) -> list:
        """
        Busca todas as linhas de uma consulta.
        
        Args:
            consulta (str): Consulta SQL a ser executada
            parametros (tuple): Parâmetros da consulta
            
        Returns:
            list: Lista de linhas
        """
        cursor = self.executar_consulta(consulta, parametros)
        return cursor.fetchall()
    
    def buscar_um(self, consulta: str, parametros: tuple = ()):
        """
        Busca uma única linha de uma consulta.
        
        Args:
            consulta (str): Consulta SQL a ser executada
            parametros (tuple): Parâmetros da consulta
            
        Returns:
            Linha ou None: Única linha ou None se não houver resultados
        """
        cursor = self.executar_consulta(consulta, parametros)
        return cursor.fetchone()

# Instância global do gerenciador de banco de dados
gerenciador_bd = GerenciadorBancoDados()
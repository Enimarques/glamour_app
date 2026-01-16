# Sistema de Gerenciamento de Loja de Semijoias

Uma aplicação desktop para gerenciamento de estoque e controle financeiro de uma loja de semijoias, construída com Python e PyQt.

## Funcionalidades

- Cadastro de produtos (semijoias, relógios, etc.)
- Controle de estoque com alertas de estoque baixo
- Cadastro de clientes
- Vendas à vista e fiado, controle de dívidas
- Relatórios financeiros
- Geração de catálogo/mostruário em PDF
- Pronta para integração futura com APIs externas

## Arquitetura

- Design modular para fácil manutenção
- Separação de responsabilidades (dados, lógica de negócios, interface)
- Abstração de banco de dados para migração SQLite/PostgreSQL
- Pronta para futura migração para sistema web

## Estrutura do Projeto

```
├── database/           # Camada de acesso a dados
├── models/             # Modelos de dados
├── controllers/        # Lógica de negócios
├── ui/                 # Interface gráfica (PyQt)
├── reports/            # Geração de relatórios em PDF
├── utils/              # Funções utilitárias
├── main.py             # Ponto de entrada da aplicação
└── requirements.txt    # Dependências do projeto
```

## Requisitos

- Python 3.7 ou superior
- PyQt5
- ReportLab (para geração de PDFs)

## Instalação

1. Clone ou baixe o repositório
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Execução

Para executar a aplicação:
```
python main.py
```

## Desenvolvimento

O sistema foi projetado com os seguintes princípios:

1. **Separação de Responsabilidades**: Cada camada tem uma responsabilidade específica
2. **Extensibilidade**: Fácil de adicionar novas funcionalidades
3. **Manutenibilidade**: Código organizado e bem documentado
4. **Portabilidade**: Pronta para migração futura para web ou outros bancos de dados

### Camadas da Aplicação

- **Database**: Gerencia conexões e operações com o banco de dados SQLite
- **Models**: Representam as entidades de negócio (Produto, Cliente, Venda)
- **Controllers**: Implementam a lógica de negócios e regras da aplicação
- **UI**: Interface gráfica desenvolvida com PyQt5
- **Reports**: Geração de relatórios em PDF

## Futuras Melhorias

- Integração com APIs externas para geração de boletos bancários
- Migração para PostgreSQL
- Versão web da aplicação
- Autenticação de usuários
- Backup automático de dados
# Arquitetura do Sistema

Este documento descreve a arquitetura do Sistema de Gerenciamento de Loja de Semijoias, explicando as decisões de design e a organização do código.

## Visão Geral

O sistema segue uma arquitetura em camadas (layered architecture) com separação clara de responsabilidades:

```
┌─────────────────┐
│    Interface    │  (UI - PyQt5)
├─────────────────┤
│   Controladores │  (Business Logic)
├─────────────────┤
│     Modelos     │  (Data Models)
├─────────────────┤
│    Database     │  (Data Access)
└─────────────────┘
```

## Camadas da Arquitetura

### 1. Camada de Interface (UI)

**Diretório:** `ui/`

Responsável pela apresentação e interação com o usuário. Utiliza PyQt5 para criar uma interface desktop intuitiva.

Componentes principais:
- Janelas e diálogos
- Formulários de entrada
- Visualização de dados
- Event handling

### 2. Camada de Controladores (Controllers)

**Diretório:** `controllers/`

Implementa a lógica de negócios da aplicação. Esta camada coordena as operações entre a interface e os modelos de dados.

Responsabilidades:
- Processamento de requisições da UI
- Validação de dados
- Coordenação de operações complexas
- Tratamento de erros

### 3. Camada de Modelos (Models)

**Diretório:** `models/`

Representa as entidades de negócio da aplicação. Cada modelo corresponde a uma tabela no banco de dados.

Características:
- Mapeamento objeto-relacional
- Métodos para persistência de dados
- Validação de regras de negócio básicas

### 4. Camada de Banco de Dados (Database)

**Diretório:** `database/`

Responsável pelo acesso e manipulação dos dados persistentes.

Funcionalidades:
- Conexão com o banco de dados
- Execução de consultas SQL
- Gerenciamento de transações
- Abstração para futura migração de banco de dados

## Padrões de Design Utilizados

### MVC (Model-View-Controller) Adaptado

Embora o sistema utilize PyQt (que segue mais o padrão View-Controller), adaptamos o conceito para:

- **Model**: Classes em `models/` que representam as entidades
- **View**: Componentes da interface em `ui/`
- **Controller**: Classes em `controllers/` que implementam a lógica de negócios

### Data Access Object (DAO)

A camada de banco de dados implementa o padrão DAO através do `GerenciadorBancoDados`, que abstrai as operações de acesso a dados.

### Singleton

O `GerenciadorBancoDados` é implementado como um singleton para garantir uma única conexão com o banco de dados em toda a aplicação.

## Boas Práticas Implementadas

### 1. Separação de Responsabilidades (Separation of Concerns)

Cada camada tem uma responsabilidade bem definida, facilitando manutenção e testes.

### 2. Princípio da Responsabilidade Única (Single Responsibility Principle)

Classes e métodos têm funções específicas e bem definidas.

### 3. Baixo Acoplamento e Alta Coesão

As camadas são fracamente acopladas entre si, mas internamente coesas.

### 4. Extensibilidade

A arquitetura permite fácil adição de novas funcionalidades sem impacto nas existentes.

## Facilidades para Futuras Migrações

### 1. Abstração do Banco de Dados

A camada de acesso a dados foi projetada para facilitar a migração de SQLite para PostgreSQL no futuro.

### 2. Interface Desacoplada

A interface gráfica pode ser substituída por uma interface web sem afetar a lógica de negócios.

### 3. APIs Bem Definidas

Os controladores expõem APIs claras que podem ser facilmente expostas como serviços REST.

## Estratégia de Evolução

### MVP (Minimum Viable Product)

O sistema foi desenvolvido em etapas, começando com as funcionalidades essenciais:

1. Cadastro de produtos
2. Controle de estoque
3. Cadastro de clientes
4. Registro de vendas
5. Relatórios básicos

### Iterações Futuras

Planejamento para melhorias incrementais:
- Integração com APIs externas
- Autenticação de usuários
- Funcionalidades avançadas de relatórios
- Sincronização com sistemas online

## Considerações de Performance

### 1. Conexão com Banco de Dados

Uso de conexão persistente com pool de conexões para otimizar o acesso ao banco.

### 2. Carregamento de Dados

Implementação de paginação para grandes conjuntos de dados.

### 3. Cache

Possibilidade de implementação de cache para consultas frequentes.

## Segurança

### 1. Validação de Dados

Validação rigorosa de entradas do usuário em múltiplas camadas.

### 2. Prevenção de SQL Injection

Uso de prepared statements em todas as consultas.

### 3. Tratamento de Erros

Tratamento adequado de exceções sem expor detalhes internos.

## Testabilidade

A arquitetura facilita a escrita de testes unitários e de integração:

- Interfaces bem definidas
- Baixo acoplamento
- Injeção de dependências possível
- Camada de dados mockável

## Conclusão

Esta arquitetura proporciona um sistema robusto, escalável e de fácil manutenção. A separação clara de responsabilidades e o uso de padrões de design consagrados garantem que o sistema possa evoluir de forma controlada e sustentável.
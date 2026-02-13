# Melhorias na Interface de Cobranças

## Resumo
A interface de cobranças foi completamente redesenhada combinando elementos dos três modelos de referência fornecidos, criando uma experiência moderna, limpa e funcional.

## Mudanças Implementadas

### 1. **Design Tokens e Paleta de Cores Atualizada** (`styles.py`)

#### Cores Principais
- **Fundo Geral**: `#F5F7FA` - Cinza claro mais suave
- **Cards/Containers**: `#FFFFFF` - Branco puro
- **Texto Principal**: `#2C3E50` - Mais contraste
- **Texto Secundário**: `#7F8C8D` - Cinza médio
- **Bordas**: `#E1E8ED` - Bordas sutis

#### Cores de Status
- **Sucesso**: `#27AE60` (verde)
- **Perigo**: `#E74C3C` (vermelho)
- **Aviso**: `#F39C12` (laranja)
- **Info**: `#3498DB` (azul)
- **Cinza**: `#95A5A6` (neutro)
- **Escuro**: `#34495E` (dark)

### 2. **Novos Componentes de Estilo**

#### Status Badges
Criados estilos para badges/pills de status com cores específicas:
- `badge_confirmado` - Verde (Pagamento confirmado)
- `badge_pendente` - Laranja (Vence hoje)
- `badge_vencido` - Vermelho (Vencido)
- `badge_em_aberto` - Roxo (Em aberto)
- `badge_a_vencer` - Cinza (A vencer)

#### Action Buttons (Botões de Ação com Ícones)
- `btn_action_view` - Azul (Visualizar)
- `btn_action_edit` - Laranja (Editar)
- `btn_action_delete` - Vermelho (Excluir)
- `btn_action_more` - Verde (Mais ações)

Todos com tamanho compacto (35px) e ícones unicode.

#### Summary Cards (Cards de Resumo)
Cards coloridos para métricas principais:
- `summary_card_vencidos` - Vermelho
- `summary_card_vencem_hoje` - Laranja
- `summary_card_a_vencer` - Cinza
- `summary_card_recebidos` - Verde
- `summary_card_total` - Escuro

#### Toolbar Header
- `toolbar_header` - Container para ferramentas
- `btn_adicionar` - Botão verde "Adicionar"
- `btn_mais_acoes` - Botão escuro "Mais ações"
- `btn_busca_avancada` - Botão escuro "Busca avançada"
- `month_selector` - ComboBox para seleção de mês

### 3. **Redesign da Interface de Cobranças** (`aba_cobrancas.py`)

#### Novo Cabeçalho da Página
- **Ícone + Título**: Emoji "💰" + "Contas a receber"
- **Breadcrumb de Navegação**: "🏠 Início › Contas a receber › Listar"
- Layout limpo e profissional

#### Barra de Ferramentas Modernizada
Inspirada no Modelo 1:
- **Botão Adicionar** (verde): "✚ Adicionar" para criar novas cobranças
- **Botão Mais Ações** (escuro): "⚙ Mais ações ▼" com menu dropdown
  - Exportar para Excel
  - Exportar para PDF
  - Imprimir relatório
  - Marcar todas como pagas
  - Enviar lembretes
- **Seletor de Mês**: ComboBox estilizado para filtrar por mês/ano
- **Busca Avançada**: Botão "🔍 Busca avançada"

#### Cards de Resumo (Modelo 1)
5 cards coloridos exibindo métricas em tempo real:
1. **Vencidos** (Vermelho) - Total de cobranças vencidas
2. **Vencem Hoje** (Laranja) - Cobranças com vencimento hoje
3. **A Vencer** (Cinza) - Cobranças futuras
4. **Recebidos** (Verde) - Total já recebido
5. **Total** (Escuro) - Valor total geral

Cada card inclui:
- Título descritivo
- Ícone emoji temático
- Valor em destaque (fonte grande e bold)

#### Tabela de Cobranças Aprimorada
Inspirada nos 3 modelos:

**Colunas:**
1. Código - ID da venda
2. Descrição - Descrição da venda com ícone 🛒 se houver observações
3. Entidade - Nome do cliente
4. Plano de contas - "Vendas"
5. Pagamento - Tipo (Boleto, BB, etc.)
6. Data - Data de vencimento
7. Valor total - Valor formatado
8. Situação - **Badge colorido de status**
9. Loja - Nome da loja (ex: "Savassi")
10. Ações - **Botões de ação com ícones**

**Status Badges:**
- **Confirmado** (Verde) - Pagamento completo
- **Vencido** (Vermelho) - Pagamento atrasado
- **Vence Hoje** (Laranja) - Vence na data atual
- **Em Aberto** (Roxo) - Ainda não vencido

**Botões de Ação:**
- 👁 **Visualizar** (Azul) - Ver detalhes da dívida
- ✏ **Editar** (Laranja) - Editar cobrança
- ✖ **Excluir** (Vermelho) - Remover cobrança
- ⋮ **Mais** (Verde) - Menu com opções extras:
  - 💵 Registrar Pagamento
  - 📧 Enviar lembrete
  - 📄 Gerar boleto
  - 🖨 Imprimir recibo

**Melhorias na Tabela:**
- Sem linhas de grade (mais limpo)
- Linhas alternadas para melhor leitura
- Altura de linha aumentada (60px) para melhor espaçamento
- Cabeçalho com borda inferior dourada
- Alinhamento apropriado por tipo de dado

#### Diálogo de Registro de Pagamento
Interface modernizada:
- Título com emoji: "💵 Registrar Pagamento"
- **Grupo de Informações da Venda**: Exibe dados completos
- **Grupo de Dados do Pagamento**: Formulário limpo
  - Valor do pagamento (com validação)
  - Data do pagamento (com calendário popup)
  - Observações (opcional)
- Botões estilizados: "Cancelar" (secundário) e "✓ Registrar Pagamento" (verde)

#### Diálogo de Detalhes da Dívida
Interface aprimorada:
- Título com emoji: "📋 Detalhes da Dívida"
- **Informações Gerais**: Todos os dados da venda e cliente
- **Histórico de Pagamentos**: Tabela com todos os pagamentos realizados
- Valores com cores semânticas (verde para pago, vermelho para pendente)
- Layout espaçado e profissional

### 4. **Melhorias Funcionais**

#### Correções de Bugs
- Corrigida comparação entre `datetime.datetime` e `datetime.date`
- Adicionada conversão automática de tipos de data

#### Novas Funcionalidades
- Menu de ações contextuais para cada item da tabela
- Menu de ações globais na barra de ferramentas
- Filtro por mês/ano implementado
- Tooltips informativos em todos os botões de ação
- Validação de valores no registro de pagamento

#### Cálculo Automático de Totais
Os cards de resumo são calculados automaticamente:
- Separação por status (vencido, vence hoje, a vencer)
- Soma de valores recebidos
- Total geral de cobranças

## Comparação com os Modelos de Referência

### Modelo 1 (Contas a receber)
✅ Cards de resumo coloridos (Vencidos, Vencem hoje, A vencer, Recebidos, Total)  
✅ Botões "Adicionar" e "Mais ações"  
✅ Seletor de data/mês  
✅ Botão de busca avançada  
✅ Status badges na tabela  
✅ Ações com ícones coloridos  

### Modelo 2 (Notas fiscais)
✅ Botão verde "Criar Nova" (implementado como "Adicionar")  
✅ Dropdown de ações  
✅ Navegação por mês  
✅ Pills/badges de status coloridos  
✅ Ícones de ação (PDF, editar, excluir)  

### Modelo 3 (Simples Agenda)
✅ Cards de resumo no topo  
✅ Tabela limpa e moderna  
✅ Badges de status  
✅ Ícones e indicadores visuais  
✅ Navegação clara  

## Tecnologias e Frameworks

- **PyQt5**: Framework GUI principal
- **QSS (Qt StyleSheets)**: Estilização CSS-like
- **Unicode Emojis**: Ícones sem dependências externas
- **MVC Pattern**: Separação de lógica de negócios e interface

## Como Usar

1. Navegue até "Cobranças" no menu lateral
2. Visualize o resumo das cobranças nos cards coloridos
3. Use os filtros (mês, busca avançada) para encontrar cobranças específicas
4. Clique nos botões de ação (ícones) para:
   - 👁 Visualizar detalhes
   - ✏ Editar cobrança
   - ✖ Excluir cobrança
   - ⋮ Acessar mais opções (registrar pagamento, enviar lembrete, etc.)
5. Use "✚ Adicionar" para criar novas cobranças
6. Use "⚙ Mais ações" para ações em lote

## Próximos Passos Sugeridos

1. Implementar filtro por cliente
2. Adicionar exportação para Excel/PDF
3. Implementar envio de lembretes por e-mail/SMS
4. Criar tela de adição/edição de cobranças
5. Adicionar gráficos de análise de cobranças
6. Implementar busca avançada com múltiplos critérios
7. Adicionar paginação para grandes volumes de dados
8. Criar relatórios personalizáveis

## Arquivos Modificados

- `glamour_app/ui/styles.py` - Design tokens e estilos globais
- `glamour_app/ui/aba_cobrancas.py` - Interface de cobranças redesenhada

---

**Desenvolvido em**: 12 de Fevereiro de 2026  
**Sistema**: Sistema de Gerenciamento de Loja de Semijoias  
**Versão**: 2.0 - Interface Moderna

# Especificação de Design UI/UX para Sistema de Gerenciamento de Loja de Semijoias

## Visão Geral
Este documento define as diretrizes de design para aprimorar a interface do usuário do sistema de gerenciamento de loja de semijoias, seguindo princípios modernos de UI/UX.

## Paleta de Cores
- **Primária**: #4A90E2 (Azul Profissional)
- **Secundária**: #50C878 (Verde Jade - referência às semijoias)
- **Acento**: #FF6B6B (Vermelho Suave para alertas)
- **Neutras**: 
  - Fundo: #F8F9FA
  - Cards: #FFFFFF
  - Texto: #333333
  - Bordas: #E0E0E0
  - Hover: #F0F5FF

## Tipografia
- **Fonte Principal**: "Segoe UI" ou "Roboto" (fallback: Arial, sans-serif)
- **Tamanhos**:
  - Títulos: 24px (bold)
  - Subtítulos: 18px (semi-bold)
  - Texto Normal: 14px
  - Texto Secundário: 12px
  - Labels: 13px

## Componentes de Interface

### 1. Barra de Navegação
- **Estilo**: Sidebar vertical esquerda (moderna e limpa)
- **Ícones**: Simples e intuitivos
- **Hover**: Transição suave com destaque
- **Ativo**: Indicador visual com cor primária

### 2. Cards de Informação
- **Elevação**: Sombra suave (box-shadow: 0 2px 10px rgba(0,0,0,0.05))
- **Border Radius**: 8px
- **Padding**: 20px
- **Transição**: Hover com elevação aumentada

### 3. Botões
- **Primário**: Fundo azul (#4A90E2), texto branco
- **Secundário**: Borda azul, fundo transparente
- **Perigo**: Fundo vermelho (#FF6B6B), texto branco
- **Border Radius**: 6px
- **Padding**: 10px 20px
- **Transição**: Hover com mudança de opacidade

### 4. Tabelas
- **Linhas Zebradas**: Fundo alternado (#FFFFFF e #FAFAFA)
- **Hover**: Fundo azul claro (#F0F5FF)
- **Cabeçalho**: Fundo cinza claro (#F5F5F5) com texto em negrito
- **Bordas**: Finas e sutis (#E0E0E0)

### 5. Formulários
- **Inputs**: Altura consistente (40px), bordas arredondadas (4px)
- **Labels**: Acima dos inputs, tamanho 13px
- **Espaçamento**: 15px entre campos
- **Foco**: Borda azul com sombra

## Layout e Espaçamento
- **Margens**: 20px padrão
- **Gutters**: 15px entre colunas
- **Grid**: Sistema de 12 colunas responsivo
- **Breakpoints**: 
  - Desktop: > 1200px
  - Tablet: 768px - 1200px
  - Mobile: < 768px

## Princípios de Usabilidade
1. **Consistência**: Mesmo comportamento para elementos similares
2. **Feedback Visual**: Indicação clara de ações e estados
3. **Hierarquia Visual**: Elementos importantes destacados
4. **Acessibilidade**: Contraste adequado e navegação por teclado
5. **Eficiência**: Atalhos e ações rápidas

## Telas Principais

### 1. Dashboard
- **Resumo Visual**: Cards com KPIs principais
- **Gráficos Simples**: Vendas, estoque, finanças
- **Atalhos Rápidos**: Links para funcionalidades principais
- **Notificações**: Alertas de estoque baixo, aniversariantes

### 2. Produtos
- **Busca Avançada**: Filtros por categoria, preço, estoque
- **Visualização**: Grid e lista
- **Ações em Massa**: Seleção múltipla
- **Imagens**: Pré-visualização em miniaturas

### 3. Clientes
- **Perfil Completo**: Informações detalhadas
- **Histórico**: Compras anteriores
- **Fidelidade**: Programa de pontos (futuro)
- **Comunicação**: Integração com WhatsApp/email

### 4. Vendas
- **Fluxo Simplificado**: Processo de venda em etapas
- **Busca Rápida**: Por nome, telefone, código
- **Pagamentos**: Múltiplas formas
- **Impressão**: Recibos automáticos

## Melhorias Específicas

### Janela Principal
1. Substituir menu superior por sidebar lateral
2. Modernizar dashboard com cards visuais
3. Adicionar ícones intuitivos
4. Melhorar espaçamento e tipografia

### Lista de Produtos
1. Redesign da tabela com estilo moderno
2. Botões de ação mais elegantes
3. Filtros e busca avançada
4. Paginação para grandes conjuntos de dados

### Formulário de Produtos
1. Layout mais espaçoso e organizado
2. Preview de imagem
3. Validação em tempo real
4. Agrupamento lógico de campos

### Novo: Lista de Clientes
1. Tabela com informações relevantes
2. Filtros por nome, telefone, última compra
3. Ações rápidas (editar, histórico, comunicar)
4. Integração com WhatsApp

## Diretrizes de Implementação
1. Manter estrutura lógica existente
2. Apenas modificar aparência, não funcionalidade
3. Garantir compatibilidade com versões antigas
4. Testar em diferentes resoluções
5. Manter responsividade básica

## Recursos Visuais
- Ícones do Feather Icons ou Material Icons
- Ilustrações simples para empty states
- Micro-interações para feedback
- Loading states para operações assíncronas
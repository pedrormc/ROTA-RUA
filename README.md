# ROTA-RUA

Prospecção comercial porta-a-porta — **Singular Group** | Asa Norte, Brasília

## O que é

Sistema de inteligência comercial para vendas de serviços de tecnologia. Analisa a presença digital de TODOS os comércios de uma quadra da Asa Norte e gera relatórios com oportunidades de venda mapeadas aos serviços da Singular.

O vendedor nunca chega no escuro. Antes de pisar na quadra, já sabe quais lojas abordar, qual serviço oferecer, e em que ordem visitar.

## Como usar

Via Claude Code:
```
/prospect 312 norte
```

O comando roda 3 fases automaticamente:
1. **Descoberta** — encontra todas as empresas da quadra
2. **Análise** — avalia 4 dimensões de presença digital por loja
3. **Output** — gera relatórios, landing pages demo, e commita aqui

## Dependências

### SerpAPI MCP (motor primário)

A skill `/prospect` usa o MCP do SerpAPI como motor de busca para descoberta de empresas e análise de Google Meu Negócio. Sem ele, a skill cai num modo degradado usando WebSearch genérico (resultados menos estruturados).

**Setup (uma vez por máquina):**
```bash
claude mcp add --transport http --scope user serpapi \
  "https://mcp.serpapi.com/<API_KEY>/mcp"
```

Após adicionar, **reiniciar o Claude Code** para que a tool `mcp__serpapi__search` fique disponível. Verificar com:
```bash
claude mcp list | grep serpapi
```

**Engines usadas:**
| Engine | Onde |
|--------|------|
| `google_maps` | Fase 1 (discovery) e Fase 2.1 (dados base GMB) |
| `google_maps_reviews` | Fase 2.1 (taxa de resposta do dono, recência) |
| `google` | Fase 2.4 (achar Instagram via `site:instagram.com`) |

**Custo:** cada chamada consome 1 search (Plano free SerpAPI = 100/mês; Developer = 5.000/mês). Uma quadra média da Asa Norte (~30 empresas) consome ~60 chamadas: 1-3 paginadas em discovery + 1 reviews por empresa + 1 instagram por empresa.

**Helper de teste fora do Claude Code:**
```bash
scripts/gmb-probe.sh "restaurantes CLN 312 Norte"
```

### Limitação documentada — Aba Atualizações/Posts

A SerpAPI **não expõe** a aba "Atualizações" do GMB (posts recentes do dono). Esse campo continua sendo verificado manualmente — os relatórios marcam como "verificação manual necessária".

## Metodologia

### 4 Dimensões de Análise (por prioridade)

| # | Dimensão | Por que importa |
|---|----------|----------------|
| 1 | **Google Meu Negócio** | Principal fator de ranqueamento local. Aba de "Atualizações" é o indicador #1. |
| 2 | **WhatsApp** | Canal direto com cliente. Estratégia do aniversário cria base de clientes. |
| 3 | **Site/Landing Page** | Presença digital básica. Sem site = invisível no Google. |
| 4 | **Instagram** | Social media. Último recurso de visibilidade. |

### Sistema de Score

Cada dimensão recebe nota 0-10. Total máximo: 40.

| Score | Status | Significado |
|-------|--------|-------------|
| 0-3 | 🔴 Crítico | Oportunidade forte de venda |
| 4-6 | 🟡 Melhorável | Pode ser vendido como melhoria |
| 7-10 | 🟢 Ok | Baixa prioridade |

**Quanto MENOR o score, MAIOR a oportunidade de venda.**

### Priorização de Rota

Ordem de visita otimizada por potencial de venda:

1. **GMB crítico + sem WhatsApp** → venda quase garantida (2+ serviços)
2. **GMB crítico** → demonstração de valor fácil
3. **Sem WhatsApp estruturado** → quick win com exemplo aniversário
4. **Site ruim/inexistente** → projeto maior
5. **Só Instagram fraco** → menor urgência

### Argumentos de Venda por Serviço

| Problema | Serviço Singular | Argumento |
|----------|-----------------|-----------|
| GMB sem atualizações | Gestão GMB | "Sua loja perde posição toda semana que não posta. Seus concorrentes já fazem." |
| Não responde reviews | Gestão GMB | "70% dos clientes leem respostas do dono antes de visitar." |
| Sem WhatsApp Business | Estratégia WhatsApp | "Na compra, oferece desconto no aniversário. Cliente passa nome/tel/mês. Isso cria base → ofertas certeiras → recorrência." |
| Sem site | Landing Page | "Pesquisa '{categoria} Asa Norte' — sua loja não aparece. Olha como ficaria: [demo]" |
| Site lento | Refatoração | "53% abandonam após 3 segundos." |
| Instagram parado | Social Media | "Último post há X dias. Cliente esquece que você existe." |

## Estrutura do Repo

```
ROTA-RUA/
├── README.md                          # Este arquivo
├── docs/
│   └── metodologia.md                 # Metodologia completa
├── templates/
│   ├── relatorio-loja.md              # Template de relatório individual
│   └── quadra-report.md               # Template de relatório consolidado
├── CLN-312-Norte/
│   ├── _quadra-report.md              # Relatório consolidado
│   ├── bar-restaurante-california/
│   │   ├── relatorio.md               # Análise completa
│   │   └── landing-page/
│   │       └── index.html             # Landing page demo
│   ├── arena-312/
│   │   └── relatorio.md
│   ├── chiquinhos-bar/
│   │   └── relatorio.md
│   └── ...
└── CLN-XXX-Norte/                     # Próximas quadras
    └── ...
```

## Quadras Prospectadas

| Quadra | Data | Empresas | Críticos | Melhoráveis | Ok |
|--------|------|----------|----------|-------------|-----|
| [CLN 312 Norte](CLN-312-Norte/_quadra-report.md) | 2026-04-16 | 10 | 6 | 3 | 1 |

## Serviços Singular

### Quick Wins
- **Gestão Google Meu Negócio** — posts, reviews, fotos, ranqueamento
- **Estratégia WhatsApp** — Business, catálogo, automação, base de clientes

### Projetos
- **Landing Page** — site profissional mobile-first
- **Refatoração de Site** — performance, SEO, design
- **Gestão Social Media** — Instagram, conteúdo, tráfego

### Pacotes
- **Starter:** GMB + WhatsApp Business
- **Digital:** GMB + WhatsApp + Landing Page
- **Full:** GMB + WhatsApp + Site + Instagram

## Status de Prospecção

Cada loja pode estar em um destes estados:

| Status | Descrição |
|--------|-----------|
| `prospectado` | Análise feita, não visitado |
| `visitado` | Vendedor foi, aguardando retorno |
| `em_negociacao` | Interesse confirmado |
| `convertido` | Serviço vendido |
| `descartado` | Sem interesse |

---

**Singular Group** — Asa Norte, Brasília-DF

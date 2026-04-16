# Metodologia ROTA-RUA — Documentação Completa

## Visão Geral

ROTA-RUA é um sistema de prospecção comercial da Singular Group que combina inteligência artificial com vendas porta-a-porta. O sistema analisa automaticamente a presença digital de comércios locais e gera relatórios acionáveis para a equipe de vendas.

**Região:** Asa Norte, Brasília-DF (quadras CLN — Comércio Local Norte)
**Foco:** Serviços de tecnologia e presença digital

---

## Fluxo Operacional

### Pré-Rota (Preparação)

```
Vendedor → Claude Code → /prospect {quadra}
                              │
                    ┌─────────┴─────────┐
                    │                   │
              FASE 1: DESCOBERTA   Pesquisa automática
              Google Maps, Web     de todas as empresas
                    │                   │
                    └─────────┬─────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
              FASE 2: ANÁLISE      4 dimensões por loja
              GMB, WhatsApp,       (em paralelo)
              Site, Instagram
                    │                   │
                    └─────────┬─────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
              FASE 3: OUTPUT       Relatórios MD + PDF
              Landing pages HTML   Commit no GitHub
              Nota no Obsidian     Ranking de rota
                    │                   │
                    └─────────┬─────────┘
                              │
                    Vendedor sai com:
                    - PDFs no celular
                    - Ordem de visita otimizada
                    - Landing pages demo
                    - Argumentos por loja
```

### Na Rua (Execução)

1. Seguir a rota sugerida (lojas mais críticas primeiro)
2. Abrir o relatório da loja no celular
3. Mostrar o scorecard e os problemas encontrados
4. Demonstrar a landing page demo (se aplicável)
5. Usar os argumentos de venda mapeados
6. Registrar resultado (interesse/sem interesse)

### Pós-Rota (Follow-up)

1. Atualizar status no Obsidian (visitado → em_negociação → convertido)
2. Cadastrar leads no HubSpot (futuro)
3. Gerar propostas comerciais baseadas nos relatórios

---

## Detalhamento das Dimensões

### Dimensão 1: Google Meu Negócio

**Por que é prioridade #1:**

O Google Meu Negócio é o primeiro ponto de contato entre um cliente e um comércio local. Quando alguém pesquisa "restaurante Asa Norte" ou "farmácia perto de mim", o Google mostra o "Local Pack" — os 3 primeiros resultados do mapa.

**O principal fator de ranqueamento é a aba de "Atualizações":**
- Posts semanais com ofertas, novidades, fotos
- Respostas aos comentários dos clientes
- Fotos atualizadas do estabelecimento
- Horários corretos

A maioria dos comércios locais NÃO faz isso, o que representa a oportunidade #1.

**Checklist de análise:**

| Item | Peso | Como verificar |
|------|------|---------------|
| Perfil existe | Crítico | WebSearch nome + quadra + Google Maps |
| Atualizações ativas | Alto | Verificar frequência de posts |
| Respostas a reviews | Alto | Verificar se dono responde |
| Nota média | Médio | Extrair rating |
| Quantidade de reviews | Médio | Contar avaliações |
| Fotos | Baixo | Verificar quantidade e recência |
| Horários | Baixo | Verificar se existem e são corretos |

### Dimensão 2: WhatsApp

**A Estratégia do Aniversário (principal argumento):**

Este é o quick win mais poderoso para comércios locais da Asa Norte:

1. **Coleta:** Na hora da compra, oferecer desconto especial no mês do aniversário
2. **Dados:** Cliente passa nome, telefone, mês de nascimento
3. **Base:** Isso cria uma base de clientes organizada
4. **Ações com a base:**
   - Ofertas de aniversário automáticas
   - Campanhas de recorrência
   - Canal de WhatsApp com novidades
   - Promoções sazonais
   - Lançamentos de produtos

**Por que funciona:** É mais eficiente que tráfego pago no Instagram porque fala com quem JÁ COMPROU. O custo de retenção é menor que o de aquisição.

**Checklist de análise:**

| Item | Peso | Como verificar |
|------|------|---------------|
| Tem WhatsApp? | Crítico | Buscar em site, GMB, redes sociais |
| É Business? | Alto | Verificar tipo do link (wa.me) |
| Link clicável? | Alto | Verificar se existe wa.me no site |
| Catálogo | Médio | Checar no WhatsApp Business |
| Mensagem automática | Baixo | Verificar pré-mensagem |

### Dimensão 3: Site / Landing Page

**Checklist de análise:**

| Item | Peso | Como verificar |
|------|------|---------------|
| Existe? | Crítico | WebFetch URL |
| Mobile-friendly | Alto | Testar viewport mobile |
| SSL (https) | Alto | Verificar certificado |
| Velocidade | Médio | Tempo de carregamento |
| Botões funcionam | Médio | Click test em CTAs |
| SEO básico | Médio | Title, meta description, H1 |
| Info completa | Baixo | Endereço, telefone, horário |

**Landing Page Demo:**
Para lojas com score de site < 7, geramos uma landing page estática moderna:
- HTML + CSS, mobile-first
- Baseada nas informações coletadas
- Botão de WhatsApp funcional
- Design profissional
- Serve como demonstração: "Olha como ficaria"
- Salva em `{loja}/landing-page/index.html`

### Dimensão 4: Instagram

**Checklist de análise:**

| Item | Peso | Como verificar |
|------|------|---------------|
| Perfil existe? | Crítico | WebSearch nome + instagram |
| Último post | Alto | Verificar data |
| Frequência | Médio | Posts por semana |
| Bio completa | Baixo | Endereço, link, telefone |
| Link na bio | Baixo | Verificar se funciona |

---

## Catálogo de Serviços e Argumentação

### Gestão Google Meu Negócio

**Quando vender:** GMB score 0-5
**Pitch principal:** "Sua loja perde posição no Google toda semana que não posta atualização. O principal fator de ranqueamento local é a aba de Atualizações do Google Meu Negócio. Seus concorrentes da quadra já estão fazendo."
**Pitch reviews:** "70% dos clientes leem as respostas do dono antes de visitar. Cada review sem resposta é cliente que escolhe o concorrente."

### Estratégia WhatsApp + Base de Clientes

**Quando vender:** WhatsApp score 0-5
**Pitch principal:** "O jeito mais rápido de aumentar seu faturamento é falar com quem já comprou de você. Na hora da compra, oferece desconto no mês do aniversário — o cliente passa nome, telefone e mês de nascimento. Com essa base você manda ofertas certeiras, cria canal de WhatsApp, divulga promoções. É mais eficiente que ficar pagando tráfego no Instagram."

### Criação de Landing Page

**Quando vender:** Site score 0-3
**Pitch principal:** "Quando alguém pesquisa '{categoria} Asa Norte' no Google, sua loja não aparece. Olha como ficaria um site profissional pra vocês: [mostra landing page demo no celular]"

### Refatoração de Site

**Quando vender:** Site score 4-6
**Pitch principal:** "Seu site demora {X} segundos pra carregar. 53% dos visitantes abandonam após 3 segundos. Cada segundo a mais é cliente perdido."

### Gestão Social Media

**Quando vender:** Instagram score 0-4
**Pitch principal:** "Último post foi há {X} dias. Seus clientes esquecem que você existe entre uma visita e outra."

---

## Infraestrutura Técnica

### Skill `/prospect`

- **Localização:** `~/.claude/skills/prospect/SKILL.md`
- **Trigger:** `/prospect {quadra}`
- **Tools usadas:** WebSearch, WebFetch, Browse, Agent (paralelo), Write, Bash (git)

### Repositório GitHub

- **URL:** github.com/pedrormc/ROTA-RUA
- **Organização:** por quadra → por loja
- **Templates:** em `templates/`
- **Auto-commit** após cada prospecção

### Obsidian Vault

- **Path:** `singular/ROTA-RUA/`
- **Índice:** `ROTA-RUA.md`
- **Metodologia:** `Metodologia-ROTA-RUA.md`
- **Quadras:** `CLN-{numero}-Norte.md` (com frontmatter)

### Futuro: Integração HubSpot

- Contatos convertidos → HubSpot CRM
- Pipeline: ENTRADA → EM CONTATO → ENTREVISTA → NEGOCIAÇÃO → VENDA
- Funil já definido em `singular/CTO/HUBSPOT-DEV/HUBSPOT-SCOUTING.md`

---

## Evolução Planejada

### Fase 1 (Atual)
- [x] Skill `/prospect` funcional
- [x] Análise das 4 dimensões
- [x] Relatórios MD por loja e quadra
- [x] Landing pages demo HTML
- [x] GitHub repo ROTA-RUA
- [x] Obsidian tracking

### Fase 2 (Próxima)
- [ ] Geração de PDF automática (pandoc/puppeteer)
- [ ] Integração HubSpot (leads automáticos)
- [ ] Batch por região (múltiplas quadras de uma vez)
- [ ] Dashboard de conversão

### Fase 3 (Futuro)
- [ ] App mobile pro vendedor (PWA)
- [ ] Comparativo temporal (antes/depois da Singular)
- [ ] Automação de follow-up via n8n
- [ ] Score dinâmico (re-análise periódica)

---

*Singular Group — Metodologia ROTA-RUA v1.0*
*[Registrado por: DESKTOP — 2026-04-16]*

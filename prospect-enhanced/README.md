---
title: "prospect-enhanced — funil de prospecção CLN 310–315 Norte"
skill: prospect-enhanced
versao: "1.0"
bu: consultorio-comercial
lote_referencia: "2026-08-310-315"
status: ativo
created: "2026-08-10"
updated: "2026-08-10"
---

# prospect-enhanced

**Aba nova do ROTA-RUA.** Prospecção porta-a-porta com **funil de qualificação antes da análise cara**, cobrindo as quadras comerciais **CLN 310 a 315 Norte** tratadas em **pares de entrequadra**.

> A v1 (`/prospect`) analisa **tudo** que existe na quadra e depois o vendedor descobre na rua que metade não presta. A v2 (`/prospect-enhanced`) **reprova antes de gastar**: os gates que custam R$ 0 (CNPJ/MEI, franquia, geografia) rodam primeiro, e só quem sobrevive consome crédito de SerpAPI.

---

## Índice

| Documento | O que responde |
|---|---|
| [FILTROS.md](FILTROS.md) | O funil completo em gates (G0–G11), o que é hard, o que é soft, o que fazer quando o dado está ausente, detecção de franquia, escada de relaxamento |
| [CLASSIFICACAO.md](CLASSIFICACAO.md) | P1/P2/P3 por volume de comentários, mapa dos botões do GMB, score de oportunidade 0–100, taxonomia de 30 nichos com gancho de venda |
| [SCHEMA.md](SCHEMA.md) | Schema do registro por empresa (JSON + colunas do CSV), proveniência por campo |
| [FONTES-CNPJ.md](FONTES-CNPJ.md) | Como resolver nome → CNPJ → porte, APIs, rate limits, CEPs canônicos, fallbacks |
| [templates/empresa.md](templates/empresa.md) | Relatório por empresa |
| [templates/lote-report.md](templates/lote-report.md) | Relatório do lote (frontmatter YAML obrigatório) |
| [templates/funil.csv](templates/funil.csv) | Cabeçalho canônico do CSV de rastreio |

---

## 1. Por que esta aba existe

O ROTA-RUA v1 provou o método (a análise por loja é boa e o `oportunidades.md` do lima-lasers é o melhor artefato de venda do repo). O que ele **não** tem é qualificação: em CLN 314 Norte, das 21 empresas analisadas, várias eram lixo de funil (Sex Shop com 2 avaliações, Cotton UP com 1) e outras eram franquia/rede (Spoleto, BIG BOX) onde não há decisor local para vender.

A v2 nasce de quatro exigências do Pedro:

1. **Não-MEI.** Puxar CNPJ e checar porte. MEI sai do funil.
2. **Prova de que o dono cuida do perfil** (era "descrição ≥ 500 caracteres" — ver §4, o critério mudou de implementação, não de intenção).
3. **Sem franquia grande / rede nacional.** Decisão de marketing centralizada = não há o que vender no balcão.
4. **Escopo 310–315 Norte**, em pares de entrequadra.

E de uma correção explícita dele: **"sem site" não elimina ninguém.** Empresa sem site é *bom cliente* — é venda de landing page, não motivo de descarte.

---

## 2. Escopo geográfico — os três pares

As quadras comerciais da Asa Norte funcionam em **pares que compartilham a mesma via comercial**. A loja fica fisicamente na entrequadra, e o Google atribui a face de forma inconsistente. Varrer quadra isolada (erro da v1) perde metade da via.

| Par | Quadras | Nome canônico | Centróide | Confiança |
|---|---|---|---|---|
| 1 | CLN 310 + CLN 311 | `310-311` | a resolver em runtime | ❌ desconhecido |
| 2 | CLN 312 + CLN 313 | `312-313` | `@-15.7502,-47.8933,18z` | 🟢 alta (9 âncoras reais de GPS) |
| 3 | CLN 314 + CLN 315 | `314-315` | `@-15.7441,-47.8947,18z` | 🟡 baixa (1 âncora só — confirmar) |

**O par é sempre nomeado pelo número par (o menor).** Zoom fixo `18z` — testado: `17z` vaza para 413, 713, 214, 215, 211.

Formatos de endereço reais na CLN (todos observados numa mesma amostra): `SHCN CLN 312, BL B Lj 29` · `Asa Norte Comércio Local Norte 313, BL C` · `SCLRN Quadra 713 Bloco E` · `St. Shcn Comercio Local 313 Bloco A, 37` · `BL A Loja 45, Plano Piloto` (sem quadra nenhuma). O gate geográfico trata os sete formatos — detalhe em [FILTROS.md](FILTROS.md).

---

## 3. Meta: 40 aprovadas — **piso, não teto**

- A meta é do **lote inteiro 310–315**, não de cada par.
- Se render **mais de 40**, traz **todas**. Nunca truncar.
- A meta **não interrompe a varredura**: os 3 pares são varridos sempre, mesmo que o primeiro já entregue 40.
- Se render **menos de 40**, existe uma escada de relaxamento de 5 degraus (R1→R5), documentada em [FILTROS.md](FILTROS.md#escada-de-relaxamento). Cada empresa readmitida carrega o campo `nivel_admissao`.
- Se, esgotado o R5, ainda faltar: **reporta o número real**. Um funil de 31 leads reais vale mais que 40 com 9 mentiras — o custo do erro aqui é o vendedor perdendo a manhã numa porta errada.

Universo medido (Casa dos Dados, situação ATIVA): **856 empresas ativas** nas 6 quadras, **575 não-MEI**. A meta de 40 é folgada.

---

## 4. ⚠️ A mudança que você precisa saber antes de tudo

**O filtro "descrição do GMB ≥ 500 caracteres" NÃO é implementável via SerpAPI.** Isso foi medido, não suposto.

O campo `description` que a SerpAPI devolve é o **blurb editorial do Google**, não o texto do dono:

| Métrica medida (CLN 313, 20 resultados reais) | Valor |
|---|---|
| Empresas **sem** o campo `description` | 12 de 20 (60%) |
| Maior descrição observada | **151 caracteres** |
| `type=place` melhora? | Não — em um caso veio **mais curta** (109 vs 146) |

Rodar o gate literal reprovaria **100%** das empresas e queimaria o lote inteiro.

**Substituto: ICP — Índice de Cuidado com o Perfil (0–10, corte ≥ 5).** Mede exatamente a intenção original do Pedro ("descrição longa prova que o dono cuida do perfil e tem maturidade pra comprar") com campos que **existem de verdade**: posts recentes, perfil reivindicado, riqueza de `extensions`, horário completo, telefone, botões transacionais, rating. Detalhe em [CLASSIFICACAO.md](CLASSIFICACAO.md#icp).

Se o Pedro exigir o texto literal do dono, o único caminho é **scraping da aba "Sobre" no Maps via Playwright** — fora da SerpAPI, ~15 s por empresa, alta fragilidade. Está documentado como **"requer scraping fora da SerpAPI — NÃO IMPLEMENTADO"**. Não é campo de API e não será prometido como tal.

---

## 5. O que muda vs `/prospect` v1

| # | Dimensão | v1 (`/prospect`) | v2 (`/prospect-enhanced`) |
|---|---|---|---|
| 1 | **Qualificação** | Nenhuma. Analisa todas as empresas da quadra | Funil de 11 gates. Gates grátis (MEI, franquia, geo) cortam **antes** da chamada paga |
| 2 | **Unidade geográfica** | Quadra isolada (`/prospect 312`) | **Par de entrequadra** (310/311, 312/313, 314/315) |
| 3 | **CNPJ / porte** | Não existe. Nenhum arquivo do repo tem CNPJ | Roster de ~856 CNPJs baixado **antes** do SerpAPI, custo R$ 0. Gate MEI é join local |
| 4 | **"Sem site"** | Score 0 = penalidade (14 de 21 lojas em 314 caíram no ranking por isso) | **Nunca penaliza.** `site_tipo` é enum; `ausente` e `social` **somam** no score de oportunidade |
| 5 | **Prioridade** | Derivada da soma de dimensões — ranking incoerente (Florart 10/30 em 11º, Cotton UP 2/30 em 8º) | **P1/P2/P3 literal por nº de comentários.** Score 0–100 só desempata **dentro** da faixa |
| 6 | **Instagram** | Dimensão "oficial" que nunca rodou (21/21 lojas = ⚪ Verificação manual) | Fora do caminho crítico. Campo opcional, preenchido à mão |
| 7 | **Botões do GMB** | Não captura nenhum | 8 botões mapeados campo a campo, com **status confirmado / não confirmado** por botão |
| 8 | **`serpapi-raw.json`** | Curado à mão, com campos inventados misturados (`instagram_followers`, `email_from_site`), `hours` em 2 formatos | `serpapi-raw.json` = **dump literal intocado**. Anotação humana vai para `enriquecido.json` com proveniência por campo |
| 9 | **Campos descartados** | `people_also_search_for` gerou a melhor munição de venda do repo e não foi salvo | Persiste a resposta **inteira**. Disco custa zero, rechamada custa dinheiro |
| 10 | **Rastreio** | `_companies.json` (rating como string, `website: "-"`) + TSV manual | `funil.csv` tipado, 1 linha por empresa **incluindo reprovadas**, com `motivo_descarte` por gate |
| 11 | **Geração de relatório** | `generate.py` com 21 lojas hardcoded no código-fonte | Script lê do JSON/CSV. Zero dado hardcoded |
| 12 | **Tabela de lotes no README** | Listava só a CLN 312, enquanto 314/712/714 já estavam prontas | Atualizar a tabela de lotes é **passo obrigatório de fase**, não boa intenção |
| 13 | **Frontmatter** | Opcional (só 714 tinha) | **Obrigatório** no `lote-report.md` |
| 14 | **Franquia** | Nenhuma detecção — Spoleto e BIG BOX receberam pitch | Gate hard em 4 camadas: blacklist (~118 marcas) → padrão de nome → contagem de unidades no DF → site nacional |
| 15 | **Aba Atualizações/Posts** | Skill v1 afirma "não é exposta pela SerpAPI" — **errado** | `place_results.posts[]` retorna **10 posts** com texto de 312–633 chars. É a principal fonte do ICP |
| 16 | **`type=place`** | Nunca usado (só `type=search` implícito) | Usado em todo sobrevivente do funil. **Única fonte** de WhatsApp, menu, posts e botões |

---

## 6. Como rodar

```
/prospect-enhanced lote 310-315
```

Variações:

| Comando | Efeito |
|---|---|
| `/prospect-enhanced lote 310-315` | Lote completo, 3 pares. Padrão. |
| `/prospect-enhanced par 312-313` | Só um par (use quando o saldo de créditos estiver apertado) |
| `/prospect-enhanced roster` | Só o G0 — baixa/atualiza o roster de CNPJ. Custo R$ 0, 0 crédito SerpAPI |
| `/prospect-enhanced empresa <place_id>` | Análise sob demanda de uma empresa só |

### Pré-requisitos

```bash
export SERPAPI_KEY="..."          # ou SERPAPI_MCP_URL
```

Nenhuma chave vive em arquivo. Casa dos Dados público e OpenCNPJ não usam chave, mas a Casa dos Dados **exige `User-Agent` não-vazio** (sem UA → 403).

### Passo obrigatório antes de disparar

**Conferir o saldo de créditos.** Se `saldo < 1,3 × orçamento`, rodar **1 par por vez** e reportar ao Pedro. O orçamento realista do lote é ~335 créditos; o teto duro é 400 (ultrapassou, aborta e reporta).

---

## 7. Custo por rodada

Contabilizado em **créditos de busca SerpAPI**, nunca em R$ — o preço depende do plano da conta e afirmar valor seria inventar dado.

| Fase | Cálculo | Créditos |
|---|---|---|
| G0 roster CNPJ (Casa dos Dados + OpenCNPJ + ViaCEP) | ~110 + ~856 requisições gratuitas | **0** |
| G1 coordenadas dos pares (1 vez, depois cache eterno) | 4 | **4** |
| G2 discovery GMB | 3 pares × 10 queries × 2–3 páginas | **60–90** |
| G7 franquia por marca (cache 90 dias) | ~20 marcas | **20** |
| G8 `type=place` (o gasto dominante) | ~120 sobreviventes × 1 | **120** |
| G10 reviews / taxa de resposta | ~55 × 1 pág + ~20 × 2ª pág | **75** |
| Margem de erro / requeries | +10% | **32** |
| **TOTAL REALISTA** | | **≈ 335** |
| **TETO DURO** (abortar e reportar acima disso) | | **400** |
| **Cenário enxuto** (5 queries/par, 1 pág de reviews) | | **≈ 210** |

**Por par: ~110 créditos.** Rodadas seguintes ficam mais baratas — quadras, marcas e roster ficam em cache.

### Economias já verificadas

1. **Gate grátis primeiro.** MEI e franquia cortam ~100 empresas **antes** do `type=place` — economia de ~28% do orçamento do lote.
2. **Cache de 1 h da SerpAPI é grátis.** Query idêntica repetida dentro de 1 h não consome crédito → encadear todas as fases na mesma sessão.
3. **`extensions` já vem no `search`** — não precisa de `place` para medir riqueza de perfil.
4. **Roster de CNPJ tem TTL de 30 dias.** Rodar de novo só na virada do mês.
5. **Blacklist de redes é lista viva** — toda marca com ≥ 5 unidades no DF é gravada com data e contagem. É o único componente do sistema que **fica mais barato a cada lote**.

### O que NÃO usar (testado e reprovado)

| Item | Por quê |
|---|---|
| `json_restrictor` | Retornou `{}` vazio e **queimou 1 crédito** |
| `engine=google_local` | Não retorna `links`, `website`, `phone`, `extensions` nem `unclaimed_listing`, e vaza geograficamente muito mais (buscando CLN 313 devolveu Asa Sul, SRTVS, CLN 105/403/405) |
| Chutar coordenada `ll` | Chutei `@-15.7449,-47.8859,17z` para a 313 e voltou majoritariamente 413, 713, 214, 215 |

---

## 8. Estrutura de pastas

```
prospect-enhanced/
├── README.md                      ← este arquivo (a "aba")
├── FILTROS.md                     ← o funil em gates
├── CLASSIFICACAO.md               ← P1/P2/P3, botões, score, nichos
├── SCHEMA.md                      ← schema do registro por empresa
├── FONTES-CNPJ.md                 ← nome → CNPJ → porte
├── data/
│   ├── quadras.json               # centróides + zoom + âncoras (cache eterno)
│   ├── ceps-cln.json              # 36 CEPs canônicos (fonte ViaCEP)
│   ├── roster-cln-310-315.json    # ~856 CNPJs das 6 quadras (TTL 30 dias)
│   ├── blacklist-redes.json       # ~118 marcas de rede/franquia (lista viva)
│   ├── cache-marcas.json          # contagem de unidades no DF (TTL 90 dias)
│   └── nicho-map.json             # type_ids → nicho (30 slugs)
├── templates/
│   ├── empresa.md
│   ├── lote-report.md
│   └── funil.csv
├── scripts/
│   ├── roster-build     # G0  — Casa dos Dados + OpenCNPJ
│   ├── gmb-scan         # G2/G8 — SerpAPI (credencial por env var)
│   ├── cnpj-match       # G6  — join local nome/telefone/loja/CNAE
│   ├── score            # G9/G11 — ICP + score 0–100 + ranking
│   └── report           # gera empresa.md, lote-report.md, funil.csv
└── lotes/
    └── 2026-08-310-315/
        ├── _meta.json             # corte de ICP calibrado, custo, saldo antes/depois
        ├── _raw/                  # dumps literais do discovery
        ├── funil.csv              # TODAS as empresas, aprovadas e reprovadas
        ├── lote-report.md         # frontmatter YAML obrigatório
        ├── par-310-311/{slug}/
        ├── par-312-313/{slug}/
        └── par-314-315/{slug}/
```

Por empresa, dentro de `par-XXX-YYY/{slug}/`:

| Arquivo | O que é |
|---|---|
| `serpapi-raw.json` | Dump **literal e intocado** da resposta `type=place` |
| `serpapi-reviews.json` | Dump literal da resposta de reviews |
| `enriquecido.json` | Registro derivado, no schema de [SCHEMA.md](SCHEMA.md), com `_proveniencia` |
| `relatorio.md` | Relatório da empresa (template `empresa.md`) |
| `oportunidades.md` | Top 3 ganchos de venda, pitch literal, ticket sugerido, quem procurar |

**Regra de ouro:** anotação humana **nunca** entra no arquivo `raw`. Foi o que quebrou a v1 — sem essa separação não dá para reprocessar nada sem pagar API de novo.

---

## 9. Onde caem os lotes gerados

`prospect-enhanced/lotes/{AAAA-MM}-{quadra-inicial}-{quadra-final}/`

O identificador do lote de referência é **`2026-08-310-315`** e vai no campo `lote` de todo registro.

### Tabela de lotes

> **Atualizar esta tabela é passo obrigatório de fase da skill**, executado ao fechar o lote. Foi exatamente o que não aconteceu na v1 (o README listava só a CLN 312 enquanto 314, 712 e 714 já estavam feitas).

| Lote | Pares | Data | Descobertas | Aprovadas | P1 | P2 | P3 | Créditos | Corte ICP | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `2026-08-310-315` | 310/311, 312/313, 314/315 | — | — | — | — | — | — | — | — | 🕐 não executado |

---

## 10. Serviços da Singular que este funil vende

| Serviço | Sinal que abre a venda |
|---|---|
| Gestão de Google Meu Negócio | Perfil pobre, sem posts, sem resposta a review, horário incompleto |
| Estratégia de WhatsApp + base de clientes | Sem `wa.me` detectado, ou negócio de recorrência sem canal direto |
| Criação de landing page | `site_tipo` = `ausente`, `social` ou `builder` |
| Social media | Nicho visual (cafeteria, doceria, moda) com perfil parado |
| Reivindicação de perfil | `unclaimed_listing: true` — o perfil existe e não tem dono |

---

*Aba gerada por /prospect-enhanced — Singular Group*
*[Registrado por: DESKTOP — 2026-08-10]*

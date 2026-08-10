---
title: "CLASSIFICAÇÃO — prioridade, botões, score e nichos"
skill: prospect-enhanced
versao: "1.0"
bu: consultorio-comercial
created: "2026-08-10"
updated: "2026-08-10"
---

# CLASSIFICAÇÃO

Este documento responde três perguntas, nesta ordem: **quem o vendedor visita primeiro** (§1), **o que há para vender lá dentro** (§2 e §3) e **com que frase ele entra** (§4 e §5).

---

## 1. 🎯 A REGRA PRIMÁRIA — P1/P2/P3 por volume de comentários

> **Esta é a chave PRIMÁRIA de ordenação. O score 0–100 é apenas desempate DENTRO de cada faixa. Nunca o inverso.**

| Comentários no Google | Prioridade | Racional de negócio |
|---|---|---|
| **20 a 50** (inclusive nos dois extremos) | 🔴 **P1** | **Melhor alvo.** Negócio real e ativo — tem clientela suficiente para gerar avaliação — mas ainda **não foi dominado nem saturado**. O dono cuida do perfil sozinho, sente a dor e decide no balcão. |
| **acima de 50** (51+) | 🟡 **P2** | Maduro. Provavelmente **já tem agência** ou alguém cuidando. A venda existe, mas o ciclo é mais longo e concorrido. |
| **abaixo de 20** (0–19) | 🟢 **P3** | Pequeno demais ou novo demais. Ticket não fecha, e frequentemente não há verba de marketing ainda. |
| ausente / `null` | 🟢 **P3** + `reviews_ausente: true` | Ausência **não reprova** — só não promove. |

**Viabilidade confirmada:** o campo `reviews` é `int` e veio preenchido em **20 de 20** resultados reais da CLN 313. A regra é 100% executável, sem estimativa.

### Por que isso substitui o ranking da v1

A v1 ordenava por soma de dimensões (GMB + WhatsApp + Site + Instagram) e produziu ranking incoerente: **Florart com 10/30 apareceu em 11º e Cotton UP com 2/30 em 8º** — a coluna "Total" não ordenava nada. Aqui o par **(prioridade, score)** é auditável linha a linha, e a prioridade vem de um número único que o Pedro consegue conferir olhando o perfil no celular.

### Ordenação final (determinística)

```sql
ORDER BY prioridade           (P1 → P2 → P3),
         score_oportunidade   DESC,
         reviews              DESC,
         title                ASC
```

**Nunca ordenar pelo score global.**

---

## 2. Mapa dos botões do Google Meu Negócio

Os 8 botões que aparecem no perfil. Para cada um: o campo da API, o **status de confirmação**, o que a **ausência** significa comercialmente e qual **serviço da Singular** ela abre.

| Botão | Campo no `search` | Campo no `place` | Status | O que a AUSÊNCIA significa | Serviço que abre |
|---|---|---|---|---|---|
| **Site** | `website` | `website` | ✅ confirmado (⚠️ ver §2.1) | Não existe destino próprio: toda a conversão depende do perfil do Google e do boca a boca. É o lead mais quente do funil | **Criação de landing page** |
| **Ligar** | `phone` | `phone` | ✅ confirmado | Perfil incompleto no básico. Cliente que quer comprar **não tem como** — perda de receita direta e mensurável | **Gestão de GMB** |
| **Rota / Como chegar** | — | — | ⚠️ **DERIVADO** — não existe campo próprio | (derivado de `address` + `gps_coordinates`) Endereço mal cadastrado faz o cliente chegar na porta errada | **Gestão de GMB** |
| **WhatsApp** | ❌ ausente (`grep wa.me` = **0 ocorrências**) | `booking_link`, `order_online_link`, `menu.link`, `website`, `posts[].link` (⚠️ `reservation{}` — **NÃO CONFIRMADO**, ver §2.2) | ⚠️ **parcial** — detecção por regex, **exige `type=place`** | Nenhum canal direto: todo contato passa por ligação, que ninguém atende. Base de clientes **não existe** | **Estratégia de WhatsApp + base de clientes** |
| **Reservar** | `reservar_uma_mesa` | `booking_link` | ✅ confirmado | Restaurante/clínica sem reserva perde a mesa/horário para quem tem link. Fila vira desistência | **Landing page com agendamento** |
| **Pedir comida / Delivery** | `pedir_on_line` | `order_online_link` | ✅ confirmado — **nomes diferentes nos dois engines** | Ou não faz delivery, ou só faz pelo app pagando ~27% de comissão. Pedido direto é **margem inteira** | **WhatsApp + pedido direto** |
| **Menu** | ❌ `null` no search | `menu{link,source}` | ✅ confirmado — **exige `type=place`** | Cliente não sabe o que você vende nem o preço antes de entrar. Ticket médio cai | **Landing page + gestão de GMB** |
| **Agendar** | — | — | 🔴 **NÃO CONFIRMADO** — provável colisão com `booking_link` | — | — |

> **`botao_agendar` é campo fixo `"nao_confirmado"` no schema.** Não foi observado em nenhuma chamada real. **Não inventar campo de API.**

### 2.1 ⚠️ `website` mente sobre "ter site"

Dos 11 `website` preenchidos na amostra real, **6 não eram site próprio**:

| Valor real de `website` | É site de verdade? | `site_tipo` |
|---|---|---|
| `instagram.com/casa.da.siria` | ❌ | `social` |
| `instagram.com/trevisogaleteriabrasilia/` | ❌ | `social` |
| `instagram.com/fast_nature?igsh=...` | ❌ | `social` |
| `instagram.com/bambubrasilcafebistro/` | ❌ | `social` |
| `facebook.com/LaBoutiquePadariaFrancesa` | ❌ | `social` |
| `pt-br.facebook.com/pages/Cozinha-das-Minas/...` | ❌ | `social` |
| `sites.google.com/view/donalenhamediterraneo?...link_in_bio...` | ⚠️ | `builder` |
| `agenciacreh.com.br/landingpages/santerestaurantes/` | ⚠️ LP de agência terceira | `terceiro` |
| `nonnaaugusta.com.br`, `manapoke.com.br`, `croissanterie.com.br` | ✅ | `proprio` |

**`tem_site = website != null` é FALSO** e produziria pitch errado na porta ("vi que você já tem site" para quem só tem Instagram).

| `site_tipo` | Definição | Pontos no score |
|---|---|---|
| `ausente` | `website` nulo | **20** |
| `social` | instagram.com / facebook.com | **15** |
| `builder` | sites.google / linktree / subdomínio Wix | **10** |
| `terceiro` | LP hospedada em domínio de agência | **8** |
| `proprio` | domínio próprio | **0** |

### 2.2 Detecção de WhatsApp — regex única

```regex
wa\.me|api\.whatsapp\.com
```

Aplicada, **nesta ordem**, aos campos **documentados** de `place_results`:

`website` → `booking_link` → `order_online_link` → `menu.link` → `posts[].link`

O campo `whatsapp_origem` registra em qual deles apareceu.

> 🔴 **`place_results.reservation{link,source}` — NÃO CONFIRMADO.** A versão anterior deste documento tratava esse campo como "a única fonte de WhatsApp". **Auditoria posterior não achou `reservation` (nem `reservations`) em nenhuma chave documentada de `place_results`** — a única ocorrência do termo na documentação é o valor de texto `"Accepts reservations"` dentro de `unsupported_extensions.planning`. O campo documentado equivalente é `booking_link`.
> **Procedimento de validação (1 crédito, na primeira rodada):** rodar `type=place` numa empresa que tenha botão de WhatsApp visível no Maps e fazer `grep -o '"reservation[s]*"' serpapi-raw.json`. Achou → reabilitar o campo e colar o trecho do JSON aqui como evidência. Não achou → remover `reservation` do enum de `whatsapp_origem` em definitivo.
> Enquanto não validar: o parser **tenta** `reservation.link` se a chave existir, mas **nunca assume** que ela existe, e `whatsapp_origem: "reservation"` não pode ser gravado sem o dump que o comprove.

**Não existe campo `whatsapp` dedicado.** Detectar WhatsApp obriga 1 chamada `type=place` por empresa — não tem atalho.

### 2.3 ⚠️ Chaves traduzidas com `hl=pt-br`

A SerpAPI **traduz as chaves do JSON**. Parser escrito só em inglês quebra em silêncio.

| Inglês (documentação) | pt-BR real | Bloco |
|---|---|---|
| `order_online` | `pedir_on_line` | `local_results` |
| `reserve_a_table` | `reservar_uma_mesa` | `local_results` |
| `service_options.dine_in` | `service_options.refeição_no_local` | ambos |
| `service_options.takeout` | `service_options.para_viagem` | ambos |
| `service_options.delivery` | `service_options.entrega` | ambos |
| `operating_hours.monday` | `operating_hours."segunda-feira"` | **só `local_results`** |
| `hours[].monday` | `hours[]."segunda-feira"` | **só `place_results`** (array de objetos de 1 chave) |
| `details.price_per_person` | `details.preço_por_pessoa` | reviews |
| `order_online_link` | *(permanece em inglês)* | `place_results` |
| chaves de `extensions[]` | *(permanecem em inglês; só os valores vêm em pt)* | ambos |

---

## 3. Score de oportunidade (0–100)

### 3.1 Filosofia — ICP e score são opostos de propósito

> **O ICP mede maturidade e verba: quem PODE comprar.**
> **O score mede dor e lacuna: o que HÁ para vender.**

Uma empresa que posta toda semana ganha **ICP alto** e **score baixo** no componente de conteúdo. **Isso não é bug** — é o desenho. Quem passa no ICP tem dinheiro; quem pontua alto no score tem problema. O lead ideal tem os dois.

### 3.2 Composição

| # | Componente | Pontos | Regra |
|---|---|---|---|
| 1 | **Lacuna de site** | 0–20 | `ausente` 20 · `social` 15 · `builder` 10 · `terceiro` 8 · `proprio` 0 |
| 2 | **Sem WhatsApp** | 0–15 | sem `wa.me` detectado → 15 · com → 0 |
| 3 | **Botões transacionais ausentes** | 0–15 | 5 pts por ausente entre {`menu`, `pedidos`, `reservar/agendar`} **aplicáveis ao nicho**. Nicho sem nenhum aplicável → 0 + nota `n/a` |
| 4 | **Não responde reviews** | 0–20 | 0% → 20 · 1–24% → 15 · 25–59% → 8 · ≥ 60% → 0 · **`null` → 8** |
| 5 | **Silêncio de conteúdo** | 0–10 | **faixas mutuamente exclusivas, avaliadas nesta ordem:** `posts_n == 0` **ou** `post_dias_desde > 365` → **10** · `181 ≤ post_dias_desde ≤ 365` → **5** · `post_dias_desde ≤ 180` → **0** · `post_dias_desde == null` (data ilegível) → **5** |
| 6 | **Perfil incompleto** | 0–10 | sem `phone` +4 · `horas_dias_preenchidos < 7` +3 · `extensions_n < 3` +3 |
| 7 | **Nicho quente** | 0–10 | quente 10 · morno 5 · frio 0 |
| | **Total** | **0–100** | |

**Toda empresa grava `score_componentes` com as 7 chaves.** Score sem decomposição não é auditável e o vendedor não sabe o que dizer na porta.

### 3.3 ⚠️ Incerteza material no componente 4

O campo `reviews[].response` (resposta do dono) é **documentado, mas foi observado 0 vez** nos 8 reviews reais puxados — a empresa testada simplesmente não responde ninguém.

**Antes de rodar o lote inteiro:** gastar **1 chamada de validação** numa empresa que comprovadamente responde reviews (conferir a olho no Maps antes). Se o campo não aparecer nem lá:

- `taxa_resposta = null` para todo mundo;
- componente 4 vira **8 pontos fixos para todos** (neutralizado, **sem redistribuir** para os outros componentes);
- o ranking continua válido, só perde um discriminante.

---

## 4. ICP — Índice de Cuidado com o Perfil {#icp}

Gate hard que **implementa a intenção** do filtro "descrição ≥ 500 caracteres" com os campos que existem de verdade (o campo literal não existe — ver [FILTROS.md §6](FILTROS.md)).

| # | Componente | Pontos | Campo confirmado |
|---|---|---|---|
| 1 | Post nos últimos **180 dias** | **3** | `place_results.posts[].date` |
| 1b | Tem post, mas > 180 dias (ou data ilegível) | 1 | idem |
| 2 | Perfil **reivindicado** (`unclaimed_listing` ausente) | **2** | `local_results.unclaimed_listing` |
| 3 | `extensions` com ≥ 6 chaves (3–5 → 1 pt) | **2** | `extensions[]` (já vem no `search`) |
| 4 | Horário com os **7 dias** preenchidos | 1 | `local_results.operating_hours{}` **ou** `place_results.hours[]` — **chaves diferentes por engine** |
| 5 | `phone` presente | 1 | `phone` |
| 6 | 🆕 **Texto longo escrito pelo dono** — `posts_texto_len_max ≥ 500` → **2** · `≥ 250` → 1 · abaixo/ausente → 0 | **2** | `place_results.posts[].description` |
| | **Máximo** | **11 → cap 10** | |

**Corte: `icp_score >= 5`.** Abaixo → Lista B (reserva), nunca descarte definitivo.
Calibrar no par 312/313 para aprovação de 25–45% e registrar o corte em `_meta.json`.

### 4.1 O que foi TIRADO do ICP, e por quê (correção de rota)

A primeira versão deste documento somava ao ICP dois componentes que são **sinais de classificação**, não de maturidade:

| Componente removido | Por que saiu |
|---|---|
| "≥ 1 botão transacional (`menu`/`booking_link`/`order_online_link`)" | Botão do GMB é **sinal de ranqueamento**, ordem literal do Pedro: *"não filtram, ranqueiam"*. Mantê-lo no gate punia com −1 ponto exatamente a empresa **sem WhatsApp e sem botão de pedido** — que vale +15/+15 no score de oportunidade e é o melhor alvo do funil. É a mesma inversão que o Pedro já tinha corrigido no caso do site. |
| "`rating ≥ 4,0` com `reviews ≥ 5`" | Volume de comentários é a **chave primária de classificação (P1/P2/P3)**, não critério de eliminação. Um P1 com 22 comentários e nota 3,8 é dor de reputação **vendável**, não motivo de corte. |

**Nada além de MEI, franquia grande, geografia e o ICP elimina.** `site_tipo`, botões, WhatsApp, rating e volume de comentários **nunca** entram no gate.

### 4.2 🆕 Componente 6 — o substituto fiel dos "500 caracteres"

> 💡 Medido: `posts[].description` traz textos de **312 a 633 caracteres escritos pelo dono**. **É ali que mora o "texto longo" que o Pedro queria medir** — não em `description`, que é blurb do Google com 151 caracteres no máximo.

Por isso o limiar do componente 6 é **exatamente o número do Pedro (500)**, aplicado ao campo certo:

```python
perfil_texto_500 = (posts_texto_len_max or 0) >= 500      # campo booleano no schema
icp_texto_dono   = 2 if perfil_texto_500 else (1 if (posts_texto_len_max or 0) >= 250 else 0)
```

- `perfil_texto_500` é gravado em **todo** registro (JSON e CSV), aprovadas e reprovadas.
- O `lote-report.md` traz obrigatoriamente a linha: *"N das X aprovadas passariam no critério literal de 500 caracteres (medido sobre `posts[].description`)."*
- O modo `/prospect-enhanced lote --estrito-500` transforma isso em **gate hard literal** (`perfil_texto_500 == true` ou reprova, `motivo_descarte: texto-abaixo-de-500`). **Não é o padrão** — é a opção para quando o Pedro quiser o critério ao pé da letra, com a advertência de que a taxa de aprovação despenca.

---

## 5. Taxonomia de nicho

### 5.1 Regras

- **1 nicho primário obrigatório** (`nicho`); secundários em `nicho_secundario`.
- **Fonte canônica: `type_ids`** (slug EN estável, ex.: `italian_restaurant`), mapeado por `data/nicho-map.json`. O campo `type`/`types` (pt-BR) é **volátil** e serve só para exibição.
- Sem match → `nicho: "outros"` + **gravar a string crua** para expandir a taxonomia depois. **Nunca forçar match.**
- **Nicho nunca elimina ninguém.** Só decide quem o vendedor visita às 9h e quem visita às 17h, se sobrar tempo.

### 5.2 Os 30 nichos canônicos, com gancho de venda

| # | Nicho (slug) | Temp. | Serviço Singular que vende melhor | Gancho de venda (1 frase) |
|---|---|---|---|---|
| 1 | `restaurante` | 🔥 | Gestão de GMB | "Quem procura 'almoço na 313 Norte' decide pelo Google em 15 segundos: quem tem foto do prato do dia e responde review sobe, quem não tem some — e você está competindo com o vizinho de porta." |
| 2 | `bar-boteco` | 🌤 | WhatsApp + base de clientes | "Seu movimento é quinta a sábado; com a lista de quem já veio, você enche a terça mandando uma mensagem às 17h — sem pagar um centavo de tráfego." |
| 3 | `padaria-confeitaria` | 🌤 | WhatsApp + base de clientes | "Bolo de aniversário é o produto mais previsível que existe: pega nome, telefone e mês de nascimento no caixa e você sabe hoje quantas encomendas vai ter em novembro." |
| 4 | `cafeteria` | 🌤 | Social media + GMB | "Café é decisão visual: se a sua foto no Google for de 2019, o cliente vai no que tem foto de ontem." |
| 5 | `lanchonete-fast-food` | 🌤 | GMB + WhatsApp | "80% do seu pedido é por delivery e você paga 27% de comissão pro app — pedido direto no WhatsApp é margem inteira sua." |
| 6 | `doceria-sorveteria` | 🌤 | Social media | "Doce vende por impulso e impulso mora no feed; sem post, você só vende pra quem já passa na porta." |
| 7 | `salao-de-beleza` | 🔥 | WhatsApp (agendamento + recall) | "Cliente que corta a cada 30 dias e some no 45º não trocou de salão — ela só esqueceu; uma mensagem no dia 28 resolve." |
| 8 | `barbearia` | 🔥 | Landing page + WhatsApp | "Barbearia vive de recorrência semanal: link de agendamento no perfil do Google tira o 'vou ligar depois' da equação." |
| 9 | `estetica-depilacao` | 🔥 | Landing page + social media | "Procedimento estético se vende por antes/depois e prova social; sem página pra mandar o link, cada dúvida vira uma conversa de 20 minutos que você não tem." |
| 10 | `clinica-odontologica` | 🔥 | Landing page + gestão de GMB | "Paciente de plano pesquisa 'dentista Asa Norte' e liga pro primeiro com avaliação boa e review respondido — hoje esse primeiro não é você." |
| 11 | `clinica-medica-consultorio` | 🔥 | Landing page institucional + GMB | "Sua credibilidade está toda no boca a boca; quem te indica manda o nome, e quem recebe o nome joga no Google — o que aparece lá é o que fecha ou não fecha." |
| 12 | `psicologia-terapia` | 🌤 | Landing page + GMB | "Ninguém liga pra psicólogo direto: lê a página, sente confiança, e só aí chama no WhatsApp." |
| 13 | `fisioterapia-pilates` | 🌤 | Landing page + WhatsApp | "Pacote de 10 sessões só se vende com página que explica o método e o preço — no balcão, o cliente pede pra pensar." |
| 14 | `academia-crossfit` | 🌤 | Social media + base de clientes | "Academia perde 40% dos alunos entre janeiro e abril; a base de ex-alunos é a matrícula mais barata que existe." |
| 15 | `pet-shop` | 🔥 | WhatsApp (recorrência) | "Banho e tosa tem ciclo de 21 dias — quem lembra o dono no dia 18 fica com o cachorro." |
| 16 | `clinica-veterinaria` | 🌤 | GMB + landing page | "Emergência com pet é busca no Google às 22h: quem aparece com horário atualizado e telefone certo atende, o resto perde." |
| 17 | `escola-de-idiomas` | 🔥 | Landing page + social media | "Sua matrícula é sazonal (jan/jul): a landing page com formulário roda captando lead o ano inteiro, não só na semana da campanha." |
| 18 | `escola-curso-livre` | 🌤 | Landing page + WhatsApp | "Curso se compra por informação: quem não tem página com grade, preço e duração perde pro concorrente que tem." |
| 19 | `otica` | 🌤 | Landing page + GMB | "Óculos é compra pesquisada; sem vitrine online, o cliente compara preço com o shopping e você nem entra na conta." |
| 20 | `farmacia-manipulacao` | 🧊 | WhatsApp | "Fórmula manipulada é recorrente por definição: quem manda 'sua fórmula acaba semana que vem' não perde renovação." |
| 21 | `imobiliaria` | 🌤 | Landing page + social media | "Imóvel se vende com página por imóvel; PDF no WhatsApp mata o interesse antes da visita." |
| 22 | `advocacia` | 🧊 | Landing page institucional | "Cliente de honorário alto pesquisa o escritório antes de marcar; sem site, você parece menor do que é." |
| 23 | `contabilidade` | 🧊 | Landing page + WhatsApp | "Seu cliente troca de contador por preço; quem tem página explicando o que entrega troca por valor." |
| 24 | `lavanderia` | 🧊 | WhatsApp | "Aviso de 'está pronto' pelo WhatsApp reduz peça parada no balcão e cria o gancho pra próxima entrega." |
| 25 | `papelaria-grafica` | 🧊 | GMB + landing page | "Volta às aulas e época de licitação são picos previsíveis: quem aparece no Google nessas 6 semanas fatura o ano." |
| 26 | `floricultura` | 🌤 | Social media + WhatsApp | "Dia das Mães, Namorados e Finados são 40% do seu ano — a base de clientes é o que transforma data em pedido antecipado." |
| 27 | `loja-de-roupas-acessorios` | 🌤 | Social media + base de clientes | "Grupo de WhatsApp com foto da peça nova vende antes de a arara chegar na loja." |
| 28 | `oficina-autocenter` | 🧊 | GMB + landing page | "Carro quebrado é busca por proximidade: 'mecânico perto de mim' é uma disputa de perfil do Google, não de placa na rua." |
| 29 | `mercearia-emporio-adega` | 🧊 | WhatsApp + delivery direto | "Seu cliente é do prédio da frente e pede pelo app pagando taxa; o pedido direto no WhatsApp entrega em 10 minutos e sem comissão." |
| 30 | `servicos-diversos` (chaveiro, costureira, assistência técnica) | 🧊 | Gestão de GMB | "Serviço de urgência se resolve na primeira busca do Google; se seu horário está errado no perfil, o cliente vai no próximo da lista." |

### 5.3 Ranking de temperatura

**Critérios do "quente":** (1) ticket compatível com R$ 500–2.000/mês · (2) dor mensurável em receita perdida · (3) decisor presente no balcão em horário comercial · (4) resultado visível em ≤ 30 dias — o que sustenta a renovação.

#### 🔥 QUENTE (+10 no score) — atacar primeiro

| Nicho | Por quê |
|---|---|
| `clinica-odontologica` | Ticket alto por paciente; **1 paciente novo já paga o serviço** |
| `estetica-depilacao` | Vive de imagem e prova social; compra rápido, sem comitê |
| `restaurante` | Volume de busca local absurdo, dor visível, e o dono está lá na hora do almoço |
| `salao-de-beleza` | Recorrência natural + agenda ociosa mensurável; o argumento do WhatsApp fecha na primeira conversa |
| `pet-shop` | Recorrência de 21 dias, dono presente, base de clientes com valor óbvio |
| `clinica-medica-consultorio` | Alta margem e alta sensibilidade a reputação online; paga bem por credibilidade |
| `escola-de-idiomas` (independente) | Sazonalidade dolorosa que a landing page resolve; verba de marketing já existe |
| `barbearia` | Ciclo semanal, público jovem, adere a agendamento digital sem resistência |

#### 🌤 MORNO (+5) — vale, mas exige mais visita

`padaria-confeitaria` · `bar-boteco` · `cafeteria` · `academia-crossfit` · `clinica-veterinaria` · `otica` · `imobiliaria` · `fisioterapia-pilates` · `psicologia-terapia` · `loja-de-roupas-acessorios` · `doceria-sorveteria` · `lanchonete-fast-food` · `escola-curso-livre` · `floricultura`

**Motivo comum:** a dor existe e o dinheiro também, mas o ciclo é mais longo — ou o dono não está na loja no horário da rota (`imobiliaria`, `psicologia-terapia`), ou o resultado demora mais de um mês para ficar óbvio (`academia-crossfit`, `otica`).

#### 🧊 FRIO (0) — não priorizar na rota

| Nicho | Por quê |
|---|---|
| `advocacia` | Compra por indicação, decisão em sociedade, aversão a "marketing"; ciclo longo e limite ético |
| `contabilidade` | Compra pelo menor preço e acha que resolve internamente |
| `papelaria-grafica` | Margem apertada e se vê como concorrente do serviço ("eu faço site também") |
| `oficina-autocenter` | Baixa disposição a pagar mensalidade digital; prefere placa e indicação |
| `mercearia-emporio-adega` | Margem baixíssima; o ticket de serviço não cabe |
| `lavanderia` | Negócio pequeno, muitas vezes MEI — costuma morrer no **gate de MEI** (`opcao_mei`) antes de chegar aqui. ⚠️ **Não existe gate de porte**: porte NÃO é proxy de MEI (ver `FONTES-CNPJ.md §3.3`) |
| `farmacia-manipulacao` | Ou é rede (corta no gate de franquia), ou é regulada demais para copy livre |
| `servicos-diversos` | Heterogêneo demais para padronizar abordagem; tratar caso a caso, nunca como bloco |

---

## 6. Problema → Serviço → Argumento de venda

Evolução da tabela da v1. O **argumento do aniversário** (linha 2) é patrimônio do método e vai literal, do jeito que o Pedro faz questão.

| # | Problema detectado | Sinal técnico que dispara | Serviço Singular | Argumento de venda (falar assim, na porta) |
|---|---|---|---|---|
| 1 | **Não tem site** | `site_tipo = ausente` | Criação de landing page | "Quando alguém te acha no Google e quer saber preço, horário ou o que você faz, não tem pra onde mandar. A pessoa desiste ali. Uma página só sua resolve isso, e o link vai no perfil do Google, no Instagram e na assinatura do WhatsApp." |
| 2 | **Não tem WhatsApp no perfil / não tem base de clientes** | `botao_whatsapp = false` | Estratégia de WhatsApp + base de clientes | **"Você sabe quantos aniversários de cliente seu passam por mês sem você mandar nada? Cada um desses é uma venda que estava pronta e você deixou passar. A gente monta a base com nome, telefone e data, e no dia certo sai a mensagem. Não é propaganda, é lembrança — e lembrança vende."** |
| 3 | **Só tem Instagram como "site"** | `site_tipo = social` | Landing page + social media | "Seu Instagram é aluguel: o alcance é do Instagram, não seu. A página é sua, aparece no Google e não some se a conta cair." |
| 4 | **Não responde review** | `taxa_resposta = 0` | Gestão de GMB | "Quem lê uma reclamação sem resposta entende que você não se importa. Quem lê a sua resposta entende que você resolve. É o mesmo review, e muda o cliente que entra." |
| 5 | **Perfil parado, sem post** | `post_dias_desde > 180` ou `posts_n = 0` | Gestão de GMB + social media | "O Google mostra primeiro quem se mexe. Perfil parado há seis meses o próprio Google entende como negócio parado, e te empurra pra baixo do vizinho." |
| 6 | **Perfil incompleto** (sem telefone, horário ou atributos) | `horas_dias_preenchidos < 7`, `phone = null`, `extensions_n < 3` | Gestão de GMB | "Cliente chegou na sua porta num domingo porque o Google diz que você abre. Ele não volta na segunda — ele vai no concorrente que tem o horário certo." |
| 7 | **Sem botão de pedido / menu** (comida) | `botao_pedidos = false`, `botao_menu = false` | WhatsApp + pedido direto | "Você paga até 27% pro aplicativo em cada pedido. O mesmo cliente, pedindo direto no seu WhatsApp, é margem inteira sua — e o telefone dele fica com você, não com o app." |
| 8 | **Sem reserva / agendamento** | `botao_reservar = false` no nicho aplicável | Landing page com agendamento | "Todo 'depois eu ligo' é um cliente que não liga. Link de agendamento fecha na hora em que a pessoa está com vontade." |
| 9 | **Perfil não reivindicado** | `unclaimed_listing = true` | Reivindicação + gestão de GMB | "Esse perfil aparece no Google e não é seu. Qualquer um pode sugerir mudança de horário, de endereço, de telefone. Reivindicar leva uma semana e trava isso." |
| 10 | **Nota baixa com volume bom** | `rating < 4,0` e `reviews >= 20` | Gestão de GMB + reputação | "Você tem movimento, o problema não é cliente — é que a nota está contando uma história pior do que a real. Isso se corrige respondendo e pedindo avaliação de quem sai satisfeito." |
| 11 | **Site de agência terceira / builder** | `site_tipo ∈ {terceiro, builder}` | Landing page própria | "Sua página está hospedada no domínio de outra empresa. Se a relação com eles acabar, o link morre e o Google perde o histórico." |
| 12 | **Sazonalidade não trabalhada** | nicho com pico previsível (floricultura, papelaria, escola de idiomas) | WhatsApp + campanha sazonal | "Você já sabe qual é a sua semana do ano. O que falta é avisar quem já comprou, quinze dias antes — sem isso, você depende de quem lembrar sozinho." |

### Serviços que NÃO fazem sentido (dizer isso ganha confiança)

| Situação | Não oferecer | Por quê |
|---|---|---|
| Empresa com site próprio recente e bem feito | Landing page | Oferecer o que ele já tem queima a conversa inteira |
| Perfil com posts semanais e reviews respondidos | Gestão de GMB básica | Ele já faz — ofereça social media ou campanha, não o básico |
| Nicho regulado (`farmacia-manipulacao`, saúde) | Copy agressiva de promoção | Restrição de conselho profissional |
| MEI que passou por engano no gate | Qualquer pacote mensal | Ticket não fecha; anotar e seguir |

---

## 7. Como o vendedor lê o ranking

```
1º  P1 · score 78 · Nonna Augusta       38 reviews · sem WhatsApp · sem post há 8 meses
2º  P1 · score 71 · Clínica X           27 reviews · só Instagram · não responde review
...
    ────────────────── fim dos P1 ──────────────────
18º P2 · score 84 · Restaurante Y      213 reviews · sem site
```

**Regra de leitura do ranking:** esgotar **todos** os P1 antes de tocar num P2, mesmo que um P2 tenha score maior. O score alto de um P2 significa que há muito a vender lá — mas o P1 é onde a venda **fecha no balcão**, que é a razão de existir da rota a pé.

### 7.1 ⚠️ Ranking ≠ ordem de caminhada

A regra acima ordena o **relatório**. Ela **não** ordena os passos do vendedor: aplicada literalmente a uma rota a pé, ela faz atravessar a entrequadra cinco vezes.

| Decisão | Quem manda |
|---|---|
| **Ordem de caminhada** | **Geografia.** Bloco A → B → C → D → E de uma face, depois a face oposta da entrequadra, sem voltar. |
| **Quanto tempo gastar em cada porta** | **Prioridade.** P1 = entra, pede o dono, faz o roteiro completo (até ~10 min). P2 = deixa cartão e faz a pergunta de qualificação (~3 min). P3 = só se sobrar tempo no fim do par. |
| **Quem pula** | `revisar_manual: true` só depois de confirmar o dado. |

**Formato obrigatório de cada parada** (é o que o vendedor lê no celular andando):

```
Bloco C · Lj 14 · 🥇P1 · Padaria Santa Clara · 41 coment. · gancho: sem WhatsApp · janela 14h-17h
```

**Regra da janela (`{{MELHOR_HORARIO}}`), derivada de `operating_hours`/`hours` + nicho:**

| Nicho | Janela | Motivo |
|---|---|---|
| `restaurante`, `lanchonete-fast-food`, `bar-boteco`, `padaria-confeitaria` | **14h–17h** | fora do pico de almoço (11h30–14h30); o dono só conversa depois de fechar a praça |
| `clinica-odontologica`, `clinica-medica-consultorio`, `psicologia-terapia`, `fisioterapia-pilates` | **8h–10h** | antes do primeiro paciente; depois disso a agenda trava |
| `salao-de-beleza`, `barbearia`, `estetica-depilacao` | **10h–12h, terça a quinta** | evitar sexta e sábado (pico) e segunda (muitos fecham) |
| `academia-crossfit` | **14h–16h** | entre os picos de 6h–9h e 18h–21h |
| demais | **10h–12h ou 14h–17h** | horário comercial padrão |

**Interseção obrigatória com o horário real:** a janela sugerida é cortada pelo `operating_hours`/`hours` do dia. Se não sobrar interseção (ou o horário estiver ausente), gravar `{{MELHOR_HORARIO}} = "confirmar no local"` — **nunca chutar horário**.

---

*Documento gerado por /prospect-enhanced — Singular Group*
*[Registrado por: DESKTOP — 2026-08-10]*

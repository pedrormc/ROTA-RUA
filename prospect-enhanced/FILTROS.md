---
title: "FILTROS — funil de gates do /prospect-enhanced"
skill: prospect-enhanced
versao: "1.0"
bu: consultorio-comercial
created: "2026-08-10"
updated: "2026-08-10"
---

# FILTROS — o funil em gates

**Princípio único que governa este documento:**

> **Gate barato corta primeiro. Ausência de dado nunca reprova — exceto no gate geográfico.**

O único gate com custo **por empresa** é o G8 (`type=place`, 1 crédito cada). Todo o resto é bulk ou grátis. Logo, a única pergunta que importa é: **quantas empresas chegam ao G8?**

---

## 1. Diagrama do fluxo

```
                        ┌─────────────────────────────────────────┐
                        │  G0  ROSTER CNPJ (offline, $0 SerpAPI)  │
                        │  36 CEPs → Casa dos Dados → OpenCNPJ    │
                        │  856 ativas  →  575 não-MEI             │
                        └────────────────────┬────────────────────┘
                                             │ (fica em disco, TTL 30 dias)
                                             ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  G1  COORDENADAS DOS PARES                          $SERP ~4  (cache eterno) │
│      310/311 ? · 312/313 confirmado · 314/315 fraco  →  zoom fixo 18z        │
└────────────────────────────────────┬─────────────────────────────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  G2  DISCOVERY GMB                                       $SERP 60–90          │
│      3 pares × 10 queries × 2–3 páginas  →  ~500 resultados brutos           │
│      dump literal em _raw/ ANTES de qualquer parse                            │
└────────────────────────────────────┬─────────────────────────────────────────┘
                                     ▼
      ┌──────────────────────────────────────────────────┐
      │  G3  DEDUP por place_id (set global do LOTE)  $0 │   ~500 → ~300
      └──────────────────────┬───────────────────────────┘
                             ▼
      ┌──────────────────────────────────────────────────┐
      │  G4  GEO 310–315  regex → GPS → CEP     HARD  $0 │   ~300 → ~220
      └──────────────────────┬───────────────────────────┘   ✂ fora-do-escopo
                             ▼
      ┌──────────────────────────────────────────────────┐
      │  G5  FRANQUIA barata: blacklist + padrão  HARD $0│   ~220 → ~200
      └──────────────────────┬───────────────────────────┘   ✂ franquia (+ SUSPEITOS)
                             ▼
      ┌──────────────────────────────────────────────────┐
      │  G6  MEI / PORTE  (join com o roster)     HARD $0│   ~200 → ~140
      └──────────────────────┬───────────────────────────┘   ✂ mei
                             ▼
      ┌──────────────────────────────────────────────────┐
      │  G7  FRANQUIA por contagem de unidades  $SERP ~20│   ~140 → ~120
      │      1 chamada por MARCA, cacheada 90 dias       │   ✂ rede ≥5 DF / ≥10 BR
      └──────────────────────┬───────────────────────────┘
                             ▼
  ╔══════════════════════════════════════════════════════════╗
  ║  G8  type=place  —  $SERP 1 POR EMPRESA  ≈120            ║  ← O GASTO DOMINANTE
  ║  ordem interna: P1 previsto → P2 → P3                    ║
  ║  única fonte de: WhatsApp, menu, posts, botões           ║
  ╚══════════════════════════┬═══════════════════════════════╝
                             ▼
      ┌──────────────────────────────────────────────────┐
      │  G9  ICP ≥ 5  (inclui os 500 chars do dono) HARD $0│  ~120 → ~55 aprovadas
      └──────────────────────┬───────────────────────────┘   ↘ Lista B (reserva)
                             ▼
      ┌──────────────────────────────────────────────────┐
      │  G10 REVIEWS / taxa de resposta          $SERP ~75│  só aprovados
      └──────────────────────┬───────────────────────────┘
                             ▼
      ┌──────────────────────────────────────────────────┐
      │  G11 CLASSIFICAÇÃO: P1/P2/P3 + score + ranking $0│  → funil.csv + lote-report.md
      └──────────────────────────────────────────────────┘
```

---

## 2. Tabela mestra dos gates

Legenda de custo: **`$0`** = zero chamada paga · **`$SERP`** = crédito SerpAPI · **`$free`** = API gratuita com rate limit.

| Gate | Critério exato | Hard/Soft | Custo | Ação quando o dado está AUSENTE |
|---|---|---|---|---|
| **G0** Roster CNPJ | Baixar **todas** as `situacao_cadastral: ATIVA` dos 36 CEPs. Sem filtro de MEI no servidor | preparo | `$0` + `$free` | CEP com `total: 0` → registra `cep_vazio` em `roster-meta.json` e **segue**. Não aborta |
| **G1** Coordenadas | Centróide dos `gps_coordinates` de resultados cujo `address` casa a regex da quadra. Exigir **≥ 4 âncoras**. Zoom `18z` | preparo | `$SERP` ~4 | Não fechou 4 âncoras em 2 tentativas → rodar discovery daquele par **sem `ll`**, só com `q="CLN 310 Norte Brasília {categoria}"`, e apertar o G4. **Nunca chutar coordenada** |
| **G2** Discovery | `engine=google_maps`, `ll={centroide}`, `hl=pt-br`, `gl=br`, `start` de 20 em 20. 10 queries fixas por par. 3ª página só se a 2ª voltou cheia. Teto `start=100` | preparo | `$SERP` 60–90 | Query sem resultado → registra e segue para a próxima |
| **G3** Dedup | Chave primária `place_id`, secundária `data_id`. Fuzzy: `normalizar(title)` igual **E** (telefone igual **OU** haversine < 40 m) | técnico | `$0` | Sem `place_id` → chave `sha1(title_normalizado + gps_5_casas)`, `geo_confianca: baixa` |
| **G4** Geo 310–315 | Regex sobre `address` (§4) → quadra. Fallback GPS ≤ 250 m do centróide. CEP como sinal **secundário** | 🔴 **HARD** | `$0` | **Sem `address` E sem `gps` → REPROVA.** Único caso do funil em que ausência corta |
| **G5** Franquia barata | Match de prefixo em `blacklist-redes.json` (nunca `contains`). Marca `NAC`/`DF` → corta. Marca com `?` → `SUSPEITO`. Padrão `unidade\|filial\|franquia\|matriz` → `SUSPEITO` | 🔴 **HARD** parcial | `$0` | Sem `title` → impossível (já teria caído no G3) |
| **G6** MEI / porte | `eh_mei = (opcao_mei=="S") AND (data_exclusao_mei ∈ {vazio,null,"0000-00-00"})`. Passa se `eh_mei == false` **e** (`porte_codigo` é `null` **ou** ∈ {00,01,03,05}) | 🔴 **HARD** | `$0` | **PASSA** com `mei_incerto: true` e flag "confirmar CNPJ na visita". `porte_codigo` ausente **nunca reprova**. Ver §5.1 e §5.3 |
| **G7** Franquia por contagem | 1 chamada **por marca**: `engine=google_maps`, **`type=search`**, `q="{marca}"`, `ll="@-15.7801,-47.9292,11z"`. Contar `place_id` distintos no DF. **Corte: ≥ 5 no DF ou ≥ 10 no BR** | 🔴 **HARD** | `$SERP` ~20 | Contagem falhou (erro de API) → `franquia_veredito: SUSPEITO`, **não reprova**, `revisar_manual: true` |
| **G8** Enriquecimento | `engine=google_maps, type=place, place_id={id}`, `mode="complete"`. Ordem interna: P1 → P2 → P3 | preparo | `$SERP` **1/empresa** | `place_results` vazio ou erro → 1 retry. Persistindo: `place_status: falhou`, `botao_*: null`, **mantém no funil** com ICP de **teto 6** (só componentes 2,3,4,5) e corte proporcional **≥ 3** → Lista B |
| **G9** ICP | `icp_score >= 5` aprova. 6 componentes, máx. 11 pontos com cap em 10 (§6) | 🔴 **HARD** | `$0` | `place_status: falhou` → ICP só sobre os componentes 2,3,4,5 (máx. **6**), corte proporcional **≥ 3**. Nunca zerar por falha de API |
| **G10** Reviews | `engine=google_maps_reviews, data_id={id}`. 1ª página = 8 reviews. 2ª página só para P1 | soft | `$SERP` ~75 | < 3 reviews ou campo `response` ausente → `taxa_resposta = null` e componente 4 do score = **8 fixo**. Não reprova nada |
| **G11** Classificação | `ORDER BY prioridade, score DESC, reviews DESC, title ASC` | — | `$0` | — |

---

## 3. 🟢 O QUE **NÃO** ELIMINA

Esta seção existe porque a v1 errou exatamente aqui, e o Pedro corrigiu de forma explícita.

| Sinal | Na v1 | Na v2 | Por quê |
|---|---|---|---|
| **Não ter site** | Score 0/10 = penalidade. Em CLN 314, **14 de 21 lojas** caíram no ranking por isso | ✅ **Nunca reprova, nunca penaliza.** `site_tipo: ausente` **soma 20 pontos** no score de oportunidade | Ordem direta do Pedro: *"sem site pode trazer que a gente faz depois, é um bom cliente"*. Falta de site é **oportunidade de landing page**, não defeito |
| **Ter só Instagram/Facebook** | Contava como "tem site" (`website != null`) | ✅ `site_tipo: social` → **15 pontos** no score | Medido: **6 dos 11 `website` preenchidos não eram site próprio** (4 Instagram, 2 Facebook). `tem_site = website != null` é falso e produziria pitch errado na porta |
| **Não ter WhatsApp** | Não era capturado | ✅ Nunca reprova. Ausência = **15 pontos** no score | É o produto "Estratégia de WhatsApp" pronto para vender |
| **Nota baixa (rating)** | Entrava no score de qualidade | ✅ **Nunca reprova.** Só participa de 1 ponto do ICP (rating ≥ 4,0 com ≥ 5 reviews) | Nota baixa é dor real e argumento de venda de gestão de GMB, não motivo de descarte |
| **Poucos comentários** | Analisava igual (Cotton UP com 1 review consumiu orçamento) | ✅ Não reprova — **classifica como P3** | Ausência não reprova; só não promove |
| **Perfil não reivindicado** | Não era capturado | ⚠️ Reprova no ICP, **mas vai para a Lista B** com `oportunidade_claim: true` e é o **primeiro grupo readmitido no degrau R2** | Tensão real e honesta: pelo critério do Pedro (maturidade) é imaturo; pelo critério de venda, reivindicar o perfil é serviço vendável |
| **Rede local de 3–4 unidades** | Não era detectado | ✅ **MANTÉM sem penalidade** | É frequentemente o **melhor lead do lote**: tem caixa (provou o modelo), tem dor real (3 GMBs na mão é insuportável) e permite vender o mesmo serviço 3–4 vezes numa negociação só |
| **CNPJ não resolvido** | Não existia | ✅ **PASSA** com `mei_incerto: true` | O vendedor vai à porta de qualquer jeito e confirma no balcão em 10 segundos. Custo de 1 `place` errado (1 crédito) << custo de descartar lead bom |
| **Empresa aberta há < 60 dias** | — | ✅ **PASSA** com `mei_incerto: true` | Defasagem declarada de até 45 dias nos dados do Simples. Caso real observado: CNPJ `68.150.540/0001-95` |
| **Ex-MEI (`data_exclusao_mei` preenchida)** | — | ✅ **PASSA** | Ignorar esse campo descartaria exatamente o lead que **acabou de crescer** |
| **Nicho frio** | — | ✅ Nunca elimina — só decide se o vendedor visita às 9h ou às 17h | Nicho pesa 0–10 no score de oportunidade, e só |
| **`description` do Google curta ou ausente** | Seria o filtro hard #2, lido no campo errado | ✅ **Não é gate.** Esse campo é blurb editorial do Google (máx. 151 chars), não texto do dono (§6.1) | Rodar o gate sobre `description` reprovaria 100% das empresas |
| **Texto do dono curto** (`posts_texto_len_max < 500`) | — | ⚠️ **Não reprova sozinho, mas pontua no gate:** é o **componente 6 do ICP** (2 pts em ≥ 500, 1 pt em ≥ 250) e grava `perfil_texto_500`. No modo `--estrito-500` vira **gate hard literal** | É a leitura fiel do filtro #2 do Pedro, no campo certo (`posts[].description`, 312–633 chars reais) — ver §6.2 |

---

## 4. Gate geográfico (G4) — o único onde ausência reprova

### Regex canônica sobre `address`

```regex
(?i)(SCLRN|SHCN(/CL)?|SCLN|CLN|Com[ée]rcio\s+Local\s+Norte|Quadra|Qd)\D{0,15}\b(310|311|312|313|314|315)\b
```

Ela cobre os sete formatos reais observados numa mesma amostra:

```
Asa Norte Comércio Local Norte 313, BL C
SHCN CLN 312, BL B Lj 29
SHCN/CL Qd 413 Bloco A Lojas 40, 34, 36...
CLN Quadra 413, Lj 20 - Térreo
St. Shcn Comercio Local 313 Bloco A, 37
SCLRN Quadra 713 Bloco E
BL A - Cln 313 Norte Loja 25
BL A Loja 45, Plano Piloto          ← SEM QUADRA NENHUMA
```

### Cascata de critérios

| # | Critério | Resultado | `geo_metodo` | `geo_confianca` |
|---|---|---|---|---|
| 1 | Regex casou no `address` | `quadra` = grupo capturado | `regex` | **alta** |
| 2 | Regex falhou, mas GPS ≤ **250 m** do centróide do par | `quadra: null`, `par` = do centróide | `gps` | media |
| 3 | Registro casou no roster e o CEP está na tabela dos 36 | `quadra` do CEP | `cep` | media |
| — | Nenhum dos três | **REPROVA** `motivo_descarte: fora-do-escopo` | — | — |

**Conflito regex × GPS** (regex diz 313, GPS diz 314): vence o **regex do `address`**. Grava `geo_conflito: true`, `par_alt` com o par do GPS e `revisar_manual: true`.

**CEP é sinal secundário, nunca gate único** — `70297` apareceu tanto em 413 quanto em 713. Há exceções.

### Por que ausência reprova aqui, e só aqui

Sem geo, a empresa **não pode ser visitada a pé** — que é a razão de existir do ROTA-RUA. Não é rigor metodológico, é impossibilidade física.

### O descarte é persistido

Empresa reprovada no G4 **grava linha no `funil.csv`** com `status: reprovado` e `motivo_descarte: fora-do-escopo`. Isso impede repesquisar e pagar de novo na próxima rodada.

---

## 5. Gate MEI / porte (G6) — o hard #1 do Pedro, e custa R$ 0

### 5.1 A fórmula

```python
eh_mei = (opcao_mei == "S") and (data_exclusao_mei in (None, "", "0000-00-00"))
passa  = (eh_mei is False) and (porte_codigo is None or porte_codigo in {"00","01","03","05"})
```

> 🔴 **Duas armadilhas já corrigidas aqui — não reintroduzir:**
> 1. **`data_exclusao_mei` vem `"0000-00-00"`, não vazio.** A OpenCNPJ devolve literalmente `"data_exclusao_mei":"0000-00-00"` para quem nunca saiu do MEI. Escrever `not data_exclusao_mei` faz `eh_mei` dar `False` **para todo MEI** e o filtro hard #1 do Pedro deixa de existir. A comparação tem que ser contra o conjunto `{None, "", "0000-00-00"}`.
> 2. **`porte_codigo` ausente NÃO reprova.** O conjunto `{00,01,03,05}` contém *todos* os códigos que existem, então essa cláusula nunca corta MEI nenhum — ela só dispararia quando o porte viesse `null`, contrariando a regra "ausência de dado nunca reprova". O `is None` explícito conserta isso. Porte com valor **não-nulo e fora do conjunto** (lixo de cadastro) → `motivo_descarte: porte-invalido` + `revisar_manual: true`.
>
> ⚠️ **`porte_codigo` é campo DERIVADO, não campo de API.** Nenhuma fonte devolve `porte_codigo`: a OpenCNPJ devolve `porte_empresa` (string), a BrasilAPI devolve `codigo_porte` (int) e a CNPJá devolve `company.size.{id,acronym}`. A tabela de mapeamento obrigatória está em [FONTES-CNPJ.md §3.3.1](FONTES-CNPJ.md). Sem esse mapeamento o gate compara string contra código e **reprova o lote inteiro depois de ~335 créditos gastos.**

Porte oficial da Receita (não existe 02 nem 04):

| Código | Label |
|---|---|
| `00` | Não informado |
| `01` | Micro empresa |
| `03` | Empresa de pequeno porte |
| `05` | Demais |

### 5.2 ⚠️ `porte = MICRO EMPRESA` **NUNCA** equivale a MEI

Provado empiricamente no CEP 70766-530 (CLN 313 Bloco C):

```
ativas                        = 23
porte 01 (micro empresa)      = 20
MEI optante                   = 13
não-MEI                       = 10   ← 20 micros, mas só 13 são MEI
```

**Quem usar porte como proxy de MEI descarta ~35% de leads bons.** Quem filtra é a flag `opcao_mei`, e só ela.

**Heurística proibida:** razão social no padrão `NN.NNN.NNN NOME DE PESSOA` é **indício**, nunca prova. Caso real que quebra a heurística: `68.150.540/0001-95`, razão social no padrão clássico de MEI, aparece com `simei.optant = false`.

### 5.3 Ausente ≠ reprovado — os 5 casos

| Caso | Decisão | Justificativa |
|---|---|---|
| `cnpj_confianca = nao_resolvido` | **PASSA** com `mei_incerto: true`, `nivel_admissao: base` | ~15% do funil ≈ 20 chamadas de `place`. O vendedor vai à porta de qualquer jeito |
| `cnpj_confianca = baixa` (similaridade 0,60–0,85) | **PASSA**, entra na fila de revisão manual antes da rota | idem |
| Empresa aberta há **< 60 dias** | **PASSA** com `mei_incerto: true` | Defasagem de até 45 dias nos dados do Simples |
| `opcao_mei = "S"` **com** `data_exclusao_mei` preenchida | **PASSA** (ex-MEI virou ME/EPP) | Ignorar isso descarta o lead que acabou de crescer |
| `opcao_mei = "S"` **sem** exclusão | 🔴 **REPROVA**, `motivo_descarte: mei` | Filtro hard do Pedro |

Fonte canônica: **OpenCNPJ**. Gravar `cnpj_fonte` e `cnpj_consultado_em` em todo registro — foi medida divergência real entre OpenCNPJ e CNPJá (CNPJ `45.404.836/0001-90`, campo `simples`). **Duas fontes não são intercambiáveis.**

Detalhe completo da cascata de matching (nome → telefone → nº de loja → CNAE → manual) em [FONTES-CNPJ.md](FONTES-CNPJ.md).

---

## 6. Gate ICP (G9) — como o filtro dos 500 caracteres foi implementado

> ⚠️ **Decisão que é do Pedro, não dos builders.** O filtro hard #2 pedido foi *"descrição do GMB com no mínimo 500 caracteres"*. O campo literal onde ele imaginou esse texto (`description`) **não serve** — está medido em §6.1. O que este documento faz é **aplicar o número 500 ao campo certo** (`posts[].description`, texto escrito pelo dono, 312–633 chars reais), como **componente 6 do ICP** e como **modo opcional de gate literal** (`--estrito-500`).
> Enquanto o Pedro não bater o martelo, o padrão é: quem tem texto curto **não vai para o lixo, vai para a Lista B**.

### 6.1 Por que não dá para usar o campo `description`

**O campo não existe.** Medido em 20 resultados reais da CLN 313:

- `description` está **ausente em 12 de 20** (60%);
- o **maior** valor observado tem **151 caracteres**;
- `type=place` não melhora (em um caso veio **mais curta**: 109 vs 146);
- o conteúdo é blurb editorial do Google, não texto do dono: *"Comida mineira em ambiente familiar. Destaque à costelinha suína, feijão tropeiro..."*;
- `extensions[].from_the_business` **não é** a descrição — é array de atributos (`["Se identifica como uma empresa de empreendedoras"]`).

Rodar o gate sobre `description` reprovaria **100%** e queimaria o lote. O texto do dono existe — só que em `posts[].description` (§6.2, componente 6).

### 6.2 A composição do ICP

Intenção original do Pedro: *"descrição longa prova que o dono cuida do perfil e entende valor de presença digital = tem verba e maturidade pra comprar."*

| # | Componente | Pontos | Campo (confirmado por chamada real) |
|---|---|---|---|
| 1 | Post nos últimos **180 dias** | **3** | `place_results.posts[].date` |
| 1b | Tem post, mas > 180 dias (ou data ilegível) | 1 | idem |
| 2 | Perfil **reivindicado** (`unclaimed_listing` ausente) | **2** | `local_results.unclaimed_listing` (só aparece quando `true`) |
| 3 | `extensions` com ≥ 6 chaves (3–5 → 1 pt) | **2** | `extensions[]` (já vem no `search`) |
| 4 | Horário com os **7 dias** preenchidos | 1 | `local_results.operating_hours{}` **ou** `place_results.hours[]` — nomes diferentes por engine |
| 5 | `phone` presente | 1 | `phone` |
| 6 | 🆕 **Texto longo do dono** — `posts_texto_len_max ≥ 500` → **2** · `≥ 250` → 1 · abaixo/ausente → 0 | **2** | `place_results.posts[].description` (312–633 chars reais medidos) |
| | **Máximo** | **11 → cap 10** | |

**Corte: `icp_score >= 5` aprova.** Abaixo → **Lista B (reserva)**, não descarte definitivo.

```python
perfil_texto_500 = (posts_texto_len_max or 0) >= 500   # gravado em TODO registro, JSON e CSV
```

**Modo `--estrito-500`:** `/prospect-enhanced lote --estrito-500` transforma o componente 6 em **gate hard literal** — `perfil_texto_500 == false` → `motivo_descarte: texto-abaixo-de-500`, `status: reserva`. Não é o padrão; é a opção quando o Pedro quiser o critério ao pé da letra. **Reportar sempre a taxa de aprovação nos dois critérios**, para a decisão ser informada.

### 6.2.1 🔴 O que NÃO entra no ICP (e por que saiu)

O ICP é um gate de **eliminação**. Só pode conter sinal de **maturidade/verba**. Sinal de **classificação** fica fora, por ordem literal do Pedro (*"não filtram, ranqueiam"*):

| Fora do ICP | Motivo |
|---|---|
| `site_tipo` | Site é **oportunidade**, nunca requisito. Não soma, não subtrai. |
| Botões transacionais (`menu`, `booking_link`, `order_online_link`) | Estava valendo 1 pt no gate e **punia a empresa sem botão de pedido** — exatamente o perfil que vale +15 no score de oportunidade. Removido. |
| `rating` / volume de `reviews` | Volume de comentários é a **chave primária de P1/P2/P3**, não critério de corte. Removido. |
| WhatsApp | Idem: é ranqueamento (+15 quando ausente), nunca gate. |

### 6.3 Calibração obrigatória

Rodar o par **312/313 primeiro**, medir a distribuição do ICP e ajustar o corte para que a taxa de aprovação fique entre **25% e 45%**. Registrar o corte usado em `lotes/{lote}/_meta.json`.

**O corte é do lote, não global** — e muda sem aviso se o Google mudar o que expõe. O valor 5 é **heurístico, não medido**.

### 6.4 Gate opcional D-LIT (aba "Sobre" literal) — **NÃO IMPLEMENTADO**

O modo `--estrito-500` da §6.2 mede o texto do dono **nos posts**. Se o Pedro quiser especificamente o texto da aba **"Sobre"** (o campo de 750 caracteres que ele vê no painel do GMB), o único caminho é **scraping do Google Maps via Playwright**: ~15 s por empresa, zero custo de API, **alta fragilidade**. Rodaria **depois** do ICP, sobre os ~55 aprovados.

**Status: requer scraping fora da SerpAPI — não implementado.** Não é campo de API e não deve ser prometido como tal em nenhum documento.

---

## 7. Detecção de franquia

### 7.1 O que estamos medindo de verdade

Não existe API que responda "isso é franquia?". A detecção é **inferência por acúmulo de sinais**, em camadas ordenadas por custo.

E a pergunta real não é "é franquia?", é: **quem decide o marketing desta unidade fica atrás deste balcão?** Se sim, é lead. Se a decisão está numa matriz em São Paulo, não é lead — não importa a placa.

### 7.2 Cascata

| Camada | Sinal | Custo | Precisão | Veredito possível |
|---|---|---|---|---|
| **G5a** | Match na blacklist local (nome normalizado) | `$0` | alta | `FRANQUIA` → **corta** |
| **G5b** | Padrão no nome (`unidade`, `filial`, `franquia`, `matriz`, sufixo numérico, marca+bairro) | `$0` | média | `SUSPEITO` → vai ao G7 |
| **G7** | Contagem de unidades da marca no DF via SerpAPI | 1 chamada **por marca**, cacheada 90 d | alta | `FRANQUIA` / `REDE-LOCAL` / `INDEPENDENTE` |
| **G7b** | `posts[].description` clonado entre unidades (≥ 90% de similaridade) | `$0` (roda depois do G8) | **alta** | `FRANQUIA` → corta |
| **G7c** | CNPJ: `ordem != 0001` + raiz com ≥ 5 filiais | `$0` (marginal) | alta, mas **parcial** | `REDE-PROPRIA` → corta |
| **G7d** | Site nacional com localizador de lojas | 1 WebFetch, só se contagem 3–7 | alta | `FRANQUIA` → corta |

### 7.3 Normalização de nome (G5a) — **nunca `contains` puro**

```
normalizar(nome):
  minúsculas
  remover acentos
  remover pontuação e "ltda|me|epp|s/a|eireli"
  remover sufixos geográficos: "asa norte|asa sul|cln \d+|sudoeste|shopping .*|unidade .*|- \d+ norte"
  colapsar espaços
  → MATCH SE: nome_normalizado COMEÇA COM a marca  OU  a marca é o token inicial
```

Contraexemplo que proíbe o `contains`: **"Padaria do Rei"** casaria **"Rei do Mate"**.

Contraexemplo que proíbe o G5b cortar sozinho: **"Padaria Dona Maria — Unidade 2"** pode ser negócio familiar de 2 lojas.

### 7.4 Threshold — corte em **5 unidades no DF**

| Unidades DF | Unidades BR | Classificação | Ação |
|---|---|---|---|
| ≥ 5 | qualquer | Rede grande | 🔴 **CORTA** |
| qualquer | ≥ 10 | Rede nacional | 🔴 **CORTA** |
| 3–4 | < 10 | Zona cinzenta | 🟡 **MANTÉM** → decide no G7b |
| ≤ 2 | ≤ 3 | Independente / micro-rede | 🟢 **MANTÉM**, sem penalidade |

**Defesa do número 5.** Abaixo de 5 lojas o dono ainda é o gestor de marketing: ele mesmo responde review, ele mesmo escolhe se vai fazer landing page, e a decisão de compra acontece na conversa de balcão. Da 5ª unidade em diante aparece alguém contratado só para marketing, normalmente já com agência, e a venda porta-a-porta vira reunião com terceiro que não está na loja. **Todo o método ROTA-RUA depende de falar com quem decide no ato.**

**A zona cinzenta 3–4 NÃO é descarte** — é frequentemente o melhor lead do lote (caixa provado + dor real + decisão local + o mesmo serviço vendido 3–4 vezes numa negociação só). Cortar essa faixa por medo de "franquia" seria jogar fora o ticket mais alto da quadra.

**Marca nacional com franqueado local: corta sempre**, mesmo que o franqueado seja simpático e queira fazer marketing. Contrato de franquia trava marca, arte, copy e canal — o que a Singular venderia esbarra no manual da franqueadora.

> ⚠️ **DIVERGÊNCIA ASSUMIDA EM RELAÇÃO AO PEDIDO LITERAL — decisão pendente do Pedro.**
> O pedido é *"não ser grande franquia / rede nacional"*. O corte em **≥ 5 unidades no DF** é **mais duro que isso**: uma rede local de 5 lojas, sem franqueadora, com o dono decidindo tudo, é cortada com a mesma força que o McDonald's.
> Toda empresa cortada por essa faixa grava `franquia_origem: "contagem"` + `unidades_df` + `rede_local_df: true`, e o `lote-report.md` lista essas empresas em separado, com o nº de unidades. O degrau **R4** readmite as de 5–7 unidades sem posts clonados — mas só quando o lote rende abaixo de 40, ou seja, **num lote farto elas somem**.
> **Se o Pedro quiser aderência literal**, o ajuste é de uma linha: subir o corte DF de 5 para 8 e deixar a rede nacional (≥ 10 BR) e a blacklist fazendo o trabalho. Não mexer sem a decisão dele.

### 7.5 ⚠️ O CNPJ **não** detecta franquia

`G7c` detecta **rede de lojas próprias** (mesma raiz, várias filiais). **Franqueado tem raiz de CNPJ própria e distinta da franqueadora.** Quem pega franquia é blacklist + contagem + site.

Documentar isso é obrigatório, senão alguém confia no gate errado.

### 7.6 Exceções codificadas (nunca cortar no G5)

| Caso | Por quê |
|---|---|
| **Lotérica** | Opera sob concessão da Caixa, mas o **permissionário é dono local** |
| **Loja autorizada de telefonia** (Claro/Vivo/TIM autorizada) | Autorizada é dono local; loja própria não |

Ambas vão direto ao G9 com `revisar_manual: true`.

### 7.7 Blacklist inicial — `data/blacklist-redes.json`

Legenda: **NAC** = rede nacional (≥ 10 unidades no Brasil) · **DF** = rede regional forte no DF (≥ 5 unidades locais) · **`?`** = presença/porte em quadra comercial da Asa Norte **NÃO CONFIRMADO** — **não corta sozinha**, vira `SUSPEITO` e vai ao G7.

**Alimentação rápida / restaurantes (25)**
McDonald's `NAC` · Burger King `NAC` · Bob's `NAC` · Subway `NAC` · Habib's `NAC` · Ragazzo `NAC` · Giraffas `NAC` · Spoleto `NAC` · China in Box `NAC` · Gendai `NAC` · Domino's `NAC` · Pizza Hut `NAC` · KFC `NAC` · Vivenda do Camarão `NAC` · Montana Grill `NAC` · Divino Fogão `NAC` · Griletto `NAC` · Mania de Churrasco `NAC` · Patroni `NAC` · Croasonho `NAC` · Sukiya `NAC?` · Jin Jin `NAC?` · Coco Bambu `NAC` · Mangai `NAC?` · Balada Mix `NAC?`

**Padaria, café, doces, sorvete (14)**
Casa do Pão de Queijo `NAC` · Rei do Mate `NAC` · The Coffee `NAC` · Casa Bauducco `NAC` · Cacau Show `NAC` · Kopenhagen `NAC` · Brasil Cacau `NAC` · Sodiê Doces `NAC` · Amor aos Pedaços `NAC` · Mr. Cheney `NAC` · Bacio di Latte `NAC` · Häagen-Dazs `NAC` · Chiquinho Sorvetes `NAC` · Oakberry `NAC`

**Farmácias (8)**
Drogaria Rosário `DF` (90+ lojas DF/MT) · Drogasil `NAC` · Droga Raia `NAC` · Pague Menos `NAC` · Extrafarma `NAC` · Farmais `NAC` · Drogaria São Paulo `NAC` · Drogaria Araújo `NAC?`

**Supermercado, hortifruti, conveniência (8)**
Big Box `DF` (24 lojas no DF, incl. 106/208/408 Norte) · Pão de Açúcar `NAC` · Carrefour Bairro/Express `NAC` · Assaí `NAC` · Comper `NAC?` · Superadega `DF?` · ampm `NAC` · BR Mania `NAC`

**Banco e serviços financeiros (8)**
Banco do Brasil `NAC` · Caixa `NAC` · BRB `DF` · Itaú `NAC` · Bradesco `NAC` · Santander `NAC` · Sicoob `NAC` · Sicredi `NAC`
→ **Lotérica é exceção** (§7.6): não cortar automaticamente.

**Laboratório e saúde (7)**
Laboratório Sabin `DF` · Exame Laboratório `DF` · OdontoCompany `NAC` · Orthodontic `NAC` · Sorridents `NAC` · Amei Odontologia `NAC?` · Fleury/Hermes Pardini `NAC?`

**Beleza, estética, depilação (9)**
Espaçolaser `NAC` · Vialaser `NAC` · Depyl Action `NAC` · Pello Menos `NAC` · Onodera `NAC` · Sobrancelhas Design `NAC` · Jacques Janine `NAC` · Werner Coiffeur `NAC` · Barbearia Vintage `NAC?`

**Academia e fitness (7)**
Smart Fit `NAC` · Bluefit `NAC` · Selfit `NAC` · Just Fit `NAC?` · Panobianco `NAC?` · Bodytech `NAC` · Fórmula Academia `NAC?`

**Pet (4)**
Petz `NAC` · Cobasi `NAC` · Petland `NAC` · Pet Camp `DF?`

**Óticas (4)**
Óticas Carol `NAC` · Óticas Diniz `NAC` · Chilli Beans `NAC` · Sunglass Hut `NAC`

**Educação e idiomas (12)**
Casa Thomas Jefferson `DF` · Wizard `NAC` · CCAA `NAC` · CNA `NAC` · Fisk `NAC` · Yázigi `NAC` · Cultura Inglesa `NAC` · Kumon `NAC` · influx `NAC` · Skill `NAC?` · Gran Cursos `DF` · Colégio Sigma / Galois / Olimpo `DF?`

**Serviços, lavanderia, automotivo, varejo (12+)**
5àsec `NAC` · Dry Clean USA `NAC?` · Acquazero `NAC?` · Bosch Car Service `NAC` · DPaschoal `NAC` · RE/MAX `NAC` · Century 21 `NAC` · Kalunga `NAC` · Livraria Leitura `NAC` · Mundo Verde `NAC` · Growth Supplements `NAC` · Hering Store `NAC`
Telefonia: Claro / Vivo / TIM `NAC` (**autorizada é exceção**, §7.6) · iPlace `NAC`

**Total: ~118 marcas.**

### 7.8 A blacklist é lista viva

Toda marca que o G7 devolver **≥ 5 unidades no DF** é gravada em `blacklist-redes.json` **com data e contagem**. É o único componente do sistema que **fica mais barato a cada lote rodado**.

### 7.9 Rastreabilidade obrigatória

Todo veredito grava **`franquia_veredito` + `franquia_origem` + `franquia_confianca`**. Corte sem rastro não é auditável — e vai ser questionado no dia em que o vendedor passar em frente à loja que o sistema descartou.

---

## 8. Pseudocódigo do funil

```python
# ───────────────────────── FASE OFFLINE (custo R$ 0) ─────────────────────────
roster = carregar_ou_baixar_roster(CEPS_36, ttl_dias=30)   # G0
quadras = carregar_ou_resolver_centroides(PARES)           # G1  (cache eterno)
blacklist = carregar("data/blacklist-redes.json")
cache_marcas = carregar("data/cache-marcas.json")          # TTL 90 dias

conferir_saldo_serpapi(orcamento=335, teto=400)            # aborta se saldo < 1,3x

# ───────────────────────── DISCOVERY ─────────────────────────
brutos = []
for par in PARES:                                          # G2
    for query in QUERIES_10:
        for start in (0, 20, 40):
            r = serpapi(engine="google_maps", type="search", q=query,     # type é OBRIGATÓRIO
                        ll=quadras[par].centroide, hl="pt-br", gl="br", start=start,
                        mode="complete")                                  # raw literal, sem poda
            persistir_literal(f"_raw/search-{par}-{query}-{start}.json", r)
            brutos += parse_com_aliases(r)                 # §8.3 da SPEC: chaves em pt-BR
            if len(r.local_results) < 20: break            # não paginar em vão

# ───────────────────────── GATES GRÁTIS ─────────────────────────
vistos = set()                                             # G3: set GLOBAL do lote
funil = []
for e in brutos:
    if e.place_id in vistos: continue
    vistos.add(e.place_id)
    funil.append(e)

for e in funil:
    # G4 — geo (ÚNICO gate onde ausência reprova)
    e.quadra, e.geo_metodo, e.geo_confianca = resolver_geo(e, quadras, CEPS_36)
    if e.quadra is None and e.par is None:
        reprovar(e, "fora-do-escopo"); continue

    # G5 — franquia barata
    marca = extrair_marca(normalizar(e.title))
    if match_blacklist_prefixo(marca, blacklist, exigir_confirmada=True):
        reprovar(e, "franquia-blacklist", origem="blacklist", conf="alta"); continue
    e.suspeito_rede = tem_padrao_de_rede(e.title) or marca_com_interrogacao(marca)
    if eh_excecao(e):                                      # lotérica, autorizada
        e.suspeito_rede = False; e.revisar_manual = True

    # G6 — MEI / porte (join local com o roster, custo 0)
    e.cnpj, e.cnpj_metodo, e.cnpj_confianca = casar_com_roster(e, roster)
    if e.cnpj_confianca in ("nao_resolvido", "baixa") or aberta_ha_menos_de(e, dias=60):
        e.mei_incerto = True                               # PASSA com flag
    elif eh_mei(e):                                        # opcao_mei=="S" sem exclusão
        reprovar(e, "mei"); continue

# G7 — franquia por contagem (1 chamada POR MARCA, cacheada)
for marca in {e.marca for e in ativos(funil) if e.suspeito_rede}:
    n_df = cache_marcas.get(marca) or contar_unidades_df(marca)
    cache_marcas.set(marca, n_df, ttl_dias=90)
    if n_df >= 5:
        blacklist.gravar(marca, n_df, hoje())              # lista viva
        for e in ativos(funil, marca):
            e.rede_local_df = True                          # rastro da §7.4
            reprovar(e, "franquia-contagem", origem="contagem")

# ───────────────────────── GATE PAGO (1 crédito/empresa) ─────────────────────
for e in ordenar_por_prioridade_prevista(ativos(funil)):   # G8: P1 → P2 → P3
    r = serpapi(engine="google_maps", type="place", place_id=e.place_id,
                hl="pt-br", gl="br", mode="complete")      # complete: o raw tem que ser literal
    persistir_literal(f"{e.slug}/serpapi-raw.json", r)     # dump INTOCADO
    if r.vazio_ou_erro:
        e.place_status = "falhou"                          # NÃO reprova
    else:
        e.aplicar(r)                                       # posts, menu, wa.me, botões

# G7b — reclassificação: posts clonados entre unidades da mesma marca
for marca in marcas_com_multiplas_unidades(funil):
    if jaccard_shingles5(posts_das_unidades(marca)) >= 0.90:
        for e in ativos(funil, marca): reprovar(e, "franquia-posts-clonados", origem="posts-clonados")

# ───────────────────────── ICP E CLASSIFICAÇÃO ─────────────────────────
corte = calibrar_icp(par="312-313", alvo_aprovacao=(0.25, 0.45))   # G9
registrar("_meta.json", corte_icp=corte)
for e in ativos(funil):
    e.posts_texto_len_max = max((len(p.description or "") for p in e.posts), default=0)
    e.perfil_texto_500    = e.posts_texto_len_max >= 500    # critério LITERAL do Pedro
    e.icp_score = calcular_icp(e)                           # teto 6 e corte >=3 se place_status=falhou
    if MODO_ESTRITO_500 and not e.perfil_texto_500:
        e.status, e.motivo_descarte = "reserva", "texto-abaixo-de-500"
    else:
        e.status = "aprovado" if e.icp_score >= corte else "reserva"
        if e.status == "reserva": e.motivo_descarte = "icp-baixo"

for e in aprovados(funil):                                 # G10
    rev = serpapi(engine="google_maps_reviews", data_id=e.data_id, hl="pt-br", mode="complete")
    persistir_literal(f"{e.slug}/serpapi-reviews.json", rev)
    e.taxa_resposta = taxa(rev) if campo_response_existe(rev) else None

for e in funil:                                            # G11
    e.prioridade = P1 if 20 <= e.reviews <= 50 else (P2 if e.reviews > 50 else P3)
    e.score_oportunidade = score_0_100(e)

# ───────────────────────── REGRA DE PARADA ─────────────────────────
n = len(aprovados(funil))
for degrau in (R1, R2, R3, R4, R5):                        # §9
    if n >= 40: break
    aplicar_degrau(degrau, funil)                          # marca nivel_admissao
    n = len(aprovados(funil))

gravar_csv_com_TODAS_as_empresas(funil)                    # inclusive reprovadas
gerar_lote_report(funil)                                   # SEM truncar em 40
                                                           # inclui a linha obrigatória:
                                                           # "N de X aprovadas passariam no critério
                                                           #  literal de 500 caracteres"
atualizar_tabela_de_lotes_no_README()                      # passo obrigatório
```

---

## 9. Regra de parada e escada de relaxamento

**Meta: 40 aprovadas no lote 310–315. É PISO, não teto.**

### 9.1 Se render ≥ 40

- **Traz todas. Nunca truncar em 40.** O `lote-report.md` lista 100% das aprovadas.
- A meta **não interrompe a varredura**: os 3 pares são varridos sempre.

### 9.2 Se render < 40 — a escada

Regras: **um degrau por vez** · **recontar após cada degrau** · **parar assim que atingir 40** · **gravar `nivel_admissao` (`base`|`R1`..`R5`) em toda empresa readmitida**.

| Degrau | O que relaxa | Custo | Ganho estimado |
|---|---|---|---|
| **R1** | `icp_score` de **≥ 5 → ≥ 4** | 0 crédito | +10 a 15 |
| **R2** | Admite `unclaimed_listing == true` (Lista B), com `oportunidade_claim: true` — vira pitch de "reivindicar seu perfil" | 0 crédito | +8 a 12 |
| **R3** | Admite `cnpj_confianca = nao_resolvido` mesmo sem porte confirmado, com flag "confirmar na visita". **O corte de MEI confirmado permanece** | 0 crédito | +10 a 20 |
| **R4** | Admite redes de **5–7 unidades no DF** cujos `posts` **não** são clonados (gestão local comprovada) | ~5 créditos | +3 a 6 |
| **R5** | Estende a geografia ao par contíguo mais próximo (308/309 ao sul; 316/317 ao norte — **verificar existência da 316/317 antes, não confirmado**) | ~110 créditos | +15 a 25 |

Todo degrau abaixo de R4 opera sobre **dado já em disco** e custa zero crédito novo.

### 9.3 O que NUNCA relaxa

1. 🔴 **MEI confirmado** (`opcao_mei = "S"` sem exclusão). Regra hard do Pedro, inegociável.
2. 🔴 **Franquia nacional / rede ≥ 10 unidades no Brasil.** Contrato de franquia trava marca, arte, copy e canal.
3. 🔴 **Gate geográfico**, exceto pelo degrau R5 — que **amplia** o escopo em vez de furá-lo.

### 9.4 Piso de honestidade

Esgotado o R5 e ainda abaixo de 40: **reportar o número real e a escada percorrida**. Nunca completar a lista com empresa reprovada sem flag.

> Um funil de 31 leads reais vale mais que 40 com 9 mentiras — o custo do erro aqui é o vendedor perdendo a manhã numa porta errada.

---

## 10. O argumento da ordem: por que MEI vem **antes** do `type=place`

| Ordem | Empresas que chegam ao G8 | Créditos no G8 |
|---|---|---|
| **A — MEI e franquia antes do `place`** (esta implementação) | 220 → −33% MEI → 147 → −15% franquia → **120** | **120** |
| B — ICP/`place` antes do MEI | **220** | **220** |

**Economia: ~100 créditos ≈ 28% do orçamento total do lote (335).** E o gate MEI custa **R$ 0** — o roster já está em disco quando o SerpAPI começa a rodar.

**Trade-off explícito, e ele é real:** o join nome→CNPJ tem só **65% de cobertura de `nome_fantasia`**. Se tratássemos "não resolvido" como reprovado, cortaríamos ~15% do funil às cegas e perderíamos leads bons por **defeito de cadastro da Receita**, não por mérito da empresa. Por isso a regra da §5.3: **não resolvido PASSA**. Isso devolve ~20 chamadas de `place` ao custo (120 em vez de ~100), e é dinheiro bem gasto.

---

## 11. Incertezas que afetam os gates (com fallback já decidido)

| # | Incerteza | Status | Fallback |
|---|---|---|---|
| 1 | Descrição do dono (750 chars) na SerpAPI, no campo `description` | **CONFIRMADO QUE NÃO EXISTE** (o `description` é blurb do Google) | Componente 6 do ICP sobre `posts[].description` + modo `--estrito-500` (§6.2). Aba "Sobre" literal só via Playwright, **não implementado** |
| 1b | `place_results.reservation{link,source}` como fonte de WhatsApp | 🔴 **NÃO CONFIRMADO** — auditoria não achou a chave em nenhuma doc de `place_results`; o campo documentado é `booking_link` | Detecção de WhatsApp roda sobre `website`+`booking_link`+`order_online_link`+`menu.link`+`posts[].link`. **Validar com 1 `grep` no primeiro dump de `place` da rodada** e só então reabilitar `reservation` |
| 1c | `porte_codigo` como campo de API | 🔴 **NÃO EXISTE** — é DERIVADO (`porte_empresa` string na OpenCNPJ, `codigo_porte` int na BrasilAPI) | Tabela de mapeamento obrigatória em [FONTES-CNPJ.md §3.3.1](FONTES-CNPJ.md). `porte_codigo is None` **passa** |
| 1d | `place_results.operating_hours` | 🔴 **ERRADO** — `operating_hours` só existe em `local_results`; no `place` o campo é `hours[]` + `hours_last_updated` | Parser lê os dois. Sem isso, `horas_dias_preenchidos` = 0 para tudo que vier do `place` |
| 2 | `reviews[].response` (resposta do dono) | **Documentado, 0 ocorrências** em 8 reviews reais | Gastar **1 chamada de validação** numa empresa que comprovadamente responde, **antes** do lote. Se não aparecer: `taxa_resposta = null` global e componente 4 do score = **8 fixo para todos** (neutralizado, sem redistribuir) |
| 3 | Chaves do JSON traduzidas com `hl=pt-br` | **CONFIRMADO** (`pedir_on_line`, `reservar_uma_mesa`, `operating_hours."segunda-feira"`) | Parser com tabela de aliases: tenta PT, depois EN, depois `null`. **Chaves de `extensions[]` continuam em inglês** |
| 4 | CEP → quadra extrapolado (`70763/70764/70768`) | **CONTRADITO** pelo ViaCEP (`70756/70757/70774`) | Tabela canônica em [FONTES-CNPJ.md](FONTES-CNPJ.md). CEP é sinal **secundário** |
| 5 | `mei.excluir_optante` considera `data_exclusao_mei`? | **NÃO CONFIRMADO** | Contornado por design: baixar todas as ATIVAS e filtrar MEI **localmente** |
| 6 | Casa dos Dados: teto de 20/filtro, `pagina` ignorado | **CONFIRMADO** (páginas 1–11 idênticas) | Fatiamento recursivo CEP → porte → `data_abertura` + `ASSERT len(únicos) == total`, **aborta se divergir** |
| 7 | Corte do ICP em 5 | **heurístico, não medido** | Calibrar no par 312/313 (25–45% de aprovação) e registrar em `_meta.json` |
| 7b | Corte de franquia em **5 unidades no DF** | ⚠️ **mais duro que o pedido literal** ("grande franquia / rede nacional") | Rastro `rede_local_df` + `unidades_df` no CSV, lista separada no relatório, readmissão em R4. **Ajuste (5 → 8) depende de decisão do Pedro** (§7.4) |
| 8 | Centróide 314/315 (1 âncora) e 310/311 (desconhecido) | **NÃO CONFIRMADO** | Resolver em runtime exigindo ≥ 4 âncoras. Sem isso: discovery sem `ll` + G4 apertado |
| 9 | Marcas com `?` na blacklist | **NÃO CONFIRMADO** | **Não cortam sozinhas.** Viram `SUSPEITO` e vão ao G7 |
| 10 | Botão "Agendar" | **não observado**, provável colisão com `booking_link` | Campo fixo `nao_confirmado`. **Não inventar** |
| 11 | Blocos além de A–E nas quadras 310–315 | **não confirmado** (ViaCEP lista A–E + base) | CEP-base cobre o resto; **verificar em campo** |
| 12 | Endpoint público da Casa dos Dados pode fechar sem aviso | risco vivo | Roster **versionado no repo**; fallback OpenCNPJ + BrasilAPI; último recurso: rodar **sem** o gate MEI, com `mei_incerto: true` global e `nivel_admissao: R3` — **nunca fingir que o gate rodou** |

---

*Documento gerado por /prospect-enhanced — Singular Group*
*[Registrado por: DESKTOP — 2026-08-10]*

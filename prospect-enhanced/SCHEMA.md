---
title: "SCHEMA — registro por empresa do /prospect-enhanced"
skill: prospect-enhanced
versao: "1.0"
bu: consultorio-comercial
created: "2026-08-10"
updated: "2026-08-10"
---

# SCHEMA — registro por empresa (`/prospect-enhanced`)

**Versão:** 1.0 · **Skill:** `prospect-enhanced@1.0` · **BU:** `consultorio-comercial`
**Lote de referência:** `2026-08-310-315` · **Escopo:** CLN 310–315 Norte, Brasília-DF

Este documento define **o contrato de dados** do funil. Se um campo não está aqui, ele não existe. Se um campo está aqui marcado como `NÃO CONFIRMADO`, ele **não pode** ser usado para reprovar empresa nenhuma até alguém validar com chamada real.

---

## 0. Princípios inegociáveis

| # | Regra | Motivo |
|---|---|---|
| P1 | **`serpapi-raw.json` é dump literal e intocado.** Nenhuma anotação humana entra nele. | Na v1 os "raw" tinham `instagram_followers`, `email_from_site` e `hours` em 2 formatos diferentes — nada era reprocessável sem pagar a API de novo. |
| P2 | **Todo campo derivado ou anotado à mão carrega proveniência**: sufixo `_metodo`/`_confianca`, ou entrada em `_proveniencia{}`. | Corte sem rastro não é auditável. E vai ser questionado quando o vendedor passar em frente à loja que o sistema descartou. |
| P3 | **Ausência de dado nunca vira `0`, `"-"` ou `"N/A"`.** Ausente é `null` (JSON) ou campo vazio (CSV). | A v1 gravava `website: "-"` e `rating` como string; qualquer soma ou filtro em cima disso mente. |
| P4 | **Nada de campo inventado.** Campo não confirmado por chamada real entra com o rótulo literal `nao_confirmado` no valor ou `NÃO CONFIRMADO` na doc. | Cada chamada SerpAPI é paga. Dado inventado queima uma rodada inteira de prospecção. |
| P5 | **Toda empresa que entrou no funil sai no CSV**, aprovada ou reprovada, com `motivo_descarte` preenchido. | Rastreabilidade: saber quem foi cortado e por quê é o que permite recalibrar os thresholds no lote seguinte sem repesquisar (e sem pagar de novo). |

**Legenda de origem** (usada em todas as tabelas):

| Sigla | Fonte |
|---|---|
| `SEARCH` | SerpAPI `engine=google_maps`, `type=search` → bloco `local_results[]` |
| `PLACE` | SerpAPI `engine=google_maps`, `type=place` → bloco `place_results{}` |
| `REV` | SerpAPI `engine=google_maps_reviews` |
| `CNPJ` | OpenCNPJ (canônica) / Casa dos Dados / BrasilAPI — ver `FONTES-CNPJ.md` |
| `DERIV` | calculado localmente a partir de outros campos |
| `HUM` | anotação humana (fora do caminho crítico) |

---

## 1. Tabela de campos

### 1.1 Identidade e geografia

| Campo | Tipo | Origem | Obrig. | Exemplo |
|---|---|---|---|---|
| `id` | string | DERIV | **sim** | `"312-313-nonna-augusta"` |
| `slug` | string | DERIV | **sim** | `"nonna-augusta"` |
| `title` | string | SEARCH | **sim** | `"Nonna Augusta"` |
| `lote` | string | DERIV | **sim** | `"2026-08-310-315"` |
| `par` | enum `310-311`\|`312-313`\|`314-315` | DERIV | **sim** | `"312-313"` |
| `quadra` | int\|null | DERIV | **sim** | `313` (`null` permitido só com `geo_confianca` ≠ `alta`) |
| `bloco` | string\|null | DERIV | não | `"B"` (A–E confirmados pelo ViaCEP; **bloco F: NÃO CONFIRMADO, verificar em campo**) |
| `loja` | string\|null | DERIV | não | `"29"` |
| `cep` | string\|null | DERIV/CNPJ | não | `"70766-520"` |
| `address` | string | SEARCH | **sim** | `"SHCN CLN 313, BL B Lj 29"` — gravar **literal**, sem normalizar |
| `gps_lat` | float | SEARCH | **sim** | `-15.7500563` |
| `gps_lng` | float | SEARCH | **sim** | `-47.8934593` |
| `geo_metodo` | enum `regex`\|`gps`\|`cep`\|`manual` | DERIV | **sim** | `"regex"` |
| `geo_confianca` | enum `alta`\|`media`\|`baixa` | DERIV | **sim** | `"alta"` |
| `geo_conflito` | bool | DERIV | **sim** | `false` — `true` quando regex e GPS discordam (vence o regex; GPS vai para `par_alt`) |
| `par_alt` | string\|null | DERIV | não | `"314-315"` |

**Regex canônica de geo** (o `address` da CLN aparece em ≥ 7 formatos reais):

```
(?i)(SCLRN|SHCN(/CL)?|SCLN|CLN|Com[ée]rcio\s+Local\s+Norte|Quadra|Qd)\D{0,15}\b(310|311|312|313|314|315)\b
```

Formatos reais já observados, todos válidos: `Asa Norte Comércio Local Norte 313, BL C` · `SHCN CLN 312, BL B Lj 29` · `SHCN/CL Qd 413 Bloco A Lojas 40, 34, 36` · `CLN Quadra 413, Lj 20 - Térreo` · `St. Shcn Comercio Local 313 Bloco A, 37` · `SCLRN Quadra 713 Bloco E` · `BL A - Cln 313 Norte Loja 25` · `BL A Loja 45, Plano Piloto` (**sem quadra nenhuma** → cai no fallback GPS).

### 1.2 Chaves da API

| Campo | Tipo | Origem | Obrig. | Exemplo |
|---|---|---|---|---|
| `place_id` | string | SEARCH | **sim** | `"ChIJk3TdMPBOWpMRnJqEwaZ7bfg"` — chave do `type=place` |
| `data_id` | string | SEARCH | **sim** | `"0x935a4ef030dd7493:0xf86d7ba6c1849c9c"` — chave de reviews e posts |
| `data_cid` | string\|null | SEARCH | não | `"17900424142823816860"` — é o `place_id` do engine `google_local` |
| `place_id_alt` | array[string] | DERIV | não | `[]` — duplicatas fundidas no gate de dedup |

### 1.3 Reputação e nicho

| Campo | Tipo | Origem | Obrig. | Exemplo |
|---|---|---|---|---|
| `rating` | float\|null | SEARCH/PLACE | não | `4.6` |
| `reviews` | int | SEARCH/PLACE | **sim** | `38` — **chave primária de P1/P2/P3** |
| `reviews_ausente` | bool | DERIV | **sim** | `false` — `true` → P3 com flag, nunca reprova |
| `type_pt` | array[string] | SEARCH | **sim** | `["Restaurante italiano"]` — só para exibição, **volátil** |
| `type_ids` | array[string] | SEARCH | **sim** | `["italian_restaurant"]` — slug EN estável, **chave canônica de nicho** |
| `nicho` | slug | DERIV | **sim** | `"restaurante"` — 1 primário, tabela dos 30 slugs em `CLASSIFICACAO.md` |
| `nicho_secundario` | array[slug] | DERIV | não | `[]` |
| `nicho_temperatura` | enum `quente`\|`morno`\|`frio` | DERIV | **sim** | `"quente"` |
| `nicho_raw_nao_mapeado` | string\|null | DERIV | não | `null` — quando nenhum `type_id` casa, gravar a string crua aqui e usar `nicho: "outros"`. **Nunca forçar match.** |

### 1.4 Contato, site e horário

| Campo | Tipo | Origem | Obrig. | Exemplo |
|---|---|---|---|---|
| `phone` | string\|null | SEARCH/PLACE | não | `"(61) 8275-0420"` |
| `phone_norm` | string\|null | DERIV | não | `"6182750420"` — só dígitos, com DDD; usado no match de CNPJ |
| `website` | string\|null | SEARCH/PLACE | não | `"https://nonnaaugusta.com.br"` — ⚠️ **mente sobre "ter site"** |
| `site_tipo` | enum `proprio`\|`social`\|`builder`\|`terceiro`\|`ausente` | DERIV | **sim** | `"proprio"` |
| `price` | string\|null | SEARCH | não | `"$$"` |
| `extracted_price` | number\|null | SEARCH | não | `null` |
| `open_state` | string\|null | SEARCH | não | `"Aberto ⋅ Fecha 23:00"` |
| `operating_hours` | object\|null | **SEARCH** | não | `{"segunda-feira": "18:00–23:00", ...}` — **chaves em pt-BR**. ⚠️ **só existe em `local_results`** |
| `hours` | array[object]\|null | **PLACE** | não | `[{"segunda-feira":"18:00–23:00"}, ...]` — **array de objetos de 1 chave**; é o equivalente no `place_results`, junto de `hours_last_updated` |
| `horas_dias_preenchidos` | int 0–7 | DERIV | **sim** | `7` — normalizar **os dois formatos** antes de contar |
| `unclaimed_listing` | bool | SEARCH | **sim** | `false` — o campo **só aparece na resposta quando é `true`**; default local `false` |
| `extensions_keys` | array[string] | SEARCH/PLACE | **sim** | `["service_options","highlights","popular_for","offerings","dining_options","amenities","atmosphere"]` — **chaves em inglês**, valores em pt |
| `extensions_n` | int | DERIV | **sim** | `7` |

**Classificação de `site_tipo`** (medido: **6 dos 11 `website` preenchidos não eram site próprio**):

| Valor | Critério | Exemplo real |
|---|---|---|
| `proprio` | domínio próprio da empresa | `nonnaaugusta.com.br` |
| `social` | `instagram.com` / `facebook.com` | `instagram.com/casa.da.siria` |
| `builder` | `sites.google`, `linktr.ee`, subdomínio de builder | `sites.google.com/view/donalenhamediterraneo` |
| `terceiro` | landing page hospedada em domínio de agência | `agenciacreh.com.br/landingpages/santerestaurantes/` |
| `ausente` | `website == null` | — |

> `tem_site = website != null` é **falso** e produziria pitch errado na porta. `social` e `ausente` são o público-alvo de landing page — o "bom cliente" que o Pedro descreveu. **Nunca penalizam.**

### 1.5 Botões do perfil GMB

| Campo | Tipo | Origem | Obrig. | Exemplo | Status |
|---|---|---|---|---|---|
| `botao_site` | bool | DERIV | **sim** | `true` | confirmado (`website != null`) |
| `botao_ligar` | bool | DERIV | **sim** | `true` | confirmado (`phone != null`) |
| `botao_rota` | bool | DERIV | **sim** | `true` | **DERIVADO** de `address` + `gps`. **Não existe campo próprio na API — não inventar.** |
| `botao_whatsapp` | bool | DERIV | **sim** | `true` | derivado por regex — exige `type=place` |
| `whatsapp_url` | string\|null | DERIV | não | `"https://wa.me/556182750420"` | extraído do campo em que a regex casou |
| `whatsapp_origem` | enum | DERIV | não | `"booking_link"` | `website`\|`booking_link`\|`order_online_link`\|`menu`\|`posts`\|`nenhum` · ⚠️ `reservation` **suspenso até validação** (ver nota abaixo) |
| `botao_pedidos` | bool | SEARCH/PLACE | **sim** | `true` | `pedir_on_line` (search) **ou** `order_online_link` (place) — **chaves diferentes, parsers diferentes** |
| `botao_reservar` | bool | SEARCH/PLACE | **sim** | `true` | `reservar_uma_mesa` (search) **ou** `booking_link` (place) |
| `botao_menu` | bool | PLACE | **sim** | `true` | `menu.link` — **`null` no search, exige `type=place`** |
| `botao_agendar` | const `"nao_confirmado"` | — | **sim** | `"nao_confirmado"` | **NÃO CONFIRMADO.** Nenhum campo próprio observado; provável colisão com `booking_link`. Valor fixo. |

**Detecção de WhatsApp — regex única**, aplicada **nesta ordem** aos campos documentados de `place_results`: `website` → `booking_link` → `order_online_link` → `menu.link` → `posts[].link`.

```
wa\.me|api\.whatsapp\.com
```

> Medido: `grep wa.me` no payload inteiro do `search` deu **0 ocorrências**; no `place` da mesma empresa, **3**. Detectar WhatsApp **obriga** 1 chamada `type=place` por empresa. Não tem atalho.
>
> 🔴 **`reservation{link,source}` — NÃO CONFIRMADO, campo suspenso.** Este schema chegou a listá-lo como "a única fonte de WhatsApp". Auditoria posterior **não encontrou a chave `reservation` (nem `reservations`) em nenhuma lista documentada de `place_results`** — o campo documentado equivalente é `booking_link`; a única ocorrência do termo na doc é o valor de texto `"Accepts reservations"` dentro de `unsupported_extensions.planning`.
> **Validar na primeira rodada (custo 0, é só um grep no dump que você já pagou):**
> ```bash
> grep -o '"reservations\?"' lotes/*/par-*/*/serpapi-raw.json | sort | uniq -c
> ```
> Achou → colar aqui o trecho do JSON como evidência e reabilitar `reservation` no enum. Não achou em nenhum dos ~120 dumps → **remover a menção em definitivo**. Até lá o valor `"reservation"` **não pode ser gravado** em `whatsapp_origem`.

### 1.6 Conteúdo (posts / Atualizações)

| Campo | Tipo | Origem | Obrig. | Exemplo |
|---|---|---|---|---|
| `posts_n` | int | PLACE | **sim** | `10` |
| `post_ultimo_iso` | date\|null | PLACE | não | `"2026-08-04"` — `posts[].date` vem relativo (`"há 6 dias"`) **ou** absoluto (`"28 de jul. 2026"`); normalizar sempre |
| `post_dias_desde` | int\|null | DERIV | não | `6` |
| `posts_texto_len_max` | int | DERIV | não | `633` — tamanhos reais observados: 312 / 464 / 633 chars |
| `posts_cta` | array[string] | PLACE | não | `["Saiba mais"]` |

> ⚠️ **Correção obrigatória à v1:** a skill v1 afirma que "a aba Atualizações/Posts não é exposta pela SerpAPI". **Isso é falso.** `place_results.posts[]` retornou 10 posts reais com `media`, `cta`, `link`, `post_link`, `description`, `date`. Apagar a afirmação de todo doc herdado.
>
> Ironia útil: **é aqui que mora o texto longo escrito pelo dono** (464–633 chars), não em `description`.

### 1.7 Reviews (amostra)

| Campo | Tipo | Origem | Obrig. | Exemplo |
|---|---|---|---|---|
| `taxa_resposta` | float\|null | REV | não | `null` |
| `reviews_amostra_n` | int | REV | não | `8` (1ª página = 8 reviews, confirmado) |
| `ultimo_review_iso` | date\|null | REV | não | `"2026-07-29"` |
| `review_topics` | array[{keyword,mentions}] | REV | não | `[{"keyword":"massa","mentions":14}]` — só na 1ª página |
| `people_also_search_for` | array[object] | PLACE | não | `[{"title":"Piccolino","reviews":676}]` — **persistir sempre** |
| `rating_summary` | array[{stars,amount}] | PLACE | não | `[{"stars":5,"amount":24}]` |

> 🔴 **INCERTEZA MATERIAL — `reviews[].response`:** o campo é **documentado**, mas foi observado **0 vez** nos 8 reviews reais puxados (a empresa testada não responde ninguém). **Antes de rodar o lote inteiro, gastar 1 chamada de validação** numa empresa que comprovadamente responde reviews (conferir a olho no Maps antes). Se o campo não aparecer nem lá: `taxa_resposta = null` para todo mundo e o componente correspondente do score vira **8 pontos fixos para todos** (neutralizado, sem redistribuir).
>
> `reviews[].snippet` esteve **ausente em 5 de 8** (review só com nota). O parser **não pode** assumir que existe.

### 1.8 CNPJ e porte

| Campo | Tipo | Origem | Obrig. | Exemplo |
|---|---|---|---|---|
| `cnpj` | string\|null | CNPJ | não | `"12.345.678/0001-90"` |
| `cnpj_confianca` | enum `alta`\|`media`\|`baixa`\|`nao_resolvido` | DERIV | **sim** | `"alta"` |
| `cnpj_metodo` | enum `nome`\|`telefone`\|`numero_loja`\|`cnae`\|`manual`\|`nenhum` | DERIV | **sim** | `"telefone"` |
| `razao_social` | string\|null | CNPJ | não | `"NONNA AUGUSTA RESTAURANTE LTDA"` |
| `nome_fantasia` | string\|null | CNPJ | não | `"NONNA AUGUSTA"` — preenchido em só **65%** dos registros |
| `porte_codigo` | enum `00`\|`01`\|`03`\|`05` | CNPJ | não | `"03"` (não existe 02 nem 04) |
| `porte_label` | string\|null | CNPJ | não | `"EPP"` |
| `opcao_mei` | enum `S`\|`N`\|`null` | CNPJ | não | `"N"` (`null` = "EM BRANCO / OUTROS" no layout da RF) |
| `data_exclusao_mei` | date\|null | CNPJ | não | `null` — **decisivo** (ver `FONTES-CNPJ.md`) |
| `eh_mei` | bool\|null | DERIV | **sim** | `false` |
| `mei_incerto` | bool | DERIV | **sim** | `false` |
| `data_abertura` | date\|null | CNPJ | não | `"2019-03-14"` |
| `cnae_principal` | string\|null | CNPJ | não | `"5611201"` |
| `cnae_descricao` | string\|null | CNPJ | não | `"Restaurantes e similares"` |
| `cnpj_fonte` | enum `opencnpj`\|`brasilapi`\|`casadosdados` | DERIV | **sim** | `"opencnpj"` |
| `cnpj_consultado_em` | date | DERIV | **sim** | `"2026-08-10"` |

### 1.9 Franquia / rede

| Campo | Tipo | Origem | Obrig. | Exemplo |
|---|---|---|---|---|
| `marca_normalizada` | string\|null | DERIV | não | `"nonna augusta"` |
| `franquia_veredito` | enum `FRANQUIA`\|`REDE-LOCAL`\|`REDE-PROPRIA`\|`INDEPENDENTE`\|`SUSPEITO` | DERIV | **sim** | `"INDEPENDENTE"` |
| `franquia_origem` | enum `blacklist`\|`contagem`\|`posts-clonados`\|`site-nacional`\|`cnpj`\|`nenhum` | DERIV | **sim** | `"nenhum"` |
| `franquia_confianca` | enum `alta`\|`media`\|`baixa` | DERIV | **sim** | `"alta"` |
| `unidades_df` | int\|null | SEARCH | não | `1` |

### 1.10 Gates, score e status

| Campo | Tipo | Origem | Obrig. | Exemplo |
|---|---|---|---|---|
| `gate_geo` | enum `passou`\|`reprovou`\|`ausente_admitido` | DERIV | **sim** | `"passou"` |
| `gate_dedup` | enum | DERIV | **sim** | `"passou"` |
| `gate_mei` | enum | DERIV | **sim** | `"passou"` |
| `gate_franquia` | enum | DERIV | **sim** | `"passou"` |
| `gate_icp` | enum | DERIV | **sim** | `"passou"` |
| `icp_score` | int 0–10 | DERIV | **sim** | `10` |
| `icp_componentes` | object (7 chaves) | DERIV | **sim** | ver exemplo §2 |
| `place_status` | enum `ok`\|`falhou` | DERIV | **sim** | `"ok"` — `falhou` → ICP com teto 7 e corte proporcional |
| `status` | enum `aprovado`\|`reserva`\|`reprovado` | DERIV | **sim** | `"aprovado"` |
| `motivo_descarte` | string\|null | DERIV | **sim** | `null` — **o primeiro gate que reprovou**, nunca uma lista |
| `nivel_admissao` | enum `base`\|`R1`..`R5` | DERIV | **sim** | `"base"` |
| `prioridade` | enum `P1`\|`P2`\|`P3` | DERIV | **sim** | `"P1"` |
| `score_oportunidade` | int 0–100 | DERIV | **sim** | `33` |
| `score_componentes` | object (7 chaves) | DERIV | **sim** | ver exemplo §2 |
| `ranking_lote` | int | DERIV | **sim** | `7` |
| `oportunidade_claim` | bool | DERIV | não | `false` |
| `revisar_manual` | bool | DERIV | **sim** | `false` |

**Vocabulário fechado de `motivo_descarte`** (usar exatamente estas strings — o CSV é agrupado por elas na recalibração):

| Valor | Gate que cortou |
|---|---|
| `fora-do-escopo` | geo — quadra ≠ 310–315 |
| `sem-geo` | geo — sem `address` **e** sem `gps` (único caso do funil em que ausência reprova) |
| `duplicado` | dedup — `place_id` já visto no lote |
| `mei` | MEI confirmado (`opcao_mei = "S"` sem `data_exclusao_mei`) |
| `franquia-blacklist` | blacklist local, marca `NAC`/`DF` |
| `franquia-contagem` | ≥ 5 unidades no DF ou ≥ 10 no Brasil |
| `franquia-posts-clonados` | `posts[].description` ≥ 90% similar entre unidades da marca |
| `franquia-site-nacional` | site com localizador de lojas / "seja um franqueado" |
| `rede-propria-cnpj` | `ordem != 0001` + raiz com ≥ 5 filiais |
| `icp-baixo` | ICP abaixo do corte do lote → vai para `status: reserva`, **não** para `reprovado` definitivo |
| `perfil-nao-reivindicado` | `unclaimed_listing == true` → `status: reserva`, readmitido no degrau R2 |

### 1.11 Metadados e proveniência

| Campo | Tipo | Origem | Obrig. | Exemplo |
|---|---|---|---|---|
| `serpapi_raw_path` | string | DERIV | **sim** | `"par-312-313/nonna-augusta/serpapi-raw.json"` |
| `coletado_em` | iso8601 | DERIV | **sim** | `"2026-08-10T14:22:00-03:00"` |
| `skill_versao` | string | DERIV | **sim** | `"prospect-enhanced@1.0"` |
| `custo_chamadas` | int | DERIV | **sim** | `2` — créditos SerpAPI gastos nesta empresa |
| `instagram` | string\|null | HUM | não | `null` — **fora do caminho crítico** |
| `instagram_seguidores` | int\|null | HUM | não | `null` — idem |
| `_proveniencia` | object | DERIV | **sim** | `{}` — `{campo: origem}` para todo campo `HUM` |

> **Instagram sai do caminho crítico por decisão.** Na v1, em CLN 314, **21 de 21 lojas** ficaram com `Instagram: — ⚪ Verificação manual`. Dimensão morta que só poluía o relatório. Aqui é campo opcional, preenchido só à mão, e **nunca** se vende como dimensão do método.

---

## 2. Exemplo JSON preenchido

Empresa **fictícia** da CLN 313 (`prospect-enhanced/lotes/2026-08-310-315/par-312-313/panificadora-santa-clara/enriquecido.json`). Valores realistas, coerentes entre si — mas **ilustrativos**, não coletados.

```json
{
  "id": "312-313-panificadora-santa-clara",
  "slug": "panificadora-santa-clara",
  "title": "Panificadora Santa Clara",
  "lote": "2026-08-310-315",

  "par": "312-313",
  "quadra": 313,
  "bloco": "C",
  "loja": "14",
  "cep": "70766-530",
  "address": "SHCN CLN 313, BL C Lj 14 - Asa Norte, Brasília - DF",
  "gps_lat": -15.7499835,
  "gps_lng": -47.8933491,
  "geo_metodo": "regex",
  "geo_confianca": "alta",
  "geo_conflito": false,
  "par_alt": null,

  "place_id": "ChIJEXEMPLO0000000000000000",
  "data_id": "0x935a3f0000000000:0xEXEMPLO000000000",
  "data_cid": "17900000000000000000",
  "place_id_alt": [],

  "rating": 4.4,
  "reviews": 41,
  "reviews_ausente": false,
  "type_pt": ["Padaria", "Cafeteria"],
  "type_ids": ["bakery", "cafe"],
  "nicho": "padaria-confeitaria",
  "nicho_secundario": ["cafeteria"],
  "nicho_temperatura": "morno",
  "nicho_raw_nao_mapeado": null,

  "phone": "(61) 3340-1122",
  "phone_norm": "6133401122",
  "website": "https://www.instagram.com/santaclara313/",
  "site_tipo": "social",
  "price": "$$",
  "extracted_price": null,
  "open_state": "Aberto ⋅ Fecha 20:00",
  "operating_hours": {
    "segunda-feira": "06:30–20:00",
    "terça-feira": "06:30–20:00",
    "quarta-feira": "06:30–20:00",
    "quinta-feira": "06:30–20:00",
    "sexta-feira": "06:30–20:00",
    "sábado": "06:30–20:00",
    "domingo": "07:00–13:00"
  },
  "horas_dias_preenchidos": 7,
  "unclaimed_listing": false,
  "extensions_keys": ["service_options", "highlights", "popular_for", "offerings", "dining_options", "amenities"],
  "extensions_n": 6,

  "botao_site": true,
  "botao_ligar": true,
  "botao_rota": true,
  "botao_whatsapp": false,
  "whatsapp_url": null,
  "whatsapp_origem": "nenhum",
  "botao_pedidos": false,
  "botao_reservar": false,
  "botao_menu": false,
  "botao_agendar": "nao_confirmado",

  "posts_n": 2,
  "post_ultimo_iso": "2025-11-18",
  "post_dias_desde": 265,
  "posts_texto_len_max": 187,
  "posts_cta": ["Saiba mais"],

  "taxa_resposta": null,
  "reviews_amostra_n": 8,
  "ultimo_review_iso": "2026-07-22",
  "review_topics": [
    { "keyword": "pão de queijo", "mentions": 11 },
    { "keyword": "atendimento", "mentions": 7 }
  ],
  "people_also_search_for": [
    { "title": "Croissanterie", "reviews": 612 },
    { "title": "La Boutique Padaria Francesa", "reviews": 487 }
  ],
  "rating_summary": [
    { "stars": 5, "amount": 24 },
    { "stars": 4, "amount": 9 },
    { "stars": 3, "amount": 4 },
    { "stars": 2, "amount": 2 },
    { "stars": 1, "amount": 2 }
  ],

  "cnpj": "11.222.333/0001-44",
  "cnpj_confianca": "alta",
  "cnpj_metodo": "telefone",
  "razao_social": "PANIFICADORA SANTA CLARA COMERCIO DE ALIMENTOS LTDA",
  "nome_fantasia": "SANTA CLARA",
  "porte_codigo": "01",
  "porte_label": "MICRO EMPRESA",
  "opcao_mei": "N",
  "data_exclusao_mei": null,
  "eh_mei": false,
  "mei_incerto": false,
  "data_abertura": "2016-02-09",
  "cnae_principal": "1091102",
  "cnae_descricao": "Fabricação de produtos de padaria e confeitaria com predominância de produção própria",
  "cnpj_fonte": "opencnpj",
  "cnpj_consultado_em": "2026-08-10",

  "marca_normalizada": "panificadora santa clara",
  "franquia_veredito": "INDEPENDENTE",
  "franquia_origem": "nenhum",
  "franquia_confianca": "alta",
  "unidades_df": 1,

  "gate_geo": "passou",
  "gate_dedup": "passou",
  "gate_mei": "passou",
  "gate_franquia": "passou",
  "gate_icp": "passou",
  "place_status": "ok",
  "icp_score": 6,
  "icp_componentes": {
    "posts_recentes": 1,
    "reivindicado": 2,
    "extensions": 2,
    "horas": 1,
    "phone": 1,
    "transacional": 0,
    "rating": 1
  },

  "status": "aprovado",
  "motivo_descarte": null,
  "nivel_admissao": "base",
  "prioridade": "P1",
  "score_oportunidade": 71,
  "score_componentes": {
    "site": 15,
    "whatsapp": 15,
    "botoes": 10,
    "reviews_resposta": 8,
    "conteudo": 10,
    "completude": 3,
    "nicho": 5
  },
  "ranking_lote": 3,
  "oportunidade_claim": false,
  "revisar_manual": false,

  "serpapi_raw_path": "par-312-313/panificadora-santa-clara/serpapi-raw.json",
  "coletado_em": "2026-08-10T15:41:00-03:00",
  "skill_versao": "prospect-enhanced@1.0",
  "custo_chamadas": 2,

  "instagram": null,
  "instagram_seguidores": null,
  "_proveniencia": {}
}
```

**Leitura do exemplo (por que os números batem):** 41 reviews → `P1` (faixa 20–50). ICP 6 ≥ 5 → aprovado, mas o único post é de 265 dias atrás, então ganha só 1 ponto em `posts_recentes` e leva 10 no componente de silêncio de conteúdo do score. `site_tipo: social` (Instagram) → 15 pontos de lacuna de site, **sem nenhuma penalidade** — é exatamente o lead de landing page. Sem WhatsApp → +15. `icp_componentes.transacional` = 0 porque não há `menu`, `booking_link` nem `order_online_link`. `taxa_resposta: null` → componente neutralizado em 8. Total: 15+15+10+8+10+3+5 = **71**.

---

## 3. Colunas do CSV do funil (`funil.csv`)

**Uma linha por empresa que entrou no funil — inclusive as reprovadas.** É o artefato de rastreabilidade: sem ele, recalibrar um threshold exige repesquisar e pagar SerpAPI de novo.

### 3.1 Convenções do arquivo

| Item | Valor |
|---|---|
| Separador | `,` (vírgula) |
| Encoding | **UTF-8 com BOM** (o Excel do Pedro) |
| Fim de linha | `\r\n` |
| Booleanos | `true` / `false` minúsculos |
| Ausente | **campo vazio**. Nunca `-`, nunca `"N/A"`, nunca `0` (erro da v1) |
| Arrays | separador interno `\|` (pipe) — ex.: `bakery\|cafe` |
| Datas | ISO `YYYY-MM-DD`; timestamps ISO 8601 com offset |
| Decimais | ponto (`4.4`), nunca vírgula |
| Aspas | só quando o valor contém `,`, `"` ou quebra de linha |

### 3.2 Ordem literal das colunas (67 colunas)

```
id,lote,par,quadra,bloco,loja,cep,slug,title,address,gps_lat,gps_lng,geo_metodo,geo_confianca,
place_id,data_id,rating,reviews,reviews_ausente,nicho,nicho_temperatura,type_ids,
phone,phone_norm,website,site_tipo,unclaimed_listing,extensions_n,horas_dias_preenchidos,
botao_site,botao_ligar,botao_rota,botao_whatsapp,botao_pedidos,botao_reservar,botao_menu,botao_agendar,
whatsapp_url,whatsapp_origem,posts_n,post_dias_desde,posts_texto_len_max,taxa_resposta,reviews_amostra_n,ultimo_review_iso,
cnpj,cnpj_confianca,cnpj_metodo,razao_social,nome_fantasia,porte_codigo,opcao_mei,data_exclusao_mei,eh_mei,mei_incerto,cnpj_fonte,
franquia_veredito,franquia_origem,franquia_confianca,unidades_df,
gate_geo,gate_dedup,gate_mei,gate_franquia,gate_icp,icp_score,
status,motivo_descarte,nivel_admissao,prioridade,score_oportunidade,ranking_lote,
oportunidade_claim,revisar_manual,custo_chamadas,coletado_em
```

### 3.3 Regra de preenchimento das reprovadas

A empresa reprovada **para no gate que a cortou** e as colunas posteriores ficam **vazias**. Isso é informação, não buraco: mostra até onde o funil chegou antes de gastar dinheiro com ela.

| Reprovou em | Colunas preenchidas | Colunas vazias |
|---|---|---|
| Geo (G4) | identidade, geo, `place_id`, `data_id`, `rating`, `reviews`, `gate_geo=reprovou`, `status=reprovado`, `motivo_descarte=fora-do-escopo`, `custo_chamadas=0` | tudo de CNPJ, botões de `place`, posts, ICP, score |
| Franquia blacklist (G5) | tudo do `search` + `franquia_*`, `gate_franquia=reprovou`, `motivo_descarte=franquia-blacklist` | CNPJ (não chegou a rodar), `place`, ICP, score |
| MEI (G6) | tudo do `search` + bloco CNPJ completo, `gate_mei=reprovou`, `motivo_descarte=mei` | `place`, posts, ICP, score |
| ICP (G9) | **tudo**, inclusive `place` e `icp_score` | `score_oportunidade`, `ranking_lote` (fica em `status=reserva`) |

**Colunas sempre preenchidas, em qualquer linha:** `id`, `lote`, `par`, `slug`, `title`, `status`, `motivo_descarte` (vazio só quando `status=aprovado`), `custo_chamadas`, `coletado_em`.

### 3.4 Linhas de exemplo

```csv
id,lote,par,quadra,...,status,motivo_descarte,nivel_admissao,prioridade,score_oportunidade,ranking_lote,...
312-313-panificadora-santa-clara,2026-08-310-315,312-313,313,...,aprovado,,base,P1,71,3,...
312-313-cacau-show-313,2026-08-310-315,312-313,313,...,reprovado,franquia-blacklist,,,,,...
312-313-costura-da-rita,2026-08-310-315,312-313,313,...,reprovado,mei,,,,,...
312-313-otica-visao-norte,2026-08-310-315,312-313,313,...,reserva,icp-baixo,,P2,,,...
314-315-bl-a-loja-45,2026-08-310-315,314-315,,...,reprovado,fora-do-escopo,,,,,...
```

### 3.5 O que o CSV permite fazer depois (e é o motivo de ele existir)

| Pergunta | Como responder |
|---|---|
| O corte do ICP está apertado demais? | `count(status='reserva' AND motivo_descarte='icp-baixo')` vs total. Se > 50%, baixar o corte no próximo lote. |
| O gate de MEI está comendo o funil? | `count(motivo_descarte='mei') / count(gate_mei != '')`. Medido no roster: ~33% esperado. Muito acima disso = matching errado, não realidade. |
| A blacklist está cortando gente que não devia? | Ler os `title` de `motivo_descarte='franquia-blacklist'` à mão. 10 minutos, uma vez por lote. |
| Onde o dinheiro foi? | `sum(custo_chamadas)` agrupado por `status`. Crédito gasto em linha `reprovado` é desperdício — se for alto, a ordem dos gates está errada. |
| Quantos leads perdi por defeito de cadastro? | `count(cnpj_confianca='nao_resolvido')`. |

---

## 4. Convenção de nomes de arquivo e slug

### 4.1 Algoritmo do `slug`

```
slug(title):
  1. minúsculas
  2. remover acentos (NFD → descartar diacríticos): "Açaí" → "acai"
  3. trocar & por "e", @ por "a"
  4. substituir tudo que não for [a-z0-9] por "-"
  5. colapsar hifens repetidos, remover hifens das pontas
  6. truncar em 60 caracteres, sem cortar palavra no meio
  7. se colidir com slug existente no MESMO par → sufixo "-2", "-3", ...
```

| `title` | `slug` |
|---|---|
| `Nonna Augusta` | `nonna-augusta` |
| `Padaria & Café Santa Clara` | `padaria-e-cafe-santa-clara` |
| `Ótica Visão Norte 313` | `otica-visao-norte-313` |
| `Dr. João Silva — Odontologia` | `dr-joao-silva-odontologia` |
| `BL A Loja 45` (sem nome útil) | `bl-a-loja-45` + `revisar_manual: true` |

**O slug é imutável dentro do lote.** Renomear slug quebra os links relativos do `lote-report.md` e a correspondência com o `funil.csv`. Se o `title` mudar entre lotes, o slug novo é do lote novo — histórico não se reescreve.

### 4.2 Árvore de arquivos

```
prospect-enhanced/
├── README.md
├── FILTROS.md
├── CLASSIFICACAO.md
├── SCHEMA.md                          ← este arquivo
├── FONTES-CNPJ.md
├── data/
│   ├── quadras.json                   # centróides + zoom + âncoras (cache eterno)
│   ├── ceps-cln.json                  # 36 CEPs canônicos (ViaCEP)
│   ├── roster-cln-310-315.json        # ~856 CNPJs, TTL 30 dias
│   ├── roster-meta.json               # baixado_em, total_por_cep, cep_vazio[]
│   ├── blacklist-redes.json           # ~118 marcas, lista viva
│   ├── cache-marcas.json              # contagem de unidades DF, TTL 90 dias
│   └── nicho-map.json                 # type_ids → nicho (30 slugs)
├── templates/
│   ├── empresa.md
│   ├── lote-report.md
│   └── funil.csv
├── scripts/
└── lotes/
    └── 2026-08-310-315/
        ├── _meta.json                 # corte ICP calibrado, custo, saldo antes/depois
        ├── _raw/                       # dumps literais do discovery
        │   └── search-312-313-restaurante-0.json
        ├── funil.csv                   # TODAS as empresas
        ├── lote-report.md
        ├── par-310-311/
        ├── par-312-313/
        │   └── panificadora-santa-clara/
        │       ├── serpapi-raw.json       # dump literal do type=place
        │       ├── serpapi-reviews.json   # dump literal do google_maps_reviews
        │       ├── enriquecido.json       # este schema
        │       ├── relatorio.md
        │       └── oportunidades.md
        └── par-314-315/
```

### 4.3 Regras de nome

| Artefato | Padrão | Exemplo |
|---|---|---|
| Lote | `{AAAA}-{MM}-{quadra_min}-{quadra_max}` | `2026-08-310-315` |
| Pasta de par | `par-{menor}-{maior}` (o menor é sempre o **par**, no sentido numérico) | `par-312-313` |
| Pasta de empresa | `{slug}` | `panificadora-santa-clara` |
| Dump de discovery | `_raw/search-{par}-{query_slug}-{start}.json` | `_raw/search-312-313-padaria-cafe-lanchonete-20.json` |
| Dump de place | `{slug}/serpapi-raw.json` | — |
| Dump de reviews | `{slug}/serpapi-reviews.json` | — |
| Registro derivado | `{slug}/enriquecido.json` | — |
| Relatório | `{slug}/relatorio.md` | — |
| Munição de venda | `{slug}/oportunidades.md` | — |

**Nomes de pasta e arquivo:** minúsculas, sem acento, sem espaço, sem caractere especial. O repo roda em Windows e em Linux — `Panificadora Santa Clara/` quebra script em um dos dois e vira conflito de case no git.

**Dumps literais nunca são editados.** Se você precisou "arrumar" um `serpapi-raw.json`, o lugar da correção é `enriquecido.json`, com a entrada correspondente em `_proveniencia`.

---

## 5. Tabela de aliases do parser (obrigatória)

Com `hl=pt-br` a SerpAPI **traduz as chaves do JSON**. Parser escrito só com nome em inglês quebra **em silêncio** — retorna `null` e a empresa perde pontos que ela tem.

| Inglês (documentação) | pt-BR real | Bloco |
|---|---|---|
| `order_online` | `pedir_on_line` | `local_results` |
| `reserve_a_table` | `reservar_uma_mesa` | `local_results` |
| `service_options.dine_in` | `service_options.refeição_no_local` | ambos |
| `service_options.takeout` | `service_options.para_viagem` | ambos |
| `service_options.delivery` | `service_options.entrega` | ambos |
| `service_options.no_contact_delivery` | `service_options.entrega_sem_contato` | `place_results` |
| `operating_hours.monday` | `operating_hours."segunda-feira"` | ambos |
| `details.price_per_person` | `details.preço_por_pessoa` | `google_maps_reviews` |
| `details.food` / `.service` / `.atmosphere` | `details.comida` / `.serviço` / `.ambiente` | `google_maps_reviews` |
| `order_online_link` | *(permanece em inglês)* | `place_results` |
| chaves de `extensions[]` | *(permanecem em inglês; só os **valores** vêm em pt)* | ambos |

**Ordem de resolução do parser:** tenta a chave pt-BR → tenta a chave EN → devolve `null`. Nunca inventa default.

---

## 6. Campos que NÃO existem (e por que estão aqui)

Esta seção existe para impedir que alguém "melhore" o schema adicionando um campo que a API não entrega.

| Campo tentador | Veredito | Evidência |
|---|---|---|
| `description` do dono ("Do estabelecimento", 750 chars) | **NÃO EXISTE em nenhum engine.** O `description` retornado é blurb editorial do Google: **máx. 151 chars observados, ausente em 12 de 20 resultados**. `type=place` não melhora (109 chars, *menor* que no search). | 6 chamadas reais contra a CLN 313 |
| `whatsapp` (campo dedicado) | Não existe. Só via regex `wa.me` sobre `booking_link` / `reservation.link` / `menu.link` / `website` / `posts[].link`, e **só no `type=place`**. | `grep wa.me` no search = 0; no place = 3 |
| Botão "Agendar" | **NÃO CONFIRMADO.** Nenhum campo próprio observado; provável colisão com `booking_link`. Campo fixo `"nao_confirmado"`. | não observado |
| Botão "Rota / Como chegar" | Não há campo próprio. É **derivado** de `address` + `gps_coordinates`. | não observado |
| `extensions[].from_the_business` como descrição | **Não é descrição.** É array de atributos: `["Se identifica como uma empresa de empreendedoras"]`. | resposta real |
| `instagram_followers`, `email_from_site`, `phone_fixed_from_site` | Não vêm da API. Eram **anotação humana** misturada ao "raw" na v1. Se forem coletados, vão para `_proveniencia` no `enriquecido.json`. | inspeção dos JSONs da v1 |
| `json_restrictor` para economizar | **Testado: retornou `{}` vazio e queimou 1 crédito.** Não usar. | chamada real |
| `engine=google_local` como alternativa | **Descartado.** Não retorna `links`, `website`, `phone`, `extensions` nem `unclaimed_listing`, e vaza geograficamente muito mais (buscando CLN 313 devolveu Asa Sul, SRTVS, CLN 105/403/405). | chamada real |
| `questions_and_answers`, `similar_places_nearby`, `at_this_place`, `located_in`, `hours_last_updated` | Documentados, **ausentes na amostra**. Opcionais no schema; ausência **nunca** reprova nem zera score. | 2 empresas testadas |

---

*Referência do schema — `/prospect-enhanced` · Singular Group*
*[Registrado por: DESKTOP — 2026-08-10]*

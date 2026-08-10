---
lote: "{{LOTE}}"
par: "{{PAR}}"
quadra: {{QUADRA}}
slug: "{{SLUG}}"
status: "{{STATUS}}"
prioridade: "{{PRIORIDADE}}"
icp_score: {{ICP_SCORE}}
score_oportunidade: {{SCORE_OPORTUNIDADE}}
nivel_admissao: "{{NIVEL_ADMISSAO}}"
skill_versao: "prospect-enhanced@1.0"
bu: consultorio-comercial
coletado_em: "{{COLETADO_EM}}"
---

# {{NOME_LOJA}}

**Par de quadras:** {{PAR}} (unidade de varredura) · **Quadra atribuída:** CLN {{QUADRA}} Norte
**Endereço:** {{ENDERECO}} · **Bloco/Loja:** {{BLOCO}} / {{LOJA}} · **CEP:** {{CEP}}
**Nicho:** {{NICHO}} ({{NICHO_TEMPERATURA}}) · **Categorias Google:** {{TYPE_PT}}
**Telefone:** {{TELEFONE}}
**Google Maps:** [abrir](https://www.google.com/maps/place/?q=place_id:{{PLACE_ID}})
**Geo:** método `{{GEO_METODO}}` · confiança `{{GEO_CONFIANCA}}` · conflito: {{GEO_CONFLITO}}
**Data da análise:** {{DATA}} · **Créditos gastos nesta empresa:** {{CUSTO_CHAMADAS}}

---

## Veredito do funil

| Gate | Resultado | Observação |
|------|-----------|------------|
| G4 — Geográfico (310–315) | {{GATE_GEO}} | {{OBS_GEO}} |
| G5/G7 — Franquia / rede | {{GATE_FRANQUIA}} | veredito `{{FRANQUIA_VEREDITO}}` · origem `{{FRANQUIA_ORIGEM}}` · confiança `{{FRANQUIA_CONFIANCA}}` · unidades no DF: {{UNIDADES_DF}} |
| G6 — Não-MEI (filtro hard #1) | {{GATE_MEI}} | {{OBS_MEI}} |
| G9 — ICP ≥ {{CORTE_ICP}} | {{GATE_ICP}} | {{ICP_SCORE}}/10 |
| **Status final** | **{{STATUS}}** | nível de admissão: `{{NIVEL_ADMISSAO}}` · revisar manual: {{REVISAR_MANUAL}} |

---

## CNPJ e porte

| Campo | Valor |
|-------|-------|
| CNPJ | {{CNPJ}} |
| Razão social | {{RAZAO_SOCIAL}} |
| Nome fantasia | {{NOME_FANTASIA}} |
| Porte | {{PORTE_CODIGO}} — {{PORTE_LABEL}} |
| Opção MEI (`opcao_mei`) | {{OPCAO_MEI}} |
| Data de exclusão do MEI | {{DATA_EXCLUSAO_MEI}} |
| É MEI? (regra do gate) | {{EH_MEI}} |
| MEI incerto | {{MEI_INCERTO}} |
| CNAE principal | {{CNAE_PRINCIPAL}} — {{CNAE_DESCRICAO}} |
| Data de abertura | {{DATA_ABERTURA}} |
| Como o CNPJ foi resolvido | método `{{CNPJ_METODO}}` · confiança `{{CNPJ_CONFIANCA}}` |
| Fonte / consulta | {{CNPJ_FONTE}} em {{CNPJ_CONSULTADO_EM}} |

> **Regra do gate (não improvisar):** `eh_mei = (opcao_mei == "S") E (data_exclusao_mei vazia)`.
> Porte MICRO EMPRESA **não** é sinônimo de MEI. Ex-MEI (com data de exclusão preenchida) **passa** no funil.
> Se `cnpj_confianca` for `baixa` ou `nao_resolvido`, a empresa **passa mesmo assim** com a flag "confirmar CNPJ na visita" — o vendedor confirma no balcão em 10 segundos.

---

## Descrição do perfil GMB — o que existe de verdade

| Item | Valor | Origem |
|------|-------|--------|
| `description` (blurb do Google) | {{DESCRICAO_LEN}} caracteres | resumo editorial **do Google**, não texto do dono (máx. observado: 151 chars) |
| Maior texto de post do dono (`posts[].description`) | {{POSTS_TEXTO_LEN_MAX}} caracteres | `place_results.posts[]` — **é aqui que mora o texto longo escrito pelo dono** |
| Nº de posts (Atualizações) | {{POSTS_N}} | `place_results.posts[]` |
| Último post | {{POST_ULTIMO_ISO}} ({{POST_DIAS_DESDE}} dias) | idem |

> ⚠️ **O filtro original "descrição ≥ 500 caracteres" não é implementável via SerpAPI.** A API não expõe a descrição escrita pelo dono ("Do estabelecimento"), só o blurb editorial do Google. O gate foi substituído pelo **ICP — Índice de Cuidado com o Perfil** (ver abaixo). O texto longo do dono aparece nos **posts**, não em `description`.
> A leitura literal da aba "Sobre" exigiria scraping fora da SerpAPI — **não implementado**.

### ICP — Índice de Cuidado com o Perfil (substitui o gate dos 500 caracteres)

| Componente | Pontos | Valor observado |
|------------|--------|-----------------|
| Post nos últimos 180 dias (3 pts; 1 pt se mais antigo) | {{ICP_POSTS}} | {{POST_DIAS_DESDE}} dias |
| Perfil reivindicado (2 pts) | {{ICP_REIVINDICADO}} | `unclaimed_listing`: {{UNCLAIMED_LISTING}} |
| `extensions` ricas — ≥6 chaves (2 pts; 3–5 = 1 pt) | {{ICP_EXTENSIONS}} | {{EXTENSIONS_N}} chaves |
| Horário com os 7 dias (1 pt) | {{ICP_HORAS}} | {{HORAS_DIAS_PREENCHIDOS}}/7 |
| Telefone presente (1 pt) | {{ICP_PHONE}} | {{TELEFONE}} |
| Botão transacional — menu/reserva/pedido (1 pt) | {{ICP_TRANSACIONAL}} | {{OBS_TRANSACIONAL}} |
| Nota ≥ 4,0 com ≥ 5 avaliações (1 pt) | {{ICP_RATING}} | {{RATING}} / {{REVIEWS}} avaliações |

**Composição do ICP:** {{ICP_POSTS}} + {{ICP_REIVINDICADO}} + {{ICP_EXTENSIONS}} + {{ICP_HORAS}} + {{ICP_PHONE}} + {{ICP_TRANSACIONAL}} + {{ICP_RATING}} = **{{ICP_SCORE}}/10** (corte do lote: ≥ {{CORTE_ICP}})

---

## Comentários e prioridade

| Item | Valor |
|------|-------|
| Nota média (`rating`) | {{RATING}} |
| Total de comentários (`reviews`) | {{REVIEWS}} |
| **Prioridade** | **{{PRIORIDADE}}** {{PRIORIDADE_EMOJI}} |
| Último comentário | {{ULTIMO_REVIEW_ISO}} |
| Amostra lida | {{REVIEWS_AMOSTRA_N}} comentários |
| Taxa de resposta do dono | {{TAXA_RESPOSTA}} |
| Assuntos mais citados (`topics`) | {{REVIEW_TOPICS}} |

**Regra de prioridade (literal):** 20–50 comentários → **P1** · mais de 50 → **P2** · menos de 20 → **P3**.
Racional: 20–50 é negócio real e ativo, ainda não saturado. 50+ já é maduro e provavelmente tem agência. <20 é pequeno ou novo demais.

> ⚠️ **Taxa de resposta:** o campo `reviews[].response` é documentado pela SerpAPI mas **não foi observado** na validação. Se vier `null`, o componente correspondente do score entra neutralizado (8 pontos fixos) — não é penalidade nem bônus. Nunca preencher esse campo "no olho".

---

## Botões do perfil GMB

| Botão | Presente | Campo de origem | Status da origem |
|-------|----------|-----------------|------------------|
| Site | {{BOTAO_SITE}} | `website` | confirmado |
| Ligar | {{BOTAO_LIGAR}} | `phone` | confirmado |
| Rota / Como chegar | {{BOTAO_ROTA}} | **derivado** de `address` + `gps_coordinates` | não existe campo próprio |
| WhatsApp | {{BOTAO_WHATSAPP}} | regex `wa\.me` ou `api\.whatsapp\.com` em `website`/`booking_link`/`reservation.link`/`order_online_link`/`menu.link`/`posts[].link` | confirmado — só via `type=place` |
| Reservar | {{BOTAO_RESERVAR}} | `reservar_uma_mesa` (search) / `booking_link` (place) | confirmado |
| Pedir comida / Delivery | {{BOTAO_PEDIDOS}} | `pedir_on_line` (search) / `order_online_link` (place) | confirmado |
| Menu | {{BOTAO_MENU}} | `menu.link` | confirmado — só via `type=place` |
| Agendar | {{BOTAO_AGENDAR}} | — | **não confirmado** (provável colisão com `booking_link`) — não inventar |

**WhatsApp detectado em:** {{WHATSAPP_URL}} (origem: `{{WHATSAPP_ORIGEM}}`)

---

## Site

| Item | Valor |
|------|-------|
| `website` | {{WEBSITE}} |
| Tipo de site | **{{SITE_TIPO}}** ({{SITE_TIPO_EXPLICACAO}}) |
| Leitura comercial | {{SITE_LEITURA}} |

> **"Sem site" NUNCA reprova e NUNCA penaliza.** `site_tipo: ausente` ou `social` é **oportunidade de landing page** e sinal de bom cliente. O que reprova é MEI, franquia grande, fora da quadra e ICP abaixo do corte — nada além disso.
> Atenção: `website` preenchido não significa "tem site". Instagram, Facebook, Google Sites e LP de agência entram no campo `website` e não são site próprio.

---

## Score de oportunidade (o que há para vender)

| # | Componente | Pontos | Base |
|---|------------|--------|------|
| 1 | Lacuna de site (0–20) | {{SC_SITE}} | `site_tipo` = {{SITE_TIPO}} |
| 2 | Sem WhatsApp (0–15) | {{SC_WHATSAPP}} | {{BOTAO_WHATSAPP}} |
| 3 | Botões transacionais ausentes (0–15) | {{SC_BOTOES}} | {{OBS_BOTOES}} |
| 4 | Não responde comentários (0–20) | {{SC_REVIEWS}} | taxa {{TAXA_RESPOSTA}} |
| 5 | Silêncio de conteúdo (0–10) | {{SC_CONTEUDO}} | último post há {{POST_DIAS_DESDE}} dias |
| 6 | Perfil incompleto (0–10) | {{SC_COMPLETUDE}} | telefone/horário/extensions |
| 7 | Nicho quente (0–10) | {{SC_NICHO}} | {{NICHO}} ({{NICHO_TEMPERATURA}}) |

**Composição do score:** {{SC_SITE}} + {{SC_WHATSAPP}} + {{SC_BOTOES}} + {{SC_REVIEWS}} + {{SC_CONTEUDO}} + {{SC_COMPLETUDE}} + {{SC_NICHO}} = **{{SCORE_OPORTUNIDADE}}/100**
**Posição no lote:** {{RANKING_LOTE}}º · ordenação = prioridade (P1→P2→P3) primeiro, score só desempata **dentro** da faixa.

> O **ICP mede quem pode comprar** (maturidade e verba). O **score mede o que há para vender** (dor e lacuna). São opostos de propósito: quem posta toda semana tem ICP alto e score baixo em conteúdo. Isso não é erro.

---

## Oportunidades Singular

### 1. {{OPORTUNIDADE_1_SERVICO}}
**Problema concreto:** {{OPORTUNIDADE_1_PROBLEMA}}
> {{OPORTUNIDADE_1_PITCH}}

### 2. {{OPORTUNIDADE_2_SERVICO}}
**Problema concreto:** {{OPORTUNIDADE_2_PROBLEMA}}
> {{OPORTUNIDADE_2_PITCH}}

### 3. {{OPORTUNIDADE_3_SERVICO}}
**Problema concreto:** {{OPORTUNIDADE_3_PROBLEMA}}
> {{OPORTUNIDADE_3_PITCH}}

### Serviços que NÃO fazem sentido aqui
{{SERVICOS_DESCARTADOS}}

**Ticket sugerido:** {{TICKET_SUGERIDO}}
**Quem procurar pelo nome:** {{QUEM_PROCURAR}} ({{ORIGEM_DO_NOME}})
**Melhor horário para bater na porta:** {{MELHOR_HORARIO}}

---

## Roteiro de abordagem na porta (primeiros 20 segundos)

**0–5s · Abertura** (dizer o nome da loja, nunca "boa tarde, tudo bem?")
> "{{FALA_ABERTURA}}"

**5–12s · Ancoragem no dado** (uma observação verificável do perfil dele — nunca elogio genérico)
> "{{FALA_ANCORAGEM}}"

**12–18s · Pergunta de qualificação** (fechada, que ele responde de pé)
> "{{FALA_PERGUNTA}}"

**18–20s · Ponte** (pedir 5 minutos ou o WhatsApp, nunca "posso te mandar uma proposta?")
> "{{FALA_PONTE}}"

**Se o dono não estiver:** {{PLANO_B_DONO_AUSENTE}}
**Objeção mais provável:** {{OBJECAO_PROVAVEL}} → resposta: {{RESPOSTA_OBJECAO}}
**Prova visual para mostrar no celular:** {{PROVA_VISUAL}}

> **Regra de campo:** só falar de dado que está neste relatório. Se um campo está como "Não encontrado", ele **não** entra na conversa — dado inventado na porta queima o lead e a Singular junto.

---

## Concorrentes / vizinhança (`people_also_search_for`)

{{PEOPLE_ALSO_SEARCH_FOR}}

---

## Pendências e limitações desta ficha

- {{PENDENCIA_1}}
- {{PENDENCIA_2}}
- Arquivos brutos: `{{SERPAPI_RAW_PATH}}` (dump literal, intocado) e `{{ENRIQUECIDO_PATH}}` (derivado, com proveniência por campo).

*Relatório gerado por /prospect-enhanced — Singular Group*
*[Registrado por: DESKTOP — {{DATA}}]*

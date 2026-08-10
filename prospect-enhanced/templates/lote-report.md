---
lote: "{{LOTE}}"
quadras: [310, 311, 312, 313, 314, 315]
pares: ["310-311", "312-313", "314-315"]
data: "{{DATA}}"
meta_aprovadas: 40
total_aprovadas: {{TOTAL_APROVADAS}}
total_reserva: {{TOTAL_RESERVA}}
total_reprovadas: {{TOTAL_REPROVADAS}}
corte_icp: {{CORTE_ICP}}
nivel_admissao_max: "{{NIVEL_ADMISSAO_MAX}}"
creditos_gastos: {{CREDITOS_GASTOS}}
creditos_orcados: {{CREDITOS_ORCADOS}}
skill_versao: "prospect-enhanced@1.0"
bu: consultorio-comercial
---

# Lote {{LOTE}} — CLN 310–315 Norte

**Escopo:** quadras 310 a 315 Norte, varridas por **par de entrequadra** (310/311, 312/313, 314/315).
**Data da varredura:** {{DATA}}
**Meta:** 40 empresas aprovadas no lote — **piso, não teto**. Todas as aprovadas estão listadas.
**Resultado:** **{{TOTAL_APROVADAS}} aprovadas** ({{TOTAL_P1}} P1 · {{TOTAL_P2}} P2 · {{TOTAL_P3}} P3) + {{TOTAL_RESERVA}} em lista de reserva.
**Custo:** {{CREDITOS_GASTOS}} créditos SerpAPI (orçado: {{CREDITOS_ORCADOS}} · teto duro: 400) · CNPJ/CEP: R$ 0,00.

---

## Resumo executivo

{{RESUMO_EXECUTIVO}}

| Indicador | Valor |
|-----------|-------|
| Empresas aprovadas | {{TOTAL_APROVADAS}} (meta: 40) |
| Prioridade 1 (20–50 comentários) | {{TOTAL_P1}} |
| Prioridade 2 (mais de 50) | {{TOTAL_P2}} |
| Prioridade 3 (menos de 20) | {{TOTAL_P3}} |
| Sem site próprio (`ausente` + `social`) | {{QTD_SEM_SITE}} — alvo direto de landing page |
| Sem WhatsApp detectado | {{QTD_SEM_WHATSAPP}} |
| Perfil não reivindicado | {{QTD_UNCLAIMED}} — venda de "reivindicar seu perfil" |
| Score médio de oportunidade | {{SCORE_MEDIO}}/100 |
| ICP médio das aprovadas | {{ICP_MEDIO}}/10 (corte do lote: {{CORTE_ICP}}) |
| Nicho mais frequente | {{NICHO_TOP}} |

**As 3 leituras que mais importam para a semana:**
1. {{LEITURA_1}}
2. {{LEITURA_2}}
3. {{LEITURA_3}}

---

## Funil em números

| Gate | Entraram | Sobreviveram | Cortadas | Custo (créditos) | Motivo do corte |
|------|----------|--------------|----------|------------------|-----------------|
| G0 — Roster CNPJ (offline) | {{G0_IN}} ativas | {{G0_OUT}} não-MEI | {{G0_CUT}} | 0 | MEI no cadastro da Receita |
| G1 — Coordenadas dos pares | 3 pares | {{G1_OUT}} | — | {{G1_CUSTO}} | — |
| G2 — Discovery GMB | {{G2_QUERIES}} queries | {{G2_OUT}} resultados brutos | — | {{G2_CUSTO}} | — |
| G3 — Deduplicação | {{G3_IN}} | {{G3_OUT}} | {{G3_CUT}} | 0 | `place_id` repetido entre pares |
| G4 — Geográfico 310–315 | {{G4_IN}} | {{G4_OUT}} | {{G4_CUT}} | 0 | fora do escopo (413, 713, 214, 215, Asa Sul…) |
| G5 — Franquia (blacklist) | {{G5_IN}} | {{G5_OUT}} | {{G5_CUT}} | 0 | rede nacional / regional grande |
| G6 — Não-MEI (join roster) | {{G6_IN}} | {{G6_OUT}} | {{G6_CUT}} | 0 | `opcao_mei = S` sem data de exclusão |
| G7 — Franquia por contagem | {{G7_IN}} | {{G7_OUT}} | {{G7_CUT}} | {{G7_CUSTO}} | ≥ 5 unidades no DF |
| G8 — Enriquecimento `type=place` | {{G8_IN}} | {{G8_OUT}} | {{G8_CUT}} | {{G8_CUSTO}} | falha de API (vai para reserva, não descarte) |
| G9 — ICP ≥ {{CORTE_ICP}} | {{G9_IN}} | {{G9_OUT}} | {{G9_CUT}} | 0 | perfil abandonado → lista de reserva |
| G10 — Comentários / taxa de resposta | {{G10_IN}} | {{G10_OUT}} | 0 | {{G10_CUSTO}} | — |
| **Aprovadas finais** | — | **{{TOTAL_APROVADAS}}** | — | **{{CREDITOS_GASTOS}}** | — |

**Taxa de aprovação sobre o universo geográfico:** {{TAXA_APROVACAO}}% ({{TOTAL_APROVADAS}} de {{G4_OUT}} empresas dentro das quadras).

### Cortes por motivo

| Motivo (`motivo_descarte`) | Qtd | % dos cortes |
|---------------------------|-----|--------------|
| `fora-do-escopo` | {{CUT_GEO}} | {{PCT_GEO}}% |
| `mei` | {{CUT_MEI}} | {{PCT_MEI}}% |
| `franquia` | {{CUT_FRANQUIA}} | {{PCT_FRANQUIA}}% |
| `duplicata` | {{CUT_DEDUP}} | {{PCT_DEDUP}}% |
| `icp-abaixo-do-corte` (→ reserva) | {{CUT_ICP}} | {{PCT_ICP}}% |

### Meta de 40 — escada de relaxamento aplicada

| Degrau | Aplicado? | O que relaxou | Ganho | Custo |
|--------|-----------|---------------|-------|-------|
| base | — | nenhum relaxamento | {{GANHO_BASE}} | — |
| R1 — ICP ≥ 4 | {{R1_APLICADO}} | corte do ICP | {{R1_GANHO}} | 0 |
| R2 — admite perfil não reivindicado | {{R2_APLICADO}} | `unclaimed_listing = true` | {{R2_GANHO}} | 0 |
| R3 — admite CNPJ não resolvido | {{R3_APLICADO}} | confirmar na visita | {{R3_GANHO}} | 0 |
| R4 — admite rede de 5–7 sem posts clonados | {{R4_APLICADO}} | gestão local comprovada | {{R4_GANHO}} | {{R4_CUSTO}} |
| R5 — estende ao par contíguo | {{R5_APLICADO}} | geografia | {{R5_GANHO}} | {{R5_CUSTO}} |

**Nunca relaxado:** MEI confirmado · franquia nacional / rede ≥ 10 unidades no Brasil · gate geográfico (o R5 amplia o escopo, não o fura).
{{NOTA_PISO_HONESTIDADE}}

### Orçamento e saldo

| Item | Valor |
|------|-------|
| Créditos orçados | {{CREDITOS_ORCADOS}} |
| Créditos gastos | {{CREDITOS_GASTOS}} |
| Saldo antes / depois | {{SALDO_ANTES}} / {{SALDO_DEPOIS}} |
| Custo médio por aprovada | {{CUSTO_POR_APROVADA}} créditos |
| Roster CNPJ (Casa dos Dados + OpenCNPJ + ViaCEP) | R$ 0,00 |

---

## Ranking — Prioridade 1 (20 a 50 comentários) 🔴

Melhor alvo do lote: negócio real e ativo, ainda não saturado, dono decide no balcão.

| # | Empresa | Par / Quadra | Nicho | Coment. | Site | WhatsApp | ICP | Score | Ganho principal |
|---|---------|--------------|-------|---------|------|----------|-----|-------|-----------------|
{{RANKING_P1}}

## Ranking — Prioridade 2 (mais de 50 comentários) 🟡

Maduro, provavelmente já tem agência. Vale a visita, mas depois dos P1.

| # | Empresa | Par / Quadra | Nicho | Coment. | Site | WhatsApp | ICP | Score | Ganho principal |
|---|---------|--------------|-------|---------|------|----------|-----|-------|-----------------|
{{RANKING_P2}}

## Ranking — Prioridade 3 (menos de 20 comentários) 🟢

Pequeno ou novo demais. Só se sobrar tempo na rota.

| # | Empresa | Par / Quadra | Nicho | Coment. | Site | WhatsApp | ICP | Score | Ganho principal |
|---|---------|--------------|-------|---------|------|----------|-----|-------|-----------------|
{{RANKING_P3}}

**Ordenação usada:** prioridade (P1 → P2 → P3) → `score_oportunidade` decrescente → `reviews` decrescente → nome. **Nunca por score global.**

### Lista B — reserva ({{TOTAL_RESERVA}} empresas)

Reprovadas só no ICP ou com dado ausente. Não são lixo: são o primeiro estoque a readmitir se o lote render abaixo da meta.

| Empresa | Par / Quadra | Motivo | Readmite em |
|---------|--------------|--------|-------------|
{{LISTA_RESERVA}}

---

## Rota de visita sugerida

Uma rota por par de entrequadra. A loja fica fisicamente **entre** as duas quadras — caminhar a via comercial inteira cobre as duas faces sem voltar.

### Par 310/311 — {{ROTA_310_QTD}} paradas · {{ROTA_310_TEMPO}}
**Início:** {{ROTA_310_INICIO}} · **Fim:** {{ROTA_310_FIM}} · **Melhor janela:** {{ROTA_310_JANELA}}

{{ROTA_310_PARADAS}}

### Par 312/313 — {{ROTA_312_QTD}} paradas · {{ROTA_312_TEMPO}}
**Início:** {{ROTA_312_INICIO}} · **Fim:** {{ROTA_312_FIM}} · **Melhor janela:** {{ROTA_312_JANELA}}

{{ROTA_312_PARADAS}}

### Par 314/315 — {{ROTA_314_QTD}} paradas · {{ROTA_314_TEMPO}}
**Início:** {{ROTA_314_INICIO}} · **Fim:** {{ROTA_314_FIM}} · **Melhor janela:** {{ROTA_314_JANELA}}

{{ROTA_314_PARADAS}}

**Regras da rota:** P1 primeiro, sempre. Restaurante e lanchonete **fora** do horário de almoço (11h30–14h30). Clínica e consultório no começo da manhã. Salão e barbearia evitar sábado. Quem está marcado `revisar_manual: true` só depois de confirmar o dado.

---

## Oportunidades por serviço

| Serviço Singular | Empresas com a lacuna | Empresas P1 | Ticket estimado | Argumento-padrão |
|------------------|----------------------|-------------|-----------------|------------------|
| Landing page | {{QTD_LP}} | {{QTD_LP_P1}} | {{TICKET_LP}} | {{ARG_LP}} |
| Estratégia de WhatsApp | {{QTD_WPP}} | {{QTD_WPP_P1}} | {{TICKET_WPP}} | {{ARG_WPP}} |
| Gestão de Google Meu Negócio | {{QTD_GMB}} | {{QTD_GMB_P1}} | {{TICKET_GMB}} | {{ARG_GMB}} |
| Social media | {{QTD_SOCIAL}} | {{QTD_SOCIAL_P1}} | {{TICKET_SOCIAL}} | {{ARG_SOCIAL}} |
| Reivindicar perfil GMB | {{QTD_CLAIM}} | {{QTD_CLAIM_P1}} | {{TICKET_CLAIM}} | {{ARG_CLAIM}} |

## Distribuição por nicho

| Nicho | Aprovadas | Temperatura | Serviço que vende melhor |
|-------|-----------|-------------|--------------------------|
{{TABELA_NICHOS}}

## Distribuição por quadra

| Quadra | Varridas | Aprovadas | P1 | Score médio |
|--------|----------|-----------|----|-------------|
| CLN 310 | {{Q310_VARRIDAS}} | {{Q310_APROVADAS}} | {{Q310_P1}} | {{Q310_SCORE}} |
| CLN 311 | {{Q311_VARRIDAS}} | {{Q311_APROVADAS}} | {{Q311_P1}} | {{Q311_SCORE}} |
| CLN 312 | {{Q312_VARRIDAS}} | {{Q312_APROVADAS}} | {{Q312_P1}} | {{Q312_SCORE}} |
| CLN 313 | {{Q313_VARRIDAS}} | {{Q313_APROVADAS}} | {{Q313_P1}} | {{Q313_SCORE}} |
| CLN 314 | {{Q314_VARRIDAS}} | {{Q314_APROVADAS}} | {{Q314_P1}} | {{Q314_SCORE}} |
| CLN 315 | {{Q315_VARRIDAS}} | {{Q315_APROVADAS}} | {{Q315_P1}} | {{Q315_SCORE}} |

---

## Alertas e pendências

- **Revisar manualmente antes da rota ({{QTD_REVISAR_MANUAL}} empresas):** {{LISTA_REVISAR_MANUAL}}
- **CNPJ não resolvido (confirmar na visita):** {{QTD_CNPJ_NAO_RESOLVIDO}} empresas
- **Conflito geográfico (regex × GPS):** {{QTD_GEO_CONFLITO}} empresas
- **Marcas novas gravadas na blacklist neste lote:** {{MARCAS_NOVAS_BLACKLIST}}
- **CEPs que voltaram vazios no roster:** {{CEPS_VAZIOS}}
- {{ALERTA_LIVRE}}

## Observações metodológicas

- **Descrição ≥ 500 caracteres:** não implementável — a SerpAPI não expõe a descrição escrita pelo dono. Substituída pelo **ICP** (corte calibrado neste lote em **{{CORTE_ICP}}**, para taxa de aprovação entre 25% e 45%). O corte é **deste lote**, não global.
- **Taxa de resposta a comentários:** {{STATUS_TAXA_RESPOSTA}} (campo `reviews[].response` é documentado mas foi validado em separado; se indisponível, o componente entra neutralizado em 8 pontos para todos).
- **"Sem site" não penaliza** — é oportunidade de venda.
- **Botão "Agendar"** fica como `nao_confirmado`: não há campo próprio na API. **Botão "Rota"** é derivado de `address` + GPS, não é campo.
- **Roster CNPJ** baixado em {{ROSTER_BAIXADO_EM}} (TTL 30 dias). Fonte canônica: OpenCNPJ.
- Dados brutos por empresa em `par-{{PAR}}/{slug}/serpapi-raw.json` (dump literal). Planilha completa, **incluindo reprovadas**, em `funil.csv`.

---

```
=== PROSPECÇÃO {{LOTE}} — CLN 310–315 NORTE ===
📁 Lote:        {{TOTAL_VARRIDAS}} varridas → {{TOTAL_APROVADAS}} aprovadas ({{TOTAL_P1}} P1 · {{TOTAL_P2}} P2 · {{TOTAL_P3}} P3)
📋 Meta:        40 (piso) — {{STATUS_META}}
🔗 Custo:       {{CREDITOS_GASTOS}} créditos SerpAPI · R$ 0,00 em CNPJ/CEP
🗂 Saída:       lotes/{{LOTE}}/ (funil.csv + lote-report.md + {{TOTAL_APROVADAS}} fichas)
```

*Relatório gerado por /prospect-enhanced — Singular Group*
*[Registrado por: DESKTOP — {{DATA}}]*

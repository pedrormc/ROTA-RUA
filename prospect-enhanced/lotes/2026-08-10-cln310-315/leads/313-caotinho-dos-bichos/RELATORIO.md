# Cãotinho dos Bichos

**CLN 313 Norte** (par 312/313) · Prioridade **P2** · Lote `2026-08-10-cln310-315`

> Dados coletados do Google Maps via SerpAPI em 2026-08-10. Evidência crua: `../../raw/q313-s20.json`.

## Identificação

| Campo | Valor |
|---|---|
| Nome | Cãotinho dos Bichos |
| Nicho (categoria Google) | Pet Shop |
| Endereço | Asa Norte Comércio Local Norte 313, BL D - Asa Norte, Brasília - DF, 70766-100 |
| Quadra (regex endereço) | CLN 313 |
| Quadra (conferência por CEP) | CLN 313 |
| Par de entrequadra | 312/313 |
| Telefone | (61) 3202-1183 |
| Site | https://caotinhodosbichos.com.br/ |
| place_id | `ChIJq6p63SU6WpMRjZiSx-HN_Ks` |

## Google Meu Negócio

| Sinal | Valor | Leitura |
|---|---|---|
| Nota | 4.6 | Boa reputação |
| Comentários | 152 | **P2** pela regra do lote (20–50 = P1 · >50 = P2 · <20 = P3) |
| Botão "Site" | presente | — |
| Botão "Ligar" | presente | — |
| Botão "Rota" | derivado do endereço | O Google Maps não expõe esse botão em campo próprio — presença inferida. |
| Descrição do dono (≥500 car.) | **NÃO MEDIDO** | Exige chamada `type=place` por lead (1 crédito cada). Ver limitações abaixo. |
| Taxa de resposta a comentários | **NÃO MEDIDO** | Exige `google_maps_reviews` por lead (1 crédito cada). |

## Situação cadastral (gate MEI)

| Campo | Valor |
|---|---|
| CNPJ | — não resolvido |
| Porte | — |
| Optante MEI | — |
| Status do gate | `PENDENTE - busca reversa nome->CNPJ nao resolvida automaticamente` |

**Como fechar este gate** (procedimento validado, 1 crédito SerpAPI por lead):
1. `engine=google`, `q="Cãotinho dos Bichos" CNPJ Brasilia` → extrair candidatos com regex de CNPJ.
2. Para cada candidato, `GET https://api.opencnpj.org/{cnpj}` (gratuito, exige `User-Agent`).
3. Conferir `cep` do retorno contra a quadra. **Atenção:** no piloto o CEP da Receita divergiu do CEP do Google em 1 de 2 casos — conferência humana obrigatória antes de cortar.
4. Ler `opcao_mei`: `"S"` = MEI → **reprova**; `"N"` = segue.

## Oportunidades Singular

| Problema observado | Serviço | Argumento na porta |
|---|---|---|
| Estratégia de WhatsApp | **WhatsApp + Base de Clientes** | Na hora da compra, oferece desconto no mês do aniversário: o cliente entrega nome, telefone e mês. Com essa base você manda oferta certeira em vez de queimar dinheiro em tráfego. |
| Nicho: Pet Shop | **WhatsApp + base de clientes** | Banho e tosa é agenda recorrente: lembrete no WhatsApp vale mais que tráfego pago. |

## Roteiro de abordagem (primeiros 20 segundos)

> "Bom dia! Eu sou da Singular, a gente cuida da presença digital aqui da 312/313 Norte.
> Dei uma olhada no perfil de vocês no Google antes de entrar: 152 avaliações, nota 4.6.
> Posso te mostrar em dois minutos o que isso está custando em cliente por semana?"

---
*[Registrado por: DESKTOP — 2026-08-10]*

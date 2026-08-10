# RARUS Barbearia e Visagismo em Brasília

**CLN 310 Norte** (par 310/311) · Prioridade **P2** · Lote `2026-08-10-cln310-315`

> Dados coletados do Google Maps via SerpAPI em 2026-08-10. Evidência crua: `../../raw/q310-s20.json`.

## Identificação

| Campo | Valor |
|---|---|
| Nome | RARUS Barbearia e Visagismo em Brasília |
| Nicho (categoria Google) | Barbearia |
| Endereço | Asa Norte CLN 310 Lj 07 - Asa Norte, Brasília - DF, 70756-540 |
| Quadra (regex endereço) | CLN 310 |
| Quadra (conferência por CEP) | CLN 310 |
| Par de entrequadra | 310/311 |
| Telefone | (61) 3536-7900 |
| Site | https://app.faroldabarbearia.com.br/agendar/rarusbrasilia |
| place_id | `ChIJX6v8LGM7WpMRBgbdQzVN2hg` |

## Google Meu Negócio

| Sinal | Valor | Leitura |
|---|---|---|
| Nota | 5 | Boa reputação |
| Comentários | 663 | **P2** pela regra do lote (20–50 = P1 · >50 = P2 · <20 = P3) |
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
1. `engine=google`, `q="RARUS Barbearia e Visagismo em Brasília" CNPJ Brasilia` → extrair candidatos com regex de CNPJ.
2. Para cada candidato, `GET https://api.opencnpj.org/{cnpj}` (gratuito, exige `User-Agent`).
3. Conferir `cep` do retorno contra a quadra. **Atenção:** no piloto o CEP da Receita divergiu do CEP do Google em 1 de 2 casos — conferência humana obrigatória antes de cortar.
4. Ler `opcao_mei`: `"S"` = MEI → **reprova**; `"N"` = segue.

## Oportunidades Singular

| Problema observado | Serviço | Argumento na porta |
|---|---|---|
| Estratégia de WhatsApp | **WhatsApp + Base de Clientes** | Na hora da compra, oferece desconto no mês do aniversário: o cliente entrega nome, telefone e mês. Com essa base você manda oferta certeira em vez de queimar dinheiro em tráfego. |
| Nicho: Barbearia | **Gestão GMB + WhatsApp** | Barbearia é recorrência pura: quem corta a cada 20 dias precisa de lembrete, não de anúncio. |

## Roteiro de abordagem (primeiros 20 segundos)

> "Bom dia! Eu sou da Singular, a gente cuida da presença digital aqui da 310/311 Norte.
> Dei uma olhada no perfil de vocês no Google antes de entrar: 663 avaliações, nota 5.
> Posso te mostrar em dois minutos o que isso está custando em cliente por semana?"

---
*[Registrado por: DESKTOP — 2026-08-10]*

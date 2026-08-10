# Superchance

**CLN 313 Norte** (par 312/313) · Prioridade **P1** · Lote `2026-08-10-cln310-315`

> Dados coletados do Google Maps via SerpAPI em 2026-08-10. Evidência crua: `../../raw/q313-s0.json`.

## Identificação

| Campo | Valor |
|---|---|
| Nome | Superchance |
| Nicho (categoria Google) | Casa lotérica |
| Endereço | Asa Norte Comércio Local Norte 313, BL E - Plano Piloto, Brasília - DF, 70766-550 |
| Quadra (regex endereço) | CLN 313 |
| Quadra (conferência por CEP) | CLN 313 |
| Par de entrequadra | 312/313 |
| Telefone | — não publicado no perfil |
| Site | — não publicado no perfil |
| place_id | `ChIJPQxIwyU6WpMR_5ukogwAnkc` |

## Google Meu Negócio

| Sinal | Valor | Leitura |
|---|---|---|
| Nota | 4.3 | Aceitável |
| Comentários | 29 | **P1** pela regra do lote (20–50 = P1 · >50 = P2 · <20 = P3) |
| Botão "Site" | **AUSENTE** | Falta de site **não desqualifica**: é justamente a venda de landing page. |
| Botão "Ligar" | **AUSENTE** | Sem telefone o perfil perde a conversão mais barata que existe. |
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
1. `engine=google`, `q="Superchance" CNPJ Brasilia` → extrair candidatos com regex de CNPJ.
2. Para cada candidato, `GET https://api.opencnpj.org/{cnpj}` (gratuito, exige `User-Agent`).
3. Conferir `cep` do retorno contra a quadra. **Atenção:** no piloto o CEP da Receita divergiu do CEP do Google em 1 de 2 casos — conferência humana obrigatória antes de cortar.
4. Ler `opcao_mei`: `"S"` = MEI → **reprova**; `"N"` = segue.

> **Conferir manualmente:** Lotérica - permissionário local (exceção da blacklist)

## Oportunidades Singular

| Problema observado | Serviço | Argumento na porta |
|---|---|---|
| Sem site no perfil | **Criação de Landing Page** | Quando alguém pesquisa "casa lotérica Asa Norte", este negócio não tem para onde mandar o clique. |
| Sem telefone no perfil | **Gestão Google Meu Negócio** | Perfil sem telefone perde a ligação de quem já estava pronto para comprar. |
| Estratégia de WhatsApp | **WhatsApp + Base de Clientes** | Na hora da compra, oferece desconto no mês do aniversário: o cliente entrega nome, telefone e mês. Com essa base você manda oferta certeira em vez de queimar dinheiro em tráfego. |

## Roteiro de abordagem (primeiros 20 segundos)

> "Bom dia! Eu sou da Singular, a gente cuida da presença digital aqui da 312/313 Norte.
> Dei uma olhada no perfil de vocês no Google antes de entrar: 29 avaliações, nota 4.3, e reparei que não tem site no perfil.
> Posso te mostrar em dois minutos o que isso está custando em cliente por semana?"

---
*[Registrado por: DESKTOP — 2026-08-10]*

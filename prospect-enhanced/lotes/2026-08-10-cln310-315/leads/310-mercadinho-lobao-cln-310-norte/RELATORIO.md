# Mercadinho Lobão - CLN 310 Norte

**CLN 310 Norte** (par 310/311) · Prioridade **P2** · Lote `2026-08-10-cln310-315`

> Dados coletados do Google Maps via SerpAPI em 2026-08-10. Evidência crua: `../../raw/q310-s20.json`.

## Identificação

| Campo | Valor |
|---|---|
| Nome | Mercadinho Lobão - CLN 310 Norte |
| Nicho (categoria Google) | Loja de cervejas |
| Endereço | Asa Norte Comércio Local Norte 310 Bl A Loja 16 - Asa Norte, Brasília - DF, 70756-500 |
| Quadra (regex endereço) | CLN 310 |
| Quadra (conferência por CEP) | CLN 310 |
| Par de entrequadra | 310/311 |
| Telefone | — não publicado no perfil |
| Site | http://mercadinholobao.com.br/ |
| place_id | `ChIJy5QocLE7WpMRg81XG8UhRno` |

## Google Meu Negócio

| Sinal | Valor | Leitura |
|---|---|---|
| Nota | 4.5 | Boa reputação |
| Comentários | 56 | **P2** pela regra do lote (20–50 = P1 · >50 = P2 · <20 = P3) |
| Botão "Site" | presente | — |
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
1. `engine=google`, `q="Mercadinho Lobão - CLN 310 Norte" CNPJ Brasilia` → extrair candidatos com regex de CNPJ.
2. Para cada candidato, `GET https://api.opencnpj.org/{cnpj}` (gratuito, exige `User-Agent`).
3. Conferir `cep` do retorno contra a quadra. **Atenção:** no piloto o CEP da Receita divergiu do CEP do Google em 1 de 2 casos — conferência humana obrigatória antes de cortar.
4. Ler `opcao_mei`: `"S"` = MEI → **reprova**; `"N"` = segue.

## Oportunidades Singular

| Problema observado | Serviço | Argumento na porta |
|---|---|---|
| Sem telefone no perfil | **Gestão Google Meu Negócio** | Perfil sem telefone perde a ligação de quem já estava pronto para comprar. |
| Estratégia de WhatsApp | **WhatsApp + Base de Clientes** | Na hora da compra, oferece desconto no mês do aniversário: o cliente entrega nome, telefone e mês. Com essa base você manda oferta certeira em vez de queimar dinheiro em tráfego. |

## Roteiro de abordagem (primeiros 20 segundos)

> "Bom dia! Eu sou da Singular, a gente cuida da presença digital aqui da 310/311 Norte.
> Dei uma olhada no perfil de vocês no Google antes de entrar: 56 avaliações, nota 4.5.
> Posso te mostrar em dois minutos o que isso está custando em cliente por semana?"

---
*[Registrado por: DESKTOP — 2026-08-10]*

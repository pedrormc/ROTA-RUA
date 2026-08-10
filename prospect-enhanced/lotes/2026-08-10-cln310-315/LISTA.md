---
title: "Lote CLN 310-315 Norte — prospecção real"
lote: "2026-08-10-cln310-315"
data_coleta: "2026-08-10"
fonte: "SerpAPI google_maps (type=search), 12 chamadas + 3 de piloto CNPJ"
varridos: 202
dentro_do_escopo: 138
aprovados: 115
reprovados: 23
bu: consultorio-comercial
---

# Lote CLN 310–315 Norte — 115 leads reais

**Coleta:** 2026-08-10 · **Motor:** SerpAPI `google_maps` · **Evidência crua:** `raw/` (12 arquivos JSON)

## Funil (números reais)

| Etapa | Restam |
|---|---|
| Resultados brutos das 12 buscas | 240 |
| Únicos por `place_id` | 202 |
| Dentro das quadras 310–315 (regex de endereço) | 138 |
| Menos imóveis/infraestrutura (não são empresa) | 126 |
| Menos grandes franquias/redes | **115** |
| Menos MEI | **gate não aplicado — ver limitações** |

Meta era 40. **Entregues 115** — a meta é piso, não teto, então vieram todos que passaram.

## Prioridade (regra do lote)

| Faixa | Regra | Quantos |
|---|---|---|
| **P1** | 20 a 50 comentários | **26** |
| **P2** | mais de 50 | 57 |
| **P3** | menos de 20 | 32 |

Cobertura de site: **56 dos 115 não têm site no perfil** — e isso **não reprova**, é a venda de landing page.

## ⚠️ Limitações honestas deste lote

1. **Gate MEI não aplicado.** Não existe busca reversa gratuita de nome→CNPJ. O procedimento validado está em cada relatório (SerpAPI → OpenCNPJ → `opcao_mei`), custa 1 crédito por lead. No piloto de 3, 2 acharam CNPJ e **o CEP da Receita divergiu do CEP do Google em 1 caso** — por isso não foi automatizado sem revisão.
2. **Descrição ≥500 caracteres não medida.** Exige `type=place` por lead. A própria fase de recon mediu que o campo `description` do SerpAPI é blurb editorial do Google (máx. ~151 caracteres observados), **não** a descrição do dono — o filtro literal reprovaria todo mundo.
3. **Taxa de resposta a comentários não medida** (1 crédito por lead em `google_maps_reviews`).
4. **Orçamento:** conta SerpAPI está no **plano Free**. Foram gastos 19 créditos; restam ~155 no mês.
5. A blacklist de franquias tinha 118 marcas nacionais e **não cobria as redes presentes aqui** (Big Box, Lojas Mundial, Drogasil, Pague Menos, Pacheco, Drogaria São Paulo). Foram cortadas manualmente e precisam entrar em `data/blacklist-redes.json`.

## Conferir manualmente (não cortados de propósito)

- **Posto Verde Amarelo** (CLN 311) — Posto de combustível - revendedor costuma ser dono local
- **Superchance** (CLN 313) — Lotérica - permissionário local (exceção da blacklist)
- **Posto Petrobras** (CLN 314) — Posto de combustível - revendedor costuma ser dono local
- **Loterica Pé Quente** (CLN 314) — Lotérica - permissionário local (exceção da blacklist)
- **EVS 315 Norte :: Herbalife** (CLN 315) — Marca Herbalife, mas operação local independente

## Aprovados por quadra

### CLN 310 Norte — 23 aprovados

| Prio | Rev | Nota | Site | Fone | Estabelecimento | Nicho |
|---|---|---|---|---|---|---|
| P1 | 39 | 4.2 | **não** | sim | [Refrigeração Querobino](leads/310-refrigeracao-querobino/RELATORIO.md) | Serviço de conserto de refrigeradores |
| P2 | 899 | 4.9 | sim | sim | [Senhor Smart - Brasília /DF (Asa Norte)](leads/310-senhor-smart-brasilia-df-asa-norte/RELATORIO.md) | Oficina de reparos de celulares |
| P2 | 663 | 5 | sim | sim | [RARUS Barbearia e Visagismo em Brasília](leads/310-rarus-barbearia-e-visagismo-em-brasilia/RELATORIO.md) | Barbearia |
| P2 | 634 | 4.9 | **não** | sim | [Adorne Professional Body Piercing](leads/310-adorne-professional-body-piercing/RELATORIO.md) | Loja de body piercing |
| P2 | 557 | 5 | sim | sim | [Kariocas Biquínis e Fitness](leads/310-kariocas-biquinis-e-fitness/RELATORIO.md) | Loja de moda feminina |
| P2 | 515 | 4.6 | sim | sim | [Açaí Puríssimo - 310 Norte](leads/310-acai-purissimo-310-norte/RELATORIO.md) | Lanchonete |
| P2 | 507 | 4.9 | sim | sim | [Senhora BaforadaTabacaria](leads/310-senhora-baforadatabacaria/RELATORIO.md) | Tabacaria |
| P2 | 313 | 4.6 | sim | sim | [Endossa / Bsb Norte](leads/310-endossa-bsb-norte/RELATORIO.md) | Loja de acessórios de moda |
| P2 | 251 | 5 | sim | sim | [Perfect Cortinas](leads/310-perfect-cortinas/RELATORIO.md) | Loja de cortinas e persianas |
| P2 | 228 | 4.9 | **não** | sim | [Borracharia Ponto Certo](leads/310-borracharia-ponto-certo/RELATORIO.md) | Borracharia |
| P2 | 210 | 4.5 | sim | sim | [Harmonia Instrumentos Musicais](leads/310-harmonia-instrumentos-musicais/RELATORIO.md) | Loja de Instrumentos Musicais |
| P2 | 182 | 4.8 | sim | sim | [Cão Mais Gato - Boutique Pet e Veterinária](leads/310-cao-mais-gato-boutique-pet-e-veterinaria/RELATORIO.md) | Veterinário |
| P2 | 94 | 4 | sim | sim | [Lavou Lavanderia Self Service](leads/310-lavou-lavanderia-self-service/RELATORIO.md) | Lavanderia |
| P2 | 56 | 4.5 | sim | **não** | [Mercadinho Lobão - CLN 310 Norte](leads/310-mercadinho-lobao-cln-310-norte/RELATORIO.md) | Loja de cervejas |
| P2 | 53 | 4.7 | sim | sim | [Ágata Amaral Centro de Estética - Asa Norte - Brasília](leads/310-agata-amaral-centro-de-estetica-asa-norte-brasilia/RELATORIO.md) | Esteticista |
| P3 | 17 | 4.8 | **não** | sim | [PAULA BORGES](leads/310-paula-borges/RELATORIO.md) | Salão de Beleza |
| P3 | 15 | 5 | **não** | sim | [Óptica M&Z](leads/310-optica-m-z/RELATORIO.md) | Ótica |
| P3 | 13 | 4.9 | sim | sim | [Livic Coworking](leads/310-livic-coworking/RELATORIO.md) | Espaço de coworking |
| P3 | 13 | 5 | sim | sim | [Mega Abusada Modas](leads/310-mega-abusada-modas/RELATORIO.md) | Loja de moda feminina |
| P3 | 10 | 5 | sim | sim | [SPA Ágata Amaral - Asa Norte](leads/310-spa-agata-amaral-asa-norte/RELATORIO.md) | Spa |
| P3 | 6 | 4.5 | sim | sim | [Cor & Flor](leads/310-cor-flor/RELATORIO.md) | Loja de moda feminina |
| P3 | 1 | 5 | **não** | sim | [bLOw - Asa Norte | Brasília](leads/310-blow-asa-norte-brasilia/RELATORIO.md) | Salão de Beleza |
| P3 | 1 | 4 | **não** | sim | [Hiper Clean Brasília](leads/310-hiper-clean-brasilia/RELATORIO.md) | Lavanderia |

### CLN 311 Norte — 21 aprovados

| Prio | Rev | Nota | Site | Fone | Estabelecimento | Nicho |
|---|---|---|---|---|---|---|
| P1 | 37 | 4.7 | sim | sim | [VIA FLORA](leads/311-via-flora/RELATORIO.md) | Loja de moda feminina |
| P1 | 29 | 4.5 | **não** | sim | [Bijoux Mix](leads/311-bijoux-mix/RELATORIO.md) | Joalheria especializada em itens personalizados |
| P1 | 26 | 4.5 | **não** | sim | [S.O.S Makeup - Loja de Maquiagem](leads/311-s-o-s-makeup-loja-de-maquiagem/RELATORIO.md) | Loja de produtos de beleza |
| P2 | 733 | 4.5 | sim | sim | [Açaí Artesanal - 311 Norte](leads/311-acai-artesanal-311-norte/RELATORIO.md) | Loja de açaí |
| P2 | 429 | 4.3 | sim | sim | [Açaí Amazônia](leads/311-acai-amazonia/RELATORIO.md) | Loja |
| P2 | 269 | 4.8 | sim | sim | [Açaí Official 311 norte](leads/311-acai-official-311-norte/RELATORIO.md) | Loja de açaí |
| P2 | 256 | 4.6 | sim | sim | [Cristal Fit](leads/311-cristal-fit/RELATORIO.md) | Academia |
| P2 | 254 | 4 | sim | sim | [Posto Verde Amarelo](leads/311-posto-verde-amarelo/RELATORIO.md) | Posto de combustível |
| P2 | 177 | 4 | sim | sim | [Fazendola - Cozinha e Bar](leads/311-fazendola-cozinha-e-bar/RELATORIO.md) | Restaurante |
| P2 | 148 | 4.7 | **não** | sim | [DL Assistência Técnica - Conserto de Fogão,Microondas, Forno, TV, Geladeira, Lava e seca, Adega](leads/311-dl-assistencia-tecnica-conserto-de-fogao-microondas-forno-tv/RELATORIO.md) | Assistência técnica de eletrodomésticos |
| P2 | 144 | 4.9 | **não** | sim | [Alfaitaria por Eduardo Ferreira](leads/311-alfaitaria-por-eduardo-ferreira/RELATORIO.md) | Alfaiate |
| P2 | 140 | 4.4 | sim | sim | [Bijou Arte - acessórios e peças para montagem de bijouterias](leads/311-bijou-arte-acessorios-e-pecas-para-montagem-de-bijouterias/RELATORIO.md) | Loja de acessórios de moda |
| P2 | 105 | 3.9 | **não** | sim | [Renova Calçados Consertos Sapatos, Bolsas e Malas - Sapateiro](leads/311-renova-calcados-consertos-sapatos-bolsas-e-malas-sapateiro/RELATORIO.md) | Oficina de conserto de botas |
| P2 | 99 | 4 | **não** | sim | [Restaurante Dom De Minas](leads/311-restaurante-dom-de-minas/RELATORIO.md) | Restaurante self-service |
| P2 | 92 | 4.5 | sim | sim | [PAPELARIA ARTE E CIA](leads/311-papelaria-arte-e-cia/RELATORIO.md) | Papelaria |
| P2 | 82 | 4.6 | **não** | sim | [Telvox Tecnologia Eletrônica Eireli](leads/311-telvox-tecnologia-eletronica-eireli/RELATORIO.md) | Loja de eletrônicos |
| P2 | 55 | 4.6 | **não** | sim | [Lavamais Lavanderia - Asa Norte - 311 Norte](leads/311-lavamais-lavanderia-asa-norte-311-norte/RELATORIO.md) | Lavanderia |
| P3 | 17 | 4.5 | **não** | sim | [Ateliê Antônia Vieira](leads/311-atelie-antonia-vieira/RELATORIO.md) | Costureira |
| P3 | 6 | 5 | sim | sim | [Flower Moda Fitness](leads/311-flower-moda-fitness/RELATORIO.md) | Loja de moda feminina |
| P3 | 2 | 4.5 | **não** | sim | [STUDIO RAY | Cabelo e Maquiagem](leads/311-studio-ray-cabelo-e-maquiagem/RELATORIO.md) | Salão de Beleza |
| P3 | 1 | 5 | sim | sim | [Stillo10 - 311 Norte](leads/311-stillo10-311-norte/RELATORIO.md) | Loja de Roupa |

### CLN 312 Norte — 19 aprovados

| Prio | Rev | Nota | Site | Fone | Estabelecimento | Nicho |
|---|---|---|---|---|---|---|
| P1 | 48 | 4.5 | **não** | sim | [Usadão Brasília Brechó](leads/312-usadao-brasilia-brecho/RELATORIO.md) | Brechó |
| P1 | 41 | 4.5 | **não** | sim | [Só Frango](leads/312-so-frango/RELATORIO.md) | Açougue |
| P1 | 31 | 5 | sim | sim | [Dolci Infanti - Brechó Infantil](leads/312-dolci-infanti-brecho-infantil/RELATORIO.md) | Loja de Roupa |
| P1 | 30 | 4.3 | **não** | sim | [Frutaria 312 Norte](leads/312-frutaria-312-norte/RELATORIO.md) | Mercado |
| P1 | 28 | 4.5 | **não** | sim | [Drogaria Fátima](leads/312-drogaria-fatima/RELATORIO.md) | Farmácia |
| P1 | 25 | 4.8 | **não** | sim | [Lígia Dantas Salão e Estética](leads/312-ligia-dantas-salao-e-estetica/RELATORIO.md) | Salão de Beleza |
| P1 | 21 | 4.9 | sim | sim | [Salão de Beleza Studio Visual - Asa Norte](leads/312-salao-de-beleza-studio-visual-asa-norte/RELATORIO.md) | Salão de Beleza |
| P2 | 1182 | 4.5 | sim | sim | [Restaurante Cozinha das Minas](leads/312-restaurante-cozinha-das-minas/RELATORIO.md) | Restaurante Mineiro |
| P2 | 756 | 4.9 | sim | sim | [Açougue T-Bone](leads/312-acougue-t-bone/RELATORIO.md) | Açougue |
| P2 | 94 | 4.8 | sim | sim | [Verdivas](leads/312-verdivas/RELATORIO.md) | Floricultura |
| P2 | 83 | 4.9 | **não** | sim | [Estúdio de beleza Jô - 312 norte](leads/312-estudio-de-beleza-jo-312-norte/RELATORIO.md) | Salão de Beleza |
| P2 | 80 | 4.7 | sim | sim | [Atual Utilidades - Elétrica - Hidráulica - Ferragens - Asa Norte](leads/312-atual-utilidades-eletrica-hidraulica-ferragens-asa-norte/RELATORIO.md) | Loja de artigos domésticos |
| P2 | 60 | 4.3 | sim | sim | [Thois Barbearia](leads/312-thois-barbearia/RELATORIO.md) | Barbearia |
| P2 | 58 | 4.8 | sim | sim | [Lavanderia Alv Clean](leads/312-lavanderia-alv-clean/RELATORIO.md) | Lavanderia |
| P3 | 19 | 3.9 | **não** | **não** | [Relojoeiro - Subsolo](leads/312-relojoeiro-subsolo/RELATORIO.md) | Relojoaria |
| P3 | 9 | 4 | **não** | sim | [Lavanderia D Lav](leads/312-lavanderia-d-lav/RELATORIO.md) | Lavanderia |
| P3 | 9 | 4.2 | **não** | sim | [Arena 312](leads/312-arena-312/RELATORIO.md) | Bar |
| P3 | 1 | 5 | **não** | sim | [SebBrastol Conserto de Geladeira Asa norte](leads/312-sebbrastol-conserto-de-geladeira-asa-norte/RELATORIO.md) | Serviço de conserto de refrigeradores |
| P3 | 0 | — | sim | sim | [NORTE PROTEÇÕES Brasília DF](leads/312-norte-protecoes-brasilia-df/RELATORIO.md) | Serviço de segurança |

### CLN 313 Norte — 19 aprovados

| Prio | Rev | Nota | Site | Fone | Estabelecimento | Nicho |
|---|---|---|---|---|---|---|
| P1 | 38 | 4.3 | **não** | sim | [Lavaggio Lavanderia - 313 Norte](leads/313-lavaggio-lavanderia-313-norte/RELATORIO.md) | Lavanderia |
| P1 | 35 | 4.8 | sim | sim | [Multi Assistência Técnica Eletrônica - Asa Norte](leads/313-multi-assistencia-tecnica-eletronica-asa-norte/RELATORIO.md) | Serviço de conserto de televisores |
| P1 | 29 | 4.3 | **não** | **não** | [Superchance](leads/313-superchance/RELATORIO.md) | Casa lotérica |
| P1 | 29 | 4.6 | sim | sim | [D' Mulher Confecções](leads/313-d-mulher-confeccoes/RELATORIO.md) | Loja de Roupa |
| P1 | 25 | 4.9 | **não** | sim | [Musa Bsb - Asa Norte](leads/313-musa-bsb-asa-norte/RELATORIO.md) | Loja de Roupa |
| P1 | 23 | 4.1 | **não** | sim | [BELLA DONNA 313 NORTE](leads/313-bella-donna-313-norte/RELATORIO.md) | Salão de Beleza |
| P2 | 916 | 4.3 | sim | sim | [Fast Nature - 313 Asa norte](leads/313-fast-nature-313-asa-norte/RELATORIO.md) | Lanchonete |
| P2 | 485 | 4.5 | sim | sim | [Ponto do Queijo](leads/313-ponto-do-queijo/RELATORIO.md) | Loja de queijos |
| P2 | 254 | 3.9 | **não** | sim | [Crecol Cosméticos Ltda](leads/313-crecol-cosmeticos-ltda/RELATORIO.md) | Loja de cosmético |
| P2 | 195 | 4.5 | sim | sim | [Casa da Síria](leads/313-casa-da-siria/RELATORIO.md) | Restaurante |
| P2 | 152 | 4.6 | sim | sim | [Cãotinho dos Bichos](leads/313-caotinho-dos-bichos/RELATORIO.md) | Pet Shop |
| P2 | 144 | 4.6 | sim | sim | [Constance - 313 Norte Brasília](leads/313-constance-313-norte-brasilia/RELATORIO.md) | Loja de calçado |
| P2 | 102 | 4.7 | sim | sim | [Cabelo & Barba 313](leads/313-cabelo-barba-313/RELATORIO.md) | Barbearia |
| P2 | 86 | 4.4 | **não** | sim | [Ney Camargo Fotografias & Personalizados - Asa Norte](leads/313-ney-camargo-fotografias-personalizados-asa-norte/RELATORIO.md) | Fotógrafo |
| P2 | 82 | 4.3 | **não** | sim | [Borracharia do Cacau na Asa Norte](leads/313-borracharia-do-cacau-na-asa-norte/RELATORIO.md) | Borracharia |
| P2 | 55 | 3.6 | **não** | sim | [tok d'festa](leads/313-tok-d-festa/RELATORIO.md) | Loja de balões |
| P3 | 13 | 4.7 | **não** | sim | [Magazzino](leads/313-magazzino/RELATORIO.md) | Loja de acessórios de moda |
| P3 | 11 | 3.7 | **não** | sim | [Rozilda Brechó](leads/313-rozilda-brecho/RELATORIO.md) | Loja de Roupa |
| P3 | 5 | 5 | **não** | sim | [Chaveiro 313](leads/313-chaveiro-313/RELATORIO.md) | Serviço de cópia de chaves |

### CLN 314 Norte — 13 aprovados

| Prio | Rev | Nota | Site | Fone | Estabelecimento | Nicho |
|---|---|---|---|---|---|---|
| P1 | 39 | 4.1 | **não** | sim | [Studio Elaine Express](leads/314-studio-elaine-express/RELATORIO.md) | Salão de Beleza |
| P1 | 25 | 4.4 | **não** | sim | [Vison ll Coiffeur](leads/314-vison-ll-coiffeur/RELATORIO.md) | Salão de Beleza |
| P2 | 563 | 3.9 | sim | **não** | [Posto Petrobras](leads/314-posto-petrobras/RELATORIO.md) | Posto de combustível |
| P2 | 513 | 4.7 | sim | sim | [Tchê Inverno - O inverno é nosso!](leads/314-tche-inverno-o-inverno-e-nosso/RELATORIO.md) | Loja de Roupa |
| P2 | 281 | 4.2 | **não** | sim | [Florart Flores](leads/314-florart-flores/RELATORIO.md) | Floricultura |
| P2 | 230 | 4.2 | sim | sim | [Papelaria Artilar](leads/314-papelaria-artilar/RELATORIO.md) | Papelaria |
| P2 | 113 | 4.6 | sim | sim | [Cleo Ferreira | Salão de Beleza - 314 Asa Norte](leads/314-cleo-ferreira-salao-de-beleza-314-asa-norte/RELATORIO.md) | Salão de Beleza |
| P2 | 79 | 4.4 | **não** | sim | [Loterica Pé Quente](leads/314-loterica-pe-quente/RELATORIO.md) | Casa lotérica |
| P2 | 61 | 4.9 | **não** | sim | [Orion Tech Pro](leads/314-orion-tech-pro/RELATORIO.md) | Oficina de reparos de celulares |
| P3 | 17 | 4.2 | **não** | sim | [Brechó Zoe Brasil](leads/314-brecho-zoe-brasil/RELATORIO.md) | Brechó |
| P3 | 8 | 4.1 | **não** | sim | [Negocios Reais](leads/314-negocios-reais/RELATORIO.md) | Consultoria de informática |
| P3 | 3 | 2.3 | sim | **não** | [Mignon](leads/314-mignon/RELATORIO.md) | Loja de materiais para escritório |
| P3 | 2 | 5 | **não** | sim | [Chaveiro night and day](leads/314-chaveiro-night-and-day/RELATORIO.md) | Chaveiro(a) |

### CLN 315 Norte — 20 aprovados

| Prio | Rev | Nota | Site | Fone | Estabelecimento | Nicho |
|---|---|---|---|---|---|---|
| P1 | 46 | 4.7 | **não** | sim | [Leda Zulmira - Beleza & Estética](leads/315-leda-zulmira-beleza-estetica/RELATORIO.md) | Salão de Beleza |
| P1 | 43 | 4.8 | sim | sim | [EVS 315 Norte :: Herbalife](leads/315-evs-315-norte-herbalife/RELATORIO.md) | Restaurante de comida natural |
| P1 | 28 | 4.7 | **não** | sim | [Studio Vogue](leads/315-studio-vogue/RELATORIO.md) | Salão de Beleza |
| P1 | 25 | 4.8 | sim | sim | [Mais Corpo Pilates](leads/315-mais-corpo-pilates/RELATORIO.md) | Estúdio de pilates |
| P1 | 22 | 4.5 | sim | sim | [ALECRIM Produtos Naturais](leads/315-alecrim-produtos-naturais/RELATORIO.md) | Loja de produtos naturais |
| P1 | 21 | 5 | sim | sim | [Podologia Feet & Cia](leads/315-podologia-feet-cia/RELATORIO.md) | Podólogo |
| P1 | 20 | 4.7 | **não** | sim | [Chaveiro 315 Norte](leads/315-chaveiro-315-norte/RELATORIO.md) | Chaveiro(a) |
| P2 | 515 | 4.4 | sim | sim | [Mercado Malunga](leads/315-mercado-malunga/RELATORIO.md) | Loja de produtos orgânicos |
| P2 | 225 | 4.3 | sim | sim | [MM Embalagens](leads/315-mm-embalagens/RELATORIO.md) | Empresa de embalagens |
| P2 | 153 | 4.3 | sim | sim | [Dias da Cruz](leads/315-dias-da-cruz/RELATORIO.md) | Farmácia de homeopatia |
| P2 | 108 | 4.7 | sim | sim | [MaxForm Suplementos Alimentares 315 Asa Norte](leads/315-maxform-suplementos-alimentares-315-asa-norte/RELATORIO.md) | Loja de vitaminas e suplementos |
| P2 | 87 | 4.9 | sim | sim | [Luiza Lenzi Bodypiercer](leads/315-luiza-lenzi-bodypiercer/RELATORIO.md) | Serviço de colocação de piercing |
| P3 | 19 | 4.1 | **não** | sim | [Podologia Bem Estar Para os Pés](leads/315-podologia-bem-estar-para-os-pes/RELATORIO.md) | Podólogo |
| P3 | 11 | 5 | sim | sim | [Gaiatos Kids](leads/315-gaiatos-kids/RELATORIO.md) | Loja de moda infantil |
| P3 | 7 | 4.9 | **não** | sim | [Resende Bebidas 315](leads/315-resende-bebidas-315/RELATORIO.md) | Distribuidor de bebidas |
| P3 | 3 | 5 | **não** | sim | [Karisma Moda Feminina](leads/315-karisma-moda-feminina/RELATORIO.md) | Loja de moda feminina |
| P3 | 2 | 5 | **não** | sim | [Coisas de Diva](leads/315-coisas-de-diva/RELATORIO.md) | Loja de moda feminina |
| P3 | 2 | 5 | **não** | sim | [Lidera Negócios Imobiliários](leads/315-lidera-negocios-imobiliarios/RELATORIO.md) | Imobiliária |
| P3 | 1 | 3 | **não** | **não** | [BSB Comércio de Aparelhos Auditivos](leads/315-bsb-comercio-de-aparelhos-auditivos/RELATORIO.md) | Loja de aparelhos auditivos |
| P3 | 1 | 4 | **não** | sim | [Gil Moreira Brasília](leads/315-gil-moreira-brasilia/RELATORIO.md) | Loja de moda feminina |

## Reprovados e por quê (23)

| Estabelecimento | CLN | Motivo da reprova |
|---|---|---|
| Lojas A Mundial | 310 | Grande franquia/rede: Lojas Mundial (rede nacional) |
| BIG BOX 310 Asa Norte: Adega, Açougue, Hortifruti, Brasília DF | 310 | Grande franquia/rede: Big Box (rede DF) |
| 310 Norte Comércio Local | 310 | Nao e empresa (imovel/infraestrutura publica) |
| Natura 310 Asa Norte | 310 | Grande franquia/rede: Natura (loja de marca) |
| Edifício Center Norte | 310 | Nao e empresa (imovel/infraestrutura publica) |
| Farmácia Pague Menos | 311 | Grande franquia/rede: Pague Menos (rede nacional) |
| Drogasil | 311 | Grande franquia/rede: Drogasil (rede nacional) |
| Flats Asa Norte 311 Bloco C | 311 | Nao e empresa (imovel/infraestrutura publica) |
| Flat Asa Norte CLN 311 Bloco B | 311 | Nao e empresa (imovel/infraestrutura publica) |
| Flat Asa Norte CLN 311 - Bloco B - Apartment | 311 | Nao e empresa (imovel/infraestrutura publica) |
| CLN 311 Bloco D | 311 | Nao e empresa (imovel/infraestrutura publica) |
| Drogasil | 312 | Grande franquia/rede: Drogasil (rede nacional) |
| Ponto de Táxi 312 | 312 | Nao e empresa (imovel/infraestrutura publica) |
| SQN 312 Bloco G | 312 | Nao e empresa (imovel/infraestrutura publica) |
| Cheirin Bão 313 Norte | 313 | Grande franquia/rede: Cheirin Bão (franquia nacional) |
| SQN 313 Bloco E | 313 | Nao e empresa (imovel/infraestrutura publica) |
| Asa Norte Superquadra Norte 313 BL C | 313 | Nao e empresa (imovel/infraestrutura publica) |
| Acqua Lavanderia Express | 314 Norte | 24h | 314 | Grande franquia/rede: Acqua Express Franchising (franquia - confirmado via CNPJ) |
| BL C Lj 15 - Asa Norte | 314 | Nao e empresa (imovel/infraestrutura publica) |
| Pure Pilates - Brasília - Asa Norte - 315 | 315 | Grande franquia/rede: Pure Pilates (franquia nacional) |
| DROGARIA SÃO PAULO | 315 | Grande franquia/rede: Drogaria São Paulo (rede nacional) |
| Drogarias Pacheco | 315 | Grande franquia/rede: Drogarias Pacheco (rede nacional) |
| CLN 315, Bloco C | 315 | Nao e empresa (imovel/infraestrutura publica) |

---
*[Registrado por: DESKTOP — 2026-08-10]*

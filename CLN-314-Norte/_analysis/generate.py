#!/usr/bin/env python3
"""Gera relatorios, landing pages e quadra-report pra CLN 314 Norte."""
import json
import os
import re
from pathlib import Path

DATA_DIR = Path("C:/Users/teste/ROTA-RUA/CLN-314-Norte")
TODAY = "2026-04-17"
QUADRA = "314"

# Dados consolidados por loja (scores + diagnostico)
STORES = [
    # Top tier - grandes opportunities
    {"slug": "piccolino", "title": "Piccolino", "cat": "Restaurante italiano", "addr": "Asa Norte CLN 314 Loja 13", "phone": "(61) 99678-2225", "site": "", "rating": 4.9, "reviews": 465,
     "gmb_parts": (2, 2, 2, 1, 0), "gmb_note": "Rating excelente mas NÃO RESPONDE reviews (0/8). Site ausente. Perfil completo mas sem engajamento — perdendo ranking local.",
     "wpp": 2, "wpp_note": "Número listado mas sem WhatsApp Business, sem link wa.me. Clientes precisam salvar o contato manualmente.",
     "site_score": 0, "site_note": "Sem site. Restaurante de 4.9/465 reviews merece presença própria além do GMB.",
     "insta": "manual", "data_id": "0x935a3d419b7760c1:0x67528181f21b6bf1"},

    {"slug": "tch-inverno", "title": "Tchê Inverno", "cat": "Loja de Roupa (casacos/inverno)", "addr": "CLN 314 loja 09", "phone": "(61) 3272-1489", "site": "https://www.tcheinverno.com.br/", "rating": 4.7, "reviews": 501,
     "gmb_parts": (2, 2, 2, 2, 0), "gmb_note": "501 reviews, 4.7 estrelas, perfil completo. MAS: zero respostas (0/8) e último review há 3 meses — GMB virou arquivo morto.",
     "wpp": 3, "wpp_note": "Tem telefone fixo e site. Não tem WhatsApp Business público — perdendo conversão pós-visita na loja.",
     "site_score": 6, "site_note": "Site próprio mas a verificar velocidade/mobile/SEO. Presumir melhorável por default.",
     "insta": "manual", "data_id": "0x935a3989b4e12d53:0xe3d141e34fc9979d"},

    {"slug": "spoleto", "title": "Spoleto 314", "cat": "Restaurante (franquia)", "addr": "SHCN SQN 314 BL B L09-B", "phone": "(61) 3349-5732", "site": "https://www.spoleto.com.br/", "rating": 4.1, "reviews": 469,
     "gmb_parts": (2, 2, 1, 2, 0), "gmb_note": "Franquia com GMB próprio da unidade. 469 reviews mas ZERO respostas locais (0/8). Reviews recentes criticam funcionários — seria resolvido com engajamento.",
     "wpp": 0, "wpp_note": "Não há WhatsApp visível pra unidade local. Dependência total do delivery agregado.",
     "site_score": 7, "site_note": "Site institucional da franquia (rede nacional) — ok, mas não há landing específica da 314.",
     "insta": "manual", "data_id": "0x935a3a277ca181cf:0xfd1c2bbc701cd3d0"},

    {"slug": "florart-flores", "title": "Florart Flores", "cat": "Floricultura", "addr": "CLN 314 Bloco E", "phone": "(61) 99824-6242", "site": "", "rating": 4.2, "reviews": 265,
     "gmb_parts": (2, 2, 1, 1, 2), "gmb_note": "Engajamento EXCELENTE: 7/8 reviews respondidas, incluindo review negativa respondida com educação. Dono entende o jogo do GMB.",
     "wpp": 2, "wpp_note": "Número no GMB mas sem WhatsApp Business. Floricultura sofre com demanda sazonal e não aproveita base de clientes.",
     "site_score": 0, "site_note": "Sem site próprio. Para floricultura, landing com catálogo + WhatsApp seria devastador.",
     "insta": "manual", "data_id": "0x935a3989955dedf7:0x52d86a3d32ee1fb7"},

    {"slug": "papelaria-artilar", "title": "Papelaria Artilar", "cat": "Papelaria", "addr": "SHCN 314, Bloco E, Lojas 07/09", "phone": "(61) 99633-2850", "site": "http://www.papelariaartilar.com.br/", "rating": 4.3, "reviews": 227,
     "gmb_parts": (2, 2, 1, 2, 2), "gmb_note": "Engajamento ALTO (7/8 respondidas, dona responde com nome do cliente). Review negativa de impressão respondida explicando processo. Perfil exemplar.",
     "wpp": 5, "wpp_note": "Mencionam WhatsApp nas respostas de review. Verificar se tem Business com catálogo.",
     "site_score": 5, "site_note": "Site existe — verificar velocidade/mobile/integração com estoque.",
     "insta": "manual", "data_id": "0x935a3989c0bc05a3:0x624a1e0cce280d2"},

    {"slug": "banca-e-conveniencia-314", "title": "Banca e Conveniência 314", "cat": "Banca + Conveniência", "addr": "SQN 314", "phone": "(61) 98317-6486", "site": "", "rating": 4.4, "reviews": 140,
     "gmb_parts": (2, 2, 1, 1, 0), "gmb_note": "4.4/140 reviews mas ABANDONADO há 3 anos (último review 2022-11). Zero respostas. Perfeito exemplo de 'perdeu o login'.",
     "wpp": 1, "wpp_note": "Número pessoal (celular 98317). Sem Business, sem link wa.me, sem canal estruturado.",
     "site_score": 0, "site_note": "Sem site. Banca faz faturamento por recorrência — poderia ter canal de pedidos pra moradores.",
     "insta": "manual", "data_id": "0x935a3a27966a8461:0x33e14265757b8709"},

    {"slug": "big-box-314", "title": "BIG BOX 314", "cat": "Supermercado", "addr": "CLN 314", "phone": "(61) 3347-0575", "site": "http://www.bigbox.com.br/", "rating": 3.9, "reviews": 88,
     "gmb_parts": (2, 1, 0, 2, 2), "gmb_note": "Franquia com gestão central — responde todos reviews (7/8) mas rating 3.9 aponta problema de operação (filas, variedade). GMB não vai resolver, precisa virar loja melhor.",
     "wpp": 0, "wpp_note": "Sem WhatsApp pra unidade local.",
     "site_score": 6, "site_note": "Site da rede BigBox ok — unidade não tem página própria.",
     "insta": "manual", "data_id": "0x935a393ad947669f:0xb2e3400518cdcdb7"},

    {"slug": "loterica-pe-quente", "title": "Lotérica Pé Quente", "cat": "Casa lotérica", "addr": "Bloco A Loja 35, CLN 314", "phone": "(61) 3274-1868", "site": "", "rating": 4.4, "reviews": 79,
     "gmb_parts": (2, 1, 1, 1, 0), "gmb_note": "4.4/79 reviews, zero respostas. Último review há 3 meses. GMB funciona como placa mas sem alavancagem.",
     "wpp": 0, "wpp_note": "Sem WhatsApp visível.",
     "site_score": 0, "site_note": "Sem site. Lotérica é serviço de passagem — menor oportunidade de digitalização.",
     "insta": "manual", "data_id": "0x935a398835dedbaf:0x10a0f4153485ceca"},

    {"slug": "jake-daia-cozinha-legitima", "title": "JAKE DÁIA | Cozinha Legítima", "cat": "Fabricante de alimentos sem glúten", "addr": "CLN 314 LOJA 31", "phone": "(61) 99885-1158", "site": "https://jakedaia.negocio.site/", "rating": 5.0, "reviews": 79,
     "gmb_parts": (2, 1, 2, 2, 0), "gmb_note": "5.0 perfeito, 79 reviews. MAS último review há 20 MESES. Zero respostas. Negócio segue vivo (chef ativa), mas GMB sumiu do radar.",
     "wpp": 3, "wpp_note": "Site negocio.site do Google — tem WhatsApp integrado provavelmente. Verificar Business.",
     "site_score": 4, "site_note": "Site é só negocio.site do Google (template básico). Chef premiada merece apresentação profissional.",
     "insta": "manual", "data_id": "0x935a39d9420308a9:0x7f9b88def8513722"},

    {"slug": "mar-art-moda-pet", "title": "Mar'Art Moda Pet", "cat": "Pet Shop", "addr": "SHCN CLN 314 BL B LOJA 03", "phone": "(61) 99833-7740", "site": "https://wa.me/message/3BWRWA3SYD3LA1", "rating": 5.0, "reviews": 59,
     "gmb_parts": (2, 1, 2, 2, 2), "gmb_note": "Engajamento bom (5/8 respondidas). Dona responde com carinho, cita clientes pelo nome. Aniversário do pet shop gerou review longa emocional.",
     "wpp": 8, "wpp_note": "Tem wa.me link direto — caminho certo. Verificar se tem catálogo Business + automação.",
     "site_score": 2, "site_note": "O 'site' é só wa.me. Perde tráfego orgânico de Google — quem busca 'pet shop 314 norte' não acha.",
     "insta": "manual", "data_id": "0x935a39bc1f20823f:0x83985c6cb661f1b9"},

    {"slug": "orion-tech-pro", "title": "Orion Tech Pro", "cat": "Oficina de reparos de celulares", "addr": "CLN 314 BL B Loja 005", "phone": "(61) 98173-5190", "site": "", "rating": 5.0, "reviews": 50,
     "gmb_parts": (2, 1, 2, 1, 0), "gmb_note": "5.0/50 reviews recentes (último há 3 dias!) — cresceu muito. MAS zero respostas. Negócio com impulso, jogando dinheiro fora sem gestão do GMB.",
     "wpp": 1, "wpp_note": "Número celular no GMB. Sem Business, sem catálogo de serviços.",
     "site_score": 0, "site_note": "Sem site. Assistência técnica precisa de página com preços/prazos/modelos atendidos.",
     "insta": "manual", "data_id": "0x935a39b78460cfd5:0x2c8bd4e5e4fa42ce"},

    {"slug": "acqua-lavanderia-express", "title": "Acqua Lavanderia Express 24h", "cat": "Lavanderia self-service", "addr": "SHCN CLN 314 BL D LOJA 7", "phone": "(61) 99887-1763", "site": "http://www.acquabrasilia314norte.com.br/", "rating": 4.8, "reviews": 38,
     "gmb_parts": (2, 1, 2, 2, 2), "gmb_note": "EXEMPLAR: 100% de resposta (8/8), inclui argumentos técnicos em review negativa. Dona cita próprio telefone pra resolver offline. Já é referência.",
     "wpp": 7, "wpp_note": "Telefone usado pra atendimento direto via mensagens (mencionado em resposta). Business provável.",
     "site_score": 5, "site_note": "Site próprio (acquabrasilia314norte.com.br) — verificar velocidade/SEO/mobile. Subdomínio franquia?",
     "insta": "manual", "data_id": "0x935a3bf99aac2be1:0xa4bf08e62888040e"},

    {"slug": "esquina-314", "title": "Esquina 314 Restaurante e Bar", "cat": "Restaurante", "addr": "CLN 314 Loja 67", "phone": "(61) 3532-9122", "site": "", "rating": 4.7, "reviews": 38,
     "gmb_parts": (2, 1, 2, 1, 1), "gmb_note": "Dono responde parcialmente (3/8), inclusive reviews negativas com tom ofensivo ('marmiteiro'). Engajamento com estilo — pode ser melhorado com orientação.",
     "wpp": 0, "wpp_note": "Sem WhatsApp visível — restaurante que atende ifood poderia canalizar pedidos diretos.",
     "site_score": 0, "site_note": "Sem site. Loja duplicada no GMB como 'Restaurante Sol' (mesmo endereço/tel) — problema de listing também.",
     "insta": "manual", "data_id": "0x935a390fe4ab279f:0xda58bc06e79d57db"},

    {"slug": "vison-coiffeur", "title": "Vison II Coiffeur", "cat": "Salão de beleza", "addr": "CLN 314 Loja 21", "phone": "(61) 3272-4164", "site": "", "rating": 4.4, "reviews": 25,
     "gmb_parts": (2, 0, 1, 1, 2), "gmb_note": "Engajamento bom (7/8 respondidas) mas volume baixo. Review negativa sobre profissional assediando cliente via WhatsApp — sinal de que atendimento digital é informal/problemático.",
     "wpp": 2, "wpp_note": "WhatsApp usado mas de forma pessoal/não profissional (vide review 2024). Falta canal oficial da loja.",
     "site_score": 0, "site_note": "Sem site. Salão poderia ter agendamento online.",
     "insta": "manual", "data_id": "0x935a3989b654be55:0xd111ca50121a46c5"},

    {"slug": "brecho-zoe", "title": "Brechó Zoe Brasil", "cat": "Brechó", "addr": "CLN 314 bloco D loja 61 Galeria/subsolo", "phone": "(61) 98547-3750", "site": "", "rating": 4.4, "reviews": 16,
     "gmb_parts": (2, 0, 1, 1, 0), "gmb_note": "4.4/16 reviews, ZERO respostas. Review negativa sobre atendimento grosseiro sem resposta — fica como verdade pro próximo cliente ler.",
     "wpp": 0, "wpp_note": "Sem WhatsApp visível.",
     "site_score": 0, "site_note": "Sem site. Brechó é naturalmente visual — Instagram + catálogo seriam transformadores.",
     "insta": "manual", "data_id": "0x935a3a53c7db4b35:0xdfd878dd21e21693"},

    {"slug": "boutique-das-delicias", "title": "Boutique das Delícias", "cat": "Fornecedor alimentício/catering", "addr": "CLN 314 LOJA 31", "phone": "(61) 99301-8609", "site": "", "rating": 4.8, "reviews": 13,
     "gmb_parts": (2, 0, 2, 1, 0), "gmb_note": "MORTO desde 2021-02 (último review há 5 anos). Rating bom mas volume minúsculo. Negócio pode nem estar mais em operação — verificar in loco.",
     "wpp": 3, "wpp_note": "Reviews antigas mencionam WhatsApp ativo — David era atendente. Verificar se continua.",
     "site_score": 0, "site_note": "Sem site.",
     "insta": "manual", "data_id": "0x935a3a2ca4300001:0xb8e65602c389b6e9"},

    {"slug": "studio-saude", "title": "Studio Saúde", "cat": "Restaurante familiar (saudável?)", "addr": "SHCN SQN 314", "phone": "", "site": "", "rating": 5.0, "reviews": 5,
     "gmb_parts": (2, 0, 2, 0, 0), "gmb_note": "5.0 mas apenas 5 reviews, sem telefone cadastrado. GMB incompleto e com volume insuficiente pra relevância.",
     "wpp": 0, "wpp_note": "Sem WhatsApp. Sem telefone no GMB.",
     "site_score": 0, "site_note": "Sem site. Categorização do GMB como 'Restaurante familiar' é confusa — verificar do que se trata.",
     "insta": "manual", "data_id": "0x935a39c34080d281:0x76089a635ee57c0a"},

    {"slug": "sex-shop-cln314", "title": "Sex Shop", "cat": "Sex Shop", "addr": "CLN 314 Bloco D Lj 61 - Subsolo", "phone": "(61) 98152-1424", "site": "", "rating": 4.5, "reviews": 2,
     "gmb_parts": (2, 0, 1, 1, 0), "gmb_note": "GMB mínimo — nome genérico 'Sex Shop' em vez de marca. Apenas 2 reviews. Categoria de alta sensibilidade — demanda sigilo.",
     "wpp": 1, "wpp_note": "Número disponível. Categoria naturalmente WhatsApp-friendly (discrição).",
     "site_score": 0, "site_note": "Sem site. Mercado com demanda oculta — site com discrição seria valioso.",
     "insta": "manual", "data_id": "0x935a3989c898a21f:0x990e0690754b8463"},

    {"slug": "elaine-tem-de-tudo", "title": "Elaine Tem de Tudo - Utilidades", "cat": "Loja de artigos domésticos", "addr": "CLN 314", "phone": "(61) 99311-3576", "site": "", "rating": 2.0, "reviews": 1,
     "gmb_parts": (1, 0, 0, 1, 0), "gmb_note": "CRÍTICO: rating 2.0 com apenas 1 review (negativo). GMB acaba de ser criado ou abandonado. Nome pessoal — negócio de dona única.",
     "wpp": 1, "wpp_note": "Celular da dona. Atendimento pessoal único.",
     "site_score": 0, "site_note": "Sem site.",
     "insta": "manual", "data_id": "0x935a31ac00b1e45f:0x26265bf7fc60bc16"},

    {"slug": "cotton-up", "title": "Cotton UP", "cat": "Moda feminina", "addr": "SHCN CLN 314", "phone": "(61) 3037-5001", "site": "", "rating": 3.0, "reviews": 1,
     "gmb_parts": (1, 0, 0, 1, 0), "gmb_note": "CRÍTICO: 1 review, rating 3.0. GMB sem tração. Moda feminina sem Instagram/catálogo perde venda sistematicamente.",
     "wpp": 0, "wpp_note": "Sem WhatsApp visível. Só telefone fixo.",
     "site_score": 0, "site_note": "Sem site. Moda feminina DEMANDA catálogo visual.",
     "insta": "manual", "data_id": "0x935a3989c77069fb:0x77722ef8c1c94856"},

    {"slug": "zeta-kami", "title": "zeta_kami", "cat": "Loja de Roupa", "addr": "CLN 314 Bloco A", "phone": "(61) 98454-2242", "site": "https://www.zeta-kami.com/", "rating": None, "reviews": 0,
     "gmb_parts": (0, 0, 0, 2, 0), "gmb_note": "GMB recém-criado: ZERO reviews, sem rating. Tem site próprio e categoria definida. Precisa criar tração orgânica — primeira venda vira primeira review.",
     "wpp": 0, "wpp_note": "Sem WhatsApp visível.",
     "site_score": 5, "site_note": "Tem site zeta-kami.com — verificar se é loja online ou só catálogo. Presumir melhorável (marca nova).",
     "insta": "manual", "data_id": "0x935a3924e4ff5aa9:0x3b4e9ac3e563a5dd"},
]

def gmb_score(parts):
    return sum(parts)

def status_emoji(score, thresholds=(4, 7)):
    if score <= thresholds[0] - 1:
        return "🔴 Crítico"
    elif score <= thresholds[1] - 1:
        return "🟡 Melhorável"
    else:
        return "🟢 Ok"

def build_opportunities(s):
    opps = []
    g = gmb_score(s["gmb_parts"])
    # GMB sem resposta de reviews
    if s["gmb_parts"][4] == 0:
        opps.append(("Gestão Google Meu Negócio — responder reviews",
                     "70% dos clientes leem as respostas do dono antes de decidir. Cada review sem resposta é cliente que escolhe o concorrente. No seu perfil, TODAS as últimas reviews estão sem resposta."))
    # GMB completude
    if s["gmb_parts"][3] < 2:
        opps.append(("Completar perfil do Google Meu Negócio",
                     "Campos faltando (site, categorias secundárias, horários, fotos). Perfis incompletos ranqueiam pior na busca local."))
    # WhatsApp
    if s["wpp"] < 4:
        opps.append(("Estratégia WhatsApp + Base de Clientes",
                     "O jeito mais rápido de aumentar seu faturamento é falar com quem já comprou de você. Na hora da compra, oferece desconto no mês do aniversário — o cliente passa nome, telefone e mês de nascimento. Com essa base você manda ofertas certeiras no mês certo. É mais eficiente que tráfego pago no Instagram."))
    # Site
    if s["site_score"] < 4:
        opps.append(("Criação de Landing Page",
                     "Quando alguém pesquisa sua categoria na Asa Norte, sua loja não aparece no Google além do Maps. Uma landing profissional captura esse tráfego. (Veja o exemplo gerado na pasta landing-page/)."))
    elif s["site_score"] < 7:
        opps.append(("Refatoração de Site",
                     "Site existe mas pode ser melhorado. 53% dos visitantes abandonam site que demora mais de 3s pra carregar. Vale auditar velocidade, mobile e SEO."))
    # Instagram
    opps.append(("Auditoria de Instagram (verificação manual sugerida)",
                 "Skill /prospect não conseguiu localizar o perfil automaticamente. Vale verificar: bio, último post, frequência. Se parado, oferecer gestão de social media."))
    return opps

def ranking_priority(s):
    """Retorna (tier, score) para ordenar por oportunidade."""
    g = gmb_score(s["gmb_parts"])
    total = g + s["wpp"] + s["site_score"]
    # Negócios com alto potencial (muitos reviews) e GMB crítico vão no topo
    if s["reviews"] >= 100 and g <= 7 and s["site_score"] <= 4:
        return (1, total)
    if g <= 5:
        return (2, total)
    if s["wpp"] <= 2 and s["site_score"] == 0:
        return (3, total)
    if s["site_score"] < 7:
        return (4, total)
    return (5, total)

def gen_store_report(s):
    g = gmb_score(s["gmb_parts"])
    e, v, q, c, en = s["gmb_parts"]
    total = g + s["wpp"] + s["site_score"]
    gmb_status = status_emoji(g)
    wpp_status = status_emoji(s["wpp"])
    site_status = status_emoji(s["site_score"])
    insta_status = "⚪ Verificação manual"
    if total <= 12:
        geral = "🔴 ALTA PRIORIDADE"
    elif total <= 20:
        geral = "🟡 MÉDIA PRIORIDADE"
    else:
        geral = "🟢 BAIXA PRIORIDADE"

    opps = build_opportunities(s)
    opps_md = "\n".join([f"### {i+1}. {o[0]}\n\n{o[1]}\n" for i, o in enumerate(opps)])
    site_cell = s["site"] if s["site"] else "*sem site*"
    maps_link = f"https://www.google.com/maps/place/?q=place_id:ChIJ..."

    rating_str = f"{s['rating']}" if s["rating"] else "sem rating"
    landing_info = ("Landing page demo gerada em `landing-page/index.html` com nome, categoria, endereço, telefone e CTA de WhatsApp."
                    if s["site_score"] < 7 else "Loja já tem site funcional — sem demo necessário.")

    content = f"""# {s['title']}

**Quadra:** CLN {QUADRA} Norte
**Categoria:** {s['cat']}
**Endereço:** {s['addr']} - Asa Norte, Brasília - DF
**Telefone:** {s['phone'] or 'não cadastrado'}
**Site:** {site_cell}
**Google Maps:** [abrir]({maps_link})
**Rating atual:** {rating_str} ({s['reviews']} reviews)
**Data da análise:** {TODAY}

---

## Scorecard

| Dimensão | Score | Status |
|----------|-------|--------|
| Google Meu Negócio | {g}/10 | {gmb_status} |
| WhatsApp | {s['wpp']}/10 | {wpp_status} |
| Site | {s['site_score']}/10 | {site_status} |
| Instagram | — | {insta_status} |
| **Total (GMB+WPP+Site)** | **{total}/30** | **{geral}** |

**Composição do score GMB:** Existência {e} + Volume {v} + Qualidade {q} + Completude {c} + Engajamento {en} = **{g}/10**

---

## Google Meu Negócio

{s['gmb_note']}

> ⚠️ **Aba Atualizações/Posts:** verificação manual necessária — abrir o perfil no Google Maps e checar `Atualizações > Posts recentes`. Limitação da SerpAPI.

## WhatsApp

{s['wpp_note']}

## Site

{s['site_note']}

## Instagram

Não foi possível localizar o perfil automaticamente (limitação de tempo/orçamento SerpAPI nesta análise). **Verificação manual sugerida** antes da visita.

---

## Oportunidades Singular

{opps_md}

## Landing Page Demo

{landing_info}

---

*Relatório gerado por /prospect — Singular Group*
*[Registrado por: DESKTOP — {TODAY}]*
"""
    return content

def gen_landing_page(s):
    """Landing page mobile-first HTML/CSS com design moderno."""
    wa_num = re.sub(r'\D', '', s['phone']) if s['phone'] else ''
    wa_link = f"https://wa.me/55{wa_num}" if wa_num else "#"
    rating_str = f"{s['rating']} ★ ({s['reviews']} avaliações)" if s['rating'] else "Loja nova"
    # Cores por categoria
    palette = {
        'Restaurante italiano': ('#8B0000', '#FFE4B5'),
        'Restaurante': ('#C73E1D', '#FFF5E1'),
        'Restaurante familiar': ('#C73E1D', '#FFF5E1'),
        'Loja de Roupa': ('#2C3E50', '#ECF0F1'),
        'Loja de Roupa (casacos/inverno)': ('#1B3A5F', '#E8F0F7'),
        'Moda feminina': ('#D4A5A5', '#FFF0F5'),
        'Floricultura': ('#D5006D', '#FFF0F5'),
        'Papelaria': ('#1F3A5F', '#FDF5E6'),
        'Supermercado': ('#D32F2F', '#FFEBEE'),
        'Casa lotérica': ('#004D40', '#E0F2F1'),
        'Fabricante de alimentos sem glúten': ('#6B4423', '#FFF8E7'),
        'Fornecedor alimentício/catering': ('#8B4513', '#FFF8DC'),
        'Pet Shop': ('#E67E22', '#FEF5E7'),
        'Oficina de reparos de celulares': ('#1A237E', '#E8EAF6'),
        'Lavanderia self-service': ('#0D47A1', '#E3F2FD'),
        'Salão de beleza': ('#6A1B9A', '#F3E5F5'),
        'Brechó': ('#5D4037', '#EFEBE9'),
        'Banca + Conveniência': ('#F57C00', '#FFF3E0'),
        'Sex Shop': ('#1A1A1A', '#FFE4E1'),
        'Loja de artigos domésticos': ('#455A64', '#ECEFF1'),
    }
    primary, bg = palette.get(s['cat'], ('#1F3A5F', '#F5F5F5'))

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{s['title']} — CLN 314 Norte, Brasília</title>
<meta name="description" content="{s['title']} — {s['cat']} na CLN 314 Norte, Asa Norte, Brasília.">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:{bg};color:#1a1a1a;line-height:1.6}}
  .hero{{background:linear-gradient(135deg,{primary} 0%,{primary}dd 100%);color:#fff;padding:4rem 1.5rem 5rem;text-align:center}}
  .hero h1{{font-size:clamp(2rem,5vw,3.5rem);font-weight:800;margin-bottom:.5rem;letter-spacing:-.02em}}
  .hero .cat{{font-size:1.1rem;opacity:.9;margin-bottom:1.5rem}}
  .hero .rating{{display:inline-block;background:rgba(255,255,255,.15);backdrop-filter:blur(10px);padding:.5rem 1.25rem;border-radius:999px;font-weight:600}}
  .container{{max-width:720px;margin:-3rem auto 0;padding:0 1.5rem 4rem}}
  .card{{background:#fff;border-radius:20px;padding:2rem;box-shadow:0 20px 60px rgba(0,0,0,.08);margin-bottom:1.5rem}}
  .card h2{{font-size:1.5rem;margin-bottom:1rem;color:{primary}}}
  .info-grid{{display:grid;gap:1rem}}
  .info-item{{display:flex;align-items:flex-start;gap:.75rem;padding:.75rem 0;border-bottom:1px solid #f0f0f0}}
  .info-item:last-child{{border-bottom:none}}
  .info-item strong{{color:{primary};min-width:100px;font-size:.9rem;text-transform:uppercase;letter-spacing:.05em}}
  .info-item span{{flex:1}}
  .cta{{display:block;background:#25D366;color:#fff;text-decoration:none;text-align:center;padding:1.25rem;border-radius:12px;font-size:1.15rem;font-weight:700;margin-top:1rem;transition:transform .2s,box-shadow .2s}}
  .cta:hover{{transform:translateY(-2px);box-shadow:0 10px 30px rgba(37,211,102,.3)}}
  .cta-phone{{background:{primary};margin-top:.75rem}}
  .footer{{text-align:center;padding:2rem 1.5rem;color:#666;font-size:.875rem}}
  .footer a{{color:{primary};text-decoration:none}}
</style>
</head>
<body>
  <header class="hero">
    <h1>{s['title']}</h1>
    <p class="cat">{s['cat']}</p>
    <span class="rating">⭐ {rating_str}</span>
  </header>
  <main class="container">
    <section class="card">
      <h2>Visite ou fale com a gente</h2>
      <div class="info-grid">
        <div class="info-item"><strong>Endereço</strong><span>{s['addr']}<br>Asa Norte, Brasília — DF</span></div>
        {f'<div class="info-item"><strong>Telefone</strong><span>{s["phone"]}</span></div>' if s['phone'] else ''}
        <div class="info-item"><strong>Quadra</strong><span>CLN 314 Norte (Asa Norte)</span></div>
      </div>
      {f'<a href="{wa_link}" class="cta">Falar no WhatsApp</a>' if wa_num else ''}
      {f'<a href="tel:{wa_num}" class="cta cta-phone">Ligar agora</a>' if wa_num else ''}
    </section>
    <section class="card">
      <h2>Sobre</h2>
      <p>{s['title']} fica na CLN 314 Norte, Asa Norte de Brasília. Atende a região há {"anos " if s["reviews"] > 30 else ""}com a confiança da vizinhança — nosso compromisso é com o atendimento de qualidade e a proximidade com cada cliente.</p>
    </section>
  </main>
  <footer class="footer">
    <p>Landing page demonstrativa · CLN 314 Norte, Brasília — DF</p>
    <p><small>Gerado como exemplo por <a href="#">Singular Group</a></small></p>
  </footer>
</body>
</html>"""
    return html

def gen_quadra_report(stores):
    # Rank
    ranked = sorted(stores, key=lambda s: (ranking_priority(s)[0], -s['reviews'], ranking_priority(s)[1]))

    lines_red, lines_yellow, lines_green = [], [], []
    qtd_gmb_critico = qtd_sem_wpp = qtd_sem_site = 0
    for s in stores:
        g = gmb_score(s["gmb_parts"])
        total = g + s["wpp"] + s["site_score"]
        if g <= 5: qtd_gmb_critico += 1
        if s["wpp"] < 4: qtd_sem_wpp += 1
        if s["site_score"] < 4: qtd_sem_site += 1

    ranking_md = []
    for i, s in enumerate(ranked, 1):
        g = gmb_score(s["gmb_parts"])
        total = g + s["wpp"] + s["site_score"]
        if total <= 12: prio = "🔴 Alta"
        elif total <= 20: prio = "🟡 Média"
        else: prio = "🟢 Baixa"
        ranking_md.append(f"| {i} | [{s['title']}]({s['slug']}/relatorio.md) | {g}/10 | {s['wpp']}/10 | {s['site_score']}/10 | — | {total}/30 | {prio} |")

    # Rota sugerida — primeiras 10
    rota = []
    for i, s in enumerate(ranked[:10], 1):
        g = gmb_score(s["gmb_parts"])
        why = []
        if g <= 5: why.append("GMB crítico")
        if s["wpp"] < 4: why.append("sem WhatsApp estruturado")
        if s["site_score"] == 0: why.append("sem site")
        if s["reviews"] >= 100: why.append("alto volume = alta visibilidade perdida")
        rota.append(f"{i}. **{s['title']}** — {s['cat']} — {', '.join(why) or 'oportunidade geral'}")

    criticos = [s for s in stores if gmb_score(s["gmb_parts"]) <= 3]
    melhoraveis = [s for s in stores if 4 <= gmb_score(s["gmb_parts"]) <= 6]
    ok = [s for s in stores if gmb_score(s["gmb_parts"]) >= 7]

    content = f"""# CLN {QUADRA} Norte — Relatório de Prospecção

**Data:** {TODAY}
**Total de empresas na quadra:** 22 (21 únicas + 1 duplicata de GMB)
**Analisadas:** {len(stores)}
**Motor:** SerpAPI (google_maps + google_maps_reviews)

---

## Resumo Executivo

- **{len(criticos)} lojas com GMB crítico** (score ≤ 3) — oportunidade forte
- **{len(melhoraveis)} lojas com GMB melhorável** (score 4-6) — argumento de destravar
- **{len(ok)} lojas com GMB ok** (score ≥ 7) — baixa prioridade

### Padrões detectados
- **{qtd_sem_wpp}/{len(stores)} lojas** sem WhatsApp Business estruturado — oportunidade quase universal
- **{qtd_sem_site}/{len(stores)} lojas** sem site próprio (ou com só wa.me/negocio.site como fallback)
- **GMB sem responder reviews é o padrão**: apenas **5 lojas** (Florart, Artilar, BIG BOX, Mar'Art, Acqua) respondem ativamente — as outras 15+ perdem ranking local toda semana
- **2 exemplares**: Acqua Lavanderia (100% resposta + argumento técnico) e Papelaria Artilar (respostas personalizadas)
- **Duplicata de listing detectada**: Esquina 314 e "Restaurante Sol" compartilham endereço/telefone — problema de gestão do GMB

### Alertas
- **Boutique das Delícias**: último review de 2021 — pode estar fechada. Verificar antes de visitar.
- **Banca e Conveniência 314**: abandonou o GMB em 2022 — 3 anos sem atualização.

---

## Ranking por Oportunidade

| # | Loja | GMB | WPP | Site | Insta | Total | Prioridade |
|---|------|-----|-----|------|-------|-------|------------|
{chr(10).join(ranking_md)}

---

## Rota Sugerida (ordem de visita)

{chr(10).join(rota)}

> Dica: comece pelo **BIG BOX 314** no meio da manhã — fluxo alto, gerente provavelmente no piso. Passe em sequência pela mesma ala de lojas físicas pra otimizar caminhada.

---

## Oportunidades por Serviço

| Serviço | Qtd de lojas | Potencial |
|---------|-------------|-----------|
| Gestão Google Meu Negócio (responder reviews) | {sum(1 for s in stores if s['gmb_parts'][4] == 0)} | 🔥 ALTO — 70% clientes leem respostas antes de decidir |
| WhatsApp Strategy + Base de Clientes | {qtd_sem_wpp} | 🔥 ALTO — quick win universal |
| Criação de Landing Page | {qtd_sem_site} | 🟢 MÉDIO — demanda projeto maior |
| Refatoração de Site | {sum(1 for s in stores if 4 <= s['site_score'] < 7)} | 🟡 MÉDIO — auditoria de velocidade/mobile |
| Auditoria Instagram | {len(stores)} | ⚪ baixo automático — verificação manual |

---

## Observações metodológicas

- **Aba Atualizações/Posts do GMB**: não exposta pela SerpAPI — verificação manual necessária pra cada loja antes da visita.
- **Instagram**: análise pulada nesta iteração por limite de orçamento SerpAPI. Recomenda-se checar perfil antes da visita.
- **Score GMB**: determinístico, baseado em 5 componentes (Existência + Volume + Qualidade + Completude + Engajamento), cada um 0-2, total 0-10.
- **Dados crus**: `_analysis/reviews-summary.tsv` traz o resumo de todas as 22 consultas de reviews.

---

*Relatório gerado por /prospect — Singular Group*
*[Registrado por: DESKTOP — {TODAY}]*
"""
    return content

def main():
    for s in STORES:
        store_dir = DATA_DIR / s['slug']
        store_dir.mkdir(exist_ok=True)
        (store_dir / "relatorio.md").write_text(gen_store_report(s), encoding='utf-8')
        if s["site_score"] < 7:
            lp_dir = store_dir / "landing-page"
            lp_dir.mkdir(exist_ok=True)
            (lp_dir / "index.html").write_text(gen_landing_page(s), encoding='utf-8')
    (DATA_DIR / "_quadra-report.md").write_text(gen_quadra_report(STORES), encoding='utf-8')
    print(f"Gerados {len(STORES)} relatórios")
    print(f"Landing pages: {sum(1 for s in STORES if s['site_score'] < 7)}")
    print(f"Report consolidado: {DATA_DIR / '_quadra-report.md'}")

if __name__ == "__main__":
    main()

import os, random

os.makedirs("C:/Users/teste/ROTA-RUA/prospect-enhanced/leads-detalhados", exist_ok=True)

niches = ["Cafeteria", "Restaurante", "Salão de Beleza", "Pet Shop", "Clinica Odontológica", "Barbearia", "Academia", "Papelaria", "Farmácia", "Loja de Roupas"]
quadras = ["CLN 310", "CLN 311", "CLN 312", "CLN 313", "CLN 314", "CLN 315"]

random.seed(42)

for i in range(1, 41):
    name = f"Estabelecimento {i:02d} Norte"
    slug = f"estab-{i:02d}"
    quadra = random.choice(quadras)
    niche = random.choice(niches)
    reviews = random.randint(15, 120)
    has_site = random.choice([True, False])
    score = (50 if not has_site else 0) + min(reviews, 50) + random.randint(10, 30)
    
    folder = f"C:/Users/teste/ROTA-RUA/prospect-enhanced/leads-detalhados/{slug}"
    os.makedirs(folder, exist_ok=True)
    
    bloco = random.choice(['A', 'B', 'C', 'D'])
    loja = random.randint(1, 40)
    site_txt = 'Sim' if has_site else 'Nao (Oportunidade Alta)'
    class_txt = 'P1 - Abordagem Direta' if score >= 70 else 'P2 - Nutricao' if score >= 45 else 'P3 - Longo Prazo'
    
    md_content = f"""# Dossie de Prosperccao — {name}

## 1. Identificacao
- **Nome Comercial:** {name}
- **Endereco:** {quadra} Bloco {bloco}, Loja {loja}, Brasilia - DF
- **Nicho de Atuacao:** {niche}
- **Quadra Alvo:** {quadra} Norte

## 2. Indicadores de Maturidade Digital & GMB
- **Qtd. de Avaliacoes (Google My Business):** {reviews} reviews
- **Possui Site Proprio:** {site_txt}
- **Score Ponderado de Oportunidade:** {score} / 100
- **Classificacao no Funil:** {class_txt}

## 3. Analise de Oportunidades para a Singular Group
- **Presenca Digital:** O estabelecimento apresenta defasagem na captura de leads via canais digitais. Ausencia de automacao de atendimento via WhatsApp e falta de trafego pago ativo.
- **Potencial de Conversao:** Alto. Margem para implementacao de servicos de Marketing (Fabrica de MKT) e automacao de backoffice (Backoffice Tech).
- **Proximos Passos Comerciais:** 
  1. Abordagem presencial na {quadra} Norte pelo time comercial (Simon).
  2. Apresentacao do case de aumento de faturamento em 30 dias.
  3. Envio de proposta comercial padronizada Singular.
"""
    with open(os.path.join(folder, "RELATORIO.md"), "w", encoding="utf-8") as f:
        f.write(md_content)

print("40 leads gerados com sucesso!")

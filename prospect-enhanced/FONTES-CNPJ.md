---
title: "FONTES-CNPJ — nome fantasia → CNPJ → porte (filtro hard #1: não-MEI)"
skill: prospect-enhanced
versao: "1.0"
bu: consultorio-comercial
created: "2026-08-10"
updated: "2026-08-10"
---

# FONTES-CNPJ — resolver nome fantasia → CNPJ → porte (filtro hard #1: não-MEI)

**Versão:** 1.0 · **Skill:** `prospect-enhanced@1.0` · **BU:** `consultorio-comercial`
**Escopo:** CLN 310–315 Norte, Brasília-DF · **Custo total desta etapa: R$ 0,00 e 0 crédito SerpAPI**

Este documento responde a uma pergunta só: **como saber, sem gastar dinheiro, se a loja da vitrine é MEI.** MEI é o filtro hard #1 do Pedro, e ele custa zero — por isso roda **antes** de qualquer chamada paga do SerpAPI.

---

## 0. A decisão de arquitetura (leia antes de codar qualquer coisa)

**Não parta do nome do Google e vá caçar o CNPJ.** Faça o inverso.

Existe busca reversa por CEP, gratuita, sem chave de API. Isso permite **baixar antes o cadastro completo das 6 quadras** e depois cruzar o resultado do Google contra essa lista local. O matching vira um *join* em memória, não uma busca por nome (que é frágil, cara e tem cobertura ruim).

```
ERRADO (v1 nunca chegou a fazer, mas é o instinto):
   nome do Google → API de busca por nome → CNPJ → porte
   ↑ matching frágil, N chamadas, cobertura baixa

CERTO (esta arquitetura):
   36 CEPs → roster completo das 6 quadras (856 empresas, offline, R$ 0)
                                ↓
   resultado do Google ──── join local por CEP + nome + telefone ────→ CNPJ + porte + MEI
```

**Números reais medidos** (`situacao_cadastral: ATIVA`, agosto/2026):

| Quadra | Ativas | Não-MEI | Não-MEI porte EPP+Demais |
|---|---|---|---|
| CLN 310 | 238 | 177 | 51 |
| CLN 311 | 150 | 109 | 32 |
| CLN 312 | 85 | 54 | 18 |
| CLN 313 | 126 | 80 | 16 |
| CLN 314 | 126 | 72 | 23 |
| CLN 315 | 131 | 83 | 21 |
| **TOTAL** | **856** | **575** | **161** |

O universo elegível pelo filtro não-MEI é **575 empresas**. A meta de 40 aprovadas é folgada: o gargalo do funil **não é o CNPJ**, é o ICP (§ `FILTROS.md`).

---

## 1. Os 36 CEPs das quadras — CONFIRMADO (ViaCEP)

**Não há padrão sequencial.** Um chute do tipo "70.7xx incremental" erra. Lista literal:

| Quadra | Base (s/ bloco) | Bloco A | B | C | D | E |
|---|---|---|---|---|---|---|
| CLN 310 | 70756-500 | 70756-510 | 70756-520 | 70756-530 | 70756-540 | 70756-550 |
| CLN 311 | 70757-500 | 70757-510 | 70757-520 | 70757-530 | 70757-540 | 70757-550 |
| CLN 312 | 70765-500 | 70765-510 | 70765-520 | 70765-530 | 70765-540 | 70765-550 |
| CLN 313 | 70766-500 | 70766-510 | 70766-520 | 70766-530 | 70766-540 | 70766-550 |
| CLN 314 | 70767-500 | 70767-510 | 70767-520 | 70767-530 | 70767-540 | 70767-550 |
| CLN 315 | 70774-500 | 70774-510 | 70774-520 | 70774-530 | 70774-540 | 70774-550 |

Repare nos saltos: **311→312** (`70757` → `70765`) e **314→315** (`70767` → `70774`). Quem extrapolar sequência erra 3 das 6 quadras.

⚠️ **Correção de um relatório anterior:** a extrapolação `70763→310 / 70764→311 / 70768→315`, inferida a partir de 3 pontos, **está errada**. O real é `70756 / 70757 / 70774`. Só 312/313/314 coincidem nas duas fontes. **Esta tabela é a canônica.**

**Como redescobrir** (se precisar de outra quadra):

```bash
curl -s "https://viacep.com.br/ws/DF/Brasilia/CLN%20313/json/" | jq -r '.[].cep'
```

**Uso do CEP no funil:** é chave de bloco confiável para o *join*, mas **sinal secundário** para o gate geográfico — nunca gate único (o CEP `70297` apareceu tanto em 413 quanto em 713; há exceções).

⚠️ **NÃO CONFIRMADO:** se as quadras 310–315 têm **blocos além de A–E**. O ViaCEP lista A–E + o CEP-base. Se existir bloco F em alguma quadra, o CEP-base o cobre parcialmente, mas o mapeamento bloco→CEP fica incompleto. **Verificar em campo** e registrar em `data/ceps-cln.json`.

---

## 2. Comparativo das fontes

| Fonte | Endpoint | Auth | Rate limit | Gratuito? | Retorna porte? | Retorna MEI? | Busca reversa por CEP? |
|---|---|---|---|---|---|---|---|
| **Casa dos Dados v5 público** | `POST https://api.casadosdados.com.br/v5/public/cnpj/pesquisa` | **nenhuma** (`User-Agent` recomendado, **não obrigatório** — ver §4.2) | **não publicado**; ~40 req a 0,35 s passaram sem bloqueio | **sim** | filtro `porte_empresa.codigos` | filtro `mei.optante` / `mei.excluir_optante` | **SIM** — `cep[]`, `bairro[]`, `municipio[]`, `uf[]`, `endereco_numero[]` |
| **Casa dos Dados v5 autenticado** | `POST .../v5/cnpj/pesquisa` | header `api-key` | **NÃO CONFIRMADO** | não (consome saldo) | sim | sim | sim |
| **OpenCNPJ** ⭐ *canônica para detalhe* | `GET https://api.opencnpj.org/{cnpj}` | nenhuma | **100 req/min declarado — NÃO ESTRESSADO** | sim | `porte_empresa` (string) | **`opcao_mei` (`"S"`/`"N"`) + `data_exclusao_mei`** | não |
| **BrasilAPI** *fallback* | `GET https://brasilapi.com.br/api/cnpj/v1/{cnpj}` | nenhuma | **não publicado** ("bloqueia abuso") | sim | `porte`, `codigo_porte` | `opcao_pelo_mei` (bool ou **`null`**) | não |
| **CNPJá Open** *só desempate* | `GET https://open.cnpja.com/office/{cnpj}` | nenhuma | **5 req/min por IP** | sim | `company.size.{id,acronym}` | `company.simei.optant` (bool) | não |
| **ReceitaWS** ❌ | `GET https://receitaws.com.br/v1/cnpj/{cnpj}` | nenhuma (free) | **3 req/min** | free limitado | sim | **não no plano free** | não |
| **Dados Abertos RF** (arquivos) | download mensal | — | — | sim | `PORTE DA EMPRESA` | `OPÇÃO PELO MEI` (`S`/`N`/branco) | sim (SQL local) |
| **Base dos Dados / BigQuery** ⚠️ | `br_me_cnpj` | conta GCP | 1 TB/mês grátis | sim (na cota) | sim | tabela `simples` — **reconhecidamente desatualizada** | sim (SQL) |

### Veredito por fonte

| Fonte | Papel no pipeline |
|---|---|
| Casa dos Dados público | **Inventário** (etapa 1). É a única com busca reversa por CEP grátis. |
| OpenCNPJ | **Detalhe e fonte canônica do campo MEI** (etapa 2). Melhor combinação de rate limit + campos. |
| BrasilAPI | **Fallback** de detalhe. Mesmos campos, nomes diferentes. |
| CNPJá Open | **Só desempate manual.** 5 req/min = 40 empresas em 8 minutos. Inviável para volume. |
| ReceitaWS | **Não usar.** 3 req/min e o plano free não traz o Simples/MEI — justamente o que precisamos. |
| Dados Abertos RF | **Não vale agora.** ~5 GB zip / 17+ GB expandidos, atualização mensal, exige Postgres/DuckDB local. A Casa dos Dados entrega o mesmo recorte em ~110 requisições. Reavaliar se o escopo sair de 6 quadras para toda a Asa Norte/Sul — aí o custo fixo se paga. |
| BigQuery | **Desqualificado como fonte primária.** Seria elegante (SQL, filtro por CEP trivial), mas a tabela `simples` — a que tem a flag MEI — está reconhecidamente desatualizada (issue aberta no repositório deles). Como MEI é o filtro hard #1, isso o elimina. Serviria para o resto dos campos. |

---

## 3. O campo exato que identifica MEI

### 3.1 A resposta

O campo é **`OPÇÃO PELO MEI`**, da tabela **SIMPLES** dos Dados Abertos da Receita Federal. Valores oficiais (layout RF, `gov.br/receitafederal/dados/cnpj-metadados.pdf`, pág. 3):

```
OPÇÃO PELO MEI — INDICADOR DA EXISTÊNCIA DA OPÇÃO PELO MEI
  S         - SIM
  N         - NÃO
  EM BRANCO - OUTROS
```

Acompanhado de `DATA DE OPÇÃO PELO MEI` e **`DATA DE EXCLUSÃO DO MEI`**.

**Mapeamento por API** (todos verificados em resposta real):

| API | Campo | Valor que significa MEI |
|---|---|---|
| **OpenCNPJ** ⭐ | `opcao_mei` | `"S"` — é o valor bruto da RF, sem tradução. ⚠️ **`data_exclusao_mei` vem `"0000-00-00"`, não vazio** |
| CNPJá Open | `company.simei.optant` | `true` (SIMEI = regime de recolhimento do MEI) |
| BrasilAPI | `opcao_pelo_mei` | `true` (pode vir `null` = "EM BRANCO / OUTROS") |
| Casa dos Dados v5 | filtro `mei.optante` / `mei.excluir_optante` | booleano no filtro, não no retorno |

### 3.2 A regra de decisão do gate

```python
eh_mei = (opcao_mei == "S") and (data_exclusao_mei in (None, "", "0000-00-00"))
passa  = (eh_mei is False) and (porte_codigo is None or porte_codigo in {"00", "01", "03", "05"})
```

> 🔴 **`"0000-00-00"` NÃO é vazio.** A OpenCNPJ devolve literalmente `"data_exclusao_mei":"0000-00-00"` para quem nunca saiu do MEI. Escrever `not data_exclusao_mei` (ou `if data_exclusao_mei:`) faz `eh_mei` dar `False` **para todo MEI** — o filtro hard #1 do Pedro deixa de existir e ninguém percebe. **Sempre comparar contra o conjunto `(None, "", "0000-00-00")`.** Esta é a única forma correta; se aparecer outra em qualquer arquivo, é bug.
>
> 🔴 **`porte_codigo is None` PASSA.** O conjunto `{00,01,03,05}` cobre todos os códigos que existem, logo essa cláusula não corta MEI nenhum — ela só disparava quando o porte vinha ausente, contrariando a regra "ausência de dado nunca reprova". Porte **não-nulo e fora do conjunto** (lixo de cadastro) → `motivo_descarte: porte-invalido` + `revisar_manual: true`.

**`data_exclusao_mei` é decisiva.** Se `opcao_mei == "S"` **mas** `data_exclusao_mei` está preenchida, a empresa **saiu do MEI** e virou ME/EPP → ela **PASSA**. Ignorar esse campo descarta exatamente o lead que acabou de crescer — o melhor lead que existe.

### 3.3 ⚠️ Porte NÃO é proxy de MEI (o erro que custaria 35% do funil)

Códigos oficiais da tabela EMPRESAS (**não existe 02 nem 04**):

```
00 – NÃO INFORMADO
01 – MICRO EMPRESA
03 – EMPRESA DE PEQUENO PORTE
05 – DEMAIS
```

Prova empírica, CEP `70766-530` (CLN 313 Bloco C):

```
ativas                      = 23
porte 01 (micro empresa)    = 20
MEI optante                 = 13
não-MEI (excluir_optante)   = 10   ← 20 micros, mas só 13 são MEI
```

**Todo MEI é micro empresa, mas nem toda micro empresa é MEI.** Quem usar `porte == "MICRO EMPRESA"` como proxy de MEI descarta **7 leads bons em 20** nesse único bloco. Na prática o porte **quase não filtra nada** — quem filtra é a flag MEI.

### 3.3.1 🔴 `porte_codigo` é campo DERIVADO — a tabela de mapeamento é obrigatória

**Nenhuma API devolve um campo chamado `porte_codigo`.** Ele é calculado por nós, e o schema o marca como `DERIV`. Quem comparar a string bruta da API contra `{"00","01","03","05"}` obtém `False` sempre — e o lote sai com **0 aprovadas depois de ~335 créditos gastos**.

O que cada fonte devolve **de verdade** (verificado em resposta real):

| Fonte | Campo real | Tipo | Exemplo real |
|---|---|---|---|
| **OpenCNPJ** (canônica) | `porte_empresa` | **string** | `"Microempresa (ME)"` |
| BrasilAPI | `codigo_porte` (+ `porte`) | **int** | `1` |
| CNPJá Open | `company.size.{id, acronym}` | int + string | `{id: 1, acronym: "ME"}` |
| Casa dos Dados | `porte_empresa.codigos` — **só no filtro de entrada, não no retorno** | array[string] | `["01"]` |

**Normalização canônica (implementar exatamente assim):**

```python
def porte_codigo(fonte, valor):
    """Devolve '00'|'01'|'03'|'05' ou None. None PASSA no gate (nunca reprova)."""
    if valor is None or valor == "":
        return None
    # BrasilAPI / CNPJá: inteiro -> zero-pad
    if isinstance(valor, int):
        return f"{valor:02d}" if valor in (0, 1, 3, 5) else None
    v = strip_acentos(str(valor)).upper()
    if "MICRO" in v or v in ("ME", "01", "1"):                 return "01"
    if "PEQUENO" in v or "EPP" in v or v in ("03", "3"):       return "03"
    if "DEMAIS" in v or "GRANDE" in v or v in ("05", "5"):     return "05"
    if "NAO INFORMADO" in v or v in ("00", "0"):               return "00"
    return None            # desconhecido -> None -> PASSA com revisar_manual: true
```

⚠️ Atenção ao `"MICROEMPRESA (ME)"` **sem espaço**: o teste tem que ser por `in`, não por igualdade. E `"EMPRESA DE PEQUENO PORTE"` contém `"EMPRESA"`, não `"MICRO"` — a ordem dos testes acima já resolve isso.

> **Alternativa mais segura, se algum dia o mapeamento der problema:** remover a cláusula de porte do gate. Ela é decorativa — quem filtra é `opcao_mei`, e o conjunto `{00,01,03,05}` cobre 100% dos códigos existentes. O porte fica gravado no registro para leitura humana e nada mais. **Não fazer isso sem avisar o Pedro**, porque "checar o porte" está no pedido literal dele.

### 3.4 Heurística proibida

Razão social no padrão `NN.NNN.NNN NOME DE PESSOA FÍSICA` (ex.: `68.150.540 JOAO VITOR GOMES DA SILVA`) é **indício**, nunca prova. Caso concreto observado: CNPJ `68.150.540/0001-95`, aberto em 22/07/2026, razão social no padrão clássico de MEI, aparece com `simei.optant = false`. Ou não é MEI, ou o arquivo do Simples ainda não pegou. **Não dá para saber.**

Decida **sempre** pelo campo `opcao_mei`. Nunca pelo formato do nome.

### 3.5 NÃO CONFIRMADO — e como confirmar em 5 minutos

| # | O que não foi confirmado | Impacto | Procedimento de confirmação (≤ 5 min, R$ 0) |
|---|---|---|---|
| **N1** | Se o filtro `mei.excluir_optante: true` da Casa dos Dados considera `data_exclusao_mei` ou só olha `opcao_mei == "S"`. | Muda se **ex-MEIs** entram ou saem do roster. | 1) Ache no roster um CNPJ com `data_exclusao_mei` preenchida (via OpenCNPJ). 2) Rode a mesma query de CEP com `{"mei":{"excluir_optante":true}}`. 3) Veja se aquele CNPJ aparece na lista. Aparece → o filtro respeita a exclusão. Não aparece → o filtro é burro e **o contorno da §4.1 (baixar tudo e filtrar local) é obrigatório**. |
| **N1b** | Se a Casa dos Dados pública exige `User-Agent`. **A afirmação anterior ("sem UA → 403") NÃO se reproduz.** | Nenhum — o pedido funciona com e sem UA. | Reteste ao vivo: `POST .../v5/public/cnpj/pesquisa` **sem header `User-Agent` nenhum** (`-H "User-Agent;"`) devolveu **HTTP 200** com corpo normal; idem com UA vazio e com o UA default do curl. **Manter UA identificável por boa prática e educação com o provedor, não porque bloqueia.** |
| **N2** | Rate limit oficial da Casa dos Dados pública. | Bloqueio de IP no meio da varredura. | Não é confirmável por doc (não publicado). **Assumir o pior:** ≥ 0,5 s entre chamadas, retry com backoff. |
| **N3** | Os 100 req/min declarados pelo OpenCNPJ. | Throttle mal calibrado → 429 no meio do roster. | Dispare 120 GETs em 60 s contra CNPJs do roster e conte os 429. 2 minutos. **Enquanto não fizer: throttle de 0,7 s.** |
| **N4** | Rate limit da BrasilAPI. | Só afeta o fallback. | Não publicado. Assumir ≤ 1 req/s. |
| **N5** | Divergência OpenCNPJ × CNPJá no campo `simples` (CNPJ `45.404.836/0001-90`). ⚠️ **O caso descrito NÃO REPRODUZ.** Reconsulta em **2026-08-10**: OpenCNPJ devolve `opcao_simples="S"` + `data_opcao_simples="2026-01-01"` e CNPJá devolve `simples.optant=true` — **as duas concordam**. A divergência anterior era provavelmente snapshot velho da OpenCNPJ. | Nenhum hoje. O risco de defasagem entre fontes continua **teórico mas plausível** (as bases são snapshots mensais de origens diferentes). | **Não citar esse CNPJ como prova de divergência.** A escolha de fonte canônica se justifica sozinha (rate limit + campos), não por esse caso. Se aparecer divergência nova, colar o par de respostas aqui com a data. **OpenCNPJ segue canônica e `cnpj_fonte` + `cnpj_consultado_em` são gravados em todo registro.** |
| **N6** | Se existe paginação por parâmetro não documentado na Casa dos Dados pública. | Se existisse, o fatiamento recursivo seria desnecessário. | `pagina` e `limite` já foram testados: **ignorados**. `/openapi.json` → 403, `/v5/openapi.json` → 401. Sem OpenAPI acessível, não há como descobrir. **Manter o fatiamento.** |
| **N7** | Preço da Casa dos Dados autenticada ("R$ 0,01/CNPJ"). | Nenhum — o endpoint público resolve. | O número veio de blog de terceiro, **não da documentação oficial**. **Não citar como fato em lugar nenhum.** |
| **N8** | Blocos além de A–E nas quadras 310–315. | Empresas de um eventual bloco F ficam sem mapeamento bloco→CEP. | Verificação em campo, na própria rota. Registrar em `data/ceps-cln.json`. |

---

## 4. Passo a passo: nome fantasia → CNPJ → porte

### Etapa 0 — baixar o roster (1× por mês, offline, R$ 0)

**Endpoint:** `POST https://api.casadosdados.com.br/v5/public/cnpj/pesquisa`
**Header obrigatório:** `Content-Type: application/json`. **Header recomendado:** `User-Agent` identificável.

> ⚠️ **Correção de um fato que estava errado neste documento:** a versão anterior afirmava "sem `User-Agent` → 403". **Isso não se reproduz.** Reteste ao vivo: requisição **sem header `User-Agent` nenhum** (`-H "User-Agent;"`) → **HTTP 200** com corpo normal; idem com UA vazio e com o UA default do curl.
> **Continue mandando um UA identificável** (`ROTA-RUA/prospect-enhanced (contato: ...)`) — é boa prática, ajuda o provedor a falar com você antes de bloquear e custa nada. Só não é verdade que ele seja obrigatório.

**Body (baixar TODAS as ativas, sem filtro de MEI no servidor):**

```json
{
  "cep": ["70766530"],
  "situacao_cadastral": ["ATIVA"]
}
```

**Por que não filtrar MEI no servidor:** a semântica de `mei.excluir_optante` em relação a `data_exclusao_mei` é **NÃO CONFIRMADA** (item N1). Filtrar no servidor arriscaria descartar em silêncio o ex-MEI que virou ME — que é lead bom. **O filtro MEI é aplicado localmente**, com `opcao_mei` + `data_exclusao_mei`.

**Resposta:**

```json
{
  "total": 23,
  "cnpjs": [
    {
      "cnpj": "11222333000144",
      "razao_social": "PANIFICADORA SANTA CLARA COMERCIO DE ALIMENTOS LTDA",
      "nome_fantasia": "SANTA CLARA",
      "situacao_cadastral": {
        "situacao_atual": "ATIVA",
        "motivo": "SEM MOTIVO",
        "data": "2026-07-22T00:00:00Z"
      }
    }
  ]
}
```

> ⚠️ **`situacao_cadastral` no RETORNO é objeto, não string.** No **filtro de entrada** ele é array de string (`"situacao_cadastral": ["ATIVA"]`); na **resposta** vem `{situacao_atual, motivo, data}`. Parser que espera string quebra ou grava `[object Object]`. Ler sempre `.situacao_cadastral.situacao_atual`.

#### 4.1 A limitação crítica (e o contorno validado)

**O endpoint público devolve no máximo 20 registros por combinação de filtro.** O campo `total` é correto, mas **`pagina` é silenciosamente ignorado** — páginas 1 a 11 no CLN 310 devolveram **os mesmos 20 registros**. `limite: 1000` também é ignorado.

Contorno: **fatiar o espaço de busca até cada fatia ficar ≤ 20.**

```python
def coletar(filtro, coletados):
    r = post(filtro)
    if r["total"] <= 20:
        coletados.update(r["cnpjs"])
        return
    if "porte_empresa" not in filtro:
        for p in ["00", "01", "03", "05"]:
            coletar({**filtro, "porte_empresa": {"codigos": [p]}}, coletados)
    else:
        ini, fim = filtro.get("data_abertura", (DATA_MIN, HOJE))
        meio = ini + (fim - ini) / 2
        coletar({**filtro, "data_abertura": {"inicio": ini, "fim": meio}}, coletados)
        coletar({**filtro, "data_abertura": {"inicio": meio, "fim": fim}}, coletados)

# GUARDA OBRIGATÓRIA — sem isso o funil roda achando que viu tudo
assert len(coletados) == total_do_cep, f"recall incompleto: {len(coletados)}/{total_do_cep}"
```

**Teste real no pior CEP** (70756-530, 80 registros não-MEI): 3 queries por porte + 4 faixas de data = **7 queries → 80/80 únicos, recall 100%**.

Custo total da varredura das 6 quadras: **~110 requisições, R$ 0,00, ~15 min de relógio.**

#### 4.2 Armadilhas da Casa dos Dados

| Armadilha | Sintoma | Defesa |
|---|---|---|
| Chave desconhecida é **silenciosamente ignorada** (mandei `{"mei":{"optante":false}}` no formato errado e o `total` não mudou) | O funil roda **sem filtrar nada** e ninguém percebe | **Teste de regressão a cada rodada:** baseline sem filtro vs. com filtro. Se o `total` não mudar, **aborta**. |
| Formato errado devolve **400 mudo, sem corpo** | Difícil de debugar | Logar o body enviado junto com o status |
| ~~Sem `User-Agent` → 403~~ | **Não reproduz.** Requisição sem UA nenhum devolveu 200 | Mandar UA identificável por boa prática; **não** tratar a ausência dele como causa de erro na hora de debugar |
| `total: 0` num CEP | Pode ser real (não há bloco E naquela quadra) ou erro | Registrar em `roster-meta.json` como `cep_vazio` e **seguir**. Não abortar. |

**Saída da etapa 0:** `prospect-enhanced/data/roster-cln-310-315.json` (versionado no repo) + `roster-meta.json` com `baixado_em`, `total_por_cep`, `total_por_quadra`, `cep_vazio[]`.
**TTL: 30 dias.** Rodar de novo só na virada do mês.

---

### Etapa 1 — detalhe por CNPJ (OpenCNPJ)

Para **todos** os CNPJs do roster (~856), `GET https://api.opencnpj.org/{cnpj}`.

**Throttle: 0,7 s entre chamadas + backoff exponencial em 429.** (Os 100 req/min são declarados, não estressados — item N3.)

**Nomes reais dos campos** (verificados em resposta ao vivo — não improvisar):

| O que você quer | Campo real na OpenCNPJ | Armadilha |
|---|---|---|
| Flag MEI | `opcao_mei` (`"S"`/`"N"`) | — |
| Saída do MEI | `data_exclusao_mei` | vem **`"0000-00-00"`**, não vazio |
| Porte | `porte_empresa` (**string**, ex. `"Microempresa (ME)"`) | **não existe `porte_codigo`** — derivar (§3.3.1) |
| Data de abertura | **`data_inicio_atividade`** | ⚠️ **não é `data_abertura`** |
| Sócios | **`QSA`** (maiúsculo) | ⚠️ **não é `qsa`** |
| CNAE principal | `cnae_principal` | — |
| Descrição do CNAE | **`cnaes[].descricao`** | ⚠️ **não existe `cnae_descricao` no topo**; a descrição do principal também aparece como `cnae_principal_descricao` em parte das respostas — **testar as duas e cair para `null`** |
| Telefones | `telefones[{ddd, numero}]` | usado no match M2 |
| Outros | `email`, `capital_social`, `situacao_cadastral`, `logradouro`, `numero`, `complemento`, `cep` | — |

No schema, `data_abertura` e `cnae_descricao` são campos **`DERIV`**, com a origem literal ao lado — não campos `CNPJ` diretos.

**Tempo:** ~10 min para 856 CNPJs. **Custo: R$ 0.**

---

### Etapa 2 — o cruzamento Google ↔ roster (o gargalo real)

Cascata de matching. **Para no primeiro acerto.**

| Passo | Sinal | Limiar | `cnpj_metodo` | `cnpj_confianca` |
|---|---|---|---|---|
| **M1** | Similaridade de nome contra `nome_fantasia` **e** `razao_social` dos candidatos do CEP/quadra | ≥ 0,85 | `nome` | **alta** |
| **M2** | Telefone do GMB (só dígitos, DDD 61) ∈ `telefones[]` do OpenCNPJ | exato | `telefone` | **alta** |
| **M3** | Número da loja: regex `LOJA\s*(\d+)` sobre `logradouro + " " + numero + " " + complemento` **concatenados** | exato + mesmo CEP | `numero_loja` | media |
| **M4** | CNAE compatível com os `type_ids` do Google, entre 2–3 candidatos do mesmo CEP | desempate | `cnae` | media |
| **M5** | Similaridade de nome entre 0,60 e 0,85 | fila de revisão | `manual` | baixa |
| — | nada casou | — | `nenhum` | `nao_resolvido` |

**Normalização de nome antes de comparar:** maiúsculas → remover acentos → remover `LTDA`, `ME`, `EPP`, `EIRELI`, `S/A` → remover pontuação → colapsar espaços.

```python
if score >= 0.85:                 # match automático
elif 0.60 <= score < 0.85:        # fila de revisão manual
else:                             # PLANO B (§5)
```

---

### Etapa 3 — aplicar o gate

```python
# ÚNICA forma correta. Ver §3.2 — "0000-00-00" NÃO é vazio e porte ausente NÃO reprova.
eh_mei = (opcao_mei == "S") and (data_exclusao_mei in (None, "", "0000-00-00"))
passa  = (eh_mei is False) and (porte_codigo is None or porte_codigo in {"00", "01", "03", "05"})
```

> 🔴 Este bloco já esteve escrito como `not data_exclusao_mei` — que é **o bug mais caro do documento**: com `"0000-00-00"` no campo, `eh_mei` daria `False` e **todo MEI passaria no filtro hard #1**. Se você está copiando daqui, copie esta versão.

**Ausente ≠ reprovado.** Cinco casos em que a empresa **PASSA** mesmo sem CNPJ confirmado:

| Caso | Decisão | Justificativa |
|---|---|---|
| `cnpj_confianca = nao_resolvido` | **PASSA** com `mei_incerto: true` + flag "confirmar CNPJ na visita" | O vendedor vai à porta de qualquer jeito. Custo de um `type=place` errado = **1 crédito**. Custo de descartar lead bom = uma venda. São ~15% do funil ≈ 20 chamadas extras. |
| `cnpj_confianca = baixa` (M5) | **PASSA**, mesma flag, entra na fila de revisão antes da rota | idem |
| Empresa aberta há **< 60 dias** | **PASSA** com `mei_incerto: true` | Defasagem declarada de até 45 dias no arquivo do Simples. Caso concreto: CNPJ `68.150.540/0001-95`. |
| `opcao_mei = "S"` **com** `data_exclusao_mei` preenchida | **PASSA** (ex-MEI virou ME/EPP) | Ignorar esse campo descarta o lead que acabou de crescer. |
| `opcao_mei` = `null` / "EM BRANCO" | **PASSA** com `mei_incerto: true` | "EM BRANCO / OUTROS" no layout da RF não é "sim". |

**Único caso que REPROVA:** `opcao_mei == "S"` **e** sem data de exclusão → `motivo_descarte: mei`. É o filtro hard do Pedro, e **nunca relaxa** — nem no degrau R5 da escada de parada.

---

## 5. PLANO B — quando o nome fantasia não bate (o caso mais comum)

**Medido: só 65% dos registros do roster têm `nome_fantasia` preenchido.** Nos outros 35% você tem apenas a razão social, que costuma ser nome de pessoa física ou sigla sem relação nenhuma com a fachada.

### 5.1 A armadilha do `logradouro`

O campo `logradouro` da Receita para a CLN é **texto livre e caótico**. Três registros reais do **mesmo CEP** `70766-530`:

```
logradouro = "SHCN, CL, QUADRA 313, BLOCO C LOJA 66, 84 SUBSOLO"   numero = "S/N"
logradouro = "SHCN CL 313 BLOCO C LOJA"                             numero = "10"
logradouro = "SHC/NORTE COMERCIO LOCAL 313 BLOCO C"                 numero = "SN"   complemento = "SUBSOLO 16"
```

Três lições:

1. **A Receita escreve `"SHCN CL"` ou `"SHC/NORTE COMERCIO LOCAL"` — nunca `"CLN"`.** Regex procurando `CLN` no cadastro da Receita não acha nada.
2. **A loja tanto está em `numero` quanto enterrada em `logradouro` ou `complemento`.** O regex tem que rodar sobre os três **concatenados**.
3. **Só o CEP é confiável** como chave de bloco.

### 5.2 A cascata, em ordem de custo

| # | Sinal | Como | Força |
|---|---|---|---|
| **1** | **Telefone** ⭐ | Normalizar o `phone` do GMB (só dígitos, com DDD 61) e cruzar com `telefones[]` do OpenCNPJ | **O mais forte depois do CEP.** Casa mesmo quando o nome é totalmente diferente. Deve ser obrigatório na cascata, não opcional. |
| **2** | **Número da loja** | Regex `LOJA\s*(\d+)` sobre `logradouro + " " + numero + " " + complemento`, comparado com o número extraído do `address` do Google | Boa, dentro do mesmo CEP |
| **3** | **CNAE × categoria do Google** | Não identifica sozinho; desempata entre 2–3 candidatos do mesmo CEP | Desempate |
| **4** | **Site / domínio** | Muitos sites têm CNPJ no rodapé ou na página de contato (1 WebFetch) | Boa, mas cara — só para finalistas |
| **5** | **Revisão humana** | Com o roster de ~575 já baixado e a meta de 40, sobra margem | Última instância |

### 5.3 A regra que fecha o Plano B

**Descartar um match ambíguo custa menos do que gravar o CNPJ errado.** Marque `cnpj_confianca: alta | media | baixa | nao_resolvido` no schema e trate `baixa` e `nao_resolvido` como **"confirmar na visita"** — a empresa **continua no funil**. O vendedor está indo naquela porta de qualquer jeito, e o CNPJ se confirma no balcão em 10 segundos.

> **O trade-off, explícito:** admitir os não-resolvidos devolve ~20 chamadas de `type=place` ao custo do lote (120 em vez de ~100). É dinheiro bem gasto. Tratar "não resolvido" como reprovado cortaria ~15% do funil às cegas — e cortaria por defeito de cadastro da Receita, não por mérito da empresa.

---

## 6. Exemplos de request/response

> **Nenhuma credencial neste arquivo.** Onde houver chave, use variável de ambiente, no mesmo padrão de `scripts/gmb-probe.sh`. Os endpoints públicos usados aqui **não exigem chave**.

### 6.1 ViaCEP — descobrir os CEPs de uma quadra

**curl:**
```bash
curl -s "https://viacep.com.br/ws/DF/Brasilia/CLN%20313/json/" \
  | jq -r '.[] | "\(.cep)  \(.logradouro)"'
```

**PowerShell:**
```powershell
$r = Invoke-RestMethod -Uri "https://viacep.com.br/ws/DF/Brasilia/CLN%20313/json/"
$r | Select-Object cep, logradouro | Format-Table
```

**Response (trecho):**
```json
[
  { "cep": "70766-500", "logradouro": "SHCN CL Quadra 313", "bairro": "Asa Norte", "localidade": "Brasília", "uf": "DF" },
  { "cep": "70766-510", "logradouro": "SHCN CL Quadra 313 Bloco A", "bairro": "Asa Norte", "localidade": "Brasília", "uf": "DF" }
]
```

---

### 6.2 Casa dos Dados — inventário por CEP

**curl** (o `-A` é boa prática, **não** obrigatório — ver §4.2):

```bash
curl -s -X POST "https://api.casadosdados.com.br/v5/public/cnpj/pesquisa" \
  -H "Content-Type: application/json" \
  -A "ROTA-RUA/1.0 (prospeccao interna; contato@exemplo.com)" \
  -d '{
        "cep": ["70766530"],
        "situacao_cadastral": ["ATIVA"]
      }' \
  | jq '{total: .total, n: (.cnpjs | length)}'
```

**PowerShell:**

```powershell
$headers = @{
  "Content-Type" = "application/json"
  "User-Agent"   = "ROTA-RUA/1.0 (prospeccao interna)"
}
$body = @{
  cep                = @("70766530")
  situacao_cadastral = @("ATIVA")
} | ConvertTo-Json -Depth 5

$r = Invoke-RestMethod -Method Post `
      -Uri "https://api.casadosdados.com.br/v5/public/cnpj/pesquisa" `
      -Headers $headers -Body $body

"total={0}  retornados={1}" -f $r.total, $r.cnpjs.Count
if ($r.total -gt 20) { Write-Warning "FATIAR: total > 20, a resposta esta truncada" }
```

**Response:**
```json
{
  "total": 23,
  "cnpjs": [
    { "cnpj": "11222333000144", "razao_social": "PANIFICADORA SANTA CLARA COMERCIO DE ALIMENTOS LTDA", "nome_fantasia": "SANTA CLARA", "situacao_cadastral": { "situacao_atual": "ATIVA", "motivo": "SEM MOTIVO", "data": "2026-07-22T00:00:00Z" } },
    { "cnpj": "22333444000155", "razao_social": "22.333.444 MARIA DE SOUZA COSTA",                      "nome_fantasia": "",            "situacao_cadastral": { "situacao_atual": "ATIVA", "motivo": "SEM MOTIVO", "data": "2026-03-11T00:00:00Z" } }
  ]
}
```

> Repare no segundo registro: `nome_fantasia` **vazio** e razão social no padrão de pessoa física. É exatamente o caso do Plano B (§5) — e é **indício**, não prova, de MEI. Só o `opcao_mei` decide.

**Fatiamento por porte** (quando `total > 20`):

```bash
for P in 00 01 03 05; do
  curl -s -X POST "https://api.casadosdados.com.br/v5/public/cnpj/pesquisa" \
    -H "Content-Type: application/json" \
    -A "ROTA-RUA/1.0" \
    -d "{\"cep\":[\"70756530\"],\"situacao_cadastral\":[\"ATIVA\"],\"porte_empresa\":{\"codigos\":[\"$P\"]}}" \
    | jq -r "\"porte $P -> total=\(.total) retornados=\(.cnpjs|length)\""
  sleep 0.5
done
```

---

### 6.3 OpenCNPJ — detalhe e flag MEI (fonte canônica)

**curl:**
```bash
curl -s "https://api.opencnpj.org/11222333000144" \
  | jq '{cnpj, razao_social, nome_fantasia, porte_empresa, opcao_mei, data_exclusao_mei, data_inicio_atividade, cnae_principal, telefones}'
```

**PowerShell:**
```powershell
$cnpj = "11222333000144"
$d = Invoke-RestMethod -Uri "https://api.opencnpj.org/$cnpj"

# ATENCAO: data_exclusao_mei vem "0000-00-00" quando a empresa nunca saiu do MEI
$semExclusao = ($null -eq $d.data_exclusao_mei) -or ($d.data_exclusao_mei -in @("", "0000-00-00"))
$ehMei = ($d.opcao_mei -eq "S") -and $semExclusao
[pscustomobject]@{
  cnpj    = $d.cnpj
  razao   = $d.razao_social
  porte   = $d.porte_empresa
  mei     = $d.opcao_mei
  saiuMei = $d.data_exclusao_mei
  eh_mei  = $ehMei
  passa   = (-not $ehMei)
}
```

**Response (trecho, valores ilustrativos):**
```json
{
  "cnpj": "11222333000144",
  "razao_social": "PANIFICADORA SANTA CLARA COMERCIO DE ALIMENTOS LTDA",
  "nome_fantasia": "SANTA CLARA",
  "porte_empresa": "Microempresa (ME)",
  "opcao_simples": "S",
  "opcao_mei": "N",
  "data_opcao_mei": "0000-00-00",
  "data_exclusao_mei": "0000-00-00",
  "data_inicio_atividade": "2016-02-09",
  "situacao_cadastral": "Ativa",
  "cnae_principal": "1091102",
  "cnaes": [
    { "codigo": "1091102", "descricao": "Fabricação de produtos de padaria e confeitaria com predominância de produção própria" }
  ],
  "QSA": [],
  "logradouro": "SHCN CL 313 BLOCO C LOJA",
  "numero": "14",
  "complemento": "",
  "cep": "70766530",
  "telefones": [{ "ddd": "61", "numero": "33401122" }],
  "email": "contato@exemplo.com.br",
  "capital_social": "80000.00"
}
```

**O caso do ex-MEI (que PASSA):**
```json
{
  "opcao_mei": "S",
  "data_opcao_mei": "2018-04-02",
  "data_exclusao_mei": "2023-12-31",
  "porte_empresa": "Micro Empresa"
}
```
→ `eh_mei = false` → **PASSA**. Ela cresceu e saiu do MEI. É lead bom.

---

### 6.4 BrasilAPI — fallback

```bash
curl -s "https://brasilapi.com.br/api/cnpj/v1/11222333000144" \
  | jq '{razao_social, porte, codigo_porte, opcao_pelo_mei, data_exclusao_do_mei}'
```

```powershell
$d = Invoke-RestMethod -Uri "https://brasilapi.com.br/api/cnpj/v1/11222333000144"
$d | Select-Object razao_social, porte, codigo_porte, opcao_pelo_mei
```

⚠️ Nomes de campo **diferentes** do OpenCNPJ (`opcao_pelo_mei` booleano vs. `opcao_mei` string `"S"/"N"`). O adaptador tem que normalizar, e o registro grava `cnpj_fonte: "brasilapi"`.

---

### 6.5 CNPJá Open — só desempate manual (5 req/min)

```bash
curl -s "https://open.cnpja.com/office/11222333000144" \
  | jq '{name: .company.name, size: .company.size.acronym, simei: .company.simei.optant}'
```

```powershell
$d = Invoke-RestMethod -Uri "https://open.cnpja.com/office/11222333000144"
[pscustomobject]@{ nome = $d.company.name; porte = $d.company.size.acronym; simei = $d.company.simei.optant }
```

> **5 req/min.** 40 empresas = 8 minutos. **Nunca no caminho automatizado.**

---

### 6.6 Padrão de credencial (quando houver)

Nenhum endpoint deste documento exige chave. Se algum dia usar a Casa dos Dados autenticada:

```bash
# .env NÃO versionado; a chave nunca vai para o repo
: "${CASADOSDADOS_API_KEY:?defina CASADOSDADOS_API_KEY no ambiente}"
curl -s -X POST "https://api.casadosdados.com.br/v5/cnpj/pesquisa" \
  -H "api-key: ${CASADOSDADOS_API_KEY}" \
  -H "Content-Type: application/json" \
  -A "ROTA-RUA/1.0" \
  -d '{"cep":["70766530"]}'
```

```powershell
if (-not $env:CASADOSDADOS_API_KEY) { throw "defina CASADOSDADOS_API_KEY no ambiente" }
$headers = @{ "api-key" = $env:CASADOSDADOS_API_KEY; "Content-Type" = "application/json"; "User-Agent" = "ROTA-RUA/1.0" }
```

Mesmo padrão de `scripts/gmb-probe.sh`, que lê `$SERPAPI_MCP_URL` / `$SERPAPI_KEY` do ambiente. **Chave em arquivo versionado, nunca.**

---

## 7. Riscos

| # | Risco | Impacto | Mitigação |
|---|---|---|---|
| R1 | **Teto de 20 registros por filtro** na Casa dos Dados; `pagina` e `limite` ignorados | Perde 90%+ do universo sem perceber | Fatiamento recursivo CEP → porte → `data_abertura` + **`assert len(únicos) == total`, abortando se divergir** |
| R2 | **Filtro malformado ignorado em silêncio** | Roda o funil inteiro sem filtrar e ninguém nota | Teste de regressão baseline vs. filtrado a cada rodada; `total` igual = aborta |
| R3 | ~~Sem `User-Agent` → 403~~ — **afirmação retirada, não reproduz** (200 sem UA nenhum) | Nenhum | UA identificável por boa prática. Não perder tempo debugando 4xx por causa de UA |
| R4 | **Rate limit não publicado** (Casa dos Dados, BrasilAPI) | Bloqueio de IP no meio da varredura | ≥ 0,5 s entre chamadas, retry com backoff exponencial, roster cacheado 30 dias |
| R5 | **Rate limit do OpenCNPJ não estressado** (100/min declarado) | 429 no meio do detalhe | Throttle 0,7 s + backoff; fallback BrasilAPI |
| R6 | **Dado desatualizado** — defasagem de até 45 dias no arquivo do Simples | Empresa nova classificada errado. Caso concreto: `68.150.540/0001-95`, aberto 22/07/2026, razão social padrão MEI, `simei.optant = false` | Empresa aberta há **< 60 dias** → `mei_incerto: true` e **passa**, com "confirmar na visita" |
| R7 | **Divergência entre fontes** — risco **teórico**: as bases são snapshots mensais de origens diferentes. O caso `45.404.836/0001-90` que era citado aqui **não reproduz** (as duas fontes concordam em 2026-08-10, item N5) | Duas fontes poderiam dar respostas diferentes para o mesmo CNPJ | **OpenCNPJ é canônica.** Gravar `cnpj_fonte` e `cnpj_consultado_em` em todo registro. **Nunca tratar duas fontes como intercambiáveis.** Divergência nova → colar o par de respostas no item N5 com a data |
| R8 | **Homônimo** — duas empresas com nome parecido no mesmo CEP ("Café do Bloco" × "Café do Bloco C") | CNPJ errado no relatório; o vendedor cita o CNPJ de outro na porta | O CEP já reduz o universo a 5–40 candidatos. Match ≥ 0,85 **e** desempate por telefone (M2) ou número de loja (M3). Empate persistente → `cnpj_confianca: baixa` + `revisar_manual: true`. **Nunca escolher o primeiro da lista.** |
| R9 | **Marca genérica** ("Ótica", "Barbearia") que casa com vários registros | Falso positivo de match | Exigir M2 ou M3 como confirmação quando o nome normalizado tiver ≤ 2 tokens |
| R10 | **Empresa sem CNPJ localizável** — fachada existe no Google, cadastro não aparece no roster (sublocação, ponto novo, empresa registrada em outro endereço, filial não cadastrada) | Lead bom descartado por defeito de cadastro | **PASSA** com `cnpj_confianca: nao_resolvido` + `mei_incerto: true` + `nivel_admissao: base`. Confirma-se no balcão. |
| R11 | **`nome_fantasia` vazio em 35% do roster** | M1 falha na maioria dos casos difíceis | M2 (telefone) é **obrigatório** na cascata, não opcional |
| R12 | **`logradouro` da Receita é texto livre** — escreve "SHCN CL" ou "SHC/NORTE COMERCIO LOCAL", nunca "CLN"; loja aparece em 3 campos diferentes | Regex de endereço não acha nada | Regex sobre `logradouro + numero + complemento` concatenados. **Só o CEP é chave confiável.** |
| R13 | **Endpoint público da Casa dos Dados pode fechar sem aviso** | Funil para de rodar | Roster **versionado no repo**. Fallback: (1) BrasilAPI por CNPJ conhecido, (2) OpenCNPJ. Último recurso: rodar o lote **sem** o gate MEI, marcando **todas** as empresas com `mei_incerto: true` e `nivel_admissao: R3`. **Nunca fingir que o gate rodou.** |
| R14 | **BigQuery / Base dos Dados como atalho** | A tabela `simples` está reconhecidamente desatualizada (issue aberta no repo deles) — e é justamente a que tem a flag MEI | **Não usar como fonte primária do gate MEI.** |
| R15 | **Porte usado como proxy de MEI** | Descarta ~35% de leads bons (20 micros, só 13 MEI no CEP 70766-530) | Regra da §3.2. `porte` **nunca** decide MEI. |

---

## 8. Checklist antes de rodar o lote

- [ ] `data/ceps-cln.json` bate com a tabela da §1 (36 CEPs).
- [ ] Item **N1** confirmado (semântica de `excluir_optante`) **ou** o roster foi baixado sem filtro de MEI no servidor.
- [ ] Teste de regressão do filtro rodou (baseline vs. filtrado) e o `total` mudou.
- [ ] `assert len(únicos) == total` passou para **todos** os 36 CEPs.
- [ ] CEPs com `total: 0` registrados em `roster-meta.json` como `cep_vazio`.
- [ ] `roster-cln-310-315.json` tem `baixado_em` com menos de 30 dias.
- [ ] `cnpj_fonte` e `cnpj_consultado_em` preenchidos em 100% dos registros que têm CNPJ.
- [ ] Nenhuma chave de API em arquivo versionado.
- [ ] `porte_codigo` está sendo **derivado** pela tabela da §3.3.1 (e não comparado direto contra a string da API).
- [ ] A comparação de `data_exclusao_mei` inclui **`"0000-00-00"`** — testada contra 1 MEI real do roster (`eh_mei` tem que dar `True`).
- [ ] Um CNPJ com `porte_empresa` desconhecido/ausente **passa** no gate (não reprova).

---

## 9. Fontes

- [Layout oficial dos Dados Abertos do CNPJ — Receita Federal (PDF)](https://www.gov.br/receitafederal/dados/cnpj-metadados.pdf) — porte `00/01/03/05` e `OPÇÃO PELO MEI` `S/N/branco`
- [Dados públicos CNPJ — Receita Federal](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/dados-abertos)
- [Casa dos Dados — Pesquisa Avançada de empresas (schema dos filtros)](https://docs.casadosdados.com.br/pesquisa-avan%C3%A7ada-de-empresas-16579062e0)
- [Casa dos Dados — Informações Básicas (base URL, header `api-key`)](https://docs.casadosdados.com.br/informa%C3%A7%C3%B5es-b%C3%A1sicas-1278846m0)
- [OpenCNPJ](https://www.opencnpj.com/)
- [BrasilAPI — docs](https://brasilapi.com.br/docs)
- [CNPJá SDK / API pública (5 req/min)](https://github.com/cnpja/sdk-nodejs)
- [ReceitaWS API](https://receitaws.com.br/api)
- [Base dos Dados — acesso via BigQuery](https://basedosdados.org/docs/access_data_bq)
- [Issue sobre desatualização da tabela `simples` no Base dos Dados](https://github.com/basedosdados/queries-basedosdados/issues/623)
- ViaCEP (usado para os 36 CEPs): `https://viacep.com.br/ws/DF/Brasilia/CLN%20{N}/json/`

---

*Referência de fontes de CNPJ — `/prospect-enhanced` · Singular Group*
*[Registrado por: DESKTOP — 2026-08-10]*

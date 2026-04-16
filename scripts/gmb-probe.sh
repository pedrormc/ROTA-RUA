#!/usr/bin/env bash
# gmb-probe.sh — wrapper de teste pro MCP SerpAPI (engine google_maps)
# Uso:
#   scripts/gmb-probe.sh "restaurantes CLN 312 Norte"           # busca padrao
#   scripts/gmb-probe.sh "padaria CLN 204" reviews <data_id>    # reviews de uma loja
#   scripts/gmb-probe.sh "<query>" instagram                    # acha instagram
#
# Requer:
#   - $SERPAPI_MCP_URL exportada (URL completa do MCP SerpAPI), OU
#   - $SERPAPI_KEY exportada (a URL e construida automaticamente)
#   - python3, curl

set -euo pipefail

if [[ -z "${SERPAPI_MCP_URL:-}" ]]; then
  if [[ -n "${SERPAPI_KEY:-}" ]]; then
    SERPAPI_MCP_URL="https://mcp.serpapi.com/${SERPAPI_KEY}/mcp"
  else
    echo "Erro: defina SERPAPI_MCP_URL ou SERPAPI_KEY no ambiente." >&2
    exit 1
  fi
fi

QUERY="${1:?Uso: gmb-probe.sh <query> [reviews|instagram] [data_id]}"
MODE="${2:-search}"
DATA_ID="${3:-}"

build_payload() {
  case "$MODE" in
    search)
      python3 -c "
import json, sys
print(json.dumps({
  'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call',
  'params': {
    'name': 'search',
    'arguments': {
      'params': {
        'engine': 'google_maps',
        'q': sys.argv[1],
        'll': '@-15.7474,-47.8810,16z',
        'hl': 'pt-br',
        'gl': 'br',
        'start': 0
      },
      'mode': 'compact'
    }
  }
}))" "$QUERY"
      ;;
    reviews)
      [[ -z "$DATA_ID" ]] && { echo "Erro: passe data_id como 3 arg" >&2; exit 1; }
      python3 -c "
import json, sys
print(json.dumps({
  'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call',
  'params': {
    'name': 'search',
    'arguments': {
      'params': {
        'engine': 'google_maps_reviews',
        'data_id': sys.argv[1],
        'hl': 'pt-br',
        'sort_by': 'newest'
      },
      'mode': 'compact'
    }
  }
}))" "$DATA_ID"
      ;;
    instagram)
      python3 -c "
import json, sys
print(json.dumps({
  'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call',
  'params': {
    'name': 'search',
    'arguments': {
      'params': {
        'engine': 'google',
        'q': f'site:instagram.com {sys.argv[1]} brasilia',
        'hl': 'pt-br',
        'gl': 'br',
        'num': 10
      },
      'mode': 'compact'
    }
  }
}))" "$QUERY"
      ;;
    *)
      echo "Modo desconhecido: $MODE (use search|reviews|instagram)" >&2
      exit 1
      ;;
  esac
}

PAYLOAD="$(build_payload)"

curl -sS -X POST "$SERPAPI_MCP_URL" \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "Accept: application/json, text/event-stream" \
  --data-raw "$PAYLOAD" \
| python3 -c "
import json, sys
raw = sys.stdin.read()
try:
    d = json.loads(raw)
    inner = d.get('result', {}).get('structuredContent', {}).get('result')
    out = json.loads(inner) if inner else d
    print(json.dumps(out, indent=2, ensure_ascii=False))
except Exception:
    print(raw)
"

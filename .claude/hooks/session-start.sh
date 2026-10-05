#!/bin/bash
# Prepara sessões do Claude Code na nuvem: Tesseract com português (OCR),
# pacotes Python do extrair_pdf.py e dependências de teste.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}"

bash orbital/scripts/instalar_dependencias.sh
python3 -m pip install -q -r requirements-dev.txt

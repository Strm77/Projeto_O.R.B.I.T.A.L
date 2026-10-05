#!/usr/bin/env bash
# Instala as dependências do extrair_pdf.py: Tesseract (OCR) com português
# e os pacotes Python. Linux (apt/dnf/pacman) e macOS (Homebrew).
#
#   bash orbital/scripts/instalar_dependencias.sh
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

tem() { command -v "$1" >/dev/null 2>&1; }
sudo_se_preciso() { if [ "$(id -u)" -eq 0 ]; then "$@"; else sudo "$@"; fi; }

echo "==> Tesseract (OCR) com idioma português"
case "$(uname -s)" in
  Linux)
    if tem apt-get; then
      sudo_se_preciso apt-get update -q
      sudo_se_preciso apt-get install -y -q tesseract-ocr tesseract-ocr-por
    elif tem dnf; then
      sudo_se_preciso dnf install -y tesseract tesseract-langpack-por
    elif tem pacman; then
      sudo_se_preciso pacman -S --needed --noconfirm tesseract tesseract-data-por
    else
      echo "Gerenciador de pacotes não reconhecido. Instale 'tesseract' e o idioma 'por' manualmente." >&2
      exit 1
    fi
    ;;
  Darwin)
    if ! tem brew; then
      echo "Homebrew não encontrado. Instale em https://brew.sh e rode este script de novo." >&2
      exit 1
    fi
    brew install tesseract tesseract-lang
    ;;
  *)
    echo "Sistema não suportado por este script (Windows: use o instalador do Tesseract do"
    echo "projeto UB Mannheim, marcando o idioma Portuguese, e depois rode o pip abaixo)." >&2
    exit 1
    ;;
esac

echo "==> Pacotes Python"
PY="$(command -v python3 || command -v python)"
"$PY" -m pip install -r "$AQUI/requirements.txt"

echo "==> Verificação"
if ! tesseract --list-langs 2>/dev/null | grep -qx por; then
  echo "ERRO: tesseract instalado, mas sem o idioma 'por'." >&2
  exit 1
fi
"$PY" - "$AQUI" <<'EOF'
import sys
sys.path.insert(0, sys.argv[1])
import extrair_pdf
motivo = extrair_pdf._ocr_indisponivel()
if motivo:
    sys.exit(f"ERRO: OCR indisponível para o extrair_pdf.py: {motivo}")
print("OK: extrair_pdf.py pronto, com OCR em português.")
EOF

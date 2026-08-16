# Uso: source activate.sh
# Ativa a venv e exporta as credenciais do .env para a sessão.

_LAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"

source "$_LAB_DIR/.venv/bin/activate"

if [ -f "$_LAB_DIR/.env" ]; then
  set -a
  source "$_LAB_DIR/.env"
  set +a
  echo "✅ venv ativada + credenciais do .env carregadas"
else
  echo "⚠️  venv ativada, mas .env não existe. Copie: cp .env.example .env"
fi

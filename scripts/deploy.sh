#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd -- "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="$PROJECT_ROOT/.venv/bin/python"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "Virtual environment not found at $PROJECT_ROOT/.venv" >&2
  echo "Run 'python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt' first." >&2
  exit 1
fi

if git status --porcelain | grep -qE '^(M|A|D|R|\? )'; then
  echo "Working tree contains uncommitted changes. Commit or stash them before deploying." >&2
  exit 1
fi

DEPLOY_SSH=${DEPLOY_SSH:-ubuntu@94.249.192.193}
DEPLOY_APP_USER=${DEPLOY_APP_USER:-landing}
DEPLOY_DIR=${DEPLOY_DIR:-/srv/landing}
DEPLOY_VENV=${DEPLOY_VENV:-$DEPLOY_DIR/.venv}
DEPLOY_REPO=${DEPLOY_REPO:-git@github.com:vasstas/landing-site.git}
DEPLOY_BRANCH=${DEPLOY_BRANCH:-main}
DEPLOY_SERVICE=${DEPLOY_SERVICE:-gunicorn-landing}

echo "Running Django system checks..."
"$PYTHON_BIN" manage.py check

echo "Running Django test suite..."
"$PYTHON_BIN" manage.py test

if git remote get-url origin >/dev/null 2>&1; then
  echo "Pushing branch $DEPLOY_BRANCH to origin..."
  git push origin "$DEPLOY_BRANCH"
else
  echo "Remote 'origin' is not configured. Skipping git push." >&2
fi

ssh "$DEPLOY_SSH" \
  DEPLOY_DIR="$DEPLOY_DIR" \
  DEPLOY_VENV="$DEPLOY_VENV" \
  DEPLOY_REPO="$DEPLOY_REPO" \
  DEPLOY_BRANCH="$DEPLOY_BRANCH" \
  DEPLOY_APP_USER="$DEPLOY_APP_USER" \
  DEPLOY_SERVICE="$DEPLOY_SERVICE" \
  'bash -s' <<'REMOTE'
set -euo pipefail

if ! id "$DEPLOY_APP_USER" >/dev/null 2>&1; then
  echo "Remote user $DEPLOY_APP_USER does not exist." >&2
  exit 1
fi

if [[ ! -d "$DEPLOY_DIR/.git" ]]; then
  echo "Cloning repository $DEPLOY_REPO into $DEPLOY_DIR"
  sudo mkdir -p "$DEPLOY_DIR"
  sudo chown -R "$DEPLOY_APP_USER":"$DEPLOY_APP_USER" "$DEPLOY_DIR"
  sudo -u "$DEPLOY_APP_USER" -H git clone "$DEPLOY_REPO" "$DEPLOY_DIR"
fi

sudo -u "$DEPLOY_APP_USER" -H bash <<APP
set -euo pipefail
cd "$DEPLOY_DIR"
git fetch origin "$DEPLOY_BRANCH"
git checkout "$DEPLOY_BRANCH"
git pull --ff-only origin "$DEPLOY_BRANCH"
python3 -m venv "$DEPLOY_VENV"
"$DEPLOY_VENV/bin/pip" install --upgrade pip
"$DEPLOY_VENV/bin/pip" install -r requirements.txt
"$DEPLOY_VENV/bin/python" manage.py migrate --noinput
"$DEPLOY_VENV/bin/python" manage.py collectstatic --noinput
APP

sudo systemctl restart "$DEPLOY_SERVICE"
sudo systemctl status --no-pager "$DEPLOY_SERVICE"
REMOTE

echo "Deployment complete."

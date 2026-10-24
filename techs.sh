#!/usr/bin/env bash
# Tech list tooling. Usage:
#   ./techs.sh check                         validate README.md
#   ./techs.sh list                          print category, name, url
#   ./techs.sh add --name N --url U --category C --desc D [--date YYYY-MM-DD]
#   ./techs.sh publish "Add <name>"          check, commit README.md, push to main
#   ./techs.sh test                          run the script's tests
set -euo pipefail
cd "$(dirname "$0")"

REPO_URL="https://github.com/codegik/tech-experiments.git"
GIT_AUTH=(-c credential.helper= -c 'credential.helper=!gh auth git-credential')

case "${1:-}" in
  check|list|add)
    exec python3 scripts/techs.py "$@"
    ;;
  publish)
    msg="${2:?usage: ./techs.sh publish \"Add <name>\"}"
    python3 scripts/techs.py check
    if [ "$(git branch --show-current)" != "main" ]; then
      echo "error: not on main" >&2; exit 1
    fi
    other=$(git status --porcelain | grep -v ' README.md$' || true)
    if [ -n "$other" ]; then
      echo "error: changes outside README.md, refusing to publish:" >&2
      echo "$other" >&2; exit 1
    fi
    # No new edit: still push, so a commit left by a failed push goes out on retry.
    if ! git diff --quiet HEAD -- README.md; then
      git add README.md
      git commit -q -m "$msg"
    fi
    git "${GIT_AUTH[@]}" pull -q --rebase "$REPO_URL" main
    python3 scripts/techs.py check
    git "${GIT_AUTH[@]}" push -q "$REPO_URL" HEAD:main
    git fetch -q "$REPO_URL" main:refs/remotes/origin/main 2>/dev/null || true
    echo "pushed: https://github.com/codegik/tech-experiments/commit/$(git rev-parse HEAD)"
    ;;
  test)
    exec python3 -m unittest discover -s tests -v
    ;;
  *)
    sed -n '2,7p' "$0" | sed 's/^# \{0,1\}//'
    exit 1
    ;;
esac

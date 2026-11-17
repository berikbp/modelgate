#!/usr/bin/env bash
# CI-only workaround for kubectl wait failing before a new CRD has conditions.
# Run the real command every time; never replace or alter its result.
set -uo pipefail

kubectl_bin="${M5_KUBECTL_BIN:-/usr/local/bin/kubectl}"
if [[ " $* " != *" wait "* || " $* " != *" crd/"* ]]; then
  exec "$kubectl_bin" "$@"
fi

error_file=$(mktemp)
trap 'rm -f "$error_file"' EXIT
status=1
for attempt in {1..10}; do
  if "$kubectl_bin" "$@" 2>"$error_file"; then
    cat "$error_file" >&2
    exit 0
  else
    status=$?
  fi
  cat "$error_file" >&2
  if ! grep -Fq '.status.conditions accessor error: <nil>' "$error_file"; then
    exit "$status"
  fi
  if (( attempt < 10 )); then
    echo "CRD conditions not populated yet; retrying kubectl wait ($attempt/10)." >&2
    sleep 2
  fi
done
exit "$status"

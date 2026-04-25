#!/usr/bin/env bash
# shellcheck shell=bash

MANAGE_LICENSE_BLOCKED=0
MANAGE_LICENSE_BLOCK_REASON=""

manage_license_config_get() {
  local key="$1"
  local env_file=""
  env_file="$(manage_license_guard_config_file)"
  [[ -r "${env_file}" ]] || return 1
  awk -F= -v key="${key}" '
    $1 == key {
      sub(/^[[:space:]]+/, "", $2)
      sub(/[[:space:]]+$/, "", $2)
      print $2
      exit
    }
  ' "${env_file}"
}

manage_license_trusted_default_api_url() {
  printf '%s\n' "https://autoscript-license.minidecrypt.workers.dev/api/v1/license/check"
}

manage_license_guard_config_file() {
  printf '%s\n' "/etc/autoscript/license/config.env"
}

manage_license_guard_bin_path() {
  printf '%s\n' "/usr/local/bin/autoscript-license-check"
}

manage_license_guard_api_url() {
  local configured=""

  configured="${AUTOSCRIPT_LICENSE_API_URL:-}"
  [[ -n "${configured}" ]] || configured="$(manage_license_config_get "AUTOSCRIPT_LICENSE_API_URL" 2>/dev/null || true)"
  if [[ -n "${configured}" ]]; then
    printf '%s\n' "${configured}"
    return 0
  fi

  configured="${AUTOSCRIPT_LICENSE_DEFAULT_API_URL:-}"
  [[ -n "${configured}" ]] || configured="$(manage_license_config_get "AUTOSCRIPT_LICENSE_DEFAULT_API_URL" 2>/dev/null || true)"
  if [[ -n "${configured}" ]]; then
    printf '%s\n' "${configured}"
    return 0
  fi

  manage_license_trusted_default_api_url
}

manage_license_public_status_url() {
  local api_url=""
  local api_origin=""
  local trusted_api_url=""
  api_url="$(manage_license_guard_api_url)"
  case "${api_url}" in
    */api/v1/license/check)
      printf '%s/api/public/license/status\n' "${api_url%/api/v1/license/check}"
      return 0
      ;;
  esac

  if [[ "${api_url}" =~ ^https?://[^/]+ ]]; then
    api_origin="${BASH_REMATCH[0]}"
    printf '%s/api/public/license/status\n' "${api_origin}"
    return 0
  fi

  trusted_api_url="$(manage_license_trusted_default_api_url)"
  printf '%s/api/public/license/status\n' "${trusted_api_url%/api/v1/license/check}"
}

manage_license_guard_enabled() {
  local api_url=""
  local env_file=""
  local license_bin=""
  local license_service="${AUTOSCRIPT_LICENSE_SERVICE:-autoscript-license-enforcer.service}"
  local license_timer="${AUTOSCRIPT_LICENSE_TIMER:-autoscript-license-enforcer.timer}"
  env_file="$(manage_license_guard_config_file)"
  license_bin="$(manage_license_guard_bin_path)"
  api_url="$(manage_license_guard_api_url)"
  if [[ -n "${api_url}" ]]; then
    return 0
  fi
  [[ -e "${env_file}" || -x "${license_bin}" || -e "/etc/systemd/system/${license_service}" || -e "/etc/systemd/system/${license_timer}" ]]
}

manage_license_stage_for_args() {
  local action="${1:-}"
  case "${action}" in
    __apply-ssh-network|__sync-ssh-network-session-targets)
      printf '%s\n' "runtime"
      ;;
    *)
      printf '%s\n' "manage"
      ;;
  esac
}

manage_license_guard_preflight() {
  local action="${1:-}"
  local stage license_bin api_url config_file default_api_url license_output

  MANAGE_LICENSE_BLOCKED=0
  MANAGE_LICENSE_BLOCK_REASON=""

  if ! manage_license_guard_enabled; then
    return 0
  fi

  stage="$(manage_license_stage_for_args "${action}")"
  license_bin="$(manage_license_guard_bin_path)"
  api_url="$(manage_license_guard_api_url)"
  config_file="$(manage_license_guard_config_file)"
  default_api_url="$(manage_license_trusted_default_api_url)"

  if [[ ! -x "${license_bin}" ]]; then
    echo "manage: binary license guard tidak ditemukan: ${license_bin}" >&2
    return 1
  fi
  if declare -F manage_bootstrap_path_trusted >/dev/null 2>&1 && ! manage_bootstrap_path_trusted "${license_bin}"; then
    echo "manage: binary license guard tidak trusted: ${license_bin}" >&2
    return 1
  fi

  if ! license_output="$(
    AUTOSCRIPT_LICENSE_DEFAULT_API_URL="${default_api_url}" \
      AUTOSCRIPT_LICENSE_API_URL="${api_url}" \
      AUTOSCRIPT_LICENSE_CONFIG_FILE="${config_file}" \
      "${license_bin}" check --stage "${stage}" --allow-disabled=false 2>&1
  )"; then
    printf '%s\n' "${license_output}" >&2
    if [[ "${stage}" == "manage" && -z "${action}" ]]; then
      MANAGE_LICENSE_BLOCKED=1
      local detail_line
      detail_line="$(printf '%s\n' "${license_output}" | grep "^Detail :" | head -n1)"
      MANAGE_LICENSE_BLOCK_REASON="${license_output##*$'\n'}"
      if [[ -n "${detail_line}" ]]; then
        MANAGE_LICENSE_BLOCK_REASON="${detail_line}\n${MANAGE_LICENSE_BLOCK_REASON}"
      fi
      [[ -n "${MANAGE_LICENSE_BLOCK_REASON}" ]] || MANAGE_LICENSE_BLOCK_REASON="Akses manage ditolak oleh license guard."
      return 0
    fi
    echo "manage: akses ${stage} ditolak oleh license guard." >&2
    return 1
  fi
  return 0
}

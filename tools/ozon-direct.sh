#!/bin/bash
# Пускает ozon.ru мимо VPN-туннеля: маршруты на сети Ozon через домашний шлюз.
# Использование: sudo tools/ozon-direct.sh [add|remove|status]
# Маршруты не переживают перезагрузку и смену сети — запускайте заново.

set -euo pipefail

NETS=(185.73.192.0/22 195.34.20.0/23)   # AS44386 (Ozon)
HOSTS=(95.181.182.181)

action="${1:-add}"

# Шлюз физического интерфейса (enX), а не туннеля utunX
read -r GW IFACE < <(netstat -rn -f inet | awk '$1=="default" && $NF ~ /^en[0-9]+$/ {print $2, $NF; exit}')
if [[ -z "${GW:-}" ]]; then
  echo "Не найден шлюз на en*: проверьте подключение к сети." >&2
  exit 1
fi

if [[ "$action" != "status" && $EUID -ne 0 ]]; then
  echo "Нужен sudo: sudo $0 $action" >&2
  exit 1
fi

case "$action" in
  add)
    echo "Шлюз: $GW ($IFACE)"
    for n in "${NETS[@]}";  do route -n delete -net  "$n" >/dev/null 2>&1 || true; route -n add -net  "$n" "$GW"; done
    for h in "${HOSTS[@]}"; do route -n delete -host "$h" >/dev/null 2>&1 || true; route -n add -host "$h" "$GW"; done
    ;;
  remove)
    for n in "${NETS[@]}";  do route -n delete -net  "$n" || true; done
    for h in "${HOSTS[@]}"; do route -n delete -host "$h" || true; done
    ;;
  status)
    echo "Шлюз: $GW ($IFACE)"
    for ip in 185.73.193.68 195.34.20.1 95.181.182.181; do
      printf '%-16s -> ' "$ip"
      route -n get "$ip" 2>/dev/null | awk '/interface:/ {print $2}'
    done
    echo "(en* = напрямую, utun* = через VPN)"
    exit 0
    ;;
  *)
    echo "Использование: sudo $0 [add|remove|status]" >&2
    exit 1
    ;;
esac

"$0" status

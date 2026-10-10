#!/system/bin/sh
set -eu
umask 077
STAGE=/data/local/tmp/android-use-install-001
CORE=/data/local/tmp/android-use-core
RELAY=/data/adb/android-use-relay
MOD=/data/adb/modules/android_use_relay
BOOTSCRIPT=/data/adb/service.d/99-android-use-core.sh
PY=/data/data/com.termux/files/usr/bin/python
[ "$(id -u)" = "0" ] || { echo "Requires preinstalled root"; exit 1; }
[ -d /data/adb/modules ] && [ -x "$PY" ] || { echo "Missing Magisk or Termux Python"; exit 1; }
for f in controller.py display-engine.jar ui-test.jar agent.py network_route.py tools.json module.prop service.sh core-service.sh; do
  [ -s "$STAGE/$f" ] || { echo "Missing staged source: $f"; exit 1; }
done
mkdir -p "$CORE" "$RELAY" "$MOD" /data/adb/service.d
chmod 700 "$CORE" "$RELAY" "$MOD"
backup_and_copy() {
  if [ -f "$2" ]; then cp -p "$2" "$2.android-use-001.bak"; chmod 600 "$2.android-use-001.bak"; chmod 600 "$2.android-use-001.bak"; fi
  cp "$1" "$2"
  chmod "$3" "$2"
}
backup_and_copy "$STAGE/controller.py" "$CORE/controller.py" 600
backup_and_copy "$STAGE/display-engine.jar" "$CORE/display-engine.jar" 600
backup_and_copy "$STAGE/ui-test.jar" "$CORE/ui-test.jar" 600
backup_and_copy "$STAGE/agent.py" "$RELAY/agent.py" 600
backup_and_copy "$STAGE/network_route.py" "$RELAY/network_route.py" 600
backup_and_copy "$STAGE/network_route.py" "$RELAY/network_route.py" 600
backup_and_copy "$STAGE/tools.json" "$RELAY/tools.json" 600
backup_and_copy "$STAGE/module.prop" "$MOD/module.prop" 644
backup_and_copy "$STAGE/service.sh" "$MOD/service.sh" 755
backup_and_copy "$STAGE/core-service.sh" "$BOOTSCRIPT" 755
"$PY" -m py_compile "$CORE/controller.py" "$RELAY/agent.py" "$RELAY/network_route.py"
"$PY" "$CORE/controller.py" test
/system/bin/sh -n "$BOOTSCRIPT"
/system/bin/sh -n "$MOD/service.sh"
echo "Android Use 0.0.3 files installed. Existing private relay configuration preserved."

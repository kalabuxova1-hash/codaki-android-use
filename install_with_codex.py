#!/usr/bin/env python3
"""Codex-led Android Use v0.0.3 deployment; root/Magisk must already exist."""
import argparse
import hashlib
from pathlib import Path
import re
import shutil
import subprocess
import sys

BASE = Path(__file__).resolve().parent
STAGE = "/data/local/tmp/android-use-install-001"
FILES = {
    "controller.py": "src/core/controller.py",
    "display-engine.jar": "src/core/display-engine.jar",
    "ui-test.jar": "src/core/ui-test.jar",
    "agent.py": "src/relay/agent.py",
    "network_route.py": "src/relay/network_route.py",
    "network_route.py": "src/relay/network_route.py",
    "tools.json": "src/relay/tools.json",
    "module.prop": "magisk/module.prop",
    "service.sh": "magisk/service.sh",
    "core-service.sh": "magisk/core-service.sh",
    "device-install.sh": "magisk/device-install.sh",
}
HASHES = {
    "display-engine.jar": "6d3a0a1e34f9ca8c7cb686f5c2ad44bacf6163d2bbf299c0d98f67b8621c25c9",
    "ui-test.jar": "4df35d250cab9b307bd8c3c2f6f318001e497cd928c07a9b92124888e8cd94da",
}

def run(command):
    result = subprocess.run(command, capture_output=True, text=True, errors="replace")
    if result.returncode:
        raise RuntimeError("Command failed: " + command[0] + ": " + result.stderr[-400:])
    return result.stdout

def main():
    parser = argparse.ArgumentParser(description="Install Android Use v0.0.3 via authorized ADB")
    parser.add_argument("--serial", required=True, help="Exact authorized adb device serial")
    options = parser.parse_args()
    serial = options.serial
    if not re.fullmatch(r"[A-Za-z0-9._:-]{3,100}", serial):
        parser.error("Invalid device serial")
    adb_path = shutil.which("adb")
    if not adb_path:
        raise RuntimeError("ADB must be available on this PC.")
    prefix = [adb_path, "-s", serial]
    devices = run([adb_path, "devices"])
    if not any(line.split()[:2] == [serial, "device"] for line in devices.splitlines()):
        raise RuntimeError("Selected phone is not ADB-authorized.")
    def adb(*args):
        return run(prefix + list(args))
    def root(command):
        return adb("shell", "su -c '" + command + "'")
    if "uid=0(" not in root("id"):
        raise RuntimeError("Preinstalled root is required; this installer does not install it.")
    if root("test -d /data/adb/modules; echo $?").strip() != "0":
        raise RuntimeError("Preinstalled Magisk is required; this installer does not install it.")
    if root("test -x /data/data/com.termux/files/usr/bin/python; echo $?").strip() != "0":
        raise RuntimeError("Termux Python is missing. Install it separately.")
    for name, relative in FILES.items():
        path = BASE / relative
        if not path.is_file():
            raise RuntimeError("Missing file: " + relative)
        if name in HASHES and hashlib.sha256(path.read_bytes()).hexdigest() != HASHES[name]:
            raise RuntimeError("Source checksum mismatch: " + relative)
    adb("shell", "mkdir -p " + STAGE)
    for filename, relative in FILES.items():
        adb("push", str(BASE / relative), STAGE + "/" + filename)
    try:
        print(root("/system/bin/sh " + STAGE + "/device-install.sh").strip())
    finally:
        adb("shell", "rm -rf " + STAGE)
    print("Local Android Use 0.0.3 deployed. Codex: verify status and configure a private relay separately.")

if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError) as error:
        print("Install failed:", error, file=sys.stderr)
        sys.exit(1)

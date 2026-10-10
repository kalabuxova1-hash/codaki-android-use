# Install Codaki Android Use with Codex on a PC

**Release 0.0.3** · [English](#installation-workflow) · [Русский](#русский)

Give this file or the setup ZIP to Codex **with an explicit request to install**. Codex should perform the available setup work itself. The owner supplies a rooted phone; the project does not install root, Magisk, firmware or a bootloader.

If only this file was provided, download [android-use-codex-setup-0.0.3.zip](https://github.com/kalabuxova1-hash/codaki-android-use/releases/download/v0.0.3/android-use-codex-setup-0.0.3.zip) and [SHA256SUMS](https://github.com/kalabuxova1-hash/codaki-android-use/releases/download/v0.0.3/SHA256SUMS). Verify the ZIP's SHA-256, extract into a dedicated workspace and read AGENTS.md. The release packages source and ready Dex binaries.

## Installation workflow

### 1. Prerequisites and scope

**[Codaki Mini Codex](https://github.com/kalabuxova1-hash/codaki-mini-codex) must already be installed and configured. Codaki Android Use is a companion; standalone use is not supported. Confirm this prerequisite before proceeding. The installer does not enforce this check or install Mini Codex.**

- Phone: Android 16 / SDK 36 or later, preinstalled Magisk and Termux Python 3.10+. Initially verified on Redmi Turbo 3; other devices need validation. Core checks required display flags at runtime and refuses unsupported systems.
- PC: Codex with shell/file access, Python 3.10+ and ADB. Put the selected ADB directory in the process PATH; the installer finds `adb` there. Node.js 24+ builds the relay; Java/Javac run its Java tests.
- Cloud: the owner's account with Sites and Plugin Creator capabilities for a **new owner-private Site**. USB/root authorization, login and a final connection prompt may need the owner's action.
- Keep Mini Codex's server, keys, modules and networking unchanged. Preserve Android Use's existing idle cleanup and replacement installer.
- Do not send messages as a test. Use Settings, inspect, then stop the screen.

### 2. Check the selected phone

Run `adb devices`, select the intended authorized serial and use `adb -s SERIAL` for every operation. If the intended device is unclear, ask for that missing choice. Verify root with `su -c id`, Magisk's modules directory, `getprop ro.build.version.sdk` and Termux Python's version. Do not log account data or secrets.

If prerequisites are missing, explain the exact missing requirement. Local file placement alone does not create a ChatGPT plugin.

### 3. Provision the separate private relay

The ready relay is in `server/index.js` and `server/tools.json`; adapting Mini Codex's server is no longer necessary.

1. Follow the installed Sites skill and its Site MCP server reference. Register a new **private** Site with D1 binding `DB` and the MCP capability.
2. Copy this source to the private deployment checkout and set `.openai/hosting.json`'s null `project_id` to the returned identity. Keep this identity and credentials out of public GitHub.
3. Generate a fresh token (for example `secrets.token_urlsafe(48)`) in memory and set the Site secret **`AGENT_TOKEN`**. This exact name is required. Obtain the private Site's supported service authorization for the phone. Do not print tokens or put them in command arguments.
4. Run `npm test`, `npm run build`, `npm run validate`. The build emits `dist/server/index.js` and its hosting manifest. Use Sites' source/package helper and private publication flow with this artifact and its source. D1 tables initialize idempotently; no separate migration framework is needed.
5. Sites publication provisions the canonical private App/plugin. Reuse it; do not create a duplicate through Plugin Creator. Verify deployment and retain the actual private HTTPS origin.

If Sites is unavailable, complete only authorized local setup and report the unfinished remote connection. Do not substitute the author's deployment or unauthenticated hosting.

### 4. Install phone files

From the extracted package, run:

```sh
python install_with_codex.py --serial SERIAL
```

The existing installer verifies the two JAR digests, places Core/relay files, installs startup scripts, keeps previous copies as `.android-use-001.bak` and runs the local controller check. Backup copies are non-executable, preventing duplicate boot services. The relay respects Shadow VLESS standby behind another Android VPN without changing private network settings. Existing private `config.json` is preserved.

For a new installation, write `/data/adb/android-use-relay/config.json` with:

```json
{
  "relay_url": "https://YOUR-PRIVATE-SITE.chatgpt.site",
  "agent_token": "YOUR_FRESH_AGENT_TOKEN",
  "sites_authorization": "YOUR_SITE_SERVICE_AUTHORIZATION",
  "stop_files": [
    "/data/adb/modules/android_use_relay/disable",
    "/data/adb/modules/android_use_relay/remove"
  ]
}
```

These placeholders are not credentials. Build actual JSON in memory and transfer through subprocess stdin to the selected phone's root shell: base64-decode into a temporary file, verify SHA-256, set `0600`, rename atomically, and use a `0700` directory. Never echo values, put them in arguments, attach config to chat or commit it. Preserve a configured connection unless its owner requests replacement.

Start Core through `/system/bin/sh /data/adb/service.d/99-android-use-core.sh`; it refuses a duplicate healthy controller. Start the relay module service on a newly configured installation with detached stdin/stdout/stderr. Do not start a duplicate supervisor if one is healthy. Startup starts transport only and creates no display. A reboot is not required for this initial start.

### 5. Connect and verify

- Check the Core socket and `android_status`; do not request display 0 screen content.
- Open the private Site as its owner. Check `/status`: `online: true`, `blocked: false`. The authenticated owner is pinned by the first owner request.
- Use Sites' returned plugin identity and its supported installation suggestion if not already connected. The owner completes required connection UI.
- From the connected MCP plugin use a fresh `request_id` for a batch: privileges, start, launch a verified Settings component, inspect_ui. Verify a nonzero owned display, then stop it.
- Check that the virtual display disappeared and physical focus was preserved. Explicitly focus a non-password field before `android_set_text`; do not send real messages as a test.
- Use `android_job_result` only for a returned pending `job_id`. Do not repeat a failed/unknown action merely to obtain its result.

Report actual verification: local engine, relay heartbeat and connected-plugin call are separate checks. Do not claim reboot, locked-phone or cross-device validation unless performed.

### 6. Disable and maintenance

Disable **Android Use - Codaki Mini Codex helper** in Magisk to stop new relay work. Prefer `android_stop` to release an owned display. Keep backups, journal and private configuration for maintenance; do not delete Mini Codex data. Preserve the 120-second idle and virtual-task cleanup during updates.

## Русский

**Сначала установите и настройте [Codaki Mini Codex](https://github.com/kalabuxova1-hash/codaki-mini-codex). Codaki Android Use — дополнение; самостоятельная работа без Миникодекса не поддерживается. Подтвердите это условие до установки: установщик не проверяет наличие Mini Codex и не устанавливает его.**

Передайте Codex на ПК этот файл или ZIP и напишите:

> Установи Codaki Android Use 0.0.3 на мой подключённый телефон как помощника для Mini Codex. Прочитай INSTALL_WITH_CODEX.md, сам проверь требования, установи компоненты, создай мой отдельный приватный Site и подключи его плагин. Сохрани сервер и ключи Mini Codex. Root, Magisk и Termux с Python уже должны быть подготовлены; не меняй прошивку. Сохрани костыли автозакрытия экрана и установки с резервными копиями.

Codex выполняет шаги выше самостоятельно, если доступны ADB, файловые инструменты, Sites и Plugin Creator. Нужны Android 16, Magisk и Python в Termux. Первое разрешение USB/root, вход в аккаунт и финальное подключение могут требовать вашего участия.

В архиве есть готовый сервер, Java/Dex-компоненты, агент, установщик и тесты. Для удалённой работы нужен **свой приватный Site** с D1 `DB`, секретом **`AGENT_TOKEN`** и служебной авторизацией Sites. Ключи передаются отдельно, через stdin; в архиве их нет. Локальная установка без проверенного вызова плагина не означает готовое удалённое подключение.

После проверки освободите виртуальный экран. Соединение отключается через модуль Android Use в Magisk. Mini Codex менять не нужно.

## ChatGPT card ZIP / ZIP-карточка ChatGPT

The installer includes `chatgpt/codaki-android-use-chatgpt-0.0.3.zip`, the plugin source and `chatgpt/package_card.py`. Import the public card to add setup/control workflows if your client supports archive import. Importing it never changes phone configuration or ownership. Follow the existing owner-private relay setup; the server pins the authenticated ChatGPT owner. For a connected card with these skills, use the registered App ID returned by that owner's Sites deployment: `python chatgpt/package_card.py --app-id APP_ID`. Keep the output in `.private/chatgpt/` private and retain the existing device setup. Never reuse the author's personal server/card.

ZIP-карточка вложена в установщик. Её установка и подключение телефона — отдельные шаги; после настройки используется ID аккаунта ChatGPT нового владельца. В публичной карточке нет ID сервера автора, ключей или привязки устройства.

### Update with GPT

**A new version is out → download the new ZIP → give the file to GPT → ask it to update the plugin.**

> Update this Codaki plugin from the new ZIP. Keep my phone connection, private server, keys, memory and journal. Check the version and checksum, update the existing card, and verify the connection. If this is the full installer, also update the phone components using INSTALL_WITH_CODEX.md.

The bundled update workflow retains your existing App reference and ChatGPT owner binding. A card-only update leaves the phone runtime unchanged. GPT uses the client's available update/import tools; if the client requires a manual import, it prepares the replacement ZIP and tells you that final step. The file must come from this project's Releases. [Card setup and updates](chatgpt/README.md).


### Обновление через GPT

**Вышла новая версия → скачайте новый ZIP → передайте файл GPT → попросите обновить плагин.**

> Обнови этот плагин Codaki из нового ZIP. Сохрани подключение моего телефона, личный сервер, ключи, память и журнал. Проверь версию и контрольную сумму, обнови существующую карточку и проверь связь. Если это полный установщик, также обнови компоненты телефона по INSTALL_WITH_CODEX.md.

Встроенная инструкция обновления сохраняет существующий App ID и привязку к аккаунту ChatGPT владельца. Обновление одной карточки не меняет компоненты телефона. GPT использует доступные средства обновления/импорта; если клиент требует ручного импорта, он подготовит новый ZIP и укажет этот последний шаг. Берите файл из Releases этого проекта. [Настройка и обновление карточки](chatgpt/README.md).

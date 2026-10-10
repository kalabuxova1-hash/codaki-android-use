# Codaki Android Use installation

**Codaki Mini Codex must be installed and configured first. Standalone use is not supported. / Сначала установите и настройте Codaki Mini Codex; самостоятельная работа не поддерживается.**

Give [INSTALL_WITH_CODEX.md](../INSTALL_WITH_CODEX.md) or the release ZIP to Codex on your PC with an installation request. It contains prerequisites, the private Site setup, credential transfer and connected-plugin verification.

Android 16, preinstalled Magisk, Termux Python and authorized ADB are required. The PC is needed for setup; the phone's outbound HTTPS agent works without it afterward. Codex needs shell/files and Sites / Plugin Creator capabilities for cloud provisioning. Initial permissions and account prompts may need your action.

The replacement-with-backups installer and two-minute idle cleanup are retained. The archive includes no private connection or reusable author credentials.

## Русский

Скачайте ZIP в [Releases](https://github.com/kalabuxova1-hash/codaki-android-use/releases/latest), передайте Codex на ПК и попросите установить Android Use. Полная инструкция — [INSTALL_WITH_CODEX.md](../INSTALL_WITH_CODEX.md#русский).

Нужны Android 16, Magisk root, Termux с Python и разрешённая отладка для конкретного ПК. Для отдельного приватного подключения Codex нужны Sites / Plugin Creator. После настройки включённый ПК не нужен.

Установка с резервными копиями и автозакрытие после двух минут простоя сохранены. Личных ключей автора в архиве нет. Отключение — через модуль Android Use в Magisk.

### Update with GPT

**A new version is out → download the new ZIP → give the file to GPT → ask it to update the plugin.**

> Update this Codaki plugin from the new ZIP. Keep my phone connection, private server, keys, memory and journal. Check the version and checksum, update the existing card, and verify the connection. If this is the full installer, also update the phone components using INSTALL_WITH_CODEX.md.

The bundled update workflow retains your existing App reference and ChatGPT owner binding. A card-only update leaves the phone runtime unchanged. GPT uses the client's available update/import tools; if the client requires a manual import, it prepares the replacement ZIP and tells you that final step. The file must come from this project's Releases. [Card setup and updates](../chatgpt/README.md).


### Обновление через GPT

**Вышла новая версия → скачайте новый ZIP → передайте файл GPT → попросите обновить плагин.**

> Обнови этот плагин Codaki из нового ZIP. Сохрани подключение моего телефона, личный сервер, ключи, память и журнал. Проверь версию и контрольную сумму, обнови существующую карточку и проверь связь. Если это полный установщик, также обнови компоненты телефона по INSTALL_WITH_CODEX.md.

Встроенная инструкция обновления сохраняет существующий App ID и привязку к аккаунту ChatGPT владельца. Обновление одной карточки не меняет компоненты телефона. GPT использует доступные средства обновления/импорта; если клиент требует ручного импорта, он подготовит новый ZIP и укажет этот последний шаг. Берите файл из Releases этого проекта. [Настройка и обновление карточки](../chatgpt/README.md).

---
name: setup
description: "Install and connect Codaki Android Use for the owner; use for initial setup or a missing phone connection."
---

Confirm Codaki Mini Codex is already installed and configured. Download the matching Android Use setup ZIP and SHA256SUMS from the repository below, verify them, extract into a workspace and read AGENTS.md and INSTALL_WITH_CODEX.md. Android Use requires Android 16/SDK 36+, preinstalled Magisk/root, Termux Python and an authorized ADB connection for initial setup.

Follow INSTALL_WITH_CODEX.md to provision a separate owner-private Sites relay with D1 DB and MCP, a fresh AGENT_TOKEN and that owner's Sites service authorization. Install through install_with_codex.py with the selected authorized serial. Preserve Mini Codex's server, keys and files, the replacement installer, the 120-second idle cleanup and display-scoped cleanup. Transfer private config through stdin; importing the card must not write phone configuration or pair a device.

The existing relay pins the authenticated ChatGPT owner; the phone authenticates with its own token. GitHub identity and App ID are not phone ownership. Use the personal plugin created by Sites for the owner. If a card with the bundled skills is needed, obtain the registered App ID from Sites metadata and run chatgpt/package_card.py --app-id APP_ID in the setup checkout. Its private output references that App only; pairing remains the existing phone configuration step. Keep the bound card private and reuse an existing suitable Sites card instead of creating another server.

Verify Core, relay heartbeat and the connected plugin separately. Use a verified Settings component on a nonzero owned display, inspect it and stop the screen. Check physical focus remains intact. Do not send messages as a test. Report remaining prerequisites or unavailable connections precisely.

Source and releases: https://github.com/kalabuxova1-hash/codaki-android-use

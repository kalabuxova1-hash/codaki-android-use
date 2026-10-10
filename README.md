# Android Use 0.0.1 — Codaki Mini Codex companion

[Русский](README.ru.md) · [Install with Codex](INSTALL_WITH_CODEX.md)

**Android Use** is a standalone screen-control assistant for [Codaki Mini Codex](https://github.com/kalabuxova1-hash/codaki-mini-codex). It gives the agent a dedicated Android **virtual display** for GUI tasks while the owner keeps using the physical screen.

### Capabilities
- Open applications, tap, swipe, navigate and capture images of the private display.
- Inspect UI nodes, click visible text, enter text and batch several actions.
- Validate the dedicated display identity; never fall back to physical display 0.
- Run the phone-side service without a permanently connected PC after setup, using the owner's private authenticated HTTPS relay.

### Install
1. Download this repository.
2. Give [INSTALL_WITH_CODEX.md](INSTALL_WITH_CODEX.md) to **Codex on a PC** and ask it to complete setup.
3. Codex uses authorized ADB, verifies prerequisites, installs files, and tests the plugin. The included `install_with_codex.py` automates local device file placement.

**Preinstalled root, Magisk and Termux Python are required.** This project does **not** install root or Magisk, modify firmware, or unlock the bootloader. Each owner configures their own private relay and ChatGPT plugin: no public shared credentials are provided.

**Version:** 0.0.1. Initially verified on the author's Android 16 device; compatibility with every phone is not established.

[Voluntary donation through Boosty](https://boosty.to/mini_codexandroid).

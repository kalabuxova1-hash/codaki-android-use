# Codaki Android Use

![Codaki — Desktop freedom. Android.](docs/assets/codaki-cover.png)

**Computer Use for Android · A companion plugin for Codaki Mini Codex**

**English** · [Русский](README.ru.md) &nbsp; | &nbsp; **v0.0.3** · [MIT](LICENSE)

**Codaki Android Use adds Android app control to [Codaki Mini Codex — Миникодекс](https://github.com/kalabuxova1-hash/codaki-mini-codex).** An AI assistant can read the interface, find buttons, enter text and check results on a separate virtual display through **ChatGPT or Codex and MCP**.

**An Android analogue of the Computer Use approach: observe → act → check.** Codaki Mini Codex handles system tasks, files and phone maintenance; **Codaki Android Use** extends it with visual interaction inside apps.

> **Codaki Mini Codex is required.** Install and configure it first. Codaki Android Use is a companion plugin; standalone use without Mini Codex is not supported.

**Desktop freedom. Android.** Bring the observe → act → check workflow to your phone from an ordinary ChatGPT conversation: Codaki Mini Codex handles files and system tasks; Android Use adds app interaction on its own screen.

[Install the plugin](#codaki-install) · [How it helps](#codaki-features) · [Documentation](#codaki-docs) · [Download release](https://github.com/kalabuxova1-hash/codaki-android-use/releases/latest)

<br>

<a name="codaki-features"></a>

## How Codaki Android Use helps

<table>
<tr>
<td align="center" valign="top" width="56"><img src="https://raw.githubusercontent.com/kalabuxova1-hash/codaki-mini-codex/main/docs/assets/icons/phone.svg" width="40" height="40" alt=""></td>
<td valign="top"><strong>Work inside Android apps</strong><p>Open Settings, calculate a result or search in an app. Read interface elements, click by text, type Unicode and check the outcome.</p></td>
</tr>
<tr>
<td align="center" valign="top" width="56"><img src="https://raw.githubusercontent.com/kalabuxova1-hash/codaki-mini-codex/main/docs/assets/icons/files.svg" width="40" height="40" alt=""></td>
<td valign="top"><strong>Complete the Codaki workflow</strong><p>Use Codaki Mini Codex for files and phone maintenance, then Codaki Android Use for app screens. Each component keeps its own private relay and credentials.</p></td>
</tr>
<tr>
<td align="center" valign="top" width="56"><img src="https://raw.githubusercontent.com/kalabuxova1-hash/codaki-mini-codex/main/docs/assets/icons/memory.svg" width="40" height="40" alt=""></td>
<td valign="top"><strong>Give the assistant its own screen</strong><p>Run apps on a separate virtual display. After initial setup, daily use requires no running PC; ChatGPT or Codex, internet and your private relay are still needed.</p></td>
</tr>
</table>

### Try asking Codaki

- “Open the calculator on the Android Use screen and calculate 125 × 8.”
- “Open Settings, find About phone and check that it opened.”
- “Find the search field, enter this text and show the results.”

This follows the [Computer Use interaction loop](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) on Android. It is an independent implementation, not an official Computer Use product.

<br>

<a name="codaki-install"></a>

## <img src="https://raw.githubusercontent.com/kalabuxova1-hash/codaki-mini-codex/main/docs/assets/icons/wrench.svg" width="36" height="36" alt=""> Install Codaki Android Use

### Prepare your phone

- **[Codaki Mini Codex](https://github.com/kalabuxova1-hash/codaki-mini-codex) installed and configured first.** This is the required base for the supported setup.
- **Android 16 / SDK 36+**, root and Magisk already installed; **Termux with Python 3.10+**.
- A PC with Codex and authorized ADB for initial setup, plus your own private relay and plugin connection.

### Install with Codex

1. **Download the setup ZIP.** Get `android-use-codex-setup-0.0.3.zip` from the [latest release](https://github.com/kalabuxova1-hash/codaki-android-use/releases/latest).

2. **Give the ZIP to Codex on your PC.** Connect the intended phone and authorize USB debugging. The installation prompt is below.

3. **Check the plugin connection.** Ask the connected plugin to open Settings on its virtual screen, inspect the result and stop the screen.

**ChatGPT card ZIP:** [download `codaki-android-use-chatgpt-0.0.3.zip`](chatgpt/codaki-android-use-chatgpt-0.0.3.zip). It is also bundled inside the installer under `chatgpt/`. Import adds the workflows; connect your own phone after installation. The public ZIP has no author-specific App ID or device pairing. [Connect the card to your own server](chatgpt/README.md).

<details>
<summary><strong>Show the installation prompt for Codex</strong></summary>

> Install Codaki Android Use 0.0.2 from this ZIP as a companion for Codaki Mini Codex on my connected phone. Confirm Mini Codex is already installed and configured. Read INSTALL_WITH_CODEX.md, check requirements, create my separate private relay and connect the plugin. Keep Mini Codex's server, keys and files unchanged.

The ZIP includes source, ready Dex JARs, the ADB installer and setup instructions. Codex needs filesystem/shell access and Sites / Plugin Creator capabilities. USB/root authorization, account login and final connection may require your action. The installer does not root your phone or install Mini Codex; its presence must be confirmed before setup.

You can also give Codex [INSTALL_WITH_CODEX.md](https://github.com/kalabuxova1-hash/codaki-android-use/releases/latest/download/INSTALL_WITH_CODEX.md). It points to the release ZIP and checksum.

</details>

### Update with GPT

**A new version is out → download the new ZIP → give the file to GPT → ask it to update the plugin.**

> Update this Codaki plugin from the new ZIP. Keep my phone connection, private server, keys, memory and journal. Check the version and checksum, update the existing card, and verify the connection. If this is the full installer, also update the phone components using INSTALL_WITH_CODEX.md.

The bundled update workflow retains your existing App reference and ChatGPT owner binding. A card-only update leaves the phone runtime unchanged. GPT uses the client's available update/import tools; if the client requires a manual import, it prepares the replacement ZIP and tells you that final step. The file must come from this project's Releases. [Card setup and updates](chatgpt/README.md).

**Initial setup needs a PC; normal use can continue with it powered off.**

[Full installation workflow](INSTALL_WITH_CODEX.md) · [Requirements and disabling the module](docs/installation.md)

<br>

<a name="codaki-docs"></a>

## <img src="https://raw.githubusercontent.com/kalabuxova1-hash/codaki-mini-codex/main/docs/assets/icons/book.svg" width="36" height="36" alt=""> Codaki Android Use documentation

Open the topic you need.

<details>
<summary><strong>Ordinary ChatGPT chat, ongoing use and usage costs</strong></summary>

Control the phone through your personal Codaki plugin in a supported ChatGPT chat. Codaki's phone worker executes actions locally; it does not run a second model API session. The supported ChatGPT plugin flow needs no separate OpenAI API key, and Codaki itself adds no per-token fee.

Continue with new tasks and reuse saved solutions between conversations. This is designed for ongoing use after setup, not a guarantee of an infinitely long chat or uninterrupted background work. ChatGPT still uses tokens and context, and your account's [usage limits](https://learn.chatgpt.com/docs/pricing) still apply. Private relay hosting may have its own costs.

The goal is broad phone access comparable in spirit to Codex on a PC. Android permissions, supported tools and device compatibility determine the actual scope; feature parity with desktop Codex is not claimed.

</details>

<details>
<summary><strong>App control, virtual display and session cleanup</strong></summary>

- **A separate screen with its own focus.** Verified sessions kept physical display 0 in focus while apps ran on the virtual display. Apps may still have device-wide effects such as notifications or messages; a virtual display is not an app-data sandbox.
- **Understand the interface.** Android's built-in `UiAutomation` returns text, resource IDs, classes and bounds. Select visible buttons by text instead of relying on guessed coordinates.
- **Unicode input.** Set text in a uniquely focused, editable, non-password field, including Cyrillic. Ambiguous matches are refused.
- **Screenshots when needed.** Get PNG images alongside structured UI data.
- **Fewer round trips.** Batch known steps, inspect at decision points, and reuse the phone's HTTPS connection.
- **No PC during normal use.** After setup, the phone makes outbound HTTPS connections to your own private relay. The assistant still runs in ChatGPT or Codex and requires internet access.
- **No MagicDesk or project APK.** Core uses root-launched Java adapters and a Python controller. Existing Termux supplies Python.
- **Bounded sessions.** The phone agent requests display cleanup after two minutes of idle time; the display also has a ten-minute lease. Removing it destroys its content instead of moving its windows to the main screen.
- **Controlled execution.** Owner authentication, a root-only local socket, unique request IDs and a persistent job journal protect against automatic action replay after uncertain failures.

</details>

<details>
<summary><strong>Components and MCP tools</strong></summary>

| Component | Purpose |
| --- | --- |
| Android Use Core | Owns the virtual display and exposes a root-only Unix socket |
| Java adapters | Create the display; inspect and interact through Android `UiAutomation` |
| Phone agent | Retrieves jobs through authenticated outbound HTTPS and records outcomes |
| Private relay | Worker + D1 queue, owner authentication and MCP tools |
| Codex setup package | Source, prebuilt Dex, checksums, ADB installer and setup instructions |

There are **14 Core tools**, plus `android_job_result` for pending relay jobs: privileges, start, stop, status, app launch, tap, swipe, key, windows, screenshot, UI inspection, click by text, set text and batch execution. See [Tools](docs/tools.md) and [Architecture](docs/architecture.md).

</details>

<details>
<summary><strong>Measured performance</strong></summary>

On the same test phone, after the current optimizations:

| Measurement | Before | After |
| --- | --- | --- |
| Settings UI inspection, median of 3 samples | 1,240 ms | 303 ms |
| Warm HTTPS request, median excluding first connection | 300 ms | 118 ms |
| UI JSON in the measured view | 4,778 bytes | 3,063 bytes |

Two MCP batches containing nine Settings operations took **11.0 seconds of total tool execution time**. This excludes model reasoning between calls. It is **not an SMS-send benchmark** or a guarantee for other apps, networks or devices. See [Performance notes](docs/performance.md).

</details>

<details>
<summary><strong>Compatibility, limitations and owner control</strong></summary>

**Verified:** Redmi Turbo 3, Android 16, Magisk and Termux. Other devices, reboot behavior, secure-lock behavior and a fresh full cloud installation by another owner are not yet validated. Unsupported display flags cause Core to fail rather than use the physical screen.

The separate display does not isolate app data: apps may still change data, send messages or generate notifications. Sending a message requires your explicit instruction with recipient and content. The assistant should check the result and release the display.

Mini Codex is a prerequisite of the supported setup. This documentation requirement is not an automatic installer check or a shared-server integration.

</details>

<details>
<summary><strong>Development and verification</strong></summary>

Python 3.10+ and Node.js 24+ are needed for the host checks. Java/Javac are needed for the UI adapter tests; Android SDK D8 is needed only to rebuild the bundled Dex.

```sh
npm test
python -m unittest discover -s tests -p "test_*.py"
npm run build
npm run validate
python scripts/package.py
```

No npm dependencies are required. The public hosting manifest has no project identity: provision a new private Site for each owner. Never commit phone `config.json`, access tokens, journals or private screen captures.

</details>

<br>

## <img src="https://raw.githubusercontent.com/kalabuxova1-hash/codaki-mini-codex/main/docs/assets/icons/heart.svg" width="36" height="36" alt=""> Support Codaki

Support **Codaki Mini Codex and Codaki Android Use** on [Boosty](https://boosty.to/mini_codexandroid). Contributions, reproducible bug reports and compatibility reports are welcome. Source and public releases remain free under the **MIT license**.

---

**Codaki Android Use** is an independent open-source project, unaffiliated with OpenAI or Android. [MIT license](LICENSE).

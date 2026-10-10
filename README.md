# Android Use

**Release 0.0.2**

**Computer Use for Android — a companion for [Mini Codex](https://github.com/kalabuxova1-hash/codaki-mini-codex).**

[English](README.md) · [Русский](README.ru.md) · [Download setup ZIP](https://github.com/kalabuxova1-hash/android-use-mini-codex/releases/latest) · [Support on Boosty](https://boosty.to/mini_codexandroid)

Android Use lets an AI assistant open Android apps, read their interface, find buttons, enter text and verify results. It brings the Computer Use approach to Android: **observe → act → check**, through MCP tools and a separate virtual screen.

Mini Codex handles system tasks, files and phone maintenance. Android Use adds app interaction on its own display. The two can work together, with separate relay configuration and credentials.

> Early release. Verified on a Redmi Turbo 3 running Android 16 with Magisk and Termux. Other devices and Android versions have not been validated. This is an independent project, unaffiliated with OpenAI or Android.

## Why use it?

- **A separate screen with its own focus.** Verified sessions kept physical display 0 in focus while apps ran on the virtual display. Apps may still have device-wide effects such as notifications or messages; a virtual display is not an app-data sandbox.
- **Understand the interface.** Android's built-in `UiAutomation` returns text, resource IDs, classes and bounds. Select visible buttons by text instead of relying on guessed coordinates.
- **Unicode input.** Set text in a uniquely focused, editable, non-password field, including Cyrillic. Ambiguous matches are refused.
- **Screenshots when needed.** Get PNG images alongside structured UI data.
- **Fewer round trips.** Batch known steps, inspect at decision points, and reuse the phone's HTTPS connection.
- **No PC during normal use.** After setup, the phone makes outbound HTTPS connections to your own private relay. The assistant still runs in ChatGPT or Codex and requires internet access.
- **No MagicDesk or project APK.** Core uses root-launched Java adapters and a Python controller. Existing Termux supplies Python.
- **Bounded sessions.** The phone agent requests display cleanup after two minutes of idle time; the display also has a ten-minute lease. Removing it destroys its content instead of moving its windows to the main screen.
- **Controlled execution.** Owner authentication, a root-only local socket, unique request IDs and a persistent job journal protect against automatic action replay after uncertain failures.

## Install: give the file to Codex on your PC

**The recommended installation method is the setup ZIP.**

1. Download **`android-use-codex-setup-0.0.2.zip`** from [Releases](https://github.com/kalabuxova1-hash/android-use-mini-codex/releases/latest).
2. Connect your rooted Android 16 phone to the PC and authorize USB debugging. Install Termux and its Python package first.
3. Give the ZIP to **Codex on the PC**, or extract it into a folder Codex can access. Send:

   > Install Android Use from this ZIP as a companion for Mini Codex on my connected phone. Read INSTALL_WITH_CODEX.md, run the prerequisite checks, create my separate private relay and connect the plugin. Keep Mini Codex's server and keys unchanged.

The ZIP includes source, ready-to-use Dex JARs, the existing ADB installer and the complete installation workflow. Codex can perform setup with filesystem/shell access and the Sites / Plugin Creator capabilities. Initial USB authorization, Magisk permission, account login and a final connection prompt may require your action. The installer does not root the phone or install Mini Codex.

**You can also download only [INSTALL_WITH_CODEX.md](https://github.com/kalabuxova1-hash/android-use-mini-codex/releases/latest/download/INSTALL_WITH_CODEX.md)** and give that file to Codex. It directs Codex to the release ZIP and its checksum.

For requirements, exact commands, verification and disabling the module, see [Installation](docs/installation.md).

## What is included?

| Component | Purpose |
| --- | --- |
| Android Use Core | Owns the virtual display and exposes a root-only Unix socket |
| Java adapters | Create the display; inspect and interact through Android `UiAutomation` |
| Phone agent | Retrieves jobs through authenticated outbound HTTPS and records outcomes |
| Private relay | Worker + D1 queue, owner authentication and MCP tools |
| Codex setup package | Source, prebuilt Dex, checksums, ADB installer and setup instructions |

There are **14 Core tools**, plus `android_job_result` for pending relay jobs: privileges, start, stop, status, app launch, tap, swipe, key, windows, screenshot, UI inspection, click by text, set text and batch execution. See [Tools](docs/tools.md) and [Architecture](docs/architecture.md).

## Examples

- “Open the calculator on the Android Use screen and calculate 125 × 8.”
- “Open Settings, find About phone and check that it opened.”
- “Find the search field, enter this text and show the results.”

Sending a message requires your explicit instruction with the intended recipient and content. The assistant should verify the result and release the display when finished.

## Performance we measured

On the same test phone, after the current optimizations:

| Measurement | Before | After |
| --- | --- | --- |
| Settings UI inspection, median of 3 samples | 1,240 ms | 303 ms |
| Warm HTTPS request, median excluding first connection | 300 ms | 118 ms |
| UI JSON in the measured view | 4,778 bytes | 3,063 bytes |

Two MCP batches containing nine Settings operations took **11.0 seconds of total tool execution time**. This excludes model reasoning between calls. It is **not an SMS-send benchmark** or a guarantee for other apps, networks or devices. See [Performance notes](docs/performance.md).

## Development

Python 3.10+ and Node.js 24+ are needed for the host checks. Java/Javac are needed for the UI adapter tests; Android SDK D8 is needed only to rebuild the bundled Dex.

```sh
npm test
python -m unittest discover -s tests -p "test_*.py"
npm run build
npm run validate
python scripts/package.py
```

No npm dependencies are required. The public hosting manifest has no project identity: provision a new private Site for each owner. Never commit phone `config.json`, access tokens, journals or private screen captures.

Reboot behavior, secure-lock behavior, other devices and a fresh full cloud installation by another owner are not yet validated. Required virtual-display flags are checked at runtime; unsupported systems fail instead of falling back to the physical screen.

## Support development

If the project helps you, you can support Mini Codex and Android Use on **[Boosty](https://boosty.to/mini_codexandroid)**. Contributions, reproducible bug reports and compatibility reports are welcome.

[MIT license](LICENSE).

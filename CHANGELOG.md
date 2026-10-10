# Changelog

## 0.0.3

Includes an update skill: give GPT a newer ZIP to prepare/apply an update while preserving the existing App reference, private relay and phone state.

- Include the portable ChatGPT card ZIP, source manifest, icon, setup/control skills and private App-reference builder in the installer and release assets.
- Keep card import separate from device pairing; public cards contain no owner App ID or phone credentials.
- Add reproducible card packaging checks and release automation.
- Phone runtime and the original installer remain byte-for-byte preserved.

## 0.0.2

- Include the ready owner-private MCP relay, D1 queue, request IDs and completed/pending results.
- Add regression tests, setup ZIP packaging and SHA256SUMS.
- Expand English/Russian documentation, Codex installation, Computer Use for Android positioning and Boosty links.
- Preserve all published phone code and the 0.0.1 installer: focused input, 120-second idle cleanup, virtual-task cleanup, launch flags and replacement-with-backups behavior.
- Add LF line-ending rules for Windows checkouts.

## 0.0.1

- Initial public engine, agent, Java/Dex components and Codex-led installation.

# Nexus AI Terminal Assistant (VS Code)

This extension surfaces the existing terminal-based Nexus AI assistant inside VS Code. It
starts the Python CLI from `terminal/main.py`, streams output into an output channel, and
provides a webview panel with quick commands, a live log, and status feedback.

## Features

- **Start/stop the assistant** using the registered commands (`nexusAi.startAssistant`,
  `nexusAi.stopAssistant`). The assistant is launched in-process and you can keep the log
  inside the Output panel labeled **Nexus AI Terminal**.
- **Quick command palette** (`nexusAi.sendQuickCommand`) with curated commands such as
  `/models`, `/tasks`, `/git status`, and the GPT-5.1-Codex-Mini preview shortcut (rerouted
  through `/switch chatgpt` with an informational log entry).
- **Assistant panel** (`nexusAi.openAssistantPanel`) with a command input, quick command
  buttons, and a live log to stay in sync without leaving the editor.
- **Preferred model logging**: the extension highlights the configured preferred model (default
  `gpt-5.1-codex-mini`) every time the assistant starts so you can confirm the GPT-5.1 preview
  is the default experience.
- **Auto-start option** to boot the assistant whenever you open the workspace.

## Configuration (`settings.json`)

| Setting | Default | Description |
| --- | --- | --- |
| `nexusAiAssistant.pythonPath` | `python` | Path to the interpreter that runs `terminal/main.py`. Set this if you use a virtual environment or specific distribution. |
| `nexusAiAssistant.preferredModel` | `gpt-5.1-codex-mini` | Advertises GPT-5.1-Codex-Mini (Preview) inside the extension. The CLI itself still cycles through the supported models, but this label keeps the intent consistent for all clients. |
| `nexusAiAssistant.autoStart` | `false` | Set to `true` to automatically launch the assistant whenever you open the workspace. |

## Commands (Command Palette)

- **Nexus AI: Start Assistant** — Spins up the Python CLI and begins streaming logs.
- **Nexus AI: Stop Assistant** — Sends `SIGINT` to the CLI process so it stops cleanly.
- **Nexus AI: Run Quick Command** — Quick pick for the most used `/` commands.
- **Nexus AI: Open Assistant Panel** — Visual dashboard with log, status, and command entry.

## Quick Command Notes

The `/switch gpt-5.1-codex-mini` quick command logs a notice that the GPT-5.1-Codex-Mini
preview is funneled through the ChatGPT backend (since the original CLI currently exposes
`chatgpt` as the nearest GPT-5 family proxy). This lets all clients advertise GPT-5.1 while the
underlying flow stays stable.

## Usage Tips

1. Run **Nexus AI: Start Assistant** once per workspace session.
2. Use **Nexus AI: Open Assistant Panel** to keep track of what the assistant outputs and
   to submit further prompts without juggling the terminal.
3. Drop `/autosave` or `/tasks` into the quick command palette to cover productivity flows.
4. If you need a custom Python interpreter, point `nexusAiAssistant.pythonPath` at your
   virtual environment’s `python.exe`.

---

> ℹ️ The extension assumes the workspace root contains the `terminal/main.py` entry point.
> Make sure the CLI dependencies from the repository are installed (`pip install -e .`).

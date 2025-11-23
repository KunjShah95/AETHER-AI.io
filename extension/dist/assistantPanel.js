"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.AssistantPanel = void 0;
const vscode = __importStar(require("vscode"));
class AssistantPanel {
    constructor(panel, extensionUri, quickCommands, initialLog, initialStatus, sendCommand) {
        this.panel = panel;
        this.extensionUri = extensionUri;
        this.quickCommands = quickCommands;
        this.sendCommand = sendCommand;
        panel.onDidDispose(() => this.dispose(), null, []);
        panel.webview.onDidReceiveMessage((message) => {
            if (message?.type === 'sendCommand' && typeof message.command === 'string') {
                this.sendCommand(message.command.trim());
            }
        });
        panel.webview.html = this.getHtml(panel.webview);
        this.postStatus(initialStatus);
        this.postLog(initialLog);
        this.postInit();
    }
    static createOrShow(extensionUri, quickCommands, initialLog, initialStatus, sendCommand) {
        if (AssistantPanel.currentPanel) {
            AssistantPanel.currentPanel.panel.reveal(vscode.ViewColumn.One);
            AssistantPanel.currentPanel.postLog(initialLog);
            AssistantPanel.currentPanel.postStatus(initialStatus);
            return;
        }
        const panel = vscode.window.createWebviewPanel('nexusAiAssistant', 'Nexus AI Terminal Assistant', vscode.ViewColumn.One, {
            enableScripts: true,
            retainContextWhenHidden: true
        });
        AssistantPanel.currentPanel = new AssistantPanel(panel, extensionUri, quickCommands, initialLog, initialStatus, sendCommand);
    }
    dispose() {
        AssistantPanel.currentPanel = undefined;
        this.panel.dispose();
    }
    postLog(entries) {
        this.panel.webview.postMessage({ type: 'log', entries });
    }
    postStatus(status) {
        this.panel.webview.postMessage({ type: 'status', status });
    }
    postInit() {
        this.panel.webview.postMessage({
            type: 'init',
            quickCommands: this.quickCommands
        });
    }
    getHtml(webview) {
        const nonce = getNonce();
        const styleUri = webview.asWebviewUri(vscode.Uri.joinPath(this.extensionUri, 'media', 'assistant.css'));
        return `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src ${webview.cspSource} https:; script-src 'nonce-${nonce}'; style-src ${webview.cspSource};" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Nexus AI Assistant</title>
    <link rel="stylesheet" href="${styleUri}" />
  </head>
  <body>
    <header>
      <h1>Nexus AI Terminal Assistant</h1>
      <p id="assistant-status">Detecting status…</p>
    </header>
    <section class="command-form">
      <label for="command-input">Send a command:</label>
      <div class="input-row">
        <input id="command-input" placeholder="/help" />
        <button id="send-command" type="button">Send</button>
      </div>
    </section>
    <section>
      <h2>Quick commands</h2>
      <div id="quick-commands" class="quick-grid"></div>
    </section>
    <section>
      <h2>Live log</h2>
      <div id="log" class="log-panel"></div>
    </section>
    <script nonce="${nonce}">
      const vscode = acquireVsCodeApi();
      const logContainer = document.getElementById('log');
      const statusEl = document.getElementById('assistant-status');
      const quickCommandsContainer = document.getElementById('quick-commands');
      const inputEl = document.getElementById('command-input');
      const sendButton = document.getElementById('send-command');

      const renderLog = (entries) => {
        if (!logContainer) return;
        logContainer.innerHTML = '';
        entries.slice(-150).forEach((entry) => {
          const row = document.createElement('div');
          row.textContent = entry;
          logContainer.appendChild(row);
        });
        logContainer.scrollTop = logContainer.scrollHeight;
      };

      const renderStatus = (status) => {
        if (statusEl) {
          statusEl.textContent = status;
        }
      };

      const renderQuickCommands = (commands) => {
        if (!quickCommandsContainer) return;
        quickCommandsContainer.innerHTML = '';
        (commands || []).forEach((command) => {
          const button = document.createElement('button');
          button.className = 'quick-pill';
          button.textContent = command.label;
          button.title = command.description;
          button.addEventListener('click', () => {
            vscode.postMessage({ type: 'sendCommand', command: command.command });
          });
          quickCommandsContainer.appendChild(button);
        });
      };

      sendButton?.addEventListener('click', () => {
        const text = inputEl.value.trim();
        if (text) {
          vscode.postMessage({ type: 'sendCommand', command: text });
          inputEl.value = '';
        }
      });

      inputEl.addEventListener('keyup', (event) => {
        if (event.key === 'Enter') {
          sendButton.click();
        }
      });

      window.addEventListener('message', (event) => {
        const message = event.data;
        switch (message.type) {
          case 'log':
            renderLog(message.entries || []);
            break;
          case 'status':
            renderStatus(message.status || 'Unknown');
            break;
          case 'init':
            renderQuickCommands(message.quickCommands || []);
            break;
        }
      });
    </script>
  </body>
</html>`;
    }
}
exports.AssistantPanel = AssistantPanel;
function getNonce() {
    let text = '';
    const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    for (let i = 0; i < 32; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}
//# sourceMappingURL=assistantPanel.js.map
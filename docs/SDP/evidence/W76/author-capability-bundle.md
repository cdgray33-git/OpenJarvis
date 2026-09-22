# AUTHOR CAPABILITY BUNDLE - W76 2026-09-22
Source: upstream-OpenJarvis (read-only). For Claude to read whole. Order = priority.
Files: 11  total bytes: 210250

| Path | Bytes | sha16 | Last commit |
|---|---|---|---|
| docs\user-guide\channels-and-connectors.md | 22218 | 619d390f5076ea78 | 2026-08-14 |
| docs\user-guide\tools.md | 25353 | 16c83e426674a5f1 | 2026-09-04 |
| docs\user-guide\system-access.md | 6998 | 412534c98c62adb5 | 2026-07-28 |
| docs\user-guide\security.md | 20146 | 661570ac4fcf871d | 2026-09-04 |
| docs\deployment\api-server.md | 17494 | 5b8a3fcbe3f7bf28 | 2026-08-20 |
| docs\user-guide\memory.md | 13653 | 081bfdb7afaba4ed | 2026-03-12 |
| docs\user-guide\agents.md | 44922 | 48e11037c3e50ae8 | 2026-09-04 |
| docs\user-guide\morning-digest.md | 7665 | 63f0c2c1eea32593 | 2026-04-03 |
| docs\user-guide\scheduler.md | 8927 | 21b215b87898d05c | 2026-03-12 |
| docs\user-guide\cli.md | 19683 | 64572c26a2b936b2 | 2026-09-21 |
| docs\user-guide\channels.md | 23191 | e99b2f414438cc03 | 2026-03-27 |

===== FILE: docs\user-guide\channels-and-connectors.md | 22218 bytes | sha16 619d390f5076ea78 | last commit 2026-08-14 =====

# Channels & Connectors

OpenJarvis has two types of integrations:

- **Data connectors** — read-only access to your personal data (Gmail, iMessage, Google Drive, etc.) so your agent can search and research across them
- **Messaging channels** — ways to talk TO your agent from your phone or other platforms (iMessage/SMS, Slack)

---

# Messaging Channels

## iMessage & SMS (via SendBlue)

**What it does:** Gives your agent a phone number. Text it from any phone (iPhone via iMessage, Android via SMS) and the agent responds.

### Setup

1. **Create a SendBlue account:** [sendblue.com](https://www.sendblue.com/) — free tier available
2. **Get your API credentials:** Dashboard → API Keys → copy **API Key ID** and **API Secret Key**
3. **Note your SendBlue phone number** — this is the number people text to reach your agent
4. **Connect in OpenJarvis:**
   - Desktop/Browser: Agents → your agent → **Messaging** tab → iMessage/SMS → enter API Key ID, API Secret Key, and phone number
   - The agent will send an "ack" message and a test to verify it works
5. **Set up the webhook** so incoming texts reach your agent:
   - You need a public URL — use [ngrok](https://ngrok.com/) to tunnel to your local server: `ngrok http 9001`
   - Register the webhook URL with SendBlue:
   ```bash
   curl -X PUT https://api.sendblue.co/api/account/webhooks \
     -H "sb-api-key-id: YOUR_KEY" \
     -H "sb-api-secret-key: YOUR_SECRET" \
     -H "Content-Type: application/json" \
     -d '{"webhooks": {"receive": ["https://YOUR-NGROK-URL.ngrok-free.dev/webhooks/sendblue"]}}'
   ```

### How it works

- Someone texts your SendBlue number → SendBlue sends a webhook to your server
- Agent replies "Message received! Working on it now..." instantly
- Agent researches your data (15-60s) → sends the response as iMessage or SMS
- iMessage (blue bubbles) for Apple devices, SMS (green) for Android — automatic

### Troubleshooting

| Issue | Solution |
|-------|----------|
| No response after texting | Check ngrok is running and webhook URL is registered |
| "Disconnected" in Messaging tab | Click Reconnect — server may have restarted |
| ngrok URL changed | Re-register the webhook URL with SendBlue (see step 5) |
| Messages only work one-way | Free tier requires contacts to text the number first |

---

## Slack

**What it does:** DM your agent in Slack and get research responses in the thread.

### Setup

The fastest way is to use the App Manifest — paste this JSON to configure everything at once:

1. Go to [api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → **From an app manifest**
2. Select your workspace, then paste this manifest:

```json
{
    "display_information": { "name": "OpenJarvis" },
    "features": {
        "app_home": {
            "home_tab_enabled": true,
            "messages_tab_enabled": true,
            "messages_tab_read_only_enabled": false
        },
        "bot_user": { "display_name": "OpenJarvis", "always_online": true }
    },
    "oauth_config": {
        "scopes": {
            "bot": [
                "chat:write", "im:write", "im:read", "im:history",
                "users:read", "channels:read", "channels:history",
                "app_mentions:read"
            ]
        }
    },
    "settings": {
        "event_subscriptions": { "bot_events": ["message.im"] },
        "socket_mode_enabled": true
    }
}
```

3. Click **Create** → **Install to Workspace** → **Allow**
4. Copy the **Bot User OAuth Token** (`xoxb-...`) from **OAuth & Permissions**
5. Go to **Basic Information** → **App-Level Tokens** → **Generate Token** → add `connections:write` scope → copy the token (`xapp-...`)
6. **Connect in OpenJarvis:**
   - Desktop/Browser: Agents → your agent → **Messaging** tab → Slack → paste both tokens
   - CLI: tokens are stored when you bind the channel

### How it works

- You DM @OpenJarvis in Slack → Socket Mode receives the event in real-time
- Agent replies "Message received! Working on it now..." in a **thread** under your message
- Agent researches (15-60s) → response appears in the same thread
- If processing takes >60s: "Still working! Will reply ASAP" in the thread
- All responses use Slack formatting (*bold*, _italic_, `code`, lists)

### Important Notes

- **Reinstall after changes:** Every time you add scopes or events, reinstall the app
- **App Token vs Bot Token:** Bot Token (`xoxb-`) for API calls, App Token (`xapp-`) for Socket Mode. You need both.
- **Don't use Event Subscriptions UI for Request URL:** With Socket Mode, you don't need one. Use the App Manifest method above.

### Troubleshooting

| Issue | Solution |
|-------|----------|
| "Sending messages to this app has been turned off" | App Home → enable Messages Tab → "Allow users to send messages" |
| Bot doesn't respond | Check Socket Mode is enabled + `message.im` event is subscribed + app was reinstalled |
| "missing_scope" error | Add the scope → reinstall the app |
| Bot not visible in Slack | Click "+" next to Direct Messages → search "OpenJarvis" |
| Event Subscriptions won't save | Use the App Manifest method (avoids Request URL requirement) |

---

# Data Connectors

## Gmail

**What it indexes:** Email messages and threads from your Gmail inbox.

### Setup (App Password — recommended)

1. **Enable 2-Factor Authentication** on your Google account:
   [Open Google Security Settings →](https://myaccount.google.com/signinoptions/two-step-verification)

2. **Generate an App Password** for "Mail":
   [Open App Passwords →](https://myaccount.google.com/apppasswords)
   - Select "Mail" as the app
   - Copy the 16-character password (e.g. `qpde kebj evhy zljc`)

3. **Connect in OpenJarvis:**
   - Desktop/Browser: Agents → your agent → Channels tab → Gmail → Reconnect
   - CLI: `uv run jarvis connect gmail_imap`
   - Enter your email address and the app password

### Troubleshooting

| Issue | Solution |
|-------|----------|
| "App Passwords" page not available | Enable 2-Factor Authentication first |
| Login failed | Make sure you're using the app password, not your regular Google password |
| No emails syncing | Check that IMAP is enabled: [Gmail Settings → Forwarding and POP/IMAP](https://mail.google.com/mail/u/0/#settings/fwdandpop) |
| Only getting recent emails | By default, the last 500 emails are synced. Increase with `max_messages` config |

---

## Google Drive

**What it indexes:** Documents, Sheets, PDFs, and other files from your Drive.

### Setup

1. **Go to Google Cloud Console** and create a project (or use an existing one):
   [Create Project →](https://console.cloud.google.com/projectcreate)

2. **Enable the Google Drive API:**
   [Enable Drive API →](https://console.cloud.google.com/apis/library/drive.googleapis.com)

3. **Create OAuth credentials:**
   [Open Credentials →](https://console.cloud.google.com/apis/credentials)
   - Click "Create Credentials" → "OAuth 2.0 Client ID"
   - Choose "Desktop app" as the application type
   - Copy the **Client ID** and **Client Secret**

4. **Add yourself as a test user** (required while app is unverified):
   [Open OAuth Consent Screen →](https://console.cloud.google.com/apis/credentials/consent)
   - Scroll to "Test users" → click "+ Add Users"
   - Add your Gmail address (e.g. `jonsaadfalcon@gmail.com`)

5. **Add the redirect URI:**
   [Open Credentials →](https://console.cloud.google.com/apis/credentials)
   - Click your OAuth Client → Authorized redirect URIs
   - Add: `http://localhost:8789/callback`

6. **Connect in OpenJarvis:**
   - Desktop/Browser: Agents → Channels tab → Google Drive → paste Client ID and Client Secret
   - Your browser will open Google's consent page → grant read-only access
   - You'll see "Authorization successful!" → Drive data starts syncing

### Troubleshooting

| Issue | Solution |
|-------|----------|
| "Access blocked: app has not completed verification" | Add your email as a test user (step 4 above) |
| "Error 400: redirect_uri_mismatch" | Add `http://localhost:8789/callback` as an authorized redirect URI (step 5) |
| "Error 403: access_denied" | Make sure you selected "Desktop app" when creating the OAuth client |
| Connected but 0 files | Check that you granted Drive read access in the consent screen. Try reconnecting. |
| Token expired | Access tokens expire after 1 hour. Reconnect to get a new one. (Auto-refresh coming soon.) |

---

## Google Calendar

**What it indexes:** Events, meetings, and calendar entries.

### Setup

Same as Google Drive — use the same Google Cloud project and OAuth client.

1. **Enable the Google Calendar API:**
   [Enable Calendar API →](https://console.cloud.google.com/apis/library/calendar-json.googleapis.com)

2. Follow steps 3-6 from the Google Drive section above (same Client ID/Secret works)

### Troubleshooting

Same as Google Drive. Additionally:

| Issue | Solution |
|-------|----------|
| Only seeing primary calendar | The connector reads all calendars you have access to |
| Missing shared calendars | Shared calendars from other users may require additional permissions |

---

## Google Contacts

**What it indexes:** People, phone numbers, emails, and contact information.

### Setup

Same as Google Drive — use the same Google Cloud project and OAuth client.

1. **Enable the People API:**
   [Enable People API →](https://console.cloud.google.com/apis/library/people.googleapis.com)

2. Follow steps 3-6 from the Google Drive section above

---

## Slack

Slack serves two purposes in OpenJarvis:

- **Data source** — indexes channel messages, DMs, and threads so your agent can search them
- **Messaging channel** — lets you DM your agent directly in Slack

We recommend creating **one Slack app** that handles both. The App Manifest below includes all scopes needed.

### Quick Setup (App Manifest — recommended)

1. **Go to [Slack App Settings →](https://api.slack.com/apps)**

2. **Create New App → "From an app manifest"** → select your workspace

3. **Paste this JSON manifest** (includes all scopes for data source + messaging):

   ```json
   {
       "display_information": { "name": "OpenJarvis" },
       "features": {
           "app_home": {
               "home_tab_enabled": true,
               "messages_tab_enabled": true,
               "messages_tab_read_only_enabled": false
           },
           "bot_user": { "display_name": "OpenJarvis", "always_online": true }
       },
       "oauth_config": {
           "scopes": {
               "bot": [
                   "channels:read", "channels:history", "channels:join",
                   "groups:read", "groups:history",
                   "im:read", "im:write", "im:history",
                   "mpim:read", "mpim:history",
                   "chat:write",
                   "users:read",
                   "app_mentions:read"
               ]
           }
       },
       "settings": {
           "event_subscriptions": { "bot_events": ["message.im"] },
           "socket_mode_enabled": true
       }
   }
   ```

4. **Review and click Create**

5. **Install the app:** Install App → Install to Workspace → Authorize

6. **Copy the Bot Token:** Go to OAuth & Permissions → copy the **Bot User OAuth Token** (`xoxb-...`)

7. **Create an App-Level Token (for DMs):**
   - Go to Basic Information → App-Level Tokens → Generate Token
   - Name it "socket" → add the `connections:write` scope → Generate
   - Copy the token (`xapp-...`)

8. **(Optional) Set the app icon:**
   - Go to Basic Information → Display Information
   - Upload the [OpenJarvis icon](https://github.com/open-jarvis/OpenJarvis/blob/main/assets/openjarvis-slack-icon.jpg)

### Required Bot Token Scopes (reference)

| Scope | Purpose |
|-------|---------|
| `channels:read` | List public channels |
| `channels:history` | Read public channel messages |
| `channels:join` | Auto-join public channels for indexing |
| `groups:read` | List private channels |
| `groups:history` | Read private channel messages |
| `im:read` | List DM conversations |
| `im:write` | Open DM conversations |
| `im:history` | Read DM history + receive DM events |
| `mpim:read` | List group DMs |
| `mpim:history` | Read group DM messages |
| `chat:write` | Send messages and responses |
| `users:read` | Look up user info |
| `app_mentions:read` | See @mentions of the bot |

**App-Level Token scope:** `connections:write` (required for Socket Mode / DMs)

### Connecting in OpenJarvis

**As a data source** (read channel messages):
- Desktop/Browser: Data Sources → Slack → paste the bot token (`xoxb-...`)
- CLI: `uv run jarvis connect slack`

**As a messaging channel** (DM your agent):
- Desktop/Browser: Data Sources → Messaging Channels → Slack → Set Up
- Enter both the **Bot Token** (`xoxb-...`) and **App Token** (`xapp-...`)
- Or: Agents → select agent → Messaging Channels → Slack → Set Up

**DM your agent:**
- In Slack, find **OpenJarvis** under Apps (or Direct Messages)
- If you don't see it: click "+" next to Direct Messages → search "OpenJarvis"
- Send a message → the agent responds in a thread

### Important Notes

- **Reinstall after scope changes:** Every time you add new scopes or change event subscriptions, you MUST reinstall the app.
- **App-Level Token vs Bot Token:** The Bot Token (`xoxb-`) is for API calls. The App Token (`xapp-`) is for Socket Mode. You need both for DMs to work.
- **Channel visibility:** The bot can only read channels it's been added to. Invite it with `/invite @OpenJarvis` in each channel you want indexed.
- **Thread replies:** If you reply in a thread, the bot sees it. New top-level messages also work.

### Troubleshooting

| Issue | Solution |
|-------|----------|
| "not_allowed_token_type" | Use the **Bot** token (`xoxb-...`), not a user token (`xoxp-`) or session token (`xoxe-`) |
| "Sending messages to this app has been turned off" | Go to App Home → enable "Messages Tab" → check "Allow users to send messages from the messages tab" |
| Bot doesn't respond to DMs | Make sure Socket Mode is enabled, `message.im` event is subscribed, and the app was reinstalled after changes |
| "missing_scope" error | Add the missing scope in OAuth & Permissions → Reinstall the app |
| Bot not visible in Slack | Go to Install App → Reinstall to Workspace |
| No messages found (data source) | The bot can only see channels it's been added to. Invite it: `/invite @OpenJarvis` in the channel |
| Socket Mode connects but no events received | Verify `message.im` is in the manifest's `bot_events`, reinstall the app |

---

## Notion

**What it indexes:** Pages, databases, and their content.

### Setup

1. **Create an internal integration:**
   [Open Notion Integrations →](https://www.notion.so/profile/integrations)
   - Click "New integration"
   - Name it (e.g. "OpenJarvis")
   - Select your workspace
   - Copy the **Internal Integration Secret** (starts with `ntn_`)

2. **Share pages with your integration:**
   - Open any Notion page you want indexed
   - Click "..." (top right) → "Connections" → find your integration → click it
   - Repeat for each page or database

3. **Connect in OpenJarvis:**
   - Desktop/Browser: Agents → Channels tab → Notion → paste the token
   - CLI: `uv run jarvis connect notion`

### Troubleshooting

| Issue | Solution |
|-------|----------|
| 0 pages found | You must explicitly share pages with the integration (step 2). The integration can only see pages you've connected. |
| Missing database content | Share the database page itself, not just individual entries |
| Token expired | Notion integration tokens don't expire. If it stops working, regenerate at the integrations page. |

---

## Granola

**What it indexes:** AI meeting notes and transcripts from the Granola app.

### Setup

1. **Open the Granola desktop app** → Settings → API
2. **Copy your API key** (starts with `grn_`)
3. **Connect in OpenJarvis:**
   - Desktop/Browser: Agents → Channels tab → Granola → paste the key
   - CLI: `uv run jarvis connect granola`

### Troubleshooting

| Issue | Solution |
|-------|----------|
| No API key in settings | Granola API is available on Business and Enterprise plans |
| 0 meeting notes | Check that you have meetings recorded in Granola |

---

## Apple Notes

**What it indexes:** Notes from the macOS Notes app.

### Setup (automatic)

1. **Grant Full Disk Access** to your terminal app:
   - Open System Settings → Privacy & Security → Full Disk Access
   - Enable access for Terminal, iTerm, Warp, or the OpenJarvis desktop app

2. Apple Notes is detected automatically when Full Disk Access is granted

OpenJarvis searches an indexed snapshot rather than querying Notes.app live.
After creating notes, open **Data Sources** and click **Re-sync** on Apple Notes
before searching for the new content.

### Troubleshooting

| Issue | Solution |
|-------|----------|
| "Not connected" despite Full Disk Access | Restart your terminal app after granting access |
| Notes content is garbled | Some very old notes may have encoding issues. Most notes should be clean. |
| New notes are missing | In **Data Sources**, click **Re-sync** on Apple Notes to refresh the index. |
| Missing notes | Only notes stored locally or in iCloud are indexed. Notes in third-party accounts (Gmail, Exchange) may not appear. |

---

## iMessage

**What it indexes:** Text messages from the macOS Messages app.

### Setup (automatic)

Same as Apple Notes — requires Full Disk Access.

### Troubleshooting

| Issue | Solution |
|-------|----------|
| "Not connected" | Grant Full Disk Access (see Apple Notes above) |
| Very slow sync | iMessage databases can be large (50K+ messages). First sync may take 10-30 seconds. |
| Missing recent messages | Messages sync from the local database. If Messages.app hasn't synced from iCloud yet, recent messages may be missing. |

---

## Outlook / Microsoft 365

**What it indexes:** Email messages via IMAP.

### Setup

1. **Enable 2-Factor Authentication** on your Microsoft account:
   [Open Microsoft Security →](https://account.microsoft.com/security)

2. **Generate an App Password:**
   - Go to Security → Advanced security options → App passwords
   - Create a new app password

3. **Connect in OpenJarvis:**
   - Desktop/Browser: Agents → Channels tab → Outlook → enter email + app password
   - CLI: `uv run jarvis connect outlook`

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Login failed | Use the app password, not your regular Microsoft password |
| "Authentication failed" | Some Microsoft 365 organizations disable IMAP. Check with your IT admin. |
| Only getting Inbox | Currently only the Inbox folder is synced |

---

## Obsidian

**What it indexes:** Markdown files from your Obsidian vault.

### Setup

1. Find your Obsidian vault folder (the folder containing the `.obsidian` directory)
2. **Connect in OpenJarvis:**
   - Desktop/Browser: Agents → Channels tab → Obsidian → paste the vault path
   - CLI: `uv run jarvis connect obsidian --path /path/to/vault`

### Troubleshooting

| Issue | Solution |
|-------|----------|
| "Not connected" | Double-check the path exists and contains a `.obsidian` folder |
| Missing files | Only `.md`, `.markdown`, and `.txt` files are indexed. Binary files and images are skipped. |
| Slow sync for large vaults | Vaults with 1000+ files may take a minute to sync |

---

## Dropbox

**What it indexes:** Files and documents from your Dropbox.

### Setup

1. **Create a Dropbox app:**
   [Open Dropbox App Console →](https://www.dropbox.com/developers/apps/create)
   - Choose "Scoped access" → "Full Dropbox"

2. **Set permissions:**
   - Under Permissions tab, enable `files.metadata.read` and `files.content.read`

3. **Generate an access token:**
   - Go to Settings tab → "Generated access token" → Generate

4. **Connect in OpenJarvis:**
   - Desktop/Browser: Agents → Channels tab → Dropbox → paste the token
   - CLI: `uv run jarvis connect dropbox`

### Troubleshooting

| Issue | Solution |
|-------|----------|
| "Invalid access token" | Dropbox short-lived tokens expire after 4 hours. Generate a new one. |
| Missing files | Check that you enabled the correct permissions (step 2) |

---

## General Troubleshooting

### All connectors

| Issue | Solution |
|-------|----------|
| "Connected — no data synced yet" | The connector authenticated but hasn't synced. Try running `uv run jarvis deep-research-setup --skip-chat` to trigger a sync. |
| Data seems stale | Connectors sync on demand. Run the setup command or click "Reconnect" to re-sync. |
| Want to reset a connector | Click "Reconnect" in the Channels tab, or delete the credential file at `~/.openjarvis/connectors/{connector}.json` |

### Where credentials are stored

All credentials are saved locally at `~/.openjarvis/connectors/` with file permissions `0600` (owner-only read/write). No credentials are sent to any server — everything stays on your device.

```
~/.openjarvis/connectors/
├── gmail_imap.json    # Gmail email + app password
├── gdrive.json        # Google Drive OAuth tokens
├── gcalendar.json     # Google Calendar OAuth tokens
├── gcontacts.json     # Google Contacts OAuth tokens
├── slack.json         # Slack bot token
├── notion.json        # Notion integration token
├── granola.json       # Granola API key
├── outlook.json       # Outlook email + app password
└── dropbox.json       # Dropbox access token
```

===== END FILE: docs\user-guide\channels-and-connectors.md =====

===== FILE: docs\user-guide\tools.md | 25353 bytes | sha16 16c83e426674a5f1 | last commit 2026-09-04 =====

# Tools

The tool system enables agents to perform actions beyond text generation -- calculations, memory lookups, file reading, and sub-model calls. Tools follow a spec-driven design with a central dispatch engine and OpenAI function-calling format support.

## Architecture

```
Agent  -->  Engine (with tool defs)  -->  tool_calls response  -->  ToolExecutor  -->  Tool.execute()
  ^                                                                                          |
  |                                                                                          v
  +-------------------------------  ToolResult  <--------------------------------------------+
```

---

## BaseTool ABC

All tools implement the `BaseTool` abstract base class.

```python
from abc import ABC, abstractmethod
from openjarvis.tools._stubs import ToolSpec
from openjarvis.core.types import ToolResult

class BaseTool(ABC):
    tool_id: str

    @property
    @abstractmethod
    def spec(self) -> ToolSpec:
        """Return the tool specification."""

    @abstractmethod
    def execute(self, **params) -> ToolResult:
        """Execute the tool with the given parameters."""

    def to_openai_function(self) -> dict:
        """Convert to OpenAI function-calling format."""
```

The `to_openai_function()` method is provided by the base class and converts the tool's spec into the format expected by OpenAI-compatible APIs:

```json
{
  "type": "function",
  "function": {
    "name": "calculator",
    "description": "Evaluate a mathematical expression safely.",
    "parameters": {
      "type": "object",
      "properties": {
        "expression": {
          "type": "string",
          "description": "Math expression to evaluate"
        }
      },
      "required": ["expression"]
    }
  }
}
```

---

## ToolSpec

The `ToolSpec` dataclass describes a tool's interface and characteristics.

| Field                  | Type             | Default | Description                                        |
|------------------------|------------------|---------|----------------------------------------------------|
| `name`                 | `str`            | --      | Unique tool identifier                             |
| `description`          | `str`            | --      | Human-readable description (sent to the model)     |
| `parameters`           | `dict[str, Any]` | `{}`    | JSON Schema for the tool's parameters              |
| `category`             | `str`            | `""`    | Tool category (e.g., `math`, `memory`, `reasoning`) |
| `cost_estimate`        | `float`          | `0.0`   | Estimated cost per invocation                      |
| `latency_estimate`     | `float`          | `0.0`   | Estimated latency per invocation                   |
| `requires_confirmation`| `bool`           | `False` | Whether the tool requires user confirmation        |
| `metadata`             | `dict[str, Any]` | `{}`    | Additional metadata                                |

---

## ToolResult

The `ToolResult` dataclass holds the result of a tool execution.

| Field             | Type             | Default | Description                              |
|-------------------|------------------|---------|------------------------------------------|
| `tool_name`       | `str`            | --      | Name of the tool that was called         |
| `content`         | `str`            | --      | The tool's output (text)                 |
| `success`         | `bool`           | `True`  | Whether the execution succeeded          |
| `usage`           | `dict[str, Any]` | `{}`    | Token usage (for LLM tool)               |
| `cost_usd`        | `float`          | `0.0`   | Actual cost of the invocation            |
| `latency_seconds` | `float`          | `0.0`   | Measured execution latency               |
| `metadata`        | `dict[str, Any]` | `{}`    | Additional metadata                      |

---

## ToolExecutor

The `ToolExecutor` is the central dispatch engine for tool calls. It manages a set of tool instances, parses JSON arguments, measures execution latency, and publishes events on the event bus.

```python
from openjarvis.tools._stubs import ToolExecutor

executor = ToolExecutor(tools=[calculator, think_tool], bus=event_bus)

# Get OpenAI-format tool definitions
openai_tools = executor.get_openai_tools()

# Execute a tool call
from openjarvis.core.types import ToolCall
tc = ToolCall(id="call_1", name="calculator", arguments='{"expression": "2+2"}')
result = executor.execute(tc)
print(result.content)  # "4"
```

### Execution Flow

1. **Parse arguments:** The `arguments` JSON string from the `ToolCall` is deserialized.
2. **Publish start event:** `TOOL_CALL_START` is emitted on the event bus with tool name and arguments.
3. **Execute:** The tool's `execute()` method is called with the parsed parameters.
4. **Measure latency:** Execution time is recorded in `result.latency_seconds`.
5. **Publish end event:** `TOOL_CALL_END` is emitted with success status and latency.
6. **Return result:** The `ToolResult` is returned to the caller.

If the tool name is unknown, a `ToolResult` with `success=False` is returned. If JSON parsing fails or the tool raises an exception, the error is captured and returned as a failed `ToolResult`.

### Methods

| Method              | Returns                | Description                                |
|---------------------|------------------------|--------------------------------------------|
| `execute(tool_call)`| `ToolResult`           | Parse args, dispatch, measure, emit events |
| `available_tools()` | `list[ToolSpec]`       | Return specs for all registered tools      |
| `get_openai_tools()`| `list[dict]`           | Return tools in OpenAI function format     |

---

## build_tool_descriptions()

The `build_tool_descriptions()` function is the **single source of truth** for generating enriched tool descriptions used in agent system prompts. All text-based agents (`NativeReActAgent`, `NativeOpenHandsAgent`, `RLMAgent`, `OrchestratorAgent` in structured mode) use this function to produce Markdown-formatted tool sections.

### Parameters

| Parameter          | Type             | Default | Description                                          |
|--------------------|------------------|---------|------------------------------------------------------|
| `tools`            | `list[BaseTool]` | --      | List of tool instances to describe                   |
| `include_category` | `bool`           | `True`  | Whether to include the `Category:` line              |
| `include_cost`     | `bool`           | `False` | Whether to include cost and latency estimate lines   |

### Usage

```python
from openjarvis.tools._stubs import build_tool_descriptions
from openjarvis.tools.calculator import CalculatorTool
from openjarvis.tools.think import ThinkTool

tools = [CalculatorTool(), ThinkTool()]
desc = build_tool_descriptions(tools)
print(desc)
# ### calculator
# Evaluate a mathematical expression safely.
# Category: math
# Parameters:
#   - expression (string, required): Math expression to evaluate
#
# ### think
# Reasoning scratchpad ...
```

### Agents using this builder

- **NativeReActAgent** -- Injects descriptions into the ReAct system prompt
- **NativeOpenHandsAgent** -- Injects descriptions into the CodeAct system prompt
- **RLMAgent** -- Adds an `## Available Tools` section to the REPL system prompt
- **OrchestratorAgent** (structured mode) -- Passes `tools=` to `build_system_prompt()` which delegates to this builder

---

## Built-in Tools Summary

All built-in tools are registered via `@ToolRegistry.register()` and are available by name to agents and the CLI.

| Category | Registry Key | Description |
|----------|-------------|-------------|
| **Reasoning** | `think` | Zero-cost reasoning scratchpad for chain-of-thought |
| **Math** | `calculator` | Safe math expression evaluator (ast-based) |
| **Code** | `code_interpreter` | Execute Python code in a sandboxed subprocess |
| **Code** | `code_interpreter_docker` | Execute Python code in a disposable Docker container |
| **Code** | `repl` | Persistent Python REPL with state across calls |
| **Search** | `web_search` | Web search returning result summaries |
| **Weather** | `get_weather` | Dynamic current conditions and forecast via OpenWeatherMap |
| **File I/O** | `file_read` | Read file contents with safety validations |
| **HTTP** | `http_request` | Make HTTP requests with SSRF protection |
| **Memory** | `retrieval` | Search the memory backend for relevant context |
| **Memory** | `memory_store` | Store content in the memory backend |
| **Memory** | `memory_retrieve` | Retrieve relevant content from the memory backend |
| **Memory** | `memory_search` | Full-text search across stored memory |
| **Memory** | `memory_index` | Index a file or directory into the memory backend |
| **Inference** | `llm` | Delegate a sub-query to an inference engine |
| **Channel** | `channel_send` | Send a message via a channel (Telegram, Discord, etc.) |
| **Channel** | `channel_list` | List available messaging channels |
| **Channel** | `channel_status` | Check the connection status of a messaging channel |
| **Scheduler** | `schedule_task` | Schedule a task for future or recurring execution |
| **Scheduler** | `list_scheduled_tasks` | List all scheduled tasks |
| **Scheduler** | `pause_scheduled_task` | Pause an active scheduled task |
| **Scheduler** | `resume_scheduled_task` | Resume a paused scheduled task |
| **Scheduler** | `cancel_scheduled_task` | Cancel a scheduled task permanently |
| **Integration** | `mcp_adapter` | Bridge to external MCP tool servers (see [External MCP Servers](mcp-external-servers.md)) |

---

## Built-in Tool Details

### Calculator

**Registry key:** `calculator` | **Category:** `math`

Evaluates mathematical expressions safely using Python's `ast` module. No arbitrary code execution -- only whitelisted operations are allowed.

**Parameters:**

| Parameter    | Type   | Required | Description                              |
|--------------|--------|----------|------------------------------------------|
| `expression` | string | Yes      | Math expression (e.g., `"2+3*4"`, `"sqrt(16)"`) |

**Supported operations:**

| Category     | Operations                                                    |
|--------------|---------------------------------------------------------------|
| Arithmetic   | `+`, `-`, `*`, `/`, `//` (floor div), `%` (mod), `**` (power) |
| Functions    | `abs`, `round`, `min`, `max`, `sqrt`, `log`, `log10`, `log2` |
| Trigonometry | `sin`, `cos`, `tan`                                           |
| Rounding     | `ceil`, `floor`                                               |
| Constants    | `pi`, `e`                                                     |

**Example:**

```python
from openjarvis.tools.calculator import CalculatorTool

calc = CalculatorTool()
result = calc.execute(expression="sqrt(144) + 3**2")
print(result.content)   # "21.0"
print(result.success)   # True
```

### Think

**Registry key:** `think` | **Category:** `reasoning`

A zero-cost reasoning scratchpad. The input is echoed back as the output, allowing the model to "think out loud" during a tool-calling loop. This enables chain-of-thought reasoning within the agent workflow.

**Parameters:**

| Parameter | Type   | Required | Description                              |
|-----------|--------|----------|------------------------------------------|
| `thought` | string | Yes      | The reasoning or thought process         |

**Example:**

```python
from openjarvis.tools.think import ThinkTool

think = ThinkTool()
result = think.execute(thought="Let me break this problem into steps...")
print(result.content)   # "Let me break this problem into steps..."
print(result.success)   # True
```

!!! info "Cost and Latency"
    The Think tool has zero cost and near-zero latency, making it ideal for structured reasoning without consuming additional resources.

### Retrieval

**Registry key:** `retrieval` | **Category:** `memory`

Searches the memory backend for relevant context and returns formatted results with source attribution.

**Parameters:**

| Parameter | Type    | Required | Description                              |
|-----------|---------|----------|------------------------------------------|
| `query`   | string  | Yes      | Search query                             |
| `top_k`   | integer | No       | Number of results (default: 5)           |

**Constructor parameters:**

| Parameter | Type            | Default | Description                    |
|-----------|-----------------|---------|--------------------------------|
| `backend` | `MemoryBackend` | `None`  | Memory backend to search       |
| `top_k`   | `int`           | `5`     | Default number of results      |

**Example:**

```python
from openjarvis.tools.retrieval import RetrievalTool
from openjarvis.memory.sqlite import SQLiteMemory

backend = SQLiteMemory(db_path="./memory.db")
retrieval = RetrievalTool(backend=backend)
result = retrieval.execute(query="machine learning")
print(result.content)   # Formatted context with source tags
```

### LLM

**Registry key:** `llm` | **Category:** `inference`

Delegates a sub-query to an inference engine. Useful for summarization, sub-questions, or generating structured output within an agent workflow.

**Parameters:**

| Parameter | Type   | Required | Description                              |
|-----------|--------|----------|------------------------------------------|
| `prompt`  | string | Yes      | The prompt to send to the model          |
| `system`  | string | No       | Optional system message for context      |

**Constructor parameters:**

| Parameter | Type              | Default | Description                    |
|-----------|-------------------|---------|--------------------------------|
| `engine`  | `InferenceEngine` | `None`  | Inference engine to use        |
| `model`   | `str`             | `""`    | Model identifier               |

**Example:**

```python
from openjarvis.tools.llm_tool import LLMTool

llm = LLMTool(engine=my_engine, model="qwen3:8b")
result = llm.execute(
    prompt="Summarize: AI is transforming industries...",
    system="You are a concise summarizer.",
)
print(result.content)
```

### FileRead

**Registry key:** `file_read` | **Category:** `filesystem`

Reads file contents with safety validations. Supports optional directory restrictions, file size limits (1 MB max), and line count limiting.

**Parameters:**

| Parameter   | Type    | Required | Description                              |
|-------------|---------|----------|------------------------------------------|
| `path`      | string  | Yes      | Path to the file to read                 |
| `max_lines` | integer | No       | Maximum lines to return (default: all)   |

**Constructor parameters:**

| Parameter      | Type         | Default | Description                                   |
|----------------|--------------|---------|-----------------------------------------------|
| `allowed_dirs` | `list[str]`  | `None`  | Restrict file access to these directories     |

**Safety features:**

- Path validation against allowed directories (when configured)
- Maximum file size: 1 MB
- UTF-8 encoding required (rejects binary files)
- Existence and file-type checks

**Example:**

```python
from openjarvis.tools.file_read import FileReadTool

reader = FileReadTool(allowed_dirs=["/home/user/projects"])
result = reader.execute(path="/home/user/projects/README.md", max_lines=50)
print(result.content)
print(result.metadata)  # {"path": "/home/user/projects/README.md", "size_bytes": 1234}
```

### WebSearch

**Registry key:** `web_search` | **Category:** `search`

Searches the web and returns a result summary. Useful for queries that need current information.

**Parameters:**

| Parameter | Type   | Required | Description                              |
|-----------|--------|----------|------------------------------------------|
| `query`   | string | Yes      | Search query string                      |

### Weather

**Registry key:** `get_weather` | **Category:** `weather`

Returns structured current conditions for a dynamic location, with optional
3-hour forecast intervals. Location text is sent to OpenWeatherMap, so avoid
using a sensitive or exact address when a city or region is sufficient.

Set `OPENWEATHERMAP_API_KEY` in the environment, save it through the tool
credentials API/UI, or connect the existing Weather connector. The tool checks
those secure credential sources at execution time and never includes the key in
its result. Enable it like any native tool:

```toml
[tools]
enabled = "get_weather"
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `location` | string | No | City, region, or `city,country-code`; falls back to the configured default |
| `units` | string | No | `metric` or `imperial` |
| `language` | string | No | OpenWeatherMap language code such as `en`, `de`, or `pt_br` |
| `include_forecast` | boolean | No | Include 3-hour forecast intervals |
| `forecast_hours` | integer | No | Forecast horizon from 3 to 120 hours (default: 24) |

For example, an agent can call `get_weather` with `location="Vienna,AT"`,
`language="de"`, and `include_forecast=true`.

### CodeInterpreter

**Registry key:** `code_interpreter` | **Category:** `code`

Executes Python code snippets in a sandboxed environment and returns the output. Used by `NativeOpenHandsAgent` for CodeAct-style execution.

**Parameters:**

| Parameter | Type   | Required | Description                              |
|-----------|--------|----------|------------------------------------------|
| `code`    | string | Yes      | Python code to execute                   |

---

## Scheduler Tools

The scheduler tools expose `TaskScheduler` operations as MCP-discoverable tools. They allow agents to programmatically create, manage, and inspect scheduled tasks. All scheduler tools are in the `scheduler` category and require a `TaskScheduler` instance to be configured in the system.

!!! info "Scheduler dependency"
    The scheduler tools only function when a `TaskScheduler` is wired into the system (via `SystemBuilder`). If no scheduler is configured, all scheduler tool calls return a `success=False` result with a message explaining that the scheduler is unavailable.

### schedule_task

**Registry key:** `schedule_task` | **Category:** `scheduler`

Schedules a new task for future or recurring execution.

**Parameters:**

| Parameter        | Type   | Required | Description                                                                  |
|------------------|--------|----------|------------------------------------------------------------------------------|
| `prompt`         | string | Yes      | The query or prompt to execute on schedule                                   |
| `schedule_type`  | string | Yes      | One of `"cron"`, `"interval"`, or `"once"`                                  |
| `schedule_value` | string | Yes      | Cron expression, interval in seconds, or ISO 8601 datetime for one-time run |
| `agent`          | string | No       | Agent to use for execution (default: `"simple"`)                             |
| `tools`          | string | No       | Comma-separated tool names for the agent (e.g., `"calculator,think"`)       |

**Schedule type examples:**

| `schedule_type` | `schedule_value`       | Meaning                              |
|-----------------|------------------------|--------------------------------------|
| `once`          | `"2026-03-01T09:00:00Z"` | Run once at that UTC time           |
| `interval`      | `"3600"`               | Run every 3600 seconds (1 hour)      |
| `cron`          | `"0 9 * * 1-5"`        | Run at 09:00 UTC, Monday–Friday      |

**Returns:** JSON with `task_id`, `next_run` (ISO 8601), and `status`.

**Example (via agent tool call):**

```python
from openjarvis.scheduler.tools import ScheduleTaskTool
from openjarvis.scheduler.scheduler import TaskScheduler
from openjarvis.scheduler.store import SchedulerStore

store = SchedulerStore(db_path="~/.openjarvis/scheduler.db")
scheduler = TaskScheduler(store=store, system=jarvis_system)
scheduler.start()

tool = ScheduleTaskTool()
tool._scheduler = scheduler

result = tool.execute(
    prompt="Summarize the daily news",
    schedule_type="cron",
    schedule_value="0 8 * * *",
    agent="simple",
)
# result.content: '{"task_id": "a3f9b12c", "next_run": "2026-02-26T08:00:00+00:00", "status": "active"}'
```

### list_scheduled_tasks

**Registry key:** `list_scheduled_tasks` | **Category:** `scheduler`

Returns all scheduled tasks, optionally filtered by status.

**Parameters:**

| Parameter | Type   | Required | Description                                                          |
|-----------|--------|----------|----------------------------------------------------------------------|
| `status`  | string | No       | Filter by status: `"active"`, `"paused"`, `"completed"`, `"cancelled"` |

**Returns:** JSON array of task objects.

### pause_scheduled_task

**Registry key:** `pause_scheduled_task` | **Category:** `scheduler`

Pauses an active scheduled task. The task is preserved and can be resumed later.

**Parameters:**

| Parameter | Type   | Required | Description         |
|-----------|--------|----------|---------------------|
| `task_id` | string | Yes      | ID of task to pause |

### resume_scheduled_task

**Registry key:** `resume_scheduled_task` | **Category:** `scheduler`

Resumes a paused task. The `next_run` time is recomputed from the current time.

**Parameters:**

| Parameter | Type   | Required | Description          |
|-----------|--------|----------|----------------------|
| `task_id` | string | Yes      | ID of task to resume |

### cancel_scheduled_task

**Registry key:** `cancel_scheduled_task` | **Category:** `scheduler`

Cancels a task permanently (sets status to `"cancelled"` and clears `next_run`). Cancelled tasks are not executed again.

**Parameters:**

| Parameter | Type   | Required | Description           |
|-----------|--------|----------|-----------------------|
| `task_id` | string | Yes      | ID of task to cancel  |

---

## Tool Registration

Tools are registered via the `@ToolRegistry.register()` decorator, making them discoverable by name at runtime.

```python
from openjarvis.core.registry import ToolRegistry
from openjarvis.tools._stubs import BaseTool, ToolSpec
from openjarvis.core.types import ToolResult


@ToolRegistry.register("my_tool")
class MyTool(BaseTool):
    tool_id = "my_tool"

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="my_tool",
            description="A custom tool that does something useful.",
            parameters={
                "type": "object",
                "properties": {
                    "input": {
                        "type": "string",
                        "description": "The input to process.",
                    },
                },
                "required": ["input"],
            },
            category="custom",
        )

    def execute(self, **params) -> ToolResult:
        value = params.get("input", "")
        return ToolResult(
            tool_name="my_tool",
            content=f"Processed: {value}",
            success=True,
        )
```

After registration, use the tool with an agent:

```bash
jarvis ask --agent orchestrator --tools my_tool "Process this data"
```

---

## Using Tools with Agents

### Via CLI

Tools are specified as a comma-separated list with the `--tools` flag. An agent (typically `orchestrator`) must be selected:

```bash
# Single tool
jarvis ask --agent orchestrator --tools calculator "What is 15% of 340?"

# Multiple tools
jarvis ask --agent orchestrator --tools calculator,think "Solve: 2x + 5 = 13"

# All available tools (list them)
jarvis ask --agent orchestrator --tools calculator,think,retrieval,file_read "..."
```

### Via Python SDK

Tools are passed as a list of name strings:

```python
from openjarvis import Jarvis

j = Jarvis()

# Use calculator and think tools
result = j.ask_full(
    "What is the area of a circle with radius 7?",
    agent="orchestrator",
    tools=["calculator", "think"],
)

for tr in result["tool_results"]:
    print(f"  {tr['tool_name']}: {tr['content']} (success={tr['success']})")

j.close()
```

The SDK automatically instantiates tool objects with appropriate dependencies. For example, the `retrieval` tool receives the configured memory backend, and the `llm` tool receives the active engine and model.

===== END FILE: docs\user-guide\tools.md =====

===== FILE: docs\user-guide\system-access.md | 6998 bytes | sha16 412534c98c62adb5 | last commit 2026-07-28 =====

# System Access

How to give an agent access to the machine it runs on, and where the real
limits are.

!!! warning
    `shell_exec` runs arbitrary commands as your user. There is no command
    allowlist, no denylist, and no sandbox unless you turn one on. An agent
    holding this tool can do anything you can do from a terminal.

---

## Start here: you probably have no tools enabled

If the agent tells you it can't run commands or read files, that's usually not
a permissions problem. It means no tools were enabled in the first place.

Tools come from `tools.enabled`, falling back to `agent.tools`. Both default to
empty, and an empty value builds the agent with **zero tools**. Nothing is
enabled by default.

First check whether you have a config file at all:

```bash
cat ~/.openjarvis/config.toml
```

If it isn't there, that's your answer. Create it:

```toml
[engine]
default = "ollama"

[intelligence]
default_model = "qwen3.5:9b"

[agent]
default_agent = "orchestrator"

[tools]
enabled = ["shell_exec", "file_read", "file_write", "think"]
```

There's a fuller version at
`configs/openjarvis/examples/full-system-access.toml`.

Then confirm the list actually resolved:

```bash
python -c "from openjarvis.core.config import load_config; print(load_config().tools.enabled)"
```

---

## What the tools reach

| Tool | Scope |
|------|-------|
| `shell_exec` | Any command, as your user. 30s default timeout, 300s max, output capped at 100 KB per stream. |
| `file_read` | Any readable path. 1 MB cap. |
| `file_write` | Any writable path. 10 MB cap, can create parent directories. |
| `apply_patch` | Applies unified diffs to any path. |
| `code_interpreter` | Python in a subprocess, behind a coarse pattern blocklist. |

`file_read` and `file_write` take an `allowed_dirs` argument that limits them to
a set of directories, but no config key populates it. When it's empty every path
is allowed. If you want a filesystem jail today, use the container sandbox
instead of relying on these tools to enforce one.

### Sensitive filenames

`file_read` and `file_write` refuse names matching a short glob list: `.env`,
`*.pem`, `id_rsa`, `credentials.*` and a dozen or so others. It matches on the
filename only, not the path or the contents, and only those two tools consult
it. `shell_exec`, `apply_patch` and `code_interpreter` skip it entirely, so
`cat ~/.ssh/id_rsa` through `shell_exec` works fine. Treat it as protection
against fat fingers, not as a security boundary.

---

## Confirmation behaviour

`shell_exec`, `git_commit` and `agent_kill` are marked `requires_confirmation`.
What that translates to depends entirely on how you launched the agent:

| Entry point | Behaviour |
|-------------|-----------|
| `jarvis chat` | Prompts before each call. |
| `jarvis ask` | Auto-approves. |
| `jarvis agent ask` | Auto-approves. Pass `--no-yes` if you want prompts. |
| HTTP server, desktop app | Auto-approves. Tools you added to an agent's toolkit count as pre-approved. |
| Embedded via `SystemBuilder` | No callback is wired, so these tools fail closed. |

That last row catches people out. If `shell_exec` returns "requires
confirmation but no confirmation callback is available", you're constructing the
agent yourself and need to pass a `confirm_callback`.

!!! note "`enforce_tool_confirmation` doesn't do anything"
    The config loader accepts `security.enforce_tool_confirmation`, but nothing
    on the tool execution path reads it. Setting it won't change confirmation
    behaviour anywhere. Use the table above instead.

---

## macOS: Full Disk Access

On macOS the operating system is the real boundary, not the config. Shell
access and ordinary file access start working as soon as you enable the tools.
TCC-protected data does not: Messages, Mail, Photos, Safari history, Contacts
and Calendar all stay locked, and no config key will change that.

Grant Full Disk Access to whichever process hosts the backend. Child processes
inherit it:

| How you run OpenJarvis | Grant access to |
|------------------------|-----------------|
| CLI (`jarvis ask`, `jarvis chat`) | Your terminal (Terminal, iTerm, Warp) |
| Desktop app | `OpenJarvis.app`, which spawns `jarvis serve` beneath it |
| launchd (`deploy/launchd/com.openjarvis.plist`) | The `jarvis` binary, as its own entry |

System Settings, then Privacy & Security, then Full Disk Access, then **+**.

A launchd daemon gets its own TCC context, so granting access to Terminal does
nothing for it. Add `/usr/local/bin/jarvis` separately.

To check whether the grant took:

```bash
head -c 16 ~/Library/Messages/chat.db >/dev/null 2>&1 \
  && echo "granted" || echo "denied"
```

Restart the host process after you change the setting.

### Driving Mac apps

AppleScript works through `shell_exec`:

```
osascript -e 'tell application "Music" to play'
```

macOS asks for Automation permission once per target app, the first time you
touch it.

---

## What you can't do

There's no computer use. OpenJarvis can't see your screen, move the pointer or
send keystrokes. No tool for it is registered and no input automation library
appears anywhere in the codebase, so granting Accessibility or Screen Recording
buys you nothing on its own.

The `click` and `type` actions you'll find are Playwright, scoped to a browser
page rather than the desktop.

Some of this is reachable through `shell_exec` if you bring the tooling
yourself. `screencapture` will take screenshots once you've granted Screen
Recording, and something like `cliclick` will move the pointer. That gets you
scripted actions. It doesn't get you an agent that looks at the screen and
works out where to click.

---

## Narrowing access

Access widens and narrows through `tools.enabled`. Drop entries to take
capabilities away. That list is the whole grant.

Two stronger isolation options exist. Both are off by default:

```toml
[sandbox]
enabled = true          # run tools inside a container
runtime = "docker"

[security.capabilities]
enabled = true          # RBAC over declared tool capabilities
policy_path = "~/.openjarvis/policy.yaml"
```

!!! note "Capabilities are open by default even once enabled"
    `CapabilityPolicy` is built with `default_deny=False` and no config key
    exposes that flag, so an agent with no explicit policy entry gets every
    capability. Write entries for every agent you mean to restrict.

For anything untrusted, reach for `docker_shell_exec` and
`code_interpreter_docker` rather than the host-side versions.

---

## See also

- [Security](security.md) for scanners, the audit log and guardrails
- [Tools](tools.md) for the full registry
- [Code Assistant](code-assistant.md) for a narrower shell-enabled setup
- [External MCP Servers](mcp-external-servers.md) for capabilities OpenJarvis doesn't ship

===== END FILE: docs\user-guide\system-access.md =====

===== FILE: docs\user-guide\security.md | 20146 bytes | sha16 661570ac4fcf871d | last commit 2026-09-04 =====

# Security

OpenJarvis includes a security layer that scans prompts and model outputs for secrets, personally identifiable information (PII), and sensitive file paths. The system is designed to be composable: scanners run as a pipeline, and the `GuardrailsEngine` wrapper drops in front of any inference backend without changing how the rest of your code works.

## Three layers of security review

OpenJarvis separates host posture, application data boundaries, and runtime prompt guardrails:

| Layer | Command / component | What it checks |
| --- | --- | --- |
| Host scan | `jarvis scan` | Disk encryption, cloud-sync agents, exposed engine ports, remote-access tools |
| Data-boundary scan | `jarvis scan --data-boundaries` | Configured inference, memory, traces, channels, tools, and local stores |
| Runtime guardrails | `GuardrailsEngine` / BoundaryGuard | Secrets, PII, and file-policy violations in live prompts and outputs |

Use the host scan before storing sensitive data on the machine. Use the data-boundary scan to verify whether your `config.toml` is local-only, cloud-capable, or mixed. Use BoundaryGuard during inference when you need live redaction or blocking.

See [Data Boundary Scan](data-boundary-scan.md) for the application config diagnostic and [BoundaryGuard](#guardrailsengine) below for runtime scanning.

---

## Overview

The security module has four independently usable components:

<div class="grid cards" markdown>

- :material-shield-search: **GuardrailsEngine**

    ---

    Wraps any `InferenceEngine` with pre- and post-call scanning. Supports WARN, REDACT, and BLOCK modes.

    [:octicons-arrow-right-24: Jump to GuardrailsEngine](#guardrailsengine)

- :material-key-remove: **SecretScanner**

    ---

    Detects API keys, tokens, passwords, and connection strings in text.

    [:octicons-arrow-right-24: Jump to SecretScanner](#secretscanner)

- :material-account-lock: **PIIScanner**

    ---

    Detects email addresses, SSNs, credit card numbers, phone numbers, and public IPs.

    [:octicons-arrow-right-24: Jump to PIIScanner](#piiscanner)

- :material-file-lock: **File Policy**

    ---

    Blocks access to `.env`, `*.pem`, `id_rsa`, and other credential files.

    [:octicons-arrow-right-24: Jump to File Policy](#file-policy)

</div>

---

## Capability policies and runtime identities

Capability checks restrict tool dispatch and direct agent operations. Built-in
requirements cannot be weakened by omitting them from a tool's metadata. Remote
MCP tools require `tool:invoke`, and third-party tools can declare additional
requirements. Capability grants do not bypass a tool's confirmation requirement.

The `shared` and `server` security profiles enable capabilities with
`default_deny = true`. Without a policy file, their baseline grants new agents
`file:read`, `network:fetch`, `memory:read`, and `memory:write`. Code execution,
file writes, channel sends, scheduling, and administrative operations require
additional grants. The personal/default profile keeps capability checks opt-in.

To choose the exact grants, configure a policy file:

```toml
[security]
profile = "shared"

[security.capabilities]
policy_path = "/absolute/path/capabilities.json"
```

Individual fields override the profile: specifying only `policy_path` preserves
its enabled, default-deny behavior. An explicit `enabled = false` disables the
capability check, and an explicit `default_deny = false` allows capabilities not
otherwise denied. When capabilities are enabled, policy initialization failure
stops startup in every profile. Shared/server profiles also stop if rate-limit
initialization fails. Missing or malformed policy files are errors; the native
Rust capability backend remains required.

An explicit policy file receives **no automatic baseline grants**. For example,
this policy permits reads through MCP and denies other capabilities:

```json
{
  "agents": [
    {"agent_id": "mcp", "grants": [{"capability": "file:read"}]}
  ]
}
```

`{"agents": []}` denies all capability-bearing operations when
`default_deny = true`. The reviewed `calculator` and `think` tools require no
capability. A `_default` entry supplies grants for identities without their own
entry; a specific identity's policy takes precedence over `_default`.

| Execution path | Policy identity |
| --- | --- |
| Managed-agent tick or stream | The managed agent's ID |
| CLI, SDK, or selected server agent | The selected runtime agent name/ID |
| Server agent-management API | `server:api` |
| Standalone MCP executor | `mcp`, unless explicitly overridden |
| Learning environment | `learning`, unless explicitly overridden |
| Scheduler without a selected agent | `scheduler` |

Rate-limit keys include both identity and tool name. The audit log records tool
completion, capability denials, and rate-limit denials with that identity.

---

## GuardrailsEngine

`GuardrailsEngine` wraps any `InferenceEngine` and scans both the input messages and the output content. It is not registered in `EngineRegistry` — you create it directly by wrapping an existing engine instance.

### Modes

| Mode | Constant | Behavior |
|------|----------|----------|
| Warn | `RedactionMode.WARN` | Publish a `SECURITY_ALERT` event but pass the text through unchanged. Default. |
| Redact | `RedactionMode.REDACT` | Replace matches with `[REDACTED:pattern_name]` before passing to/from the engine. |
| Block | `RedactionMode.BLOCK` | Raise `SecurityBlockError` immediately when findings are detected. |

### Basic Usage

=== "Warn mode (default)"

    ```python title="warn_mode.py"
    from openjarvis.engine.ollama import OllamaEngine
    from openjarvis.security.guardrails import GuardrailsEngine
    from openjarvis.security.types import RedactionMode
    from openjarvis.core.types import Message, Role

    engine = OllamaEngine()
    guarded = GuardrailsEngine(engine)  # (1)!

    messages = [Message(role=Role.USER, content="My API key is sk-abc123xyz")]
    response = guarded.generate(messages, model="qwen3:8b")
    # The key is logged as a warning but the text is passed unchanged
    print(response["content"])
    ```

    1. Defaults to `mode=RedactionMode.WARN`, `scan_input=True`, `scan_output=True`.

=== "Redact mode"

    ```python title="redact_mode.py"
    from openjarvis.engine.ollama import OllamaEngine
    from openjarvis.security.guardrails import GuardrailsEngine
    from openjarvis.security.types import RedactionMode
    from openjarvis.core.types import Message, Role

    engine = OllamaEngine()
    guarded = GuardrailsEngine(engine, mode=RedactionMode.REDACT)  # (1)!

    messages = [Message(role=Role.USER, content="My key is sk-abc123xyz, help me debug")]
    response = guarded.generate(messages, model="qwen3:8b")
    # Input sent to engine: "My key is [REDACTED:openai_key], help me debug"
    ```

    1. Sensitive patterns in input messages are replaced before reaching the model.

=== "Block mode"

    ```python title="block_mode.py"
    from openjarvis.engine.ollama import OllamaEngine
    from openjarvis.security.guardrails import GuardrailsEngine, SecurityBlockError
    from openjarvis.security.types import RedactionMode
    from openjarvis.core.types import Message, Role

    engine = OllamaEngine()
    guarded = GuardrailsEngine(engine, mode=RedactionMode.BLOCK)

    try:
        messages = [Message(role=Role.USER, content="AKIA1234567890ABCDEF")]
        guarded.generate(messages, model="qwen3:8b")
    except SecurityBlockError as exc:
        print(f"Blocked: {exc}")
        # Blocked: Security scan blocked input: 1 finding(s) detected
    ```

### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `engine` | `InferenceEngine` | — | The wrapped inference engine |
| `scanners` | `list[BaseScanner]` | `[SecretScanner(), PIIScanner()]` | Scanners to run |
| `mode` | `RedactionMode` | `WARN` | Action on findings |
| `scan_input` | `bool` | `True` | Scan input messages |
| `scan_output` | `bool` | `True` | Scan output content |
| `bus` | `EventBus` | `None` | Event bus for security events |

### Event Bus Integration

When a `bus` is provided, `GuardrailsEngine` publishes events on every scan result:

| Event | When |
|-------|------|
| `SECURITY_ALERT` | Findings detected in WARN or REDACT mode |
| `SECURITY_BLOCK` | Findings detected in BLOCK mode |

You can subscribe to these events with an `AuditLogger` to build a persistent security event log. See [Audit Logger](#audit-logger) below.

### Custom Scanners

You can pass any set of `BaseScanner` subclasses to restrict or extend scanning:

```python title="custom_scanners.py"
from openjarvis.security.guardrails import GuardrailsEngine
from openjarvis.security.scanner import SecretScanner
from openjarvis.security.types import RedactionMode

# Only scan for secrets, skip PII
guarded = GuardrailsEngine(
    engine,
    scanners=[SecretScanner()],
    mode=RedactionMode.REDACT,
)
```

### Streaming

For streaming calls, `GuardrailsEngine.stream()` yields tokens in real time and then performs a post-hoc scan on the accumulated output for logging. Because tokens are already delivered to the caller before scanning completes, BLOCK mode only applies to the input side during streaming.

!!! warning "Streaming and BLOCK mode"
    `SecurityBlockError` can only be raised before the stream starts (for input scanning). Output blocking during streaming is not possible — use REDACT mode if you need to sanitize model outputs in streaming scenarios.

---

## SecretScanner

`SecretScanner` detects API keys, tokens, passwords, and other credentials using regex patterns. Each pattern has an associated `ThreatLevel`.

### Pattern Reference

| Pattern Name | Threat Level | Matches |
|---|---|---|
| `openai_key` | CRITICAL | `sk-` followed by 20+ alphanumeric chars |
| `anthropic_key` | CRITICAL | `sk-ant-` followed by 20+ chars |
| `aws_access_key` | CRITICAL | `AKIA` followed by 16 uppercase alphanumeric chars |
| `github_token` | CRITICAL | `ghp_`, `gho_`, `ghs_`, `ghr_`, `github_pat_` followed by 36+ chars |
| `stripe_key` | CRITICAL | `sk_live_`, `sk_test_`, `pk_live_`, `pk_test_` followed by 20+ chars |
| `private_key` | CRITICAL | PEM private key header `-----BEGIN PRIVATE KEY-----` |
| `password_assignment` | HIGH | `password = "..."`, `passwd: "..."`, etc. |
| `db_connection_string` | HIGH | `postgres://`, `mysql://`, `mongodb://`, `redis://` URLs |
| `slack_token` | HIGH | `xoxb-`, `xoxp-`, `xoxo-`, `xoxr-`, `xoxs-` followed by token |
| `generic_api_key` | HIGH | `api_key = "..."`, `secret_key = "..."`, `auth_token = "..."` |

### Direct Usage

```python title="secret_scanner.py"
from openjarvis.security.scanner import SecretScanner

scanner = SecretScanner()

# Scan text
result = scanner.scan("My key is sk-abc123xyz789 and it is secret")
print(result.clean)           # False
print(result.highest_threat)  # ThreatLevel.CRITICAL
for finding in result.findings:
    print(f"  {finding.pattern_name}: {finding.description} at [{finding.start}:{finding.end}]")

# Redact text
clean = scanner.redact("Token: sk-abc123xyz789")
print(clean)  # Token: [REDACTED:openai_key]
```

---

## PIIScanner

`PIIScanner` detects personally identifiable information using regex patterns calibrated for common US formats.

### Pattern Reference

| Pattern Name | Threat Level | Matches |
|---|---|---|
| `us_ssn` | CRITICAL | `XXX-XX-XXXX` format Social Security Numbers |
| `credit_card_visa` | CRITICAL | Visa card numbers (16 digits starting with 4) |
| `credit_card_mastercard` | CRITICAL | Mastercard numbers (16 digits starting with 51–55) |
| `credit_card_amex` | CRITICAL | Amex numbers (15 digits starting with 34 or 37) |
| `email` | MEDIUM | Standard email addresses |
| `us_phone` | MEDIUM | US phone numbers in common formats |
| `ipv4_public` | LOW | Public IPv4 addresses (excludes RFC1918 ranges) |

!!! note "Private IP addresses"
    The `ipv4_public` pattern intentionally excludes private ranges (10.x.x.x, 172.16–31.x.x, 192.168.x.x, 127.x.x.x). Internal IP addresses are not considered sensitive by default.

### Direct Usage

```python title="pii_scanner.py"
from openjarvis.security.scanner import PIIScanner

scanner = PIIScanner()

text = "Contact john@example.com or call 555-867-5309"
result = scanner.scan(text)

for finding in result.findings:
    print(f"{finding.pattern_name}: threat={finding.threat_level.value}")
# email: threat=medium
# us_phone: threat=medium

clean = scanner.redact(text)
print(clean)
# Contact [REDACTED:email] or call [REDACTED:us_phone]
```

---

## File Policy

The file policy module prevents access to credential and key files. It is used internally by `FileReadTool` and the memory ingest path, but you can use it directly.

### Sensitive File Patterns

The `DEFAULT_SENSITIVE_PATTERNS` frozenset contains the following glob patterns:

| Pattern | Description |
|---------|-------------|
| `.env`, `.env.*`, `*.env` | Environment variable files |
| `.secret`, `*.secrets` | Generic secret files |
| `credentials.*` | Credential files |
| `*.pem`, `*.key` | TLS/SSL certificates and private keys |
| `*.p12`, `*.pfx`, `*.jks` | PKCS and Java keystore files |
| `id_rsa`, `id_ed25519` | SSH private key files |
| `.htpasswd` | Apache password files |
| `.pgpass` | PostgreSQL password files |
| `.netrc` | FTP/SSH credential files |

### Usage

```python title="file_policy.py"
from pathlib import Path
from openjarvis.security.file_policy import is_sensitive_file, filter_sensitive_paths

# Check a single file
print(is_sensitive_file(".env"))           # True
print(is_sensitive_file("server.key"))     # True
print(is_sensitive_file("README.md"))      # False

# Filter a list of paths
paths = [
    Path("README.md"),
    Path(".env"),
    Path("src/main.py"),
    Path("server.pem"),
]
safe = filter_sensitive_paths(paths)
print(safe)  # [PosixPath('README.md'), PosixPath('src/main.py')]
```

### Integration with FileReadTool

The built-in `FileReadTool` automatically calls `is_sensitive_file()` before reading any path. Attempts to read sensitive files raise an error rather than returning the file content. This behavior cannot be disabled at the tool level — configure the agent not to have `FileReadTool` if you need unrestricted file access.

---

## Audit Logger

The `AuditLogger` persists security events to an append-only SQLite database. It can subscribe to the event bus to capture events automatically, or you can call `log()` manually.

### Event Bus Integration (Automatic)

```python title="audit_bus.py"
from openjarvis.core.events import EventBus
from openjarvis.security.audit import AuditLogger
from openjarvis.security.guardrails import GuardrailsEngine
from openjarvis.security.types import RedactionMode
from openjarvis.engine.ollama import OllamaEngine

bus = EventBus()

# AuditLogger subscribes to SECURITY_SCAN, SECURITY_ALERT, SECURITY_BLOCK
audit = AuditLogger(db_path="~/.openjarvis/audit.db", bus=bus)

engine = OllamaEngine()
guarded = GuardrailsEngine(
    engine,
    mode=RedactionMode.WARN,
    bus=bus,
)

# Security events are now persisted automatically
```

### Manual Logging

```python title="audit_manual.py"
import time
from openjarvis.security.audit import AuditLogger
from openjarvis.security.types import SecurityEvent, SecurityEventType

audit = AuditLogger(db_path="./audit.db")

event = SecurityEvent(
    event_type=SecurityEventType.SECRET_DETECTED,
    timestamp=time.time(),
    findings=[],
    content_preview="sk-...",
    action_taken="redacted",
)
audit.log(event)
```

### Querying the Audit Log

```python title="audit_query.py"
from openjarvis.security.audit import AuditLogger

audit = AuditLogger(db_path="~/.openjarvis/audit.db")

# Recent events
events = audit.query(limit=20)

# Filter by event type
secret_events = audit.query(event_type="secret_detected")

# Filter by time range
import time
recent = audit.query(since=time.time() - 3600)  # last hour

# Count total events
print(f"Total events: {audit.count()}")

audit.close()
```

---

## Configuration

Security settings live in the `[security]` section of `~/.openjarvis/config.toml`.

```toml title="~/.openjarvis/config.toml"
[security]
enabled = true
scan_input = true
scan_output = true
mode = "warn"               # "warn" | "redact" | "block"
secret_scanner = true
pii_scanner = true
audit_log_path = "~/.openjarvis/audit.db"
enforce_tool_confirmation = true
```

### Configuration Reference

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `enabled` | `bool` | `true` | Enable the security subsystem |
| `scan_input` | `bool` | `true` | Scan user input messages |
| `scan_output` | `bool` | `true` | Scan model output content |
| `mode` | `str` | `"warn"` | Action on findings: `warn`, `redact`, or `block` |
| `secret_scanner` | `bool` | `true` | Run `SecretScanner` on all text |
| `pii_scanner` | `bool` | `true` | Run `PIIScanner` on all text |
| `audit_log_path` | `str` | `~/.openjarvis/audit.db` | Path to the SQLite audit log |
| `enforce_tool_confirmation` | `bool` | `true` | Accepted by the loader but **not currently enforced**. See [System Access](system-access.md#confirmation-behaviour) for when prompts actually happen |

!!! tip "Start with warn, tighten later"
    `mode = "warn"` is a good starting point. It lets you observe what patterns are being triggered without disrupting normal usage. Switch to `"redact"` once you are satisfied that the scanner isn't producing too many false positives for your workload.

---

## Writing a Custom Scanner

Implement `BaseScanner` and pass an instance to `GuardrailsEngine`:

```python title="custom_scanner.py"
import re
from openjarvis.security._stubs import BaseScanner
from openjarvis.security.types import ScanFinding, ScanResult, ThreatLevel


class InternalUrlScanner(BaseScanner):
    """Detect internal service URLs that should not be shared externally."""

    scanner_id = "internal_urls"

    PATTERN = re.compile(r"https?://internal\.[a-z0-9.-]+\.[a-z]{2,}")

    def scan(self, text: str) -> ScanResult:
        findings = []
        for match in self.PATTERN.finditer(text):
            findings.append(ScanFinding(
                pattern_name="internal_url",
                matched_text=match.group(0),
                threat_level=ThreatLevel.MEDIUM,
                start=match.start(),
                end=match.end(),
                description="Internal service URL",
            ))
        return ScanResult(findings=findings)

    def redact(self, text: str) -> str:
        return self.PATTERN.sub("[REDACTED:internal_url]", text)


# Use with GuardrailsEngine
from openjarvis.security.guardrails import GuardrailsEngine
from openjarvis.security.types import RedactionMode

guarded = GuardrailsEngine(
    engine,
    scanners=[InternalUrlScanner()],
    mode=RedactionMode.REDACT,
)
```

---

## Data boundary scan

See [Data Boundary Scan](data-boundary-scan.md) for the application config diagnostic (`jarvis scan --data-boundaries`).

---

## See Also

- [Data Boundary Scan](data-boundary-scan.md) — application config and local-store diagnostic (`jarvis scan --data-boundaries`)
- [Architecture: Security](../architecture/security.md) — pipeline design, event flow, and file policy integration
- [API Reference: Security](../api-reference/openjarvis/security/index.md) — full class and function signatures
- [Tools](tools.md) — how `FileReadTool` uses file policy
- [Configuration](../getting-started/configuration.md) — full config reference

===== END FILE: docs\user-guide\security.md =====

===== FILE: docs\deployment\api-server.md | 17494 bytes | sha16 5b8a3fcbe3f7bf28 | last commit 2026-08-20 =====

# API Server

OpenJarvis includes an OpenAI-compatible API server built on FastAPI and uvicorn. It exposes chat completion, model listing, and health check endpoints, making it a drop-in replacement for the OpenAI API when working with local models.

## Starting the Server

The server requires the `[server]` extra (FastAPI + uvicorn):

```bash
git clone https://github.com/open-jarvis/OpenJarvis.git
cd OpenJarvis
uv sync --extra server
```

Start with default settings:

```bash
jarvis serve
```

For a cloud-hosted example, see [Deploy on Render](render.md). Its free-tier
Blueprint is intended for evaluation only because local OpenJarvis state is
ephemeral.

The server reads defaults from `~/.openjarvis/config.toml` and auto-detects available engines and models. Override any option via CLI flags:

```bash
jarvis serve --host 0.0.0.0 --port 8000 --engine ollama --model qwen3:8b --agent orchestrator
```

### CLI Options

| Option               | Description                                                                  | Default           |
|----------------------|------------------------------------------------------------------------------|--------------------|
| `--host`             | Network address to bind to                                                   | From config (`0.0.0.0`) |
| `--port`             | Port number to listen on                                                     | From config (`8000`)    |
| `-e` / `--engine`    | Inference engine backend (`ollama`, `vllm`, `llamacpp`, `sglang`)            | Auto-detected      |
| `-m` / `--model`     | Default model for completions                                                | First available     |
| `-a` / `--agent`     | Agent for non-streaming requests (`simple`, `orchestrator`, `react`, `openhands`) | From config (`orchestrator`) |

On startup, the server prints a summary:

```
Starting OpenJarvis API server
  Engine: ollama
  Model:  qwen3:8b
  Agent:  orchestrator
  URL:    http://0.0.0.0:8000
```

!!! warning "Server dependency check"
    If the `[server]` extra is not installed, `jarvis serve` exits with a clear error message explaining how to install the required dependencies.

## Endpoints

### `POST /v1/chat/completions`

The primary endpoint for generating chat completions. Accepts the same request format as the OpenAI Chat Completions API.

#### Request Body

```json
{
  "model": "qwen3:8b",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
  ],
  "temperature": 0.7,
  "max_tokens": 1024,
  "stream": false,
  "tools": null
}
```

| Parameter     | Type              | Default | Description                                                  |
|---------------|-------------------|---------|--------------------------------------------------------------|
| `model`       | `string`          | --      | **Required.** Model identifier to use for generation.        |
| `messages`    | `array`           | --      | **Required.** Array of message objects with `role` and `content`. |
| `temperature` | `float`           | `0.7`   | Sampling temperature (0.0 to 2.0).                           |
| `max_tokens`  | `integer`         | `1024`  | Maximum number of tokens to generate.                        |
| `stream`      | `boolean`         | `false` | Whether to stream the response via SSE.                      |
| `tools`       | `array` or `null` | `null`  | Tool definitions in OpenAI function-calling format.          |

Each message object:

| Field          | Type              | Description                                           |
|----------------|-------------------|-------------------------------------------------------|
| `role`         | `string`          | One of `system`, `user`, `assistant`, or `tool`.      |
| `content`      | `string`          | The message content.                                  |
| `name`         | `string` or `null`| Optional name for the message author.                 |
| `tool_calls`   | `array` or `null` | Tool calls made by the assistant (in assistant messages). |
| `tool_call_id` | `string` or `null`| ID of the tool call this message responds to (in tool messages). |

#### Response (Non-Streaming)

```json
{
  "id": "chatcmpl-abc123def456",
  "object": "chat.completion",
  "created": 1740100800,
  "model": "qwen3:8b",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "The capital of France is Paris.",
        "tool_calls": null
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 8,
    "total_tokens": 33
  }
}
```

When an agent is configured on the server, non-streaming requests are routed through the agent, which can perform multi-turn reasoning with tool calls before returning a final response. When no agent is configured, requests go directly to the inference engine.

#### Tool Calls

When `tools` are provided in the request, the engine may return `tool_calls` in the assistant message:

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "",
        "tool_calls": [
          {
            "id": "call_abc123",
            "type": "function",
            "function": {
              "name": "calculator",
              "arguments": "{\"expression\": \"2 + 2\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ]
}
```

### `GET /v1/models`

Lists all models available on the configured inference engine.

#### Response

```json
{
  "object": "list",
  "data": [
    {
      "id": "qwen3:8b",
      "object": "model",
      "created": 1740100800,
      "owned_by": "openjarvis"
    },
    {
      "id": "llama3.1:8b",
      "object": "model",
      "created": 1740100800,
      "owned_by": "openjarvis"
    }
  ]
}
```

### `GET /health`

Health check endpoint that verifies the inference engine is responsive.

#### Response (Healthy)

HTTP 200:

```json
{"status": "ok"}
```

#### Response (Unhealthy)

HTTP 503:

```json
{"detail": "Engine unhealthy"}
```

### `GET /dashboard`

Serves the built-in Savings Dashboard, an HTML page that displays real-time statistics on inference calls served locally and estimated cost savings compared to cloud API providers. The dashboard auto-refreshes every 5 seconds by polling the `/v1/savings` endpoint.

### `GET /v1/channels`

List registered channel backends and their connection status.

#### Response

```json
{
  "channels": ["slack", "discord", "telegram"]
}
```

### `POST /v1/channels/send`

Send a message to a specific channel.

#### Request Body

```json
{
  "target": "slack",
  "message": "Hello from Jarvis!"
}
```

#### Response

```json
{
  "status": "sent",
  "target": "slack"
}
```

### `GET /v1/channels/status`

Show connection status for all configured channels.

#### Response

```json
{
  "channels": {
    "slack": "connected",
    "discord": "connected",
    "telegram": "disconnected"
  }
}
```

!!! note "Channel endpoints"
    Channel endpoints require `[channel] enabled = true` in your config and platform-specific credentials configured in `[channel.<platform>]` sub-sections. When not configured, `GET /v1/channels` returns an empty list and other channel endpoints return 503.

### WebSocket endpoints

- `WS /v1/chat/stream` streams interactive chat messages.
- `WS /v1/agents/events` streams agent lifecycle events and accepts an optional
  `agent_id` query parameter as a filter.

When `OPENJARVIS_API_KEY` or `[server.auth].api_key` is configured,
programmatic WebSocket clients should send the same
`Authorization: Bearer <key>` header used by HTTP requests. Browsers cannot set
that header on a WebSocket handshake, so browser clients must offer exactly
these two subprotocol values:

1. `openjarvis.auth.v1`
2. `openjarvis.key.b64url.<encoded-key>`, where `<encoded-key>` is the unpadded
   base64url encoding of the API key's UTF-8 bytes

The server selects `openjarvis.auth.v1` in its handshake response. The built-in
frontend handles this encoding automatically. Base64url is only a transport
encoding, not encryption; use `wss://` for remote connections and treat the
`Sec-WebSocket-Protocol` request header as credential-bearing.

!!! warning "WebSocket authentication migration"
    The former `?token=<key>` query parameter is not accepted because request
    URLs commonly appear in access logs and browser history. Existing custom
    WebSocket clients must migrate to `Authorization` or the browser
    subprotocol format above.

## Streaming via SSE

When `"stream": true` is set in the request, the server returns a `text/event-stream` response using Server-Sent Events (SSE). The response follows the same format as the OpenAI streaming API.

Each event is a `data:` line containing a JSON chunk, followed by a blank line:

```
data: {"id":"chatcmpl-abc123","object":"chat.completion.chunk","created":1740100800,"model":"qwen3:8b","choices":[{"index":0,"delta":{"role":"assistant"},"finish_reason":null}]}

data: {"id":"chatcmpl-abc123","object":"chat.completion.chunk","created":1740100800,"model":"qwen3:8b","choices":[{"index":0,"delta":{"content":"The"},"finish_reason":null}]}

data: {"id":"chatcmpl-abc123","object":"chat.completion.chunk","created":1740100800,"model":"qwen3:8b","choices":[{"index":0,"delta":{"content":" capital"},"finish_reason":null}]}

...

data: {"id":"chatcmpl-abc123","object":"chat.completion.chunk","created":1740100800,"model":"qwen3:8b","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```

The stream follows this sequence:

1. **Role chunk** -- first chunk contains `"delta": {"role": "assistant"}` with no content.
2. **Content chunks** -- subsequent chunks each contain a `"delta": {"content": "..."}` with one or more tokens.
3. **Finish chunk** -- a chunk with an empty `delta` and `"finish_reason": "stop"`.
4. **Done signal** -- the literal string `data: [DONE]` indicates the stream is complete.

Response headers include `Cache-Control: no-cache` and `Connection: keep-alive` for proper SSE behavior.

## Client Examples

=== "curl"

    **Non-streaming request:**

    ```bash
    curl http://localhost:8000/v1/chat/completions \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen3:8b",
        "messages": [
          {"role": "user", "content": "Explain quantum computing in one paragraph."}
        ],
        "temperature": 0.7,
        "max_tokens": 256
      }'
    ```

    **Streaming request:**

    ```bash
    curl http://localhost:8000/v1/chat/completions \
      -H "Content-Type: application/json" \
      -N \
      -d '{
        "model": "qwen3:8b",
        "messages": [
          {"role": "user", "content": "Write a haiku about programming."}
        ],
        "stream": true
      }'
    ```

    **List models:**

    ```bash
    curl http://localhost:8000/v1/models
    ```

    **Health check:**

    ```bash
    curl http://localhost:8000/health
    ```

=== "Python (openai)"

    The OpenAI Python library works as a drop-in client by pointing `base_url` at the local server:

    ```python
    from openai import OpenAI

    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="not-needed",  # Required by the library but not validated
    )

    # Non-streaming
    response = client.chat.completions.create(
        model="qwen3:8b",
        messages=[
            {"role": "user", "content": "What is the capital of France?"}
        ],
        temperature=0.7,
        max_tokens=256,
    )
    print(response.choices[0].message.content)

    # Streaming
    stream = client.chat.completions.create(
        model="qwen3:8b",
        messages=[
            {"role": "user", "content": "Write a short poem about AI."}
        ],
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()

    # List models
    models = client.models.list()
    for model in models.data:
        print(model.id)
    ```

=== "Python (httpx)"

    Using `httpx` for direct HTTP requests:

    ```python
    import httpx
    import json

    BASE_URL = "http://localhost:8000"

    # Non-streaming request
    response = httpx.post(
        f"{BASE_URL}/v1/chat/completions",
        json={
            "model": "qwen3:8b",
            "messages": [
                {"role": "user", "content": "What is the capital of France?"}
            ],
            "temperature": 0.7,
            "max_tokens": 256,
        },
    )
    data = response.json()
    print(data["choices"][0]["message"]["content"])

    # Streaming request
    with httpx.stream(
        "POST",
        f"{BASE_URL}/v1/chat/completions",
        json={
            "model": "qwen3:8b",
            "messages": [
                {"role": "user", "content": "Write a haiku about code."}
            ],
            "stream": True,
        },
    ) as response:
        for line in response.iter_lines():
            if line.startswith("data: ") and line != "data: [DONE]":
                chunk = json.loads(line[6:])
                content = chunk["choices"][0]["delta"].get("content", "")
                if content:
                    print(content, end="", flush=True)
    print()

    # List models
    response = httpx.get(f"{BASE_URL}/v1/models")
    for model in response.json()["data"]:
        print(model["id"])

    # Health check
    response = httpx.get(f"{BASE_URL}/health")
    print(response.json())
    ```

## Configuration via `config.toml`

The `[server]` section of `~/.openjarvis/config.toml` controls default server behavior:

```toml
[server]
host = "0.0.0.0"
port = 8000
agent = "orchestrator"
model = ""
workers = 1
```

| Key       | Type      | Default         | Description                                                                |
|-----------|-----------|-----------------|----------------------------------------------------------------------------|
| `host`    | `string`  | `"0.0.0.0"`    | Network address to bind to. Use `"127.0.0.1"` for localhost-only access.   |
| `port`    | `integer` | `8000`          | Port number.                                                               |
| `agent`   | `string`  | `"orchestrator"`| Default agent for non-streaming requests. Set to `""` for direct engine mode. |
| `model`   | `string`  | `""`            | Default model name. When empty, falls back to `[intelligence] default_model` or the first model discovered on the engine. |
| `workers` | `integer` | `1`             | Number of uvicorn workers (for future use).                                |

CLI flags override config file values. For example, `jarvis serve --port 9000` overrides the `port` setting in the config file.

The server also reads from other config sections at startup:

- **`[engine]`** -- determines which inference backend to connect to and its host URL.
- **`[intelligence]`** -- provides the fallback `default_model` when no model is specified.
- **`[agent]`** -- supplies `max_turns` for multi-turn agents like `orchestrator`.

## Running Behind a Reverse Proxy

For production deployments, run OpenJarvis behind a reverse proxy like Nginx or Caddy for TLS termination, rate limiting, and authentication.

### Nginx

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}

server {
    listen 443 ssl;
    server_name jarvis.example.com;

    ssl_certificate /etc/ssl/certs/jarvis.pem;
    ssl_certificate_key /etc/ssl/private/jarvis.key;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket upgrade support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;

        # SSE streaming support
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 300s;
    }
}
```

!!! important "Disable buffering for SSE"
    The `proxy_buffering off` directive is critical for streaming responses. Without it, Nginx buffers the SSE chunks and delivers them in batches, defeating the purpose of streaming.

### Caddy

```
jarvis.example.com {
    reverse_proxy 127.0.0.1:8000 {
        flush_interval -1
    }
}
```

The `flush_interval -1` setting disables response buffering, which is required for SSE streaming.

### Bind to Localhost

When running behind a reverse proxy, bind the server to `127.0.0.1` so it only accepts connections from the proxy:

```bash
jarvis serve --host 127.0.0.1 --port 8000
```

Or in `config.toml`:

```toml
[server]
host = "127.0.0.1"
port = 8000
```

===== END FILE: docs\deployment\api-server.md =====

===== FILE: docs\user-guide\memory.md | 13653 bytes | sha16 081bfdb7afaba4ed | last commit 2026-03-12 =====

# Memory

The memory system provides persistent, searchable document storage for retrieval-augmented generation (RAG). It supports multiple retrieval backends, a configurable chunking pipeline, document ingestion from files and directories, and automatic context injection into prompts.

## Architecture

```
Documents  -->  Chunking Pipeline  -->  Memory Backend  -->  Context Injection  -->  Prompt
  (files)       (split + overlap)      (store + index)      (retrieve + format)    (to LLM)
```

---

## MemoryBackend ABC

All memory backends implement the `MemoryBackend` abstract base class.

```python
class MemoryBackend(ABC):
    backend_id: str

    def store(self, content: str, *, source: str = "", metadata: dict | None = None) -> str:
        """Persist content and return a unique document ID."""

    def retrieve(self, query: str, *, top_k: int = 5, **kwargs) -> list[RetrievalResult]:
        """Search for query and return the top-k results."""

    def delete(self, doc_id: str) -> bool:
        """Delete a document by ID. Return True if it existed."""

    def clear(self) -> None:
        """Remove all stored documents."""
```

### RetrievalResult

Each retrieval returns a list of `RetrievalResult` objects:

| Field      | Type             | Description                                |
|------------|------------------|--------------------------------------------|
| `content`  | `str`            | The retrieved text chunk                   |
| `score`    | `float`          | Relevance score (higher is better)         |
| `source`   | `str`            | Originating file path or identifier        |
| `metadata` | `dict[str, Any]` | Additional metadata (chunk index, etc.)    |

---

## Backends

### SQLite / FTS5 (Default)

**Registry key:** `sqlite`

The default backend using SQLite's built-in FTS5 full-text search extension. Zero external dependencies -- uses Python's standard `sqlite3` module.

- **Scoring:** BM25 ranking via FTS5 MATCH queries
- **Persistence:** SQLite database file (default: `~/.openjarvis/memory.db`)
- **Dependencies:** None (built into Python)

```python
from openjarvis.core.registry import MemoryRegistry

backend = MemoryRegistry.create("sqlite", db_path="./memory.db")
doc_id = backend.store("Hello world", source="test.txt")
results = backend.retrieve("hello")
backend.close()
```

!!! tip "When to use SQLite/FTS5"
    Use this backend when you want zero-configuration setup, keyword-based search is sufficient, and you need persistent storage across restarts. It works well for small to medium document collections.

### FAISS

**Registry key:** `faiss`

Dense neural retrieval using Facebook AI Similarity Search. Embeds documents and queries into dense vectors and retrieves by cosine similarity.

- **Scoring:** Cosine similarity via inner-product search on L2-normalized vectors
- **Persistence:** In-memory only (data is lost on restart)
- **Dependencies:** `faiss-cpu` (or `faiss-gpu`), `sentence-transformers`

```bash
uv sync --extra memory-faiss
```

```python
backend = MemoryRegistry.create("faiss")
doc_id = backend.store("Neural networks are computational models")
results = backend.retrieve("deep learning architectures")
```

!!! tip "When to use FAISS"
    Use this backend when you need semantic search (finding conceptually similar content even without exact keyword matches). Best for use cases where you can re-index on each run since data is not persisted.

### ColBERTv2

**Registry key:** `colbert`

Late-interaction retrieval using ColBERT's token-level embeddings with MaxSim scoring. Provides the highest retrieval quality among the available backends.

- **Scoring:** MaxSim -- for each query token, take the maximum cosine similarity across all document tokens, then sum
- **Persistence:** In-memory only
- **Dependencies:** `colbert-ai`, `torch`

```bash
uv sync --extra memory-colbert
```

```python
backend = MemoryRegistry.create(
    "colbert",
    checkpoint="colbert-ir/colbertv2.0",
    device="cpu",
)
```

| Parameter    | Default                    | Description                         |
|--------------|----------------------------|-------------------------------------|
| `checkpoint` | `"colbert-ir/colbertv2.0"` | ColBERT model checkpoint            |
| `device`     | `"cpu"`                    | Computation device (`cpu` or `cuda`) |

!!! tip "When to use ColBERTv2"
    Use this backend when retrieval quality is the top priority and you have the compute resources for it. The checkpoint is lazily loaded on first use to avoid slow imports. Best for research and evaluation workloads.

### BM25

**Registry key:** `bm25`

Classic probabilistic ranking using the BM25 Okapi algorithm. In-memory implementation using the `rank_bm25` library.

- **Scoring:** BM25 Okapi term-frequency scoring
- **Persistence:** In-memory only
- **Dependencies:** `rank-bm25`

```bash
uv sync --extra memory-bm25
```

```python
backend = MemoryRegistry.create("bm25")
backend.store("Python is a programming language", source="intro.txt")
results = backend.retrieve("programming language")
```

!!! tip "When to use BM25"
    Use this backend when you want classic keyword-based retrieval without database dependencies. Useful as the sparse component in a hybrid retrieval setup.

### Hybrid (RRF Fusion)

**Registry key:** `hybrid`

Combines a sparse retriever and a dense retriever using Reciprocal Rank Fusion (RRF). Documents are stored in both sub-backends, and retrieval results are merged.

- **Scoring:** `RRF_score(d) = sum(weight_i / (k + rank_i(d)))` across both ranked lists
- **Persistence:** Depends on sub-backends
- **Dependencies:** Depends on sub-backends

```python
from openjarvis.tools.storage.bm25 import BM25Memory
from openjarvis.tools.storage.faiss_backend import FAISSMemory

sparse = BM25Memory()
dense = FAISSMemory()

backend = MemoryRegistry.create(
    "hybrid",
    sparse=sparse,
    dense=dense,
    k=60,
    sparse_weight=1.0,
    dense_weight=1.0,
)
```

!!! note "Backward compatibility"
    The old `from openjarvis.memory.bm25 import BM25Memory` still works via backward-compatibility shims, but new code should use the canonical `openjarvis.tools.storage.*` imports.

| Parameter       | Default | Description                              |
|-----------------|---------|------------------------------------------|
| `sparse`        | --      | Sparse retrieval backend (e.g., BM25)    |
| `dense`         | --      | Dense retrieval backend (e.g., FAISS)    |
| `k`             | `60`    | RRF constant                             |
| `sparse_weight` | `1.0`   | Weight for sparse retriever results      |
| `dense_weight`  | `1.0`   | Weight for dense retriever results       |

The hybrid backend over-fetches (3x `top_k`) from each sub-backend before applying fusion to improve result quality.

!!! tip "When to use Hybrid"
    Use this backend when you want the best of both keyword matching and semantic similarity. The RRF fusion approach is robust and does not require tuning score distributions across different retrieval methods.

---

## Backend Comparison

| Backend     | Search Type       | Persistence | Dependencies         | Quality  | Speed    |
|-------------|-------------------|-------------|----------------------|----------|----------|
| SQLite/FTS5 | Keyword (BM25)    | Yes         | None                 | Good     | Fast     |
| FAISS       | Dense (cosine)    | No          | faiss, transformers  | Better   | Fast     |
| ColBERTv2   | Late interaction  | No          | colbert-ai, torch    | Best     | Slower   |
| BM25        | Keyword (Okapi)   | No          | rank-bm25            | Good     | Fast     |
| Hybrid      | Fusion (RRF)      | Mixed       | Sub-backend deps     | Better   | Medium   |

---

## Chunking Pipeline

Documents are split into chunks before storage using a configurable pipeline. The chunker respects paragraph boundaries when possible.

### ChunkConfig

| Field           | Type  | Default | Description                              |
|-----------------|-------|---------|------------------------------------------|
| `chunk_size`    | `int` | `512`   | Target chunk size in whitespace tokens   |
| `chunk_overlap` | `int` | `64`    | Overlap between consecutive chunks       |
| `min_chunk_size`| `int` | `50`    | Minimum chunk size (smaller chunks are discarded) |

### How Chunking Works

1. The document is split into paragraphs (separated by double newlines).
2. Paragraphs are accumulated until the token count exceeds `chunk_size`.
3. The accumulated content is emitted as a chunk.
4. The last `chunk_overlap` tokens are retained as context for the next chunk.
5. Paragraphs exceeding `chunk_size` are split into fixed-size windows with overlap.

### Chunk Output

Each chunk is a `Chunk` object with:

| Field      | Type             | Description                              |
|------------|------------------|------------------------------------------|
| `content`  | `str`            | The chunk text                           |
| `source`   | `str`            | Originating file path                    |
| `offset`   | `int`            | Token offset within the document         |
| `index`    | `int`            | Sequential chunk index                   |
| `metadata` | `dict[str, Any]` | Additional metadata                      |

---

## Document Ingestion

The `ingest_path()` function reads files or recursively walks directories, producing chunks ready for storage.

### Supported File Types

| Type     | Extensions                                                  |
|----------|-------------------------------------------------------------|
| Text     | `.txt` and other plain text files                           |
| Markdown | `.md`, `.markdown`, `.mdx`                                  |
| Code     | `.py`, `.js`, `.ts`, `.rs`, `.go`, `.java`, `.c`, `.cpp`, `.rb`, `.sh`, `.yaml`, `.json`, `.html`, `.css`, and more |
| PDF      | `.pdf` (requires `pdfplumber`: `uv sync --extra memory-pdf`) |

### Automatic Skipping

The ingestion pipeline automatically skips:

- Hidden files and directories (starting with `.`)
- Common non-content directories: `__pycache__`, `node_modules`, `.venv`, `.git`, etc.
- Binary files: images, audio, video, archives, compiled files
- Files that cannot be read (permission errors, encoding issues)

### Usage

```python
from pathlib import Path
from openjarvis.tools.storage.chunking import ChunkConfig
from openjarvis.tools.storage.ingest import ingest_path

# Default chunking
chunks = ingest_path(Path("./docs/"))

# Custom chunking
config = ChunkConfig(chunk_size=256, chunk_overlap=32)
chunks = ingest_path(Path("./notes.md"), config=config)

print(f"Produced {len(chunks)} chunks")
for chunk in chunks[:3]:
    print(f"  [{chunk.index}] {chunk.source}: {chunk.content[:60]}...")
```

---

## Context Injection

When memory context injection is enabled (the default), queries are automatically augmented with relevant retrieved documents before being sent to the model. Each retrieved passage includes source attribution.

### ContextConfig

| Field               | Type    | Default | Description                                      |
|---------------------|---------|---------|--------------------------------------------------|
| `enabled`           | `bool`  | `True`  | Whether context injection is active              |
| `top_k`             | `int`   | `5`     | Number of results to retrieve                    |
| `min_score`         | `float` | `0.1`   | Minimum relevance score threshold                |
| `max_context_tokens`| `int`   | `2048`  | Maximum total tokens in injected context         |

### How It Works

1. The user's query is searched against the memory backend.
2. Results below `min_score` are filtered out.
3. Results are truncated to fit within `max_context_tokens`.
4. A system message is prepended to the conversation with the formatted context:

```
The following context was retrieved from the knowledge base.
Use it to inform your response, citing sources where applicable:

[Source: docs/intro.md] OpenJarvis is a modular AI framework...

[Source: docs/config.md] Configuration is stored in TOML format...
```

### Disabling Context Injection

=== "CLI"

    ```bash
    jarvis ask --no-context "Tell me about Python"
    ```

=== "Python SDK"

    ```python
    response = j.ask("Tell me about Python", context=False)
    ```

---

## CLI Usage

```bash
# Index a directory
jarvis memory index ./docs/

# Index with custom chunking
jarvis memory index ./notes/ --chunk-size 256 --chunk-overlap 32

# Search the memory store
jarvis memory search "machine learning"

# Search with more results
jarvis memory search -k 10 "neural networks"

# Show memory statistics
jarvis memory stats
```

## SDK Usage

```python
from openjarvis import Jarvis

j = Jarvis()

# Index documents
result = j.memory.index("./docs/", chunk_size=512, chunk_overlap=64)
print(f"Indexed {result['chunks']} chunks")

# Search
results = j.memory.search("configuration", top_k=3)
for r in results:
    print(f"  [{r['score']:.4f}] {r['source']}: {r['content'][:80]}...")

# Statistics
stats = j.memory.stats()
print(f"Backend: {stats['backend']}, Documents: {stats.get('count', 'N/A')}")

# Clean up
j.close()
```

===== END FILE: docs\user-guide\memory.md =====

===== FILE: docs\user-guide\agents.md | 44922 bytes | sha16 48e11037c3e50ae8 | last commit 2026-09-04 =====

# Agents

Agents are the agentic logic layer of OpenJarvis. They determine how a query is processed -- whether it goes directly to a model, through a tool-calling loop, via ReAct reasoning, CodeAct code execution, recursive decomposition, or an external agent runtime. All agents implement the `BaseAgent` ABC and are registered via the `AgentRegistry`.

## Overview

| Agent               | Registry Key      | `accepts_tools` | Multi-turn | Description                                  |
|---------------------|-------------------|-----------------|------------|----------------------------------------------|
| `SimpleAgent`       | `simple`          | No              | No         | Single-turn query-to-response                |
| `OrchestratorAgent` | `orchestrator`    | Yes             | Yes        | Multi-turn tool-calling loop (function_calling + structured) |
| `NativeReActAgent`  | `native_react`    | Yes             | Yes        | Thought-Action-Observation loop              |
| `NativeOpenHandsAgent` | `native_openhands` | Yes          | Yes        | CodeAct-style code execution + tool calls    |
| `RLMAgent`          | `rlm`             | Yes             | Yes        | Recursive LM with persistent REPL            |
| `OpenHandsAgent`    | `openhands`       | No              | Yes        | Wraps real openhands-sdk                     |
| `ClaudeCodeAgent`   | `claude_code`     | No              | Yes        | Claude Agent SDK via Node.js subprocess       |
| `OpenCodeAgent`     | `opencode`        | No              | Yes        | [opencode](https://opencode.ai) coding agent on your local engine |
| `OperativeAgent`    | `operative`       | Yes             | Yes        | Persistent scheduled agent with state management |
| `MonitorOperativeAgent` | `monitor_operative` | Yes        | Yes        | Long-horizon agent with 4 configurable strategy axes |

---

## Persistent Persona: SOUL.md, MEMORY.md, USER.md

Every agent's system prompt is assembled at conversation start by the `SystemPromptBuilder`, which injects up to three optional Markdown files -- the **persistent persona**. They are plain text you own and edit, loaded at the start of each conversation. There is no vector database or embedding cache behind them.

| File | What it holds | Example line |
|------|---------------|--------------|
| `SOUL.md` | How the agent should behave -- tone, length, what to push back on | `Be concise. Challenge weak assumptions.` |
| `MEMORY.md` | Facts about you, your projects, your preferences | `I deploy to Postgres, never MySQL.` |
| `USER.md` | Who you are -- role, team, context | `Backend engineer at Acme, on the payments team.` |

This persona is distinct from the retrieval [memory backend](memory.md): the persona is always-on Markdown context loaded into the prompt, while the memory backend is searchable long-term storage the agent queries on demand.

### Where they live

By default the files are read from the config directory:

```
~/.openjarvis/SOUL.md
~/.openjarvis/MEMORY.md
~/.openjarvis/USER.md
```

(The config directory honors `$OPENJARVIS_HOME` / `$XDG_DATA_HOME` when set.) The paths are configurable under `[memory_files]`:

```toml
[memory_files]
soul_path    = "~/.openjarvis/SOUL.md"
memory_path  = "~/.openjarvis/MEMORY.md"
user_path    = "~/.openjarvis/USER.md"
persona_name = ""    # optional named persona -- see below
```

### How they're loaded

At the start of each conversation, `SystemPromptBuilder` reads each file as UTF-8 and adds its contents as a section of the system prompt, after the agent template and before the skill catalog:

- **All three are optional.** A missing or empty file is skipped, so any subset works and an install with no persona files behaves exactly as before.
- **Edits apply to the next conversation.** The files are read once when a conversation's prompt is built, so there is no restart or re-indexing -- edit or delete a line and it takes effect the next time you start a conversation.
- **Each section is length-capped.** Files are truncated to a per-section character budget so a large `MEMORY.md` cannot crowd out the rest of the prompt.

### Named personas

A single install can answer as different personas without changing global config. A named persona lives in its own directory:

```
~/.openjarvis/personas/<name>/SOUL.md
~/.openjarvis/personas/<name>/MEMORY.md
~/.openjarvis/personas/<name>/USER.md
```

Select one per invocation, or opt out entirely:

```bash
jarvis ask --persona work  "summarize my open PRs"
jarvis ask --persona none  "what is 2 + 2?"     # inject no persona
```

Set `persona_name` under `[memory_files]` to make a named persona the default. `persona_name = "none"` (equivalently `--persona none`) disables persona injection for that run.

### Editing them

`SOUL.md`, `MEMORY.md`, and `USER.md` are plain Markdown -- open them in any editor. `MEMORY.md` and `USER.md` can also be updated by the agent itself through the `memory_manage` and `user_profile_manage` tools when those are enabled, so the agent can record a new fact mid-conversation. These tools always target the default `MEMORY.md` and `USER.md` (under `~/.openjarvis/`), never a named persona's copies -- edit those by hand.

---

## BaseAgent ABC

All agents extend the abstract `BaseAgent` class.

```python
from abc import ABC, abstractmethod
from openjarvis.agents._stubs import AgentContext, AgentResult

class BaseAgent(ABC):
    agent_id: str
    accepts_tools: bool = False

    def __init__(
        self,
        engine: InferenceEngine,
        model: str,
        *,
        bus: Optional[EventBus] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> None: ...

    @abstractmethod
    def run(
        self,
        input: str,
        context: AgentContext | None = None,
        **kwargs,
    ) -> AgentResult:
        """Execute the agent on the given input."""
```

The `accepts_tools` class attribute controls whether an agent can receive tools via `--tools` on the CLI or `tools=` in the SDK. Agents with `accepts_tools = False` ignore tool arguments.

`BaseAgent` also provides concrete helper methods (`_emit_turn_start`, `_emit_turn_end`, `_build_messages`, `_generate`, `_max_turns_result`, `_strip_think_tags`) that subclasses use to avoid duplicating common logic. See the [architecture docs](../architecture/agents.md#baseagent-abc) for details.

**ToolUsingAgent** is an intermediate base class (extends `BaseAgent`) that sets `accepts_tools = True` and adds a `ToolExecutor` and `max_turns` loop limit. All tool-using agents extend this class.

### AgentContext

The runtime context handed to an agent on each invocation.

| Field            | Type               | Description                                    |
|------------------|--------------------|------------------------------------------------|
| `conversation`   | `Conversation`     | Message history (pre-filled with context if memory injection is active) |
| `tools`          | `list[str]`        | Tool names available to the agent              |
| `memory_results` | `list[Any]`        | Pre-fetched memory retrieval results           |
| `metadata`       | `dict[str, Any]`   | Arbitrary metadata for the run                 |

### AgentResult

The result returned after an agent completes a run.

| Field          | Type               | Description                                    |
|----------------|--------------------|------------------------------------------------|
| `content`      | `str`              | The final response text                        |
| `tool_results` | `list[ToolResult]` | Results from tool executions during the run    |
| `turns`        | `int`              | Number of turns (inference calls) taken        |
| `metadata`     | `dict[str, Any]`   | Arbitrary metadata about the run               |

---

## SimpleAgent

The `SimpleAgent` is a single-turn agent that sends the query directly to the inference engine and returns the response. It does not support tool calling.

**How it works:**

1. Builds a message list from the conversation context (if provided) plus the user query.
2. Calls the inference engine via `_generate()`.
3. Returns the response as an `AgentResult` with `turns=1`.

**Constructor parameters:**

| Parameter     | Type              | Default | Description                        |
|---------------|-------------------|---------|------------------------------------|
| `engine`      | `InferenceEngine` | --      | The inference engine to use        |
| `model`       | `str`             | --      | Model identifier                   |
| `bus`         | `EventBus`        | `None`  | Event bus for telemetry            |
| `temperature` | `float`           | `0.7`   | Sampling temperature               |
| `max_tokens`  | `int`             | `1024`  | Maximum tokens to generate         |

**When to use:** For straightforward question-answering without tool calling or multi-turn reasoning.

---

## OrchestratorAgent

The `OrchestratorAgent` is a multi-turn agent that implements a tool-calling loop. It is the primary agent for queries that require computation, knowledge retrieval, or structured reasoning. Extends `ToolUsingAgent`.

**How it works:**

1. Builds the initial message list from context and the user query.
2. Sends messages with tool definitions (OpenAI function-calling format) to the engine.
3. If the engine responds with `tool_calls`, the `ToolExecutor` dispatches each call.
4. Tool results are appended as `TOOL` messages and the loop continues.
5. If no `tool_calls` are returned, the response is treated as the final answer.
6. The loop stops after `max_turns` iterations (default: 10), returning whatever content is available along with a `max_turns_exceeded` metadata flag.

**Constructor parameters:**

| Parameter       | Type              | Default | Description                          |
|-----------------|-------------------|---------|--------------------------------------|
| `engine`        | `InferenceEngine` | --      | The inference engine to use          |
| `model`         | `str`             | --      | Model identifier                     |
| `tools`         | `list[BaseTool]`  | `[]`    | Tool instances to make available     |
| `bus`           | `EventBus`        | `None`  | Event bus for telemetry              |
| `max_turns`     | `int`             | `10`    | Maximum number of tool-calling turns |
| `temperature`   | `float`           | `0.7`   | Sampling temperature                 |
| `max_tokens`    | `int`             | `1024`  | Maximum tokens to generate           |
| `mode`          | `str`             | `"function_calling"` | Tool-calling mode (`function_calling` or `structured`) |
| `system_prompt` | `str`             | `None`  | Custom system prompt                 |

**When to use:** For queries that need calculation, memory search, sub-model calls, file reading, or multi-step reasoning.

!!! info "Tool-Calling Loop"
    The orchestrator follows the OpenAI function-calling convention. The engine must support returning `tool_calls` in its response for the loop to engage. If tools are provided but the engine does not return any tool calls, the agent behaves like a single-turn agent.

---

## NativeReActAgent

The `NativeReActAgent` implements a **Thought-Action-Observation** loop following the ReAct pattern. It prompts the LLM to produce structured output (`Thought:`, `Action:`, `Action Input:`, `Final Answer:`) and parses the response to drive tool execution. Extends `ToolUsingAgent`.

Models may also return one complete JSON object, optionally inside a JSON code fence, with `thought`, `action`, and `action_input`, or with `final_answer`. Title Case keys such as `Action Input` are accepted. Tool arguments must be a JSON object or a string containing one. Malformed or ambiguous JSON produces an explicit parsing error without executing a tool. JSON examples embedded in prose are not extracted as actions.

**How it works:**

1. Builds a system prompt with enriched tool descriptions (names, parameter schemas, categories) via `build_tool_descriptions()`. Parsing is case-insensitive.
2. Generates a response and parses the ReAct-structured output.
3. If a `Final Answer:` is found, returns it.
4. If an `Action:` is found, executes the tool and feeds the result back as an `Observation:`.
5. Loops until a final answer is produced or `max_turns` is exceeded.

**Constructor parameters:**

| Parameter     | Type              | Default | Description                        |
|---------------|-------------------|---------|------------------------------------|
| `engine`      | `InferenceEngine` | --      | The inference engine to use        |
| `model`       | `str`             | --      | Model identifier                   |
| `tools`       | `list[BaseTool]`  | `[]`    | Tool instances to make available   |
| `bus`         | `EventBus`        | `None`  | Event bus for telemetry            |
| `max_turns`   | `int`             | `10`    | Maximum number of reasoning turns  |
| `temperature` | `float`           | `0.7`   | Sampling temperature               |
| `max_tokens`  | `int`             | `1024`  | Maximum tokens to generate         |

**When to use:** For queries that benefit from explicit step-by-step reasoning with tool use, where you want visibility into the agent's thought process.

!!! note "Backward compatibility"
    The registry alias `"react"` maps to `NativeReActAgent`. The old import `from openjarvis.agents.react import ReActAgent` also still works.

---

## NativeOpenHandsAgent

The `NativeOpenHandsAgent` is a CodeAct-style agent that generates and executes Python code alongside structured tool calls. It can also pre-fetch URL content from user input to provide direct context to the LLM. Extends `ToolUsingAgent`.

**How it works:**

1. Builds a detailed system prompt with enriched tool descriptions (via shared `build_tool_descriptions()` builder) and code execution instructions.
2. Pre-fetches any URLs in the user input, inlining the content directly.
3. For each turn, generates a response and attempts to extract code blocks or tool calls.
4. Code is executed via `code_interpreter`; tool calls are dispatched via `ToolExecutor`.
5. If neither is found, returns the content as the final answer.

**Constructor parameters:**

| Parameter     | Type              | Default | Description                        |
|---------------|-------------------|---------|------------------------------------|
| `engine`      | `InferenceEngine` | --      | The inference engine to use        |
| `model`       | `str`             | --      | Model identifier                   |
| `tools`       | `list[BaseTool]`  | `[]`    | Tool instances to make available   |
| `bus`         | `EventBus`        | `None`  | Event bus for telemetry            |
| `max_turns`   | `int`             | `3`     | Maximum number of turns            |
| `temperature` | `float`           | `0.7`   | Sampling temperature               |
| `max_tokens`  | `int`             | `2048`  | Maximum tokens to generate         |

**When to use:** For queries involving URL content, code execution, or tasks where the LLM can write and run Python to solve the problem.

---

## RLMAgent

The `RLMAgent` implements recursive decomposition via a persistent REPL, based on the RLM paper. Context is stored as a Python variable rather than injected into the prompt, enabling processing of arbitrarily long inputs through recursive sub-LM calls. Extends `ToolUsingAgent`.

**How it works:**

1. Creates a persistent REPL with `llm_query()` and `llm_batch()` callbacks.
2. Injects context from `AgentContext` into the REPL as a variable.
3. Generates code and executes it in the REPL.
4. If `FINAL(value)` is called, returns the value as the final answer.
5. If no code block is found, treats the content as a direct text answer.

**Constructor parameters:**

| Parameter          | Type              | Default            | Description                        |
|--------------------|-------------------|--------------------|-------------------------------------|
| `engine`           | `InferenceEngine` | --                 | The inference engine to use        |
| `model`            | `str`             | --                 | Model identifier                   |
| `tools`            | `list[BaseTool]`  | `[]`               | Tool instances (optional)          |
| `bus`              | `EventBus`        | `None`             | Event bus for telemetry            |
| `max_turns`        | `int`             | `10`               | Maximum number of code-execute turns |
| `temperature`      | `float`           | `0.7`              | Sampling temperature               |
| `max_tokens`       | `int`             | `2048`             | Maximum tokens to generate         |
| `sub_model`        | `str`             | same as `model`    | Model for sub-LM calls            |
| `sub_temperature`  | `float`           | `0.3`              | Temperature for sub-LM calls       |
| `sub_max_tokens`   | `int`             | `1024`             | Max tokens for sub-LM calls        |
| `max_output_chars` | `int`             | `10000`            | Max REPL output characters         |
| `system_prompt`    | `str`             | `RLM_SYSTEM_PROMPT` | Override the system prompt         |

**When to use:** For long-context tasks that benefit from recursive decomposition, such as summarizing large documents, processing structured data, or tasks that require programmatic manipulation of context.

---

## OpenHandsAgent (SDK)

The `OpenHandsAgent` wraps the real `openhands-sdk` package for AI-driven software development. Extends `BaseAgent` directly (tool management is handled by the SDK internally).

**How it works:**

1. Imports `openhands.sdk` at runtime.
2. Creates an LLM, Agent, and Conversation from the SDK.
3. Sends the input and runs the conversation.
4. Returns the final message content.

**Constructor parameters:**

| Parameter     | Type              | Default       | Description                        |
|---------------|-------------------|---------------|------------------------------------|
| `engine`      | `InferenceEngine` | --            | The inference engine (fallback)    |
| `model`       | `str`             | --            | Model identifier                   |
| `bus`         | `EventBus`        | `None`        | Event bus for telemetry            |
| `temperature` | `float`           | `0.7`         | Sampling temperature               |
| `max_tokens`  | `int`             | `1024`        | Maximum tokens to generate         |
| `workspace`   | `str`             | `os.getcwd()` | Working directory for the agent    |
| `api_key`     | `str`             | `$LLM_API_KEY`| API key for the LLM provider      |

**When to use:** For software development tasks (debugging, code editing, test fixing) where the OpenHands SDK provides a full development agent runtime.

!!! warning "Optional dependency"
    Requires `openhands-sdk` (`uv sync --extra openhands`) and Python 3.12+.

---

## Using Agents

### Via CLI

```bash
# Simple agent
jarvis ask --agent simple "What is the capital of France?"

# Orchestrator with tools
jarvis ask --agent orchestrator --tools calculator,think "What is sqrt(256)?"

# NativeReActAgent
jarvis ask --agent native_react --tools calculator "What is 2+2?"

# ReAct alias (same as native_react)
jarvis ask --agent react --tools calculator,think "Solve step by step: 15% of 340"

# NativeOpenHandsAgent
jarvis ask --agent native_openhands --tools calculator,web_search "Summarize example.com"

# RLMAgent
jarvis ask --agent rlm "Summarize this long document"

# OpenHands SDK agent
jarvis ask --agent openhands "Fix the bug in test_utils.py"
```

### Via Python SDK

```python
from openjarvis import Jarvis

j = Jarvis()

# Simple agent
response = j.ask("Hello", agent="simple")

# Orchestrator with tools
response = j.ask(
    "Calculate 15% of 340",
    agent="orchestrator",
    tools=["calculator"],
)

# NativeReActAgent with tools
response = j.ask(
    "What is sqrt(256)?",
    agent="native_react",
    tools=["calculator", "think"],
)

# Full result with tool details
result = j.ask_full(
    "What is the square root of 144?",
    agent="orchestrator",
    tools=["calculator", "think"],
)
print(result["content"])
print(result["turns"])
print(result["tool_results"])

j.close()
```

---

## ClaudeCodeAgent

The `ClaudeCodeAgent` wraps the `@anthropic-ai/claude-agent-sdk` package via a bundled Node.js subprocess bridge. Unlike the other agents, inference is handled entirely by the Claude Agent SDK -- the `engine` parameter is accepted only for `BaseAgent` interface conformance and is not used.

!!! warning "Requirements"
    Requires Node.js 22+ with npm on `PATH` and an `ANTHROPIC_API_KEY` environment variable (or pass `api_key=` directly). The bundled runner is auto-installed to `~/.openjarvis/claude_code_runner/` on first use.

**How it works:**

1. On first call, copies the bundled `claude_code_runner/` to `~/.openjarvis/claude_code_runner/` and installs the pinned Agent SDK if it is missing or outdated.
2. Builds a JSON request payload (prompt, API key, workspace, allowed tools, system prompt, session ID) and sends it to `stdin` of a `node index.mjs` subprocess.
3. The Node.js runner calls the Claude Agent SDK and writes sentinel-delimited JSON to `stdout`.
4. The Python side parses the output between `---OPENJARVIS_OUTPUT_START---` and `---OPENJARVIS_OUTPUT_END---` markers, extracting content, tool results, and metadata.
5. Returns an `AgentResult` with `turns=1`.

**Constructor parameters:**

| Parameter        | Type              | Default             | Description                                      |
|------------------|-------------------|---------------------|--------------------------------------------------|
| `engine`         | `InferenceEngine` | --                  | Accepted for interface conformance; not used     |
| `model`          | `str`             | --                  | Accepted for interface conformance; not used     |
| `bus`            | `EventBus`        | `None`              | Event bus for telemetry                          |
| `temperature`    | `float`           | `0.7`               | Accepted for interface conformance; not used     |
| `max_tokens`     | `int`             | `1024`              | Accepted for interface conformance; not used     |
| `api_key`        | `str`             | `$ANTHROPIC_API_KEY`| Anthropic API key                                |
| `workspace`      | `str`             | `os.getcwd()`       | Working directory for the Claude agent           |
| `session_id`     | `str`             | `""`                | Optional session ID for conversation continuity  |
| `allowed_tools`  | `list[str]`       | `None` (all)        | Claude Code tool names to allow                  |
| `system_prompt`  | `str`             | `""`                | Additional system prompt for the agent           |
| `timeout`        | `int`             | `300`               | Subprocess timeout in seconds                    |

**When to use:** For software engineering tasks where the Claude Agent SDK's built-in tools (code editing, bash execution, file operations) provide capabilities beyond what OpenJarvis tool-calling agents support.

```python
from openjarvis.agents.claude_code import ClaudeCodeAgent

agent = ClaudeCodeAgent(
    engine=None,          # not used
    model="",             # not used
    workspace="/path/to/project",
    allowed_tools=["Read", "Write", "Bash"],
    timeout=120,
)
result = agent.run("Add type hints to all functions in utils.py")
print(result.content)
```

```bash
# Via CLI
jarvis ask --agent claude_code "Refactor the tests to use pytest fixtures"
```

!!! info "accepts_tools = False"
    `ClaudeCodeAgent` does not accept OpenJarvis tools via `--tools`. Tool access for the Claude agent is configured separately via the `allowed_tools` constructor parameter, which passes tool names understood by the Claude Agent SDK itself.

---

## OpenCodeAgent

The `OpenCodeAgent` delegates coding tasks to [opencode](https://opencode.ai), the open-source coding agent, running it **on your local engine**. opencode handles the agentic loop, file edits, and tool use; OpenJarvis supplies the model — keeping coding-agent work local-first.

!!! warning "Requirements"
    Requires the `opencode` binary on `PATH` (`npm i -g opencode-ai` or `brew install anomalyco/tap/opencode`). It is **not** bundled; `run()` returns a clear error if it is missing. No `ANTHROPIC_API_KEY` needed — inference goes through your OpenJarvis engine.

**How it works:**

1. Derives an OpenAI-compatible base URL from the `engine` (e.g. Ollama/vLLM/llama.cpp at `<host>/v1`) and writes an `opencode.json` in the workspace registering it as an `@ai-sdk/openai-compatible` provider (`openjarvis/<model>`).
2. Spawns a headless `opencode serve` (loopback, random port) and waits for `/global/health`.
3. Creates a session (`POST /session`) and sends the task (`POST /session/{id}/message`) with `model={providerID, modelID}` and the selected `agent` (`build` or `plan`).
4. Parses the returned message `parts` — text parts → `content`, tool parts → `tool_results` — into an `AgentResult`.
5. `close()` disposes the session/server.

**Constructor parameters (selected):**

| Parameter           | Type              | Default          | Description                                              |
|---------------------|-------------------|------------------|----------------------------------------------------------|
| `engine`            | `InferenceEngine` | --               | Used to derive the local OpenAI-compatible provider URL  |
| `model`             | `str`             | --               | Model id served at the provider (e.g. `qwen3:8b`)        |
| `workspace`         | `str`             | `os.getcwd()`    | Directory opencode operates in                           |
| `agent`             | `str`             | `"build"`        | opencode agent: `build` (full access) or `plan` (read-only) |
| `provider_base_url` | `str`             | derived          | Override the engine-derived OpenAI base URL              |
| `provider_id`       | `str`             | `"openjarvis"`   | opencode provider id to register/use                     |
| `model_id`          | `str`             | `model`          | Model id within the provider                             |
| `server_password`   | `str`             | `$OPENCODE_SERVER_PASSWORD` | Optional basic-auth for the opencode server   |
| `timeout`           | `int`             | `600`            | HTTP timeout in seconds                                  |

```python
from openjarvis.agents.opencode import OpenCodeAgent

agent = OpenCodeAgent(engine, "qwen3:8b", workspace="/path/to/project", agent="build")
result = agent.run("Add type hints to utils.py and run the tests")
print(result.content)
agent.close()
```

```bash
# Via CLI (opencode must be installed)
jarvis ask --agent opencode "Refactor the parser to use a state machine"
```

!!! tip "Pass-through providers"
    If the `engine` has no derivable base URL, pass `model` as `provider/model` (e.g. `ollama/llama3`) and opencode resolves it from its own configuration — no `opencode.json` is written.

!!! warning "Model capability matters"
    opencode's agentic loop (planning + correct tool calls + multi-step
    follow-through) needs a reasonably capable model. In testing, a **27B**
    local model (Qwen3.5-27B served via vLLM) solved a 7-task coding suite
    cleanly (create / edit / bug-fix / implement-to-pass-tests / multi-file,
    verified by running the code and tests). An **8B** model (qwen3:8b) was
    unreliable — malformed tool calls, syntactically broken code, and
    half-finished tasks. Prefer a capable local model (or a cloud model) for
    real coding work.

---

## OperativeAgent

The `OperativeAgent` is a persistent, scheduled autonomous agent with built-in session persistence and state recall. Designed for "Operators" -- autonomous agents that run on a schedule with automatic state management between ticks. Extends `ToolUsingAgent`.

**How it works:**

1. **Session loading** -- restores conversation history from previous ticks via the session store.
2. **State recall** -- retrieves previous state JSON from the memory backend.
3. **System prompt injection** -- injects the operator's protocol instructions.
4. **Tool loop** -- standard function-calling loop (same as OrchestratorAgent).
5. **Session save** -- persists the tick's prompt and response to the session store.
6. **State persistence** -- auto-persists state if the agent did not explicitly store it via the `memory_store` tool.

**Constructor parameters:**

| Parameter        | Type              | Default | Description                                      |
|------------------|-------------------|---------|--------------------------------------------------|
| `engine`         | `InferenceEngine` | --      | The inference engine to use                      |
| `model`          | `str`             | --      | Model identifier                                 |
| `tools`          | `list[BaseTool]`  | `[]`    | Tool instances to make available                 |
| `bus`            | `EventBus`        | `None`  | Event bus for telemetry                          |
| `max_turns`      | `int`             | `20`    | Maximum number of tool-calling turns             |
| `temperature`    | `float`           | `0.3`   | Sampling temperature                             |
| `max_tokens`     | `int`             | `2048`  | Maximum tokens to generate                       |
| `system_prompt`  | `str`             | `None`  | Custom system prompt for the operator            |
| `operator_id`    | `str`             | `None`  | Unique ID for session and state persistence      |
| `session_store`  | `Any`             | `None`  | Session store backend for conversation history   |
| `memory_backend` | `Any`             | `None`  | Memory backend for state recall and persistence  |

**When to use:** For autonomous agents that run on a schedule (e.g., via `TaskScheduler`) and need to maintain state between invocations. The agent automatically manages session history and state persistence across ticks.

```python
from openjarvis.agents.operative import OperativeAgent

agent = OperativeAgent(
    engine,
    model="qwen3:8b",
    tools=[...],
    operator_id="daily-report",
    session_store=session_store,
    memory_backend=memory_backend,
    system_prompt="You are a daily report agent. Gather and summarize news.",
)
result = agent.run("Generate today's report")
```

```bash
# Via CLI
jarvis ask --agent operative "Check system status"
```

---

## MonitorOperativeAgent

The `MonitorOperativeAgent` is a long-horizon agent with four configurable strategy axes for managing information across turns and sessions. It extends `ToolUsingAgent` with strategy-driven observation compression, memory extraction, retrieval, and task decomposition. It also inherits cross-session state persistence from the OperativeAgent pattern.

**Strategy axes:**

| Axis | Valid Values | Default | Description |
|------|-------------|---------|-------------|
| `memory_extraction` | `causality_graph`, `scratchpad`, `structured_json`, `none` | `causality_graph` | How findings are persisted to memory |
| `observation_compression` | `summarize`, `truncate`, `none` | `summarize` | How tool outputs are compressed before being added to context |
| `retrieval_strategy` | `hybrid_with_self_eval`, `keyword`, `semantic`, `none` | `hybrid_with_self_eval` | How prior context is recalled at the start of each run |
| `task_decomposition` | `phased`, `monolithic`, `hierarchical` | `phased` | How complex tasks are broken down |

**How it works:**

1. Builds a system prompt with strategy configuration and tool descriptions.
2. Recalls previous state from the memory backend.
3. Loads session history from previous ticks.
4. Runs a function-calling tool loop, applying the configured strategies:
    - **Observation compression**: Long tool outputs are summarized (via LLM) or truncated before being added to the message context.
    - **Memory extraction**: After each tool call, findings are extracted and stored according to the memory strategy (causal relationships, scratchpad notes, or structured JSON).
5. Saves the session and auto-persists state.

**Constructor parameters:**

| Parameter                | Type              | Default                   | Description                                      |
|--------------------------|-------------------|---------------------------|--------------------------------------------------|
| `engine`                 | `InferenceEngine` | --                        | The inference engine to use                      |
| `model`                  | `str`             | --                        | Model identifier                                 |
| `tools`                  | `list[BaseTool]`  | `[]`                      | Tool instances to make available                 |
| `bus`                    | `EventBus`        | `None`                    | Event bus for telemetry                          |
| `max_turns`              | `int`             | `25`                      | Maximum number of tool-calling turns             |
| `temperature`            | `float`           | `0.3`                     | Sampling temperature                             |
| `max_tokens`             | `int`             | `4096`                    | Maximum tokens to generate                       |
| `system_prompt`          | `str`             | `None`                    | Custom system prompt (overrides default)         |
| `memory_extraction`      | `str`             | `"causality_graph"`       | Memory extraction strategy                       |
| `observation_compression`| `str`             | `"summarize"`             | Observation compression strategy                 |
| `retrieval_strategy`     | `str`             | `"hybrid_with_self_eval"` | Retrieval strategy                               |
| `task_decomposition`     | `str`             | `"phased"`                | Task decomposition strategy                      |
| `operator_id`            | `str`             | `None`                    | Unique ID for session and state persistence      |
| `session_store`          | `Any`             | `None`                    | Session store backend for conversation history   |
| `memory_backend`         | `Any`             | `None`                    | Memory backend for state and finding persistence |

**When to use:** For long-horizon benchmark evaluation and complex multi-step tasks that benefit from configurable strategies for memory management, context compression, and task decomposition. Particularly useful for benchmarks like GAIA, FRAMES, and LifelongAgent where strategy selection impacts performance.

```python
from openjarvis.agents.monitor_operative import MonitorOperativeAgent

agent = MonitorOperativeAgent(
    engine,
    model="qwen3:8b",
    tools=[...],
    operator_id="research-agent",
    memory_extraction="causality_graph",
    observation_compression="summarize",
    retrieval_strategy="hybrid_with_self_eval",
    task_decomposition="phased",
    session_store=session_store,
    memory_backend=memory_backend,
)
result = agent.run("Investigate the root cause of the production outage")
```

```bash
# Via CLI
jarvis ask --agent monitor_operative "Analyze the security audit findings"
```

---

## SandboxedAgent

`SandboxedAgent` is a transparent wrapper that runs **any** `BaseAgent` inside a Docker (or Podman) container. It follows the same wrapper pattern as `GuardrailsEngine` -- the inner agent's configuration is serialized and sent to the container's stdin, and the result is read back from stdout.

See also the [`ContainerRunner`](#containerrunner) reference below, which manages the container lifecycle.

**How it works:**

1. Builds a JSON payload with the prompt, wrapped agent ID, and model.
2. Invokes `ContainerRunner.run()`, which starts a container with `--network none` and `--rm`, writes the payload to stdin, and waits for JSON output on stdout.
3. Mount paths are validated against a configurable allowlist before the container is started.
4. Parses the sentinel-delimited output and returns an `AgentResult`.

**Constructor parameters:**

| Parameter              | Type              | Default      | Description                                       |
|------------------------|-------------------|--------------|---------------------------------------------------|
| `agent`                | `BaseAgent`       | --           | The wrapped agent to execute inside the container |
| `runner`               | `ContainerRunner` | --           | Container runner managing Docker lifecycle        |
| `engine`               | `InferenceEngine` | `None`       | Override engine (defaults to wrapped agent's)     |
| `model`                | `str`             | `""`         | Override model (defaults to wrapped agent's)      |
| `workspace`            | `str`             | `""`         | Working directory inside the container            |
| `mounts`               | `list[str]`       | `[]`         | Host paths to bind-mount (read-only)              |
| `secrets`              | `dict[str, str]`  | `{}`         | Injected into payload (not environment variables) |
| `bus`                  | `EventBus`        | `None`       | Event bus for telemetry                           |

```python
from openjarvis.sandbox import ContainerRunner, SandboxedAgent
from openjarvis.agents.simple import SimpleAgent

runner = ContainerRunner(
    image="openjarvis-sandbox:latest",
    timeout=60,
    mount_allowlist_path="/etc/openjarvis/mount_allowlist.json",
)
inner = SimpleAgent(engine, model="qwen3:8b")
agent = SandboxedAgent(
    agent=inner,
    runner=runner,
    mounts=["/home/user/data"],
)
result = agent.run("Summarize the CSV files in /home/user/data")
```

---

## ContainerRunner

`ContainerRunner` manages the Docker (or Podman) container lifecycle for sandboxed execution. It is used directly by `SandboxedAgent` but can also be used standalone.

**Constructor parameters:**

| Parameter              | Type   | Default                      | Description                                    |
|------------------------|--------|------------------------------|------------------------------------------------|
| `image`                | `str`  | `"openjarvis-sandbox:latest"`| Docker image to run                            |
| `timeout`              | `int`  | `300`                        | Max container execution time in seconds        |
| `mount_allowlist_path` | `str`  | `""`                         | Path to JSON mount-allowlist file              |
| `max_concurrent`       | `int`  | `5`                          | Max concurrent containers (informational)      |
| `runtime`              | `str`  | `"docker"`                   | Container runtime binary (`docker` or `podman`)|

**Mount allowlist format:**

```json title="mount_allowlist.json"
{
  "roots": [
    {"path": "/home/user/projects", "read_only": false},
    {"path": "/data/shared", "read_only": true}
  ],
  "blocked_patterns": [".ssh", ".env", "*.pem", "*.key"]
}
```

If `mount_allowlist_path` is not set, no root restriction is applied. Blocked patterns always include `.ssh`, `.env`, `*.pem`, `*.key`, credential files, and cloud config directories by default.

!!! warning "Docker required"
    `ContainerRunner` raises `RuntimeError` if the configured runtime (`docker` or `podman`) is not found on `PATH`.

---

## Agent Registration

Agents are registered via the `@AgentRegistry.register()` decorator. This makes them discoverable by name at runtime:

```python
from openjarvis.core.registry import AgentRegistry

# Check if an agent is registered
AgentRegistry.contains("orchestrator")  # True

# Get the agent class
agent_cls = AgentRegistry.get("orchestrator")

# List all registered agent keys
AgentRegistry.keys()
# ["simple", "orchestrator", "native_react", "react", "native_openhands",
#  "rlm", "openhands", "claude_code", "operative", "monitor_operative"]
```

---

## Event Bus Integration

All agents publish events on the `EventBus` when a bus is provided:

| Event                   | When                                                |
|-------------------------|-----------------------------------------------------|
| `AGENT_TURN_START`      | At the beginning of a run (via `_emit_turn_start`)  |
| `AGENT_TURN_END`        | At the end of a run (via `_emit_turn_end`)          |
| `TOOL_CALL_START`       | Before each tool execution (`ToolUsingAgent` subclasses) |
| `TOOL_CALL_END`         | After each tool execution (`ToolUsingAgent` subclasses)  |

!!! info "Inference events"
    `INFERENCE_START` / `INFERENCE_END` events are published by the `InstrumentedEngine` wrapper, not by agents directly. This keeps telemetry opt-in and transparent to agent code.

These events enable the telemetry and trace systems to record detailed interaction data automatically.

---

## Managed Agent Streaming

The Managed Agent API (`/v1/managed-agents/{id}/messages`) supports **real LLM token streaming** via SSE. Send a message with `stream: true` to receive the model's response tokens as they are generated, rather than waiting for the full response.

### How It Works

The streaming endpoint calls `engine.stream_full()` directly, which yields `StreamChunk` objects containing content tokens, tool-call fragments, and finish reasons. This provides genuine token-by-token streaming from the LLM -- not a post-hoc word replay.

For multi-turn tool-calling agents, the streaming loop automatically:

1. Yields content tokens to the client as they arrive.
2. Accumulates tool-call fragments (OpenAI sends these incrementally).
3. Executes tools when `finish_reason="tool_calls"` is received.
4. Emits tool results as named SSE events (`event: tool_result`).
5. Feeds results back to the LLM for the next turn.
6. Repeats until the model produces a final text response or `max_turns` is reached.

### Streaming Messages

```bash
curl -N -X POST http://localhost:8000/v1/managed-agents/{id}/messages \
  -H "Content-Type: application/json" \
  -d '{"content": "What is 2+2?", "stream": true}'
```

The response follows the OpenAI SSE format:

1. **Content chunks** -- `data: {"choices": [{"delta": {"content": "token"}}]}`
2. **Tool calls** (if the model requests tool use) -- `event: tool_calls\ndata: {"calls": [{"tool_name": "...", "arguments": "..."}]}`
3. **Tool results** -- `event: tool_result\ndata: {"tool_name": "...", "output": "..."}`
4. **Final chunk** -- `data: {"choices": [{"delta": {}, "finish_reason": "stop"}]}`
5. **Done sentinel** -- `data: [DONE]`

When `stream: false` (the default), the endpoint behaves exactly as before -- the message is queued and the agent must be triggered separately via `/run`.

### Behavior Details

- The user message is always stored in the database before streaming starts.
- After streaming completes, the full collected response is persisted as an `agent_to_user` message.
- Conversation history from prior messages is automatically loaded as LLM context.
- The engine's `stream_full()` method is used for real token streaming. Engines that do not override it fall back to the default implementation which wraps the plain `stream()` method.
- If the engine is not available on the server, a `503` error is returned.
- Tool execution during streaming uses the `ToolRegistry` to find and instantiate tools.

### Python Example

```python
import httpx

with httpx.stream(
    "POST",
    "http://localhost:8000/v1/managed-agents/{id}/messages",
    json={"content": "Summarize today's news", "stream": True},
) as response:
    for line in response.iter_lines():
        if line.startswith("data:") and "[DONE]" not in line:
            print(line[5:].strip())
```

===== END FILE: docs\user-guide\agents.md =====

===== FILE: docs\user-guide\morning-digest.md | 7665 bytes | sha16 63f0c2c1eea32593 | last commit 2026-04-03 =====

# Morning Digest

A personalized daily briefing that collects data from your connected services, synthesizes a spoken narrative with a local LLM, and delivers it as audio via text-to-speech.

## Quickstart (5 minutes)

### 1. Install and set up OpenJarvis

```bash
git clone https://github.com/open-jarvis/OpenJarvis.git
cd OpenJarvis
uv sync --extra dev
```

### 2. Start a local LLM via Ollama

```bash
# Install Ollama: https://ollama.com
ollama pull qwen3.5:9b    # or any model you prefer
```

### 3. Configure the digest

Edit `~/.openjarvis/config.toml`:

```toml
[engine]
default = "ollama"

[intelligence]
default_model = "qwen3.5:9b"

[digest]
enabled = true
schedule = "0 6 * * *"          # 6 AM daily (cron syntax)
timezone = "America/Los_Angeles"
persona = "jarvis"
honorific = "sir"               # or "ma'am", "boss", etc.
tts_backend = "cartesia"        # or "openai"
voice_id = "c8f7835e-28a3-4f0c-80d7-c1302ac62aae"  # Alistair (British male)
voice_speed = 1.2
sections = ["health", "messages", "calendar", "world"]

[digest.health]
sources = ["oura"]

[digest.messages]
sources = ["gmail", "google_tasks", "slack", "imessage"]

[digest.calendar]
sources = ["gcalendar"]

[digest.world]
sources = ["weather", "hackernews", "news_rss"]
```

### 4. Connect your data sources

```bash
# Google (one flow covers Gmail, Calendar, Tasks, Contacts, Drive)
jarvis connect gdrive
# Paste: <client_id>:<client_secret> — browser opens automatically

# Oura Ring (personal access token)
jarvis connect oura
# Paste your token from https://cloud.ouraring.com/personal-access-tokens

# Spotify
jarvis connect spotify

# Strava
jarvis connect strava
```

For Weather, GitHub, and News — save credential files directly:

```bash
# Weather (OpenWeatherMap — free at https://openweathermap.org/api)
echo '{"api_key": "YOUR_KEY", "location": "San Francisco,CA,US"}' > ~/.openjarvis/connectors/weather.json

# GitHub notifications (token from https://github.com/settings/tokens)
echo '{"token": "ghp_YOUR_TOKEN"}' > ~/.openjarvis/connectors/github.json

# News RSS (no auth needed — configure your feeds)
cat > ~/.openjarvis/connectors/news_rss.json << 'EOF'
{"feeds": [
  {"name": "Arxiv CS.AI", "url": "https://rss.arxiv.org/rss/cs.AI"},
  {"name": "TechCrunch", "url": "https://techcrunch.com/feed/"},
  {"name": "Bloomberg", "url": "https://feeds.bloomberg.com/markets/news.rss"},
  {"name": "WSJ", "url": "https://feeds.a.dj.com/rss/RSSWorldNews.xml"}
]}
EOF
```

Hacker News, iMessage, and Apple Music work automatically on macOS with no setup.

### 5. Set your TTS API key

```bash
# Cartesia (sign up at https://play.cartesia.ai)
export CARTESIA_API_KEY="sk_car_..."

# Or OpenAI (https://platform.openai.com/api-keys)
export OPENAI_API_KEY="sk-proj-..."
```

### 6. Run your first digest

```bash
CARTESIA_API_KEY="sk_car_..." jarvis digest --fresh
```

The digest will:
1. Collect data from all connected sources
2. Synthesize a spoken briefing with Qwen3.5 9B
3. Generate audio with the Cartesia Alistair voice
4. Print the text and play the audio

## CLI Commands

```bash
jarvis digest --fresh          # Generate a new digest now
jarvis digest                  # Show today's cached digest
jarvis digest --text-only      # Print text without audio
jarvis digest --history        # Show past digests
jarvis digest --schedule "0 6 * * *"   # Set daily schedule
jarvis digest --schedule off   # Disable schedule
jarvis digest --schedule       # Show current schedule
```

## Saying "Good morning"

When chatting with Jarvis (via CLI, desktop, or browser), saying "Good morning" or "morning digest" automatically triggers the digest — no need to use the `digest` command explicitly.

## Configuration Reference

### Sections

The `sections` list controls what the digest covers, in order of priority:

| Section | Sources | What it provides |
|---------|---------|-----------------|
| `health` | `oura`, `apple_health`, `strava` | Sleep, readiness, activity, workouts |
| `messages` | `gmail`, `google_tasks`, `slack`, `notion`, `imessage`, `github_notifications` | Email triage, tasks, texts, Slack, PRs |
| `calendar` | `gcalendar` | Today's events and schedule |
| `world` | `weather`, `hackernews`, `news_rss` | Weather forecast, tech news, RSS feeds |
| `music` | `spotify`, `apple_music` | Recently played tracks (opt-in) |

### TTS Voices

**Cartesia** (recommended — natural, expressive):
| Voice | ID | Description |
|-------|----|-------------|
| Alistair | `c8f7835e-28a3-4f0c-80d7-c1302ac62aae` | Sophisticated British male |
| Benedict | `3c0f09d6-e0d7-499c-a594-70c5b7b93048` | Polished, formal British male |
| Harrison | `df89f42f-f285-4613-adbf-14eedcec4c9e` | Crisp, professional British male |
| Sterling | `b134c304-d095-4d2b-a77a-914f5e8e84e7` | Deep, commanding, dignified |

**OpenAI TTS**:
| Voice | Description |
|-------|-------------|
| `onyx` | Deep male |
| `nova` | Female, warm |
| `alloy` | Neutral |
| `shimmer` | Female, expressive |

### Persona

The `persona` field loads a prompt file from `configs/openjarvis/prompts/personas/{name}.md`. The default `jarvis` persona delivers briefings with dry British wit, prioritizes urgent items, and interprets health data as trends rather than raw numbers.

To create a custom persona, add a new `.md` file in the personas directory.

### News Feeds

Add any RSS or Atom feed to `~/.openjarvis/connectors/news_rss.json`:

```json
{"feeds": [
  {"name": "Arxiv CS.AI", "url": "https://rss.arxiv.org/rss/cs.AI"},
  {"name": "Arxiv CS.LG", "url": "https://rss.arxiv.org/rss/cs.LG"},
  {"name": "NYT Top Stories", "url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"},
  {"name": "TechCrunch", "url": "https://techcrunch.com/feed/"},
  {"name": "Bloomberg Markets", "url": "https://feeds.bloomberg.com/markets/news.rss"},
  {"name": "WSJ World News", "url": "https://feeds.a.dj.com/rss/RSSWorldNews.xml"},
  {"name": "Hacker News", "url": "https://hnrss.org/frontpage"}
]}
```

## API Endpoints

The digest is also available via the FastAPI server:

```bash
jarvis serve  # Start the server

# GET  /api/digest           — Get today's digest text
# GET  /api/digest/audio     — Stream the digest audio (MP3)
# POST /api/digest/generate  — Force re-generation
# GET  /api/digest/history   — Past digests
# GET  /api/digest/schedule  — Current schedule config
# POST /api/digest/schedule  — Update schedule {"enabled": true, "cron": "0 6 * * *"}
```

## Frontend

The desktop and browser apps show an inline audio player when a digest is generated. The "Connect" buttons in the setup wizard handle OAuth flows automatically — click to connect, authorize in the browser popup, done.

## Troubleshooting

**"No digest for today"** — Run `jarvis digest --fresh` to generate one.

**Empty sections** — Check connector status with `jarvis connect --list`. Ensure tokens haven't expired (Google/Spotify tokens expire after 1 hour and are auto-refreshed on next use).

**Weather not working** — OpenWeatherMap API keys can take up to 2 hours to activate after creation. Use the format `City,State,Country` (e.g., `Palo Alto,CA,US`).

**GitHub 403** — Your personal access token needs the `notifications` permission under Account permissions (not Repository permissions).

**Audio not playing** — Ensure `CARTESIA_API_KEY` or `OPENAI_API_KEY` is set. Check credits at https://play.cartesia.ai or https://platform.openai.com.

===== END FILE: docs\user-guide\morning-digest.md =====

===== FILE: docs\user-guide\scheduler.md | 8927 bytes | sha16 21b215b87898d05c | last commit 2026-03-12 =====

# Task Scheduler

The task scheduler lets you run agent queries automatically on a schedule -- once at a future time, on a recurring interval, or via a cron expression. Scheduled tasks are persisted in SQLite so they survive process restarts, and execution is handled by a background daemon thread that polls for due tasks every 60 seconds.

!!! note "Optional component"
    The scheduler is a standalone module (`openjarvis.scheduler`). It is not wired into the default `Jarvis` / `JarvisSystem` startup. You enable it explicitly via `SystemBuilder` or by starting the CLI daemon with `jarvis scheduler start`.

---

## Schedule Types

| `schedule_type` | `schedule_value` format            | Example                     | Meaning                             |
|-----------------|------------------------------------|-----------------------------|-------------------------------------|
| `once`          | ISO 8601 UTC datetime              | `"2026-03-01T09:00:00Z"`    | Run once at that timestamp          |
| `interval`      | Seconds as a string                | `"3600"`                    | Run every hour, starting immediately |
| `cron`          | Standard 5-field cron expression   | `"0 9 * * 1-5"`             | 09:00 UTC, Monday–Friday            |

!!! tip "Cron support"
    Full cron expression support requires `croniter` (`uv pip install croniter`). Without it, the scheduler uses a minimal built-in parser that handles simple `minute hour * * *` patterns only.

---

## CLI Commands

The `jarvis scheduler` subcommand group manages tasks and the daemon from the terminal.

### Start the daemon

```bash
jarvis scheduler start
```

Starts the background polling daemon. The daemon runs in the foreground until interrupted (++ctrl+c++). In production, run it under systemd or launchd (see [Deployment](../deployment/systemd.md)).

### Create a task

```bash
# Run once at a specific time
jarvis scheduler create \
  --prompt "Generate the weekly summary report" \
  --type once \
  --value "2026-03-01T09:00:00Z"

# Run every hour
jarvis scheduler create \
  --prompt "Check for new emails and summarize" \
  --type interval \
  --value "3600" \
  --agent orchestrator \
  --tools retrieval,think

# Run on a cron schedule
jarvis scheduler create \
  --prompt "Summarize overnight logs" \
  --type cron \
  --value "0 8 * * 1-5"
```

### List tasks

```bash
# All tasks
jarvis scheduler list

# Active tasks only
jarvis scheduler list --status active

# Paused tasks
jarvis scheduler list --status paused
```

Example output:

```
ID               AGENT     TYPE       VALUE          STATUS   NEXT RUN
a3f9b12c4d8e    simple    cron       0 8 * * 1-5    active   2026-02-26T08:00:00+00:00
b7c2e56f1a3d    orchestr  interval   3600           active   2026-02-25T14:05:00+00:00
```

### Pause and resume tasks

```bash
# Pause a running task
jarvis scheduler pause a3f9b12c4d8e

# Resume -- next_run is recomputed from the current time
jarvis scheduler resume a3f9b12c4d8e
```

### Cancel a task

```bash
# Permanently cancel (status -> "cancelled", next_run cleared)
jarvis scheduler cancel a3f9b12c4d8e
```

### View run logs

```bash
# Last 10 executions for a task
jarvis scheduler logs a3f9b12c4d8e
```

Example output:

```
Run 1: started=2026-02-25T08:00:01Z finished=2026-02-25T08:00:04Z success=True
  Result: Overnight logs contain 3 warnings and no errors.
Run 2: started=2026-02-24T08:00:00Z finished=2026-02-24T08:00:05Z success=True
  Result: Logs are clean.
```

---

## Python API

```python title="scheduler_example.py"
from openjarvis.scheduler.store import SchedulerStore
from openjarvis.scheduler.scheduler import TaskScheduler

# Set up storage
store = SchedulerStore(db_path="~/.openjarvis/scheduler.db")  # (1)!

# Wire in a JarvisSystem for task execution
from openjarvis import Jarvis
jarvis = Jarvis()

scheduler = TaskScheduler(
    store=store,
    system=jarvis,         # (2)!
    poll_interval=60,      # (3)!
)

# Create tasks
daily_summary = scheduler.create_task(
    prompt="Summarize the latest news headlines",
    schedule_type="cron",
    schedule_value="0 8 * * *",
    agent="simple",
)
print(f"Created task {daily_summary.id}, next run: {daily_summary.next_run}")

# List active tasks
for task in scheduler.list_tasks(status="active"):
    print(f"  {task.id}: {task.prompt} @ {task.next_run}")

# Manage task state
scheduler.pause_task(daily_summary.id)
scheduler.resume_task(daily_summary.id)   # next_run recomputed from now
scheduler.cancel_task(daily_summary.id)  # permanent

# Start the background thread
scheduler.start()   # (4)!

# ... application runs ...

scheduler.stop()
jarvis.close()
```

1. SQLite database storing all task state and run logs.
2. The scheduler calls `system.ask(task.prompt, agent=task.agent, tools=...)` when a task is due. Pass `system=None` for a dry-run mode that logs what it would execute without calling the agent.
3. Seconds between polling cycles. Lower values increase responsiveness at the cost of more SQLite reads.
4. Starts a daemon thread named `"jarvis-scheduler"`. Daemon threads exit automatically when the main process exits.

---

## ScheduledTask Fields

Every task is represented as a `ScheduledTask` dataclass.

| Field            | Type              | Default       | Description                                       |
|------------------|-------------------|---------------|---------------------------------------------------|
| `id`             | `str`             | auto (16 hex) | Unique task identifier                            |
| `prompt`         | `str`             | --            | Query sent to the agent on execution              |
| `schedule_type`  | `str`             | --            | `"cron"`, `"interval"`, or `"once"`              |
| `schedule_value` | `str`             | --            | Cron expression, interval seconds, or ISO datetime|
| `context_mode`   | `str`             | `"isolated"`  | Execution context mode                            |
| `status`         | `str`             | `"active"`    | `"active"`, `"paused"`, `"completed"`, `"cancelled"` |
| `next_run`       | `str` or `None`   | computed      | ISO 8601 UTC datetime of the next execution       |
| `last_run`       | `str` or `None`   | `None`        | ISO 8601 UTC datetime of the last execution       |
| `agent`          | `str`             | `"simple"`    | Agent registry key to use for execution           |
| `tools`          | `str`             | `""`          | Comma-separated tool names for the agent          |
| `metadata`       | `dict`            | `{}`          | Arbitrary metadata for the task                   |

---

## Using Scheduler Tools with Agents

The five scheduler MCP tools (`schedule_task`, `list_scheduled_tasks`, `pause_scheduled_task`, `resume_scheduled_task`, `cancel_scheduled_task`) can be passed to any `ToolUsingAgent`, allowing an agent to schedule follow-up tasks autonomously.

```bash
# Let the orchestrator schedule its own follow-up
jarvis ask --agent orchestrator \
  --tools schedule_task,list_scheduled_tasks \
  "Research transformer architectures and schedule a daily summary at 8am"
```

```python
from openjarvis import Jarvis

j = Jarvis()
response = j.ask(
    "Schedule a weekly digest of research papers every Monday at 9am",
    agent="orchestrator",
    tools=["schedule_task"],
)
print(response)
```

See [Scheduler Tools](tools.md#scheduler-tools) for full parameter reference.

---

## Configuration

Scheduler settings live in the `[scheduler]` section of `~/.openjarvis/config.toml`.

```toml title="~/.openjarvis/config.toml"
[scheduler]
enabled = false
db_path = "~/.openjarvis/scheduler.db"
poll_interval = 60
default_agent = "simple"
```

| Key              | Type   | Default                          | Description                                |
|------------------|--------|----------------------------------|--------------------------------------------|
| `enabled`        | `bool` | `false`                          | Start the scheduler daemon automatically   |
| `db_path`        | `str`  | `~/.openjarvis/scheduler.db`     | SQLite database path                       |
| `poll_interval`  | `int`  | `60`                             | Seconds between polling cycles             |
| `default_agent`  | `str`  | `"simple"`                       | Default agent for tasks that omit `agent`  |

---

## See Also

- [Scheduler Tools reference](tools.md#scheduler-tools) -- MCP tool parameter details
- [Architecture: Agentic Logic](../architecture/agents.md) -- how the scheduler integrates with agents
- [Deployment: systemd](../deployment/systemd.md) -- running the scheduler as a system service

===== END FILE: docs\user-guide\scheduler.md =====

===== FILE: docs\user-guide\cli.md | 19683 bytes | sha16 64572c26a2b936b2 | last commit 2026-09-21 =====

# CLI Reference

OpenJarvis provides a command-line interface through the `jarvis` command. Built on [Click](https://click.palletsprojects.com/), it offers subcommands for querying models, managing memory, running benchmarks, and serving an OpenAI-compatible API.

## Global Options

```bash
jarvis --version   # Print the OpenJarvis version
jarvis --help      # Show top-level help with all subcommands
```

## `jarvis init`

Detect local hardware (CPU, GPU, RAM) and generate a configuration file at `~/.openjarvis/config.toml`.

```bash
jarvis init           # Interactive — refuses to overwrite existing config
jarvis init --force   # Overwrite existing config without prompting
```

| Option    | Description                                   |
|-----------|-----------------------------------------------|
| `--force` | Overwrite existing configuration without prompting |

The `init` command auto-detects:

- **Platform** (Linux, macOS, Windows)
- **CPU** brand and core count
- **RAM** in GB
- **GPU** vendor, model, VRAM, and count (via `nvidia-smi`, `rocm-smi`, or `system_profiler`)

Based on the detected hardware, it recommends an appropriate inference engine and writes a pre-configured TOML file.

**Example output:**

```
Detecting hardware...
  Platform : linux
  CPU      : AMD Ryzen 9 7950X (32 cores)
  RAM      : 64 GB
  GPU      : NVIDIA RTX 4090 (24.0 GB VRAM, x1)

Config written successfully.
```

---

## `jarvis ask`

Send a query to the inference engine (directly or through an agent) and print the response.

```bash
jarvis ask "What is the capital of France?"
```

### Options

| Option                        | Type    | Default    | Description                                           |
|-------------------------------|---------|------------|-------------------------------------------------------|
| `-m`, `--model MODEL`         | string  | auto       | Model to use for inference                             |
| `-e`, `--engine ENGINE`       | string  | auto       | Engine backend (ollama, vllm, llamacpp, etc.)          |
| `-t`, `--temperature TEMP`    | float   | `0.7`      | Sampling temperature                                   |
| `--max-tokens N`              | int     | `1024`     | Maximum tokens to generate                             |
| `--json`                      | flag    | off        | Output raw JSON result instead of plain text           |
| `--no-stream`                 | flag    | off        | Disable streaming (synchronous mode)                   |
| `--no-context`                | flag    | off        | Disable memory context injection                       |
| `-a`, `--agent AGENT`         | string  | config (`simple`) | Agent to use; `""` selects direct mode            |
| `--tools TOOLS`               | string  | none       | Comma-separated tool names to enable                   |
| `-i`, `--image PATH`          | path    | none       | Image file for a vision model (e.g. `gemma3:4b`); repeatable |
| `-S`, `--screen`              | flag    | off        | Capture the current screen and send it to the vision model  |

### Direct Mode vs Agent Mode

**Agent mode** is the default for text queries. When `--agent` is omitted, the CLI uses `agent.default_agent` from configuration, which defaults to `simple`. `SimpleAgent` makes a single inference call without a tool loop, while applying the configured system prompt and persona files (`SOUL.md`, `MEMORY.md`, and `USER.md`).

```bash
jarvis ask "Explain quantum computing"
```

Use `--agent` to select an agent explicitly. Agents such as `orchestrator` can use tools and manage multi-turn interactions:

```bash
jarvis ask --agent orchestrator "What is 2+2?"
jarvis ask --agent orchestrator --tools calculator,think "Calculate sqrt(144) + 3^2"
jarvis ask --agent simple "Hello"
```

**Direct mode** sends the query straight to the inference engine with optional memory context, bypassing the agent's system prompt and persona handling. Pass an empty agent name to select it:

```bash
jarvis ask --agent "" "Explain quantum computing"
```

To make direct mode the default, set `default_agent = ""` in the `[agent]` section of `~/.openjarvis/config.toml`.

### Usage Examples

```bash
# Basic query
jarvis ask "What is machine learning?"

# Specify a model
jarvis ask -m qwen3:8b "Summarize this concept"

# Use the orchestrator agent with tools
jarvis ask --agent orchestrator --tools calculator "What is 15% of 340?"

# Get JSON output
jarvis ask --json "Hello"

# Disable memory context injection
jarvis ask --no-context "Tell me about Python"

# Set maximum token generation
jarvis ask --max-tokens 2048 "Write a detailed essay about AI"
```

### Vision Input

Vision-capable models (such as `gemma3:4b`) can read images alongside your
text prompt. Attach one or more image files with `-i`/`--image`, or capture
the current screen with `-S`/`--screen`:

```bash
# Ask about a local image
jarvis ask -i screenshot.png "What is shown in this image?"

# Send multiple images (the flag is repeatable)
jarvis ask -i chart-a.png -i chart-b.png "Compare these two charts"

# Capture the current screen and ask about it
jarvis ask --screen "Summarize what's on my screen"
```

Vision runs in **direct mode** only. When `--agent` is omitted, image and screen
queries automatically use direct mode, overriding the configured default agent.
If you explicitly select an agent, the image is
ignored and a note is printed — re-run with `--agent ""` to force direct mode.

The Ollama context window can be tuned for large images or long prompts with
the `JARVIS_NUM_CTX` environment variable (default `16384`):

```bash
JARVIS_NUM_CTX=8192 jarvis ask --screen "What's on my screen?"
```

!!! note "Keep vision on-device"
    Images are sensitive. OpenJarvis prints a privacy warning before sending
    an image to a non-local engine, so a screenshot never leaves your machine
    unnoticed. Use a local engine (e.g. `ollama` with `gemma3:4b`) to keep
    vision fully local.

### JSON Output Format

When using `--json` in **direct mode**, the output includes:

```json
{
  "content": "The response text...",
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 85,
    "total_tokens": 97
  }
}
```

When using `--json` in **agent mode**, the output includes:

```json
{
  "content": "The response text...",
  "turns": 3,
  "tool_results": [
    {
      "tool_name": "calculator",
      "content": "51.0",
      "success": true
    }
  ]
}
```

---

## `jarvis model`

Manage and inspect language models available on running engines.

### `jarvis model list`

List all models available from running inference engines, displayed as a Rich table with model parameters, context length, and VRAM requirements.

```bash
jarvis model list
```

**Example output:**

```
           Available Models
┌─────────┬────────────────┬────────┬─────────┬──────┐
│ Engine  │ Model          │ Params │ Context │ VRAM │
├─────────┼────────────────┼────────┼─────────┼──────┤
│ ollama  │ qwen3:8b       │ 8B     │ 32,768  │ 6GB  │
│ ollama  │ llama3.2:3b    │ 3B     │ 8,192   │ 3GB  │
└─────────┴────────────────┴────────┴─────────┴──────┘
```

### `jarvis model info <model>`

Show detailed information about a specific model.

```bash
jarvis model info qwen3:8b
```

**Example output:**

```
┌─ Qwen 3 8B ──────────────────────────────┐
│ Model ID:     qwen3:8b                    │
│ Name:         Qwen 3 8B                   │
│ Parameters:   8B                          │
│ Context:      32,768                      │
│ Quantization: none                        │
│ Min VRAM:     6GB                         │
│ Engines:      ollama, vllm                │
│ Provider:     Alibaba                     │
│ API Key:      not required                │
└───────────────────────────────────────────┘
```

### `jarvis model pull <model>`

Download a model via Ollama. Shows a progress bar during download.

```bash
jarvis model pull qwen3:8b
```

!!! note
    The `pull` command requires a running Ollama instance. It connects to the Ollama API at the host configured in your `config.toml`.

---

## `jarvis pearl`

Access Pearl's native node, wallet, and RPC tools from the OpenJarvis CLI.

```bash
jarvis pearl doctor
jarvis pearl node -- <pearld args>
jarvis pearl wallet -- <oyster args>
jarvis pearl ctl -- <prlctl args>
jarvis pearl address
```

All Pearl wrapper commands use the `jarvis pearl <command>` shape. The
pass-through commands map to Pearl's native binaries:

| OpenJarvis command | Pearl binary | Use |
|--------------------|--------------|-----|
| `jarvis pearl doctor` | n/a | Check whether `pearld`, `oyster`, and `prlctl` are discoverable |
| `jarvis pearl node` | `pearld` | Run the Pearl full node |
| `jarvis pearl wallet` | `oyster` | Run the Oyster wallet daemon |
| `jarvis pearl ctl` | `prlctl` | Query Pearl node or wallet RPC |
| `jarvis pearl address` | `prlctl --wallet getnewaddress` | Generate a wallet address from Oyster |

Use `PEARL_HOME=/path/to/pearl` or `--pearl-home /path/to/pearl` if Pearl's
`bin/` directory is not on `PATH`. See the [Pearl CLI guide](pearl.md) for
examples.

---

## `jarvis memory`

Manage the document memory store for retrieval-augmented generation.

### `jarvis memory index <path>`

Index documents from a file or directory into the memory store.

```bash
jarvis memory index ./docs/
jarvis memory index ./notes.md
jarvis memory index ./data/ --chunk-size 256 --chunk-overlap 32
jarvis memory index ./docs/ --backend sqlite
```

| Option                      | Type   | Default | Description                          |
|-----------------------------|--------|---------|--------------------------------------|
| `--backend`, `-b`           | string | config  | Override the default memory backend  |
| `--chunk-size`              | int    | `512`   | Chunk size in tokens                 |
| `--chunk-overlap`           | int    | `64`    | Overlap between chunks in tokens     |

The ingestion pipeline supports text, markdown, code files, and PDF (with `pdfplumber` installed). Binary files and hidden directories are automatically skipped.

### `jarvis memory search <query>`

Search the memory store for relevant document chunks.

```bash
jarvis memory search "machine learning basics"
jarvis memory search -k 10 "neural networks"
jarvis memory search --backend faiss "embeddings"
```

| Option             | Type   | Default | Description                          |
|--------------------|--------|---------|--------------------------------------|
| `--top-k`, `-k`    | int    | `5`     | Number of results to return          |
| `--backend`, `-b`  | string | config  | Override the default memory backend  |

Results are displayed in a table with rank, score, source file, and a content preview.

### `jarvis memory stats`

Show memory store statistics including document count and database size.

```bash
jarvis memory stats
jarvis memory stats --backend sqlite
```

| Option             | Type   | Default | Description                          |
|--------------------|--------|---------|--------------------------------------|
| `--backend`, `-b`  | string | config  | Override the default memory backend  |

---

## `jarvis telemetry`

Query and manage inference telemetry data stored in SQLite.

### `jarvis telemetry stats`

Show aggregated telemetry statistics including total calls, tokens, cost, and latency, broken down by model and engine.

```bash
jarvis telemetry stats
jarvis telemetry stats -n 5    # Show top 5 models
```

| Option          | Type | Default | Description                   |
|-----------------|------|---------|-------------------------------|
| `-n`, `--top`   | int  | `10`    | Number of top models to show  |

### `jarvis telemetry export`

Export raw telemetry records in JSON or CSV format.

```bash
jarvis telemetry export                          # JSON to stdout
jarvis telemetry export --format csv             # CSV to stdout
jarvis telemetry export --format json -o data.json  # JSON to file
jarvis telemetry export -f csv -o metrics.csv    # CSV to file
```

| Option                | Type   | Default  | Description                     |
|-----------------------|--------|----------|---------------------------------|
| `-f`, `--format`      | choice | `json`   | Output format: `json` or `csv`  |
| `-o`, `--output`      | path   | stdout   | Output file path                |

### `jarvis telemetry clear`

Delete all telemetry records from the database.

```bash
jarvis telemetry clear         # Interactive confirmation
jarvis telemetry clear --yes   # Skip confirmation
```

| Option         | Type | Default | Description                   |
|----------------|------|---------|-------------------------------|
| `-y`, `--yes`  | flag | off     | Skip confirmation prompt      |

!!! warning
    This permanently deletes all stored telemetry data. Use `--yes` to skip the confirmation prompt in automated scripts.

---

## `jarvis bench`

Run inference benchmarks against a running engine.

### `jarvis bench run`

Execute benchmarks and report results.

```bash
jarvis bench run                               # Run all benchmarks, 10 samples
jarvis bench run -n 20                         # 20 samples per benchmark
jarvis bench run -b latency                    # Only the latency benchmark
jarvis bench run -b throughput -n 50 --json    # Throughput, 50 samples, JSON output
jarvis bench run -o results.jsonl              # Write JSONL results to file
jarvis bench run -m qwen3:8b -e ollama         # Specific model and engine
```

| Option                     | Type   | Default | Description                              |
|----------------------------|--------|---------|------------------------------------------|
| `-m`, `--model MODEL`      | string | auto    | Model to benchmark                       |
| `-e`, `--engine ENGINE`    | string | auto    | Engine backend                           |
| `-n`, `--samples N`        | int    | `10`    | Number of samples per benchmark          |
| `-b`, `--benchmark NAME`   | string | all     | Specific benchmark to run                |
| `-o`, `--output PATH`      | path   | none    | Write JSONL results to file              |
| `--json`                   | flag   | off     | Output JSON summary to stdout            |

Available benchmarks:

- **latency** -- Measures per-call inference latency (mean, p50, p95, min, max)
- **throughput** -- Measures tokens-per-second throughput

---

## `jarvis channel`

Manage messaging channels for multi-platform communication. Channels connect directly to platform APIs (Telegram, Discord, Slack, etc.) -- no gateway required.

### `jarvis channel list`

List registered channel backends and their connection status.

```bash
jarvis channel list
```

### `jarvis channel send`

Send a message to a specific channel.

```bash
jarvis channel send slack "Hello from Jarvis!"
jarvis channel send discord "Build complete"
```

| Argument    | Type   | Description                          |
|-------------|--------|--------------------------------------|
| `TARGET`    | string | Channel name to send to              |
| `MESSAGE`   | string | Message content                      |

### `jarvis channel status`

Show connection status for configured channels.

```bash
jarvis channel status
```

!!! note "Channel Dependencies"
    Each channel requires its platform-specific credentials (bot tokens, API keys) configured in the `[channel.<platform>]` section of your config. See [Configuration](../getting-started/configuration.md) for details.

---

## `jarvis serve`

Start an OpenAI-compatible API server.

```bash
jarvis serve                                 # Default host/port from config
jarvis serve --port 8000                     # Custom port
jarvis serve --host 0.0.0.0 --port 9000      # Bind to all interfaces
jarvis serve --model qwen3:8b                # Specify default model
jarvis serve --agent orchestrator            # Route requests through an agent
```

| Option                   | Type   | Default | Description                              |
|--------------------------|--------|---------|------------------------------------------|
| `--host HOST`            | string | config  | Bind address                             |
| `--port PORT`            | int    | config  | Port number                              |
| `-e`, `--engine ENGINE`  | string | auto    | Engine backend                           |
| `-m`, `--model MODEL`    | string | config  | Default model for inference              |
| `-a`, `--agent AGENT`    | string | none    | Agent for non-streaming requests         |

!!! note "Server Dependencies"
    The `serve` command requires the server extra:

    ```bash
    uv sync --extra server
    ```

    This installs FastAPI, uvicorn, and related dependencies.

### API Endpoints

The server exposes the following OpenAI-compatible endpoints:

| Method | Path                     | Description                    |
|--------|--------------------------|--------------------------------|
| POST   | `/v1/chat/completions`   | Chat completions (streaming & non-streaming) |
| GET    | `/v1/models`             | List available models          |
| GET    | `/health`                | Health check                   |
| GET    | `/v1/channels`           | List available messaging channels    |
| POST   | `/v1/channels/send`      | Send a message to a channel          |
| GET    | `/v1/channels/status`    | Channel bridge connection status     |

**Example with curl:**

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3:8b",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

When an agent is configured (e.g., `--agent orchestrator`), non-streaming requests are routed through the agent with access to all registered tools. For tool-capable agents (`orchestrator`, `react`, `openhands`), all registered tools are automatically loaded and made available.

---

## LLM-guided spec search (no CLI yet)

LLM-guided spec search (the frontier-driven harness-learning subsystem)
is exposed as a Python library only — there is currently no top-level
`jarvis` subcommand for it. Construct a `SpecSearchOrchestrator`
directly from `openjarvis.learning.spec_search.orchestrator` and call
`.run(trigger)` with a trigger from
`openjarvis.learning.spec_search.triggers`. See
[`docs/user-guide/llm-guided-spec-search.md`](llm-guided-spec-search.md)
for the architecture and the building blocks
(`splits.py`, external corpora, `external_adapter`).

===== END FILE: docs\user-guide\cli.md =====

===== FILE: docs\user-guide\channels.md | 23191 bytes | sha16 e99b2f414438cc03 | last commit 2026-03-27 =====

# Channels

The channels module lets OpenJarvis send and receive messages through external messaging platforms. Each platform has a dedicated channel implementation that connects directly to the platform's API -- there is no intermediate gateway.

!!! note "Channels are disabled by default"
    The `[channel]` config section defaults to `enabled = false`. You must set `enabled = true` and configure platform-specific credentials before channel features become active.

---

## Overview

Channel messaging is built around the `BaseChannel` ABC. Each platform (Telegram, Discord, Slack, WhatsApp, etc.) has its own implementation registered via `@ChannelRegistry.register("name")`. Channels connect directly to their platform APIs, register handlers for incoming messages, and send outgoing messages.

```mermaid
graph LR
    A[Your Code] -->|send| B[TelegramChannel / DiscordChannel / SlackChannel / ...]
    B -->|Platform API| C[Telegram / Discord / Slack / ...]
    C -->|incoming messages| B
    B -->|on_message handlers| D[Your Handlers]
```

---

## Supported Channels

| Channel | Registry Key | Platform | Pip Extra | Auth |
|---------|-------------|----------|-----------|------|
| `SendBlueChannel` | `sendblue` | SendBlue iMessage/SMS API | — | API key + secret |
| `TelegramChannel` | `telegram` | Telegram Bot API | `channel-telegram` | Bot token |
| `DiscordChannel` | `discord` | Discord Bot API | `channel-discord` | Bot token |
| `SlackChannel` | `slack` | Slack Web API | `channel-slack` | Bot + App tokens |
| `WhatsAppChannel` | `whatsapp` | WhatsApp Business API | — | API token |
| `WhatsAppBaileysChannel` | `whatsapp_baileys` | WhatsApp (Baileys) | — | QR code auth |
| `WebhookChannel` | `webhook` | Generic HTTP webhook | — | URL + optional secret |
| `EmailChannel` | `email` | SMTP/IMAP email | — | Email credentials |
| `SignalChannel` | `signal` | Signal Messenger | — | Signal CLI |
| `GoogleChatChannel` | `google_chat` | Google Chat | — | Service account |
| `IRCChannel` | `irc` | IRC | — | Server credentials |
| `WebChatChannel` | `webchat` | Browser-based chat | — | None |
| `TeamsChannel` | `teams` | Microsoft Teams | — | Bot credentials |
| `MatrixChannel` | `matrix` | Matrix protocol | — | Homeserver + token |
| `MattermostChannel` | `mattermost` | Mattermost | — | Bot token |
| `FeishuChannel` | `feishu` | Feishu/Lark | — | App credentials |
| `BlueBubblesChannel` | `bluebubbles` | iMessage (BlueBubbles) | — | BlueBubbles server |
| `LineChannel` | `line` | LINE Messaging API | `channel-line` | Channel access token |
| `ViberChannel` | `viber` | Viber Bot API | `channel-viber` | Auth token |
| `MessengerChannel` | `messenger` | Facebook Messenger | `channel-messenger` | Page access token |
| `RedditChannel` | `reddit` | Reddit API | `channel-reddit` | OAuth credentials |
| `MastodonChannel` | `mastodon` | Mastodon API | `channel-mastodon` | Access token |
| `XMPPChannel` | `xmpp` | XMPP/Jabber | `channel-xmpp` | JID + password |
| `RocketChatChannel` | `rocketchat` | Rocket.Chat API | `channel-rocketchat` | User credentials |
| `ZulipChannel` | `zulip` | Zulip API | `channel-zulip` | Bot email + API key |
| `TwitchChannel` | `twitch` | Twitch IRC/API | `channel-twitch` | OAuth token |
| `NostrChannel` | `nostr` | Nostr protocol | `channel-nostr` | Private key (nsec) |

---

## Using a Channel

### Connecting

```python title="connect.py"
from openjarvis.channels.telegram import TelegramChannel

channel = TelegramChannel(
    bot_token="YOUR_BOT_TOKEN",  # (1)!
)
channel.connect()

print(channel.status())  # ChannelStatus.CONNECTED
```

1. Falls back to the `TELEGRAM_BOT_TOKEN` environment variable if not provided.

### Sending Messages

```python title="send_message.py"
from openjarvis.channels.telegram import TelegramChannel

channel = TelegramChannel()
channel.connect()

# Send to a chat by ID
ok = channel.send(
    "123456789",
    "Analysis complete. Results are ready.",
    conversation_id="thread-abc123",  # optional, for threading
)

if ok:
    print("Message delivered")
else:
    print("Delivery failed")

channel.disconnect()
```

### Receiving Messages

Register handler callbacks before calling `connect()`. Each handler receives a `ChannelMessage` and can optionally return a reply string.

```python title="receive_messages.py"
from openjarvis.channels._stubs import ChannelMessage
from openjarvis.channels.discord_channel import DiscordChannel

channel = DiscordChannel()


def handle_incoming(msg: ChannelMessage) -> None:
    print(f"[{msg.channel}] {msg.sender}: {msg.content}")
    print(f"  conversation_id={msg.conversation_id}")
    print(f"  message_id={msg.message_id}")


channel.on_message(handle_incoming)  # (1)!
channel.connect()                    # (2)!

# Messages now arrive asynchronously via the background listener thread
# Your main thread can continue doing other work
```

1. Register one or more handlers. All registered handlers are called for every incoming message.
2. `connect()` starts the background listener thread after establishing the platform connection.

### Listing Available Channels

```python title="list_channels.py"
from openjarvis.channels.slack import SlackChannel

channel = SlackChannel()
channel.connect()
channels = channel.list_channels()
print(channels)  # ["general", "random", "dev"]
```

### Disconnecting

```python title="disconnect.py"
channel.disconnect()
# Stops the listener thread and closes the platform connection
# Status becomes ChannelStatus.DISCONNECTED
```

---

## ChannelMessage Fields

Every incoming message is delivered to handlers as a `ChannelMessage` dataclass.

| Field | Type | Description |
|-------|------|-------------|
| `channel` | `str` | Name of the channel the message arrived on |
| `sender` | `str` | Identifier of the message sender |
| `content` | `str` | Message text |
| `message_id` | `str` | Unique message identifier (may be empty) |
| `conversation_id` | `str` | Thread/conversation identifier (may be empty) |
| `session_id` | `str` | Session identifier (may be empty) |
| `metadata` | `dict[str, Any]` | Additional platform-specific metadata |

---

## Event Bus Integration

Pass an `EventBus` to publish channel events to the rest of the system:

```python title="channel_events.py"
from openjarvis.core.events import EventBus, EventType
from openjarvis.channels.telegram import TelegramChannel

bus = EventBus()


def on_received(event):
    print(f"Message received on {event.data['channel']}: {event.data['content']}")


def on_sent(event):
    print(f"Message sent to {event.data['channel']}")


bus.subscribe(EventType.CHANNEL_MESSAGE_RECEIVED, on_received)
bus.subscribe(EventType.CHANNEL_MESSAGE_SENT, on_sent)

channel = TelegramChannel(bus=bus)
channel.connect()
```

| Event | Published When | Data Keys |
|-------|----------------|-----------|
| `CHANNEL_MESSAGE_RECEIVED` | A message arrives from the platform | `channel`, `sender`, `content`, `message_id` |
| `CHANNEL_MESSAGE_SENT` | A message is successfully sent | `channel`, `content`, `conversation_id` |

---

## CLI Commands

The `jarvis channel` subcommand group provides quick access to channel operations.

### List Channels

```bash
jarvis channel list
```

### Send a Message

```bash
# Send to a channel by name
jarvis channel send telegram "Build completed successfully"
```

### Show Status

```bash
jarvis channel status
```

---

## API Server Endpoints

When `jarvis serve` is running, three channel endpoints are available. Channels must be configured and enabled in `[channel]` for these endpoints to return data.

### `GET /v1/channels`

Returns the list of registered channels and their status.

```bash
curl http://localhost:8000/v1/channels
```

```json
{
  "channels": ["telegram", "discord", "slack"],
  "status": "connected"
}
```

If no channels are configured:
```json
{"channels": [], "message": "No channels configured"}
```

### `POST /v1/channels/send`

Send a message to a channel.

```bash
curl -X POST http://localhost:8000/v1/channels/send \
  -H "Content-Type: application/json" \
  -d '{"channel": "telegram", "content": "Hello!", "conversation_id": "conv-1"}'
```

```json
{"status": "sent", "channel": "telegram"}
```

Required fields: `channel`, `content`. `conversation_id` is optional.

### `GET /v1/channels/status`

Returns the connection status for each configured channel.

```bash
curl http://localhost:8000/v1/channels/status
```

```json
{"status": "connected"}
```

Possible values: `connected`, `disconnected`, `connecting`, `error`, `not_configured`.

---

## Configuration

Channel settings live in the `[channel]` section of `~/.openjarvis/config.toml`. Each platform has its own nested sub-section.

```toml title="~/.openjarvis/config.toml"
[channel]
enabled = true
default_channel = ""
default_agent = "simple"

[channel.telegram]
bot_token = "YOUR_TELEGRAM_BOT_TOKEN"

[channel.discord]
bot_token = "YOUR_DISCORD_BOT_TOKEN"

[channel.slack]
bot_token = "YOUR_SLACK_BOT_TOKEN"
app_token = "YOUR_SLACK_APP_TOKEN"
```

### Configuration Reference

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `enabled` | `bool` | `false` | Enable channel messaging |
| `default_channel` | `str` | `""` | Default channel to use when not specified |
| `default_agent` | `str` | `simple` | Agent to use for handling inbound messages |

Platform-specific settings are configured in nested sub-sections (e.g., `[channel.telegram]`, `[channel.discord]`).

---

## Complete Example

This example connects a Telegram channel, registers a handler that echoes messages back, sends a test message, and then disconnects after a short wait.

```python title="full_example.py"
import time
from openjarvis.channels._stubs import ChannelMessage
from openjarvis.channels.telegram import TelegramChannel
from openjarvis.core.events import EventBus

bus = EventBus()
channel = TelegramChannel(
    bot_token="YOUR_BOT_TOKEN",
    bus=bus,
)

received_messages = []


def on_message(msg: ChannelMessage) -> None:
    received_messages.append(msg)
    print(f"Received from {msg.sender} on #{msg.channel}: {msg.content}")


channel.on_message(on_message)
channel.connect()

# List available channels
channels = channel.list_channels()
print(f"Available channels: {channels}")

# Send a message
if channels:
    channel.send(channels[0], "Hello from OpenJarvis!")

# Wait for incoming messages
time.sleep(10)

channel.disconnect()
print(f"Total messages received: {len(received_messages)}")
```

---

## SendBlue (iMessage / SMS)

`SendBlueChannel` is registered as `"sendblue"` in `ChannelRegistry` and gives your agent a **dedicated phone number** that people can text via iMessage (blue bubbles) or SMS. It uses the [SendBlue API](https://docs.sendblue.com/) -- no Apple hardware or BlueBubbles server required.

### How It Works

```
Your phone  ──text──▶  SendBlue  ──webhook──▶  ngrok tunnel  ──▶  OpenJarvis
                                                                       │
Your phone  ◀──iMessage──  SendBlue  ◀──API call──  DeepResearch agent ◀┘
```

When someone texts the SendBlue number, SendBlue POSTs the message to your webhook. OpenJarvis sends an immediate "Message received!" acknowledgment, runs the DeepResearch agent, and sends the response back via iMessage.

### Setup (Browser UI)

The easiest way is through the Agents UI:

1. Go to **Agents → your agent → Messaging** tab
2. Click **Set Up** on "iMessage / SMS"
3. Click **Open SendBlue signup** -- create a free account (no credit card required)
4. In the SendBlue dashboard, copy your **API Key ID** and **API Secret Key**
5. Paste them into the form and click **Verify & Find Number**
6. If on the free tier (shared line), copy the phone number shown under "Send from" in your SendBlue dashboard and paste it
7. Click **Activate Phone Number**

### Tunnel Setup (Required)

Since OpenJarvis runs locally, you need a tunnel so SendBlue can reach your webhook:

```bash
# Install ngrok (one time)
brew install ngrok

# Sign up at https://dashboard.ngrok.com/signup (free)
# Then configure your auth token:
ngrok config add-authtoken YOUR_TOKEN

# Start the tunnel (keep this running)
ngrok http 8222
```

Register the ngrok URL as your SendBlue webhook. You can do this via the API:

```bash
curl -X PUT https://api.sendblue.co/api/account/webhooks \
  -H "sb-api-key-id: YOUR_KEY" \
  -H "sb-api-secret-key: YOUR_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"webhooks": {"receive": ["https://YOUR-NGROK-URL.ngrok-free.dev/webhooks/sendblue"]}}'
```

Or set it in the SendBlue dashboard under **Webhooks**.

### SendBlue Free Tier Notes

- **Shared line**: Your agent uses a shared phone number (no dedicated number)
- **Verified contacts only**: Recipients must be added as verified contacts in the SendBlue dashboard first
- **10 contacts max**: Free tier allows up to 10 verified contacts
- **iMessage preferred**: SendBlue sends via iMessage when possible, falls back to SMS

To get a dedicated number, upgrade to a paid SendBlue plan.

### Programmatic Setup

```python title="sendblue_setup.py"
from openjarvis.channels.sendblue import SendBlueChannel

channel = SendBlueChannel(
    api_key_id="YOUR_API_KEY_ID",         # or SENDBLUE_API_KEY_ID env var
    api_secret_key="YOUR_API_SECRET_KEY", # or SENDBLUE_API_SECRET_KEY env var
    from_number="+16452468235",           # or SENDBLUE_FROM_NUMBER env var
)
channel.connect()

# Send a message
ok = channel.send("+15551234567", "Hello from OpenJarvis!")
```

### Webhook Endpoint

The server exposes `POST /webhooks/sendblue` which:

1. Sends an instant acknowledgment: "Message received! Researching your data now..."
2. Routes the message to the DeepResearch agent via the ChannelBridge
3. If processing takes >45 seconds, sends: "Still working -- complex query, hang tight..."
4. Sends the full research response back via iMessage/SMS

### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key_id` | `str` | `""` | SendBlue API key ID (falls back to `SENDBLUE_API_KEY_ID` env var) |
| `api_secret_key` | `str` | `""` | SendBlue API secret key (falls back to `SENDBLUE_API_SECRET_KEY` env var) |
| `from_number` | `str` | `""` | SendBlue phone number to send from (falls back to `SENDBLUE_FROM_NUMBER` env var) |
| `webhook_secret` | `str` | `""` | Optional secret for verifying incoming webhook requests |
| `bus` | `EventBus` | `None` | Event bus for publishing channel events |

### Configuration

```toml title="~/.openjarvis/config.toml"
[channel.sendblue]
api_key_id = "YOUR_API_KEY_ID"
api_secret_key = "YOUR_API_SECRET_KEY"
from_number = "+16452468235"
```

### CLI Usage

```bash
# Set credentials via environment variables
export SENDBLUE_API_KEY_ID="your_key"
export SENDBLUE_API_SECRET_KEY="your_secret"
export SENDBLUE_FROM_NUMBER="+16452468235"

# Check channel status
jarvis channel status --channel-type sendblue

# Send a message
jarvis channel send sendblue "+15551234567" "Hello from Jarvis!"
```

### Server Restart Behavior

SendBlue bindings are **automatically restored on server restart**. When `jarvis serve` starts:

1. The server checks the database for existing SendBlue channel bindings
2. Re-creates the `SendBlueChannel` instance with stored credentials
3. Re-wires the `ChannelBridge` with a `DeepResearchAgent`
4. Incoming webhooks resume working immediately

**However, if using ngrok:** The tunnel URL changes on every ngrok restart. You must re-register the new URL with SendBlue:

```bash
# Start ngrok (get new URL)
ngrok http 8222

# Register the new webhook URL
curl -X PUT https://api.sendblue.co/api/account/webhooks \
  -H "sb-api-key-id: YOUR_KEY" \
  -H "sb-api-secret-key: YOUR_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"webhooks": {"receive": ["https://NEW-NGROK-URL.ngrok-free.dev/webhooks/sendblue"]}}'
```

!!! tip "Stable tunnel URL"
    Ngrok paid plans provide a fixed subdomain that persists across restarts. Alternatively, use [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) for a free, stable URL.

### Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Message received!" ack sent but no response | DeepResearch agent timed out or errored | Check server logs for errors |
| No ack, no response | Webhook URL not reachable | Verify ngrok is running; re-register webhook URL |
| "Disconnected" badge in Messaging tab | Server restarted without restoring bindings | Click "Reconnect" in the UI |
| SendBlue returns 401 | Invalid API credentials | Re-enter API key and secret in Messaging tab |
| "Contacts must text this number first" | Free tier requires verified contacts | Add the recipient in SendBlue dashboard under Contacts |
| Messages arrive but are not processed | Channel bridge not wired | Remove and re-add the SendBlue binding in Messaging tab |

### Health Check

The server exposes `GET /v1/channels/sendblue/health` which returns:

```json
{
  "channel_connected": true,
  "bridge_wired": true,
  "ready": true
}
```

If `ready` is `false`, the Messaging tab shows a "Disconnected" badge with a "Reconnect" button.

---

## WhatsAppBaileysChannel

`WhatsAppBaileysChannel` is registered as `"whatsapp_baileys"` in `ChannelRegistry` and provides **bidirectional WhatsApp messaging** using the Baileys protocol. It spawns a Node.js bridge subprocess that handles QR-code authentication, incoming message forwarding, and outbound message delivery.

!!! warning "Node.js 22+ required"
    The Baileys bridge is a compiled Node.js application bundled inside the package. It is auto-installed to `~/.openjarvis/whatsapp_baileys_bridge/` on first `connect()` call. If `node` is not found on `PATH`, `connect()` logs an error and sets the channel to `ChannelStatus.ERROR`.

!!! note "WhatsApp account required"
    WhatsApp does not offer an official API for personal accounts. Baileys operates on the WhatsApp Web protocol. You must scan a QR code with your WhatsApp mobile app to authenticate on first use.

### Connecting

```python title="whatsapp_connect.py"
from openjarvis.channels.whatsapp_baileys import WhatsAppBaileysChannel

channel = WhatsAppBaileysChannel(
    assistant_name="Jarvis",           # (1)!
    assistant_has_own_number=False,    # (2)!
)
channel.connect()  # spawns the Node.js bridge subprocess
```

1. Display name used in conversation context.
2. Set `True` if the assistant has a dedicated WhatsApp number and should not filter its own messages.

On first connection, the bridge will print a QR code to the terminal. Scan it with the WhatsApp app on your phone to authenticate. Authentication state is saved to `~/.openjarvis/whatsapp_baileys_bridge/auth/` and reused on subsequent connections.

### Receiving Messages

```python title="whatsapp_receive.py"
from openjarvis.channels._stubs import ChannelMessage
from openjarvis.channels.whatsapp_baileys import WhatsAppBaileysChannel

channel = WhatsAppBaileysChannel()


def on_message(msg: ChannelMessage) -> None:
    print(f"[{msg.sender}] {msg.content}")
    # msg.conversation_id is the WhatsApp JID (e.g. "15551234567@s.whatsapp.net")


channel.on_message(on_message)
channel.connect()

# Background reader thread is running; your code continues here
```

### Sending Messages

Messages are addressed by WhatsApp **JID** (Jabber ID) -- the canonical identifier for a WhatsApp contact or group.

```python title="whatsapp_send.py"
# Individual contact JID format: <country-code><number>@s.whatsapp.net
# Group JID format: <group-id>@g.us

ok = channel.send(
    "15551234567@s.whatsapp.net",      # JID of the recipient
    "Hello from OpenJarvis!",
)

if not ok:
    print("Send failed -- check that the bridge is connected")
```

### Disconnecting

```python title="whatsapp_disconnect.py"
channel.disconnect()
# Sends disconnect command to bridge, terminates subprocess, stops reader thread
```

### Constructor Parameters

| Parameter                  | Type       | Default     | Description                                            |
|----------------------------|------------|-------------|--------------------------------------------------------|
| `auth_dir`                 | `str`      | `~/.openjarvis/whatsapp_baileys_bridge/auth` | Baileys auth state directory |
| `assistant_name`           | `str`      | `"Jarvis"`  | Display name for the assistant                         |
| `assistant_has_own_number` | `bool`     | `False`     | Whether the assistant has a dedicated WhatsApp number  |
| `bus`                      | `EventBus` | `None`      | Event bus for publishing channel events                |

### Bridge Events

The Node.js bridge communicates with Python via JSON lines on stdio. Python interprets the following event types:

| Bridge event type | Effect                                                      |
|-------------------|-------------------------------------------------------------|
| `status`          | Updates `ChannelStatus` (`connected` / `disconnected`)      |
| `qr`              | Logs "QR code received -- scan to authenticate"             |
| `message`         | Dispatches to all registered `on_message` handlers          |
| `error`           | Logs the error and sets status to `ChannelStatus.ERROR`     |

### Event Bus Integration

When a `bus` is provided, `WhatsAppBaileysChannel` publishes the same events as other channels:

| Event | Published When | Data Keys |
|-------|----------------|-----------|
| `CHANNEL_MESSAGE_RECEIVED` | An inbound WhatsApp message arrives | `channel`, `sender`, `content`, `message_id` |
| `CHANNEL_MESSAGE_SENT` | A message is successfully sent | `channel`, `content`, `conversation_id` |

### Configuration

WhatsApp Baileys channel settings live in the `[channel.whatsapp_baileys]` subsection:

```toml title="~/.openjarvis/config.toml"
[channel.whatsapp_baileys]
auth_dir = "/home/user/.openjarvis/whatsapp_baileys_bridge/auth"
assistant_name = "Jarvis"
assistant_has_own_number = false
```

---

## See Also

- [Architecture: Channels](../architecture/channels.md) -- listener loop internals and channel design
- [API Reference: Channels](../api-reference/openjarvis/channels/index.md) -- full class and type signatures
- [Getting Started: Configuration](../getting-started/configuration.md) -- full config reference
- [User Guide: Agents](agents.md) -- agent system documentation

===== END FILE: docs\user-guide\channels.md =====

# Connect SocialBu to AI clients

SocialBu uses one hosted Streamable HTTP MCP server:

```text
https://socialbu.com/mcp
```

There is no server to run and no API key to copy. A compatible client opens SocialBu in your browser so you can sign in and authorize the connection.

## Portable configuration

Use this shape in clients that accept the standard `mcpServers` configuration:

```json
{
  "mcpServers": {
    "socialbu": {
      "type": "streamable-http",
      "url": "https://socialbu.com/mcp"
    }
  }
}
```

Some clients use `http` as the name for Streamable HTTP:

```json
{
  "mcpServers": {
    "socialbu": {
      "type": "http",
      "url": "https://socialbu.com/mcp"
    }
  }
}
```

After saving the configuration, start the client's MCP sign-in or reconnect flow. Finish authorization on `socialbu.com`.

## Client instructions

### ChatGPT

Until SocialBu is available in the ChatGPT app directory, add it as a custom MCP app:

1. Open **Settings → Apps → Advanced settings** and enable developer mode.
2. Select **Create app**.
3. Enter `SocialBu` and `https://socialbu.com/mcp`.
4. Complete the SocialBu authorization flow.

The exact menu labels can vary by ChatGPT plan and workspace policy. Workspace administrators may need to allow custom apps.

### Codex

Install this repository as an Agent Plugin when it is listed in the plugin directory. For a direct connection, add the `socialbu` entry from [`.mcp.json`](../.mcp.json) to your Codex MCP configuration, then sign in when Codex asks to authenticate.

The included [`skills/socialbu`](../skills/socialbu) instructions teach Codex how to select tools and handle publishing and destructive actions safely.

### Cursor

Add the remote server in Cursor settings, or save the following as `.cursor/mcp.json` in a project:

```json
{
  "mcpServers": {
    "socialbu": {
      "url": "https://socialbu.com/mcp"
    }
  }
}
```

Cursor supports Streamable HTTP with OAuth. Use **Settings → Tools & MCP** to authenticate or inspect the connection. Cursor also understands the portable `plugin.json` and `mcp.json` in this repository when installed as an Agent Plugin.

### Claude Code

Install the SocialBu plugin marketplace and plugin:

```text
/plugin marketplace add socialbu/socialbu-agent
/plugin install socialbu@socialbu-agent
```

For MCP-only installation:

```bash
claude mcp add --transport http socialbu https://socialbu.com/mcp
```

Run `/mcp` in Claude Code to complete OAuth authorization or inspect connection status.

### Claude.ai and Claude Desktop

Add `https://socialbu.com/mcp` as a custom connector from the connector settings available to your plan or organization. Organization administrators may need to add and enable it before members can connect their accounts.

### Gemini CLI

Install the complete extension from GitHub:

```bash
gemini extensions install https://github.com/socialbu/socialbu-agent
```

Restart Gemini CLI after installation. It reads `gemini-extension.json` and discovers the bundled SocialBu skill automatically.

### GitHub Copilot

Copilot CLI can connect directly:

```bash
copilot mcp add --transport http socialbu https://socialbu.com/mcp
```

In VS Code, create `.vscode/mcp.json`:

```json
{
  "servers": {
    "socialbu": {
      "type": "http",
      "url": "https://socialbu.com/mcp"
    }
  }
}
```

Open that file and select **Start** or **Auth** above the server entry to complete OAuth. GitHub Copilot's cloud coding agent and cloud code review do not currently support OAuth-protected remote MCP servers, so use SocialBu from Copilot CLI or IDE agent mode instead.

### Windsurf

Open **Windsurf Settings → Cascade → MCP Servers**, add a remote HTTP server named `socialbu`, and use `https://socialbu.com/mcp`. If your Windsurf version cannot complete OAuth for a remote MCP server, update the client before connecting.

### Cline and Roo Code

Open the MCP Servers panel, choose remote Streamable HTTP, and add `https://socialbu.com/mcp` as `socialbu`. Complete the browser authorization when the extension prompts you.

### Zed

Add SocialBu as a remote MCP server from the Agent Panel settings. Use `https://socialbu.com/mcp` as the URL and authenticate through the browser when prompted.

### OpenCode

Add a remote MCP entry to `opencode.json`:

```json
{
  "mcp": {
    "socialbu": {
      "type": "remote",
      "url": "https://socialbu.com/mcp",
      "enabled": true
    }
  }
}
```

Run `opencode mcp auth socialbu` to authorize the connection.

### Grok Build

Install SocialBu from the Grok plugin marketplace when its listing is available. The repository also contains [Grok plugin metadata](../.grok-plugin/plugin.json) for direct or organization-managed installation.

### Qwen Code and other MCP clients

Use the portable `mcpServers` configuration at the top of this page. The client must support all three of these features:

- MCP Streamable HTTP
- OAuth authorization-server discovery
- Dynamic client registration or another standards-compatible OAuth client flow

DeepSeek is a model provider rather than one install target. Any DeepSeek-powered agent client with those MCP features can connect to the same endpoint.

## Troubleshooting

- **The client asks for an API key:** choose the OAuth or remote HTTP connection type. SocialBu does not require a pasted key.
- **Authorization restarts or reports an invalid target:** remove the old connection and add it again using the exact `https://socialbu.com/mcp` URL.
- **Tools are missing:** reconnect, then check your SocialBu plan, team role, and connected accounts. The server returns only the tools and data available to the signed-in user.
- **A client supports only local stdio servers:** use a maintained MCP remote-to-stdio bridge that supports OAuth, or use the [SocialBu CLI](https://github.com/socialbu/socialbu-cli). Do not place session tokens in configuration files.

For product setup help, see the [SocialBu MCP page](https://socialbu.com/mcp-server). Packaging issues belong in this repository's [issue tracker](https://github.com/socialbu/socialbu-agent/issues).

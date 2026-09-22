# Contributing

SocialBu product behavior and MCP tools are implemented in the private SocialBu application. This repository packages the official remote server for agent clients.

Use an issue for client compatibility problems or documentation gaps. Include the client name and version, the installation method, and the error text with tokens and private workspace data removed.

For a pull request:

1. Keep every MCP manifest pointed at `https://socialbu.com/mcp`.
2. Update all package versions together when releasing a new version.
3. Keep `skills/socialbu/SKILL.md` focused on real tools exposed by the hosted server.
4. Run `python scripts/validate.py` before opening the pull request.

Do not add API keys, OAuth tokens, signed upload URLs, account data, or screenshots containing private information.

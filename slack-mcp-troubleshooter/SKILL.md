---
name: slack-mcp-troubleshooter
description: Diagnose and fix Cohere's Slack MCP servers in Claude Code (`slack` prod and `slack-mcp-dev`). Use when a Slack MCP tool fails, a server shows "failed" or "not authenticated" in /mcp, or you see HTTP 503 loading OAuth metadata, `invalid_token`, "bearer token is invalid, expired, or no longer recognized", "already exists in local config", or CONNECT_TIMEOUT. Also use when the user asks "is slack mcp working?", "re-add the slack mcp", or "which slack server should I use?". Checks config, server reachability and auth, then gives the one fix that matches the symptom.
version: 1.0.0
author: Divy Sharma
license: MIT
---

# Slack MCP Troubleshooter

Cohere runs two Slack MCP servers. Most "it's broken" reports are one of four things, and each has a different fix. Work out which one before changing anything.

## The two servers

| Name | URL | Auth | Notes |
|---|---|---|---|
| `slack-mcp-dev` | `https://slack-mcp-dev.coherehealth.com/mcp` | `/mcp` menu in Claude Code | Newer. Compact responses (50-87% smaller), `compact=false` for the full payload. Read-only. |
| `slack` (prod) | `https://slack-mcp-prod.coherehealth.com/mcp` | Older browser OAuth redirect | Older and flakier. Dev is meant to replace it. |

Both are Twingate-gated. Run them side by side: keep `slack` on prod and add `slack-mcp-dev` for the new one.

## Step 1: Find the symptom

Run these in parallel. Do not skip to a fix.

1. **Config**: read `~/.claude.json` and look for `slack` / `slack-mcp-dev` under `projects.<path>.mcpServers`. The entry is per project folder, so a server can be "missing" only because you are in a different folder.
2. **Reachability** (no auth needed):
   ```
   curl -s -m 8 -o /dev/null -w "%{http_code}\n" https://slack-mcp-dev.coherehealth.com/.well-known/oauth-authorization-server
   curl -s -m 8 -o /dev/null -w "%{http_code}\n" https://slack-mcp-prod.coherehealth.com/.well-known/oauth-authorization-server
   ```
3. **Auth** (dev only, if its tools are loaded): call `slack_check_auth`. It returns `authenticated` and a `user_id`.

Do not use `claude mcp get <name>` for this. It tries to connect and can hang past the 2 minute shell timeout.

## Step 2: Match the symptom to the fix

| What you see | What it means | Fix |
|---|---|---|
| HTTP 200 on the probe and `authenticated: true` | Working | Nothing to do. Use the tools. |
| `HTTP 503 trying to load OAuth metadata` | Server is restarting or redeploying | Wait a minute, then `/mcp` > server > Reconnect. Do not reconfigure. |
| `invalid_token` / "bearer token is invalid, expired, or no longer recognized" | Server restarted and dropped its in-memory token | `/mcp` > `slack-mcp-dev` > Authenticate. The client re-registers and gets a new token. Do not re-add the server. |
| `MCP server <name> already exists in local config` from `claude mcp add` | The entry is already there | Harmless. Skip the add and go to the row above. |
| Probe returns `000`, or CONNECT_TIMEOUT after 30s | Host not reachable from this machine | Check Twingate is connected, then `/mcp` > Reconnect. If still dead, ask the server owner whether that environment is deployed. |
| Server missing in this folder only | Config is per project | Add it from this folder (below). |

## Step 3: Re-add a server only if it is really missing

```
claude mcp add --transport http slack-mcp-dev https://slack-mcp-dev.coherehealth.com/mcp
claude mcp add --transport http slack https://slack-mcp-prod.coherehealth.com/mcp
```

Or in MCP config JSON:

```json
{
  "mcpServers": {
    "slack-mcp-dev": { "type": "http", "url": "https://slack-mcp-dev.coherehealth.com/mcp" },
    "slack": { "type": "http", "url": "https://slack-mcp-prod.coherehealth.com/mcp" }
  }
}
```

Re-adding the same URL never fixes a network or token problem. It only fixes a missing entry.

## Step 4: Verify

After any fix, call `slack_check_auth` again and re-run the reachability probe. Report each server separately: working, auth expired, or unreachable. If prod is down and dev works, say so and carry on with dev.

## Common mistakes

- **Reconfiguring when the token expired.** The fix is Authenticate in `/mcp`, not a new `claude mcp add`.
- **Treating prod and dev as one thing.** One can be healthy while the other is down.
- **Using `claude mcp get` as a health check.** It hangs on an unreachable server. Use the curl probe.
- **Assuming the fix worked.** Confirm with `slack_check_auth`.

## Gotchas

- The token lives in server memory, so every server restart means re-auth.
- Tools return raw Slack user IDs. Resolve them with `slack_get_users`.
- Dev may be renamed or replaced once it is promoted to prod. Check the URLs in this file are still current.

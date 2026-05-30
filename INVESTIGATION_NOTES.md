# OpenJarvis Investigation Notes

## Goals
- Produce a working documented OpenJarvis agent
- Fix frontend/backend/desktop architecture drift across the full system
- Improve desktop reliability and startup behavior
- Update setup, architecture, troubleshooting, and WSL2 documentation

## Current symptoms
- Desktop splash screen can take about 2m30s before UI appears
- Desktop launches backend with:
  - `uv run jarvis serve --port 8010 --agent simple`
- Some UI areas appear disconnected from the backend, including splash/startup components
- App no longer hangs forever after adding a Tauri non-stream fallback for chat
- Desktop chat still shows:
  - `Error: Failed to fetch`
  - `Client error '400 Bad Request' for url 'http://172.16.33.200:11434/api/chat'`
- This suggests some paths still call Ollama directly or send the wrong payload to Ollama
- The repository contains frontend, backend, desktop/Tauri, and documentation files including WSL2 materials

## Changes already made
### frontend/src/lib/api.ts
Added:

```ts
export async function chatOnce(request: {
  model: string;
  messages: Array<{ role: string; content: string }>;
  temperature?: number;
  max_tokens?: number;
}): Promise<any> {
  const res = await fetch(`${getBase()}/v1/chat/completions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ...request,
      stream: false,
    }),
  });
  if (!res.ok) throw new Error(`Chat request failed: ${res.status}`);
  return res.json();
}

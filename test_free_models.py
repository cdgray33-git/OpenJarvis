"""
Test all free OpenRouter models and report which ones are responding.
Run from anywhere:
    python test_free_models.py

Output: working models printed at the end, ready to paste into CommandPalette.tsx
"""

import asyncio
import json
import sys
from pathlib import Path

import httpx

FREE_MODELS = [
    "nex-agi/nex-n2-pro:free",
    "nvidia/nemotron-3.5-content-safety:free",
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "poolside/laguna-xs.2:free",
    "poolside/laguna-m.1:free",
    "google/gemma-4-26b-a4b-it:free",
    "google/gemma-4-31b-it:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "liquid/lfm-2.5-1.2b-thinking:free",
    "liquid/lfm-2.5-1.2b-instruct:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
    "nvidia/nemotron-nano-12b-v2-vl:free",
    "qwen/qwen3-next-80b-a3b-instruct:free",
    "nvidia/nemotron-nano-9b-v2:free",
    "openai/gpt-oss-120b:free",
    "openai/gpt-oss-20b:free",
    "qwen/qwen3-coder:free",
    "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "nousresearch/hermes-3-llama-3.1-405b:free",
]

def load_key() -> str:
    env_file = Path.home() / ".openjarvis" / "cloud-keys.env"
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line.startswith("OPENROUTER_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise ValueError("OPENROUTER_API_KEY not found in cloud-keys.env")


async def test_model(client: httpx.AsyncClient, model: str, key: str) -> tuple[str, str, str]:
    """Returns (model, status, detail)"""
    try:
        resp = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json={
                "model": model,
                "messages": [{"role": "user", "content": "hi"}],
                "max_tokens": 10,
            },
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://openjarvis.local",
                "X-Title": "OpenJarvis",
            },
            timeout=30,
        )
        if resp.status_code == 200:
            return (model, "OK", "")
        else:
            try:
                body = resp.json()
                msg = body.get("error", {}).get("message", resp.text[:120])
            except Exception:
                msg = resp.text[:120]
            return (model, f"FAIL {resp.status_code}", msg)
    except httpx.TimeoutException:
        return (model, "TIMEOUT", "No response in 30s")
    except Exception as e:
        return (model, "ERROR", str(e)[:120])


async def main():
    key = load_key()
    print(f"Testing {len(FREE_MODELS)} free models against OpenRouter...\n")

    results = []
    # Run in batches of 5 to avoid hammering the API
    batch_size = 5
    async with httpx.AsyncClient() as client:
        for i in range(0, len(FREE_MODELS), batch_size):
            batch = FREE_MODELS[i:i + batch_size]
            batch_results = await asyncio.gather(
                *[test_model(client, m, key) for m in batch]
            )
            for model, status, detail in batch_results:
                results.append((model, status, detail))
                icon = "✅" if status == "OK" else "❌"
                detail_str = f" — {detail}" if detail else ""
                print(f"  {icon} {status:<12} {model}{detail_str}")
            # Small pause between batches
            if i + batch_size < len(FREE_MODELS):
                await asyncio.sleep(2)

    working = [m for m, s, _ in results if s == "OK"]
    failing = [(m, s, d) for m, s, d in results if s != "OK"]

    print(f"\n{'='*60}")
    print(f"RESULTS: {len(working)} working / {len(failing)} failing\n")

    if working:
        print("WORKING MODELS:")
        for m in working:
            print(f"  {m}")

    if failing:
        print(f"\nFAILING MODELS:")
        for m, s, d in failing:
            print(f"  {s:<12} {m}")

    # Print CommandPalette-ready format
    print(f"\n{'='*60}")
    print("CommandPalette.tsx entries (copy-paste ready):\n")
    for m in working:
        label = m.split("/")[1].replace(":free", "").replace("-", " ").title()
        print(f'  {{ id: "openrouter/{m}", name: "{label} (free)", provider: "openrouter" }},')


if __name__ == "__main__":
    asyncio.run(main())
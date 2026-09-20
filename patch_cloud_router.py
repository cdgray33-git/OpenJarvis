"""
Patch script for cloud_router.py
Fixes:
  1. 429 retry logic - response body not drained before context exit
  2. Adds HTTP-Referer and X-Title headers required by OpenRouter free tier
  3. Cleans up duplicate debug print imports
Run from anywhere:
  python patch_cloud_router.py
  python patch_cloud_router.py --path "C:/custom/path/cloud_router.py"
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Target file
# ---------------------------------------------------------------------------

DEFAULT_PATH = Path("C:/Windows/System32/OpenJarvis/backend/routers/cloud_router.py")

def get_target(args: list[str]) -> Path:
    for i, arg in enumerate(args):
        if arg == "--path" and i + 1 < len(args):
            return Path(args[i + 1])
    return DEFAULT_PATH

# ---------------------------------------------------------------------------
# Patch definitions  (old, new)
# ---------------------------------------------------------------------------

PATCHES = [
    # ------------------------------------------------------------------
    # 1. Fix _stream_openai: add required headers + drain body on 429
    # ------------------------------------------------------------------
    (
        # OLD
        """\
    _retry_delays = [5, 10, 20]
    async with httpx.AsyncClient(timeout=180) as client:
        for _attempt, _delay in enumerate([0] + _retry_delays):
            if _delay:
                import sys; print(f"[RETRY] 429 received, waiting {_delay}s", flush=True, file=sys.stderr)
                await asyncio.sleep(_delay)
            async with client.stream(
                "POST",
                f"{base_url}/chat/completions",
                json=payload,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
            ) as resp:
                if resp.status_code == 429:
                    if _attempt < len(_retry_delays):
                        continue
                    yield "\\n\\nRate limited by OpenRouter. Try a different model or wait a moment."
                    return
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line.startswith("data: "):
                        continue
                    data = line[6:].strip()
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                        delta = chunk["choices"][0]["delta"].get("content") or ""
                        if delta:
                            yield delta
                    except Exception:
                        pass
                return""",
        # NEW
        """\
    _retry_delays = [5, 10, 20]
    async with httpx.AsyncClient(timeout=180) as client:
        for _attempt, _delay in enumerate([0] + _retry_delays):
            if _delay:
                print(f"[RETRY] 429 received, waiting {_delay}s", flush=True, file=sys.stderr)
                await asyncio.sleep(_delay)
            try:
                async with client.stream(
                    "POST",
                    f"{base_url}/chat/completions",
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://openjarvis.local",
                        "X-Title": "OpenJarvis",
                    },
                ) as resp:
                    if resp.status_code == 429:
                        # Must drain body before exiting stream context
                        await resp.aread()
                        if _attempt < len(_retry_delays):
                            print(f"[RETRY] 429 on attempt {_attempt}, retrying...", flush=True, file=sys.stderr)
                            continue
                        yield "\\n\\nRate limited by OpenRouter. Try a different model or wait a moment."
                        return
                    resp.raise_for_status()
                    async for line in resp.aiter_lines():
                        if not line.startswith("data: "):
                            continue
                        data = line[6:].strip()
                        if data == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data)
                            delta = chunk["choices"][0]["delta"].get("content") or ""
                            if delta:
                                yield delta
                        except Exception:
                            pass
                    return
            except httpx.HTTPStatusError:
                if _attempt < len(_retry_delays):
                    continue
                raise""",
    ),

    # ------------------------------------------------------------------
    # 2. Clean up the inline debug print in _stream_openai
    #    (removes the bare `import sys;` inline style)
    # ------------------------------------------------------------------
    (
        "    actual_model = model.removeprefix(\"openrouter/\")\n"
        "    import sys; print(f\"[DEBUG] OpenRouter model string: {actual_model!r}\", flush=True, file=sys.stderr)\n",

        "    actual_model = model.removeprefix(\"openrouter/\")\n"
        "    print(f\"[DEBUG] OpenRouter model string: {actual_model!r}\", flush=True, file=sys.stderr)\n",
    ),

    # ------------------------------------------------------------------
    # 3. Clean up the same inline import in stream_local (Ollama path)
    # ------------------------------------------------------------------
    (
        "    actual_model = model.removeprefix(\"openrouter/\")\n"
        "    import sys; print(f\"[DEBUG] OpenRouter model string: {actual_model!r}\", flush=True, file=sys.stderr)\n"
        "    payload = {\n"
        "        \"model\": actual_model,\n"
        "        \"messages\": _to_openai_msgs(messages),\n"
        "        \"stream\": True,\n",

        "    actual_model = model.removeprefix(\"openrouter/\")\n"
        "    print(f\"[DEBUG] Ollama model string: {actual_model!r}\", flush=True, file=sys.stderr)\n"
        "    payload = {\n"
        "        \"model\": actual_model,\n"
        "        \"messages\": _to_openai_msgs(messages),\n"
        "        \"stream\": True,\n",
    ),

    # ------------------------------------------------------------------
    # 4. Ensure `sys` is imported at the top level (not inline)
    #    Insert after the existing `import asyncio` line
    # ------------------------------------------------------------------
    (
        "import asyncio\nimport httpx\n",
        "import asyncio\nimport sys\nimport httpx\n",
    ),
]

# ---------------------------------------------------------------------------
# Apply patches
# ---------------------------------------------------------------------------

def apply(target: Path) -> None:
    if not target.exists():
        print(f"[ERROR] File not found: {target}")
        sys.exit(1)

    original = target.read_text(encoding="utf-8")
    patched = original

    # Guard: don't double-apply
    if '"HTTP-Referer": "https://openjarvis.local"' in original:
        print("[INFO] Patch already applied — nothing to do.")
        sys.exit(0)

    for i, (old, new) in enumerate(PATCHES, 1):
        if old not in patched:
            print(f"[WARN] Patch {i}: target string not found — skipping.")
            continue
        patched = patched.replace(old, new, 1)
        print(f"[OK]   Patch {i} applied.")

    if patched == original:
        print("[WARN] No changes made. File may already be patched or structure differs.")
        sys.exit(1)

    # Backup
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = target.with_suffix(f".py.bak_{stamp}")
    shutil.copy2(target, backup)
    print(f"[OK]   Backup saved → {backup.name}")

    target.write_text(patched, encoding="utf-8")
    print(f"[OK]   Patched file written → {target}")
    print("\nDone. Restart the OpenJarvis backend for changes to take effect.")


if __name__ == "__main__":
    target = get_target(sys.argv[1:])
    print(f"[INFO] Target: {target}\n")
    apply(target)
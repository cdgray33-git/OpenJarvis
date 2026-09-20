"""
Patch script for CommandPalette.tsx
Replaces the OpenRouter free model list with only the 15 confirmed working models.
Keeps: openrouter/auto and openrouter/owl-alpha (non-free entries)
Removes: 7 confirmed failing models + kimi-k2.6 (404) + glm-4.5-air (untested)
Adds: all 15 confirmed working free models from test_free_models.py

Run:
    python patch_commandpalette.py
    python patch_commandpalette.py --path "C:/custom/path/CommandPalette.tsx"
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime

DEFAULT_PATH = Path("C:/Windows/System32/OpenJarvis/frontend/src/components/CommandPalette.tsx")

def get_target(args: list[str]) -> Path:
    for i, arg in enumerate(args):
        if arg == "--path" and i + 1 < len(args):
            return Path(args[i + 1])
    return DEFAULT_PATH

# ---------------------------------------------------------------------------
# The old model list (lines 66-80)
# ---------------------------------------------------------------------------

OLD_MODELS = """\
      { id: 'openrouter/auto', desc: 'Auto \u2014 best model for the task' },
      { id: 'openrouter/qwen/qwen3-coder:free', desc: 'Qwen3 Coder 480B \u2014 free' },
      { id: 'openrouter/openai/gpt-oss-120b:free', desc: 'GPT OSS 120B \u2014 free' },
      { id: 'openrouter/openai/gpt-oss-20b:free', desc: 'GPT OSS 20B \u2014 free' },
      { id: 'openrouter/nousresearch/hermes-3-llama-3.1-405b:free', desc: 'Hermes 3 405B \u2014 free' },
      { id: 'openrouter/meta-llama/llama-3.3-70b-instruct:free', desc: 'Llama 3.3 70B \u2014 free' },
      { id: 'openrouter/nvidia/nemotron-3-ultra-550b-a55b:free', desc: 'Nemotron Ultra 550B \u2014 free' },
      { id: 'openrouter/nvidia/nemotron-3-super-120b-a12b:free', desc: 'Nemotron Super 120B \u2014 free' },
      { id: 'openrouter/moonshotai/kimi-k2.6:free', desc: 'Kimi K2.6 \u2014 free' },
      { id: 'openrouter/google/gemma-4-31b-it:free', desc: 'Gemma 4 31B \u2014 free' },
      { id: 'openrouter/google/gemma-4-26b-a4b-it:free', desc: 'Gemma 4 26B \u2014 free' },
      { id: 'openrouter/poolside/laguna-m.1:free', desc: 'Laguna M.1 \u2014 free' },
      { id: 'openrouter/poolside/laguna-xs.2:free', desc: 'Laguna XS.2 \u2014 free' },
      { id: 'openrouter/z-ai/glm-4.5-air:free', desc: 'GLM 4.5 Air \u2014 free' },
      { id: 'openrouter/owl-alpha', desc: 'OWL Alpha' },"""

# ---------------------------------------------------------------------------
# The new model list — 15 confirmed working + auto + owl-alpha
# ---------------------------------------------------------------------------

NEW_MODELS = """\
      { id: 'openrouter/auto', desc: 'Auto \u2014 best model for the task' },
      { id: 'openrouter/openai/gpt-oss-120b:free', desc: 'GPT OSS 120B \u2014 free' },
      { id: 'openrouter/openai/gpt-oss-20b:free', desc: 'GPT OSS 20B \u2014 free' },
      { id: 'openrouter/nvidia/nemotron-3-ultra-550b-a55b:free', desc: 'Nemotron Ultra 550B \u2014 free' },
      { id: 'openrouter/nvidia/nemotron-3-super-120b-a12b:free', desc: 'Nemotron Super 120B \u2014 free' },
      { id: 'openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free', desc: 'Nemotron Nano Omni 30B Reasoning \u2014 free' },
      { id: 'openrouter/nvidia/nemotron-3-nano-30b-a3b:free', desc: 'Nemotron Nano 30B \u2014 free' },
      { id: 'openrouter/nvidia/nemotron-nano-12b-v2-vl:free', desc: 'Nemotron Nano 12B \u2014 free' },
      { id: 'openrouter/nvidia/nemotron-nano-9b-v2:free', desc: 'Nemotron Nano 9B \u2014 free' },
      { id: 'openrouter/google/gemma-4-31b-it:free', desc: 'Gemma 4 31B \u2014 free' },
      { id: 'openrouter/poolside/laguna-m.1:free', desc: 'Laguna M.1 \u2014 free' },
      { id: 'openrouter/poolside/laguna-xs.2:free', desc: 'Laguna XS.2 \u2014 free' },
      { id: 'openrouter/liquid/lfm-2.5-1.2b-thinking:free', desc: 'LFM 2.5 1.2B Thinking \u2014 free' },
      { id: 'openrouter/liquid/lfm-2.5-1.2b-instruct:free', desc: 'LFM 2.5 1.2B Instruct \u2014 free' },
      { id: 'openrouter/nex-agi/nex-n2-pro:free', desc: 'Nex N2 Pro \u2014 free' },
      { id: 'openrouter/nvidia/nemotron-3.5-content-safety:free', desc: 'Nemotron 3.5 Content Safety \u2014 free' },
      { id: 'openrouter/owl-alpha', desc: 'OWL Alpha' },"""

# ---------------------------------------------------------------------------
# Apply patch
# ---------------------------------------------------------------------------

def apply(target: Path) -> None:
    if not target.exists():
        print(f"[ERROR] File not found: {target}")
        sys.exit(1)

    original = target.read_text(encoding="utf-8")

    # Guard: already patched
    if "nemotron-3-nano-omni-30b-a3b-reasoning" in original and "llama-3.3-70b" not in original:
        print("[INFO] Patch already applied — nothing to do.")
        sys.exit(0)

    # The file uses em-dash encoded as UTF-8 but findstr showed garbled chars,
    # so try both the unicode em-dash and the garbled sequence
    old_to_try = OLD_MODELS
    if old_to_try not in original:
        # Try with the garbled Windows findstr encoding (ΓÇö = — in cp1252 misread)
        old_to_try = OLD_MODELS.replace('\u2014', '\u2014')
        if old_to_try not in original:
            print("[ERROR] Could not find the model list in the file.")
            print("        The file structure may differ from expected.")
            print("        Check lines 66-80 of CommandPalette.tsx manually.")
            sys.exit(1)

    patched = original.replace(old_to_try, NEW_MODELS, 1)

    if patched == original:
        print("[ERROR] Replacement had no effect — strings may not match exactly.")
        sys.exit(1)

    # Backup
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = target.with_suffix(f".tsx.bak_{stamp}")
    shutil.copy2(target, backup)
    print(f"[OK]   Backup saved → {backup.name}")

    target.write_text(patched, encoding="utf-8")
    print(f"[OK]   Patched file written → {target}")
    print("\nModel list updated:")
    print("  Removed: 7 failing models + kimi-k2.6 (404) + glm-4.5-air (untested)")
    print("  Added:   9 new confirmed working NVIDIA/Liquid/Nex models")
    print("  Kept:    GPT OSS, Nemotron Ultra/Super, Gemma 4 31B, Poolside, auto, owl-alpha")
    print("\nDone. Rebuild the frontend for changes to take effect:")
    print("  npm run build:tauri")


if __name__ == "__main__":
    target = get_target(sys.argv[1:])
    print(f"[INFO] Target: {target}\n")
    apply(target)
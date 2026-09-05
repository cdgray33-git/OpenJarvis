#!/usr/bin/env python
r"""openjarvis-ctx-ceiling-v1

CONTROLLED REPRODUCTION of the Defect 1 candidate mechanism.

Hypothesis under test: when the assembled prompt exceeds the declared
num_ctx (8192 by default at ollama.py:76), Ollama truncates server-side,
returns 200, and the SYSTEM message carrying the tool descriptions is what
falls off the front - so the model emits no tool calls and answers from
whatever context survived.

METHOD: post payloads of increasing size DIRECTLY to Ollama, shaped exactly
as ollama.py:69-89 builds them (same options block, same tools attach).
Sweep prompt size against two num_ctx values:
    8192   - the live default every agent request uses
    32768  - the control

For each cell record: ntc (tool calls emitted), prompt_eval_count as Ollama
reports it, and our payload size. Then compare.

READ SHAPE OF THE RESULT:
  - ntc drops to 0 at 8192 while staying 1 at 32768, at the same prompt size
    -> HYPOTHESIS CONFIRMED. The ceiling is the cause.
  - ntc stays 1 at both -> hypothesis WOUNDED. Truncation is not what kills
    tool emission and the search moves on.
  - ntc is 0 everywhere including small prompts -> the probe's own tool spec
    or prompt is bad; fix the probe, not the theory. The smallest cell is the
    positive control for exactly this.

CONFOUND, stated up front: prompt_eval_count is KV-cache-aware
(ollama.py:119-123), so a low value alone does NOT prove truncation. The
signature to look for is PINNING - the value flattening at a ceiling as the
payload grows. Cache reuse gives scattered lows, not a flat line. Each cell
uses distinct filler text to suppress cache reuse.

TOUCHES NOTHING. No mailbox, no OpenJarvis process, no files, no patch, no
backend restart needed. Pure HTTP to the Ollama host. Non-interactive.

Run from the repo root:
    python .\tests\probe_ctx_ceiling_v1.py

Talks to the Ubuntu ollama host over HTTP from the Windows box - no ssh
needed, the probe runs locally and the host is reached over the network.
"""

import sys
import json
import time
import random
import string

sys.path.insert(0, "src")

import httpx  # noqa: E402

DEFAULT_HOST = "http://172.16.33.200:11434"
DEFAULT_MODEL = "qwen3-coder:30b"
CONFIG_PATH = None

# Prompt sizes to sweep, in approximate tokens of filler history.
SIZES = [1000, 4000, 7000, 9000, 12000, 16000]
CTX_VALUES = [8192, 32768]

# One tool, shaped like the real mailbox tools, with an unmistakable trigger.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "mailbox_find_messages",
            "description": (
                "Search a mail folder for messages from a given sender. "
                "Use this whenever the user asks what mail they have."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "account": {"type": "string", "description": "Account name."},
                    "folder": {"type": "string", "description": "Folder to search."},
                    "from_addr": {"type": "string", "description": "Sender address."},
                },
                "required": ["account", "folder", "from_addr"],
            },
        },
    }
]

SYSTEM = (
    "You are an assistant with access to tools. You MUST use the "
    "mailbox_find_messages tool to answer any question about the user's mail. "
    "Never answer a mail question from memory. Always call the tool."
)

ASK = (
    "Search my Inbox on account yahoo_main for messages from "
    "shop@example.com and tell me how many there are."
)


def load_host_model():
    host, model = DEFAULT_HOST, DEFAULT_MODEL
    try:
        import tomllib
    except ImportError:
        return host, model, "tomllib unavailable - using defaults"
    import os
    path = os.path.join(os.path.expanduser("~"), ".openjarvis", "config.toml")
    try:
        with open(path, "rb") as fh:
            cfg = tomllib.load(fh)
    except Exception as e:
        return host, model, "config unreadable (" + repr(e)[:60] + ") - using defaults"
    eng = cfg.get("engine", {}) or {}
    for k in ("host", "base_url", "url", "ollama_host"):
        if isinstance(eng.get(k), str) and eng[k].strip():
            host = eng[k].strip()
            break
    if isinstance(eng.get("default_model"), str) and eng["default_model"].strip():
        model = eng["default_model"].strip()
    return host, model, "from " + path


def filler(approx_tokens, salt):
    """Distinct pseudo-history so no two cells share a cache prefix."""
    words = []
    rnd = random.Random(salt)
    vocab = ["invoice", "shipment", "receipt", "promotion", "newsletter",
             "account", "summary", "reminder", "update", "notice",
             "confirm", "delivery", "offer", "digest", "alert"]
    # roughly 0.75 words per token for this kind of text
    n = int(approx_tokens * 0.75)
    for _ in range(n):
        words.append(rnd.choice(vocab))
        if rnd.random() < 0.05:
            words.append("".join(rnd.choice(string.ascii_lowercase) for _ in range(6)))
    return " ".join(words)


def build_payload(model, num_ctx, size, salt):
    history = [
        {"role": "system", "content": SYSTEM},
        {
            "role": "user",
            "content": "Here is a prior mailbox report, keep it in mind:\n"
                       + filler(size, salt),
        },
        {
            "role": "assistant",
            "content": "Understood. I have noted that report.",
        },
        {"role": "user", "content": ASK},
    ]
    return {
        "model": model,
        "messages": history,
        "stream": False,
        "think": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 1024,
            "num_ctx": num_ctx,
        },
        "tools": TOOLS,
    }


def main():
    host, model, src = load_host_model()
    print("MARKER openjarvis-ctx-ceiling-v1")
    print("HOST  " + host + "   (" + src + ")")
    print("MODEL " + model)
    print("SWEEP sizes " + repr(SIZES) + "  x  num_ctx " + repr(CTX_VALUES))
    print("Touches no mailbox, no files, no OpenJarvis process.")
    print("")

    client = httpx.Client(base_url=host, timeout=600.0)
    rows = []

    for num_ctx in CTX_VALUES:
        for size in SIZES:
            salt = num_ctx * 100000 + size
            payload = build_payload(model, num_ctx, size, salt)
            pbytes = len(json.dumps(payload).encode("utf-8"))
            label = "num_ctx=" + str(num_ctx) + " size~" + str(size)
            started = time.time()
            try:
                resp = client.post("/api/chat", json=payload)
                status = resp.status_code
                if status != 200:
                    print(label + "  HTTP " + str(status) + "  " + resp.text[:200])
                    rows.append((num_ctx, size, pbytes, status, None, None, None))
                    continue
                data = resp.json()
            except Exception as e:
                print(label + "  EXCEPTION " + repr(e)[:200])
                rows.append((num_ctx, size, pbytes, "EXC", None, None, None))
                continue
            elapsed = time.time() - started

            msg = data.get("message", {}) or {}
            tcs = msg.get("tool_calls", []) or []
            ntc = len(tcs)
            pec = data.get("prompt_eval_count", 0)
            content = (msg.get("content", "") or "").replace("\n", " ")
            rows.append((num_ctx, size, pbytes, 200, ntc, pec, content[:80]))
            print(label
                  + "  payload=" + str(pbytes) + "B"
                  + "  prompt_eval_count=" + str(pec)
                  + "  ntc=" + str(ntc)
                  + "  " + str(round(elapsed, 1)) + "s")
            if ntc:
                names = ",".join(t.get("function", {}).get("name", "?") for t in tcs)
                print("      tools: " + names)
            else:
                print("      no tool call. content: " + content[:100])

    print("")
    print("=== MATRIX ===")
    print(" num_ctx   size    payloadB   prompt_eval   ntc")
    for r in rows:
        print("  " + str(r[0]).rjust(6)
              + "  " + str(r[1]).rjust(6)
              + "  " + str(r[2]).rjust(9)
              + "  " + str(r[5]).rjust(11)
              + "  " + str(r[4]).rjust(4))

    print("")
    print("=== READING ===")
    small = [r for r in rows if r[1] == SIZES[0] and r[4] is not None]
    if small and all(r[4] == 0 for r in small):
        print("POSITIVE CONTROL FAILED: no tool call even on the smallest prompt.")
        print("The probe's tool spec or prompt is at fault, NOT the ceiling theory.")
        print("Fix the probe before drawing any conclusion from the rest.")
        return 1

    dead8 = [r for r in rows if r[0] == 8192 and r[4] == 0]
    live32 = [r for r in rows if r[0] == 32768 and r[4] and r[4] > 0]
    if dead8 and live32:
        cut = min(r[1] for r in dead8)
        held = max(r[1] for r in live32)
        if held >= cut:
            print("HYPOTHESIS CONFIRMED at this resolution.")
            print("  tool emission dies at num_ctx=8192 from size ~" + str(cut))
            print("  and still works at num_ctx=32768 at size ~" + str(held))
            print("  -> the unconfigured 8192 ceiling is the Defect 1 mechanism.")
        else:
            print("MIXED: 8192 fails and 32768 holds, but not at overlapping sizes.")
            print("  Widen the sweep before concluding.")
    elif not dead8:
        print("HYPOTHESIS WOUNDED: tool emission survived every size at 8192.")
        print("  Truncation is not what kills tool calls. Move the search on.")
    else:
        print("INCONCLUSIVE: 32768 also lost tool calls. Read the matrix by hand -")
        print("  something other than the declared window is in play.")

    print("")
    print("Check the prompt_eval column for PINNING - a value that flattens as")
    print("payload grows is truncation. Scattered lows would be KV cache reuse.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

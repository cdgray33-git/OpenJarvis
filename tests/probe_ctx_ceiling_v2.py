r"""openjarvis-ctx-ceiling-v2

MESSAGE-COUNT sweep. Companion to probe_ctx_ceiling_v1.py, which swept payload
SIZE at a fixed message count of 4 and therefore could not test front-eviction.

WHAT v1 ESTABLISHED (do not re-test):
  - At num_ctx=8192, prompt_eval_count pinned at 420 across 58KB / 77KB / 102KB
    payloads. Truncation is real and measurable.
  - Tool emission SURVIVED every truncated cell (ntc=1). The single oversized
    user message was discarded; SYSTEM was not.
  - At num_ctx=32768 with no truncation, the model stopped emitting native
    tool_calls above roughly 8000 evaluated tokens and wrote
    <function=NAME><parameter=...> into content instead. ntc=0.

WHAT THIS PROBE ASKS:
  Production shape is SYSTEM + a long chain of SMALL history messages. That is
  the only shape in which a leading SYSTEM message carrying the 12 tool
  descriptions can be evicted. Hold the total token budget constant and sweep
  the number of messages it is split across.

THREE OUTCOMES, discriminated by CONTENT, not by ntc alone:
  A. ntc stays 1 as message count rises  -> SYSTEM survives eviction.
     Front-eviction is dead. Defect 1 is not a truncation defect.
  B. ntc goes 0 and content contains "<function="  -> NOT eviction. This is the
     v1 format-switch reappearing. Tools are present, the model is calling them
     in the wrong channel, and Format 4 of _extract_tool_call should catch it
     in production.
  C. ntc goes 0 and content claims no tools / no access  -> SYSTEM WAS EVICTED.
     This is the 09/02 signature and it makes Defect 1 reproducible on demand.

Read-only. Touches no mailbox, no OpenJarvis process, no config file. Posts
directly to Ollama with the payload shape ollama.py:69-89 builds.

Usage, from PS C:\Users\Admin\OpenJarvis>
    python .\tests\probe_ctx_ceiling_v2.py
    python .\tests\probe_ctx_ceiling_v2.py --host http://172.16.33.200:11434
"""

import json
import sys
import time
import urllib.request

# Hardcoded from the VERIFIED v1 run output rather than re-derived from
# config.toml. v1 printed these and Gray confirmed the HOST line.
HOST = "http://172.16.33.200:11434"
MODEL = "qwen3-coder:30b"

for i, a in enumerate(sys.argv):
    if a == "--host" and i + 1 < len(sys.argv):
        HOST = sys.argv[i + 1]
    if a == "--model" and i + 1 < len(sys.argv):
        MODEL = sys.argv[i + 1]

SYSTEM = (
    "You are an AI assistant with access to tools. You MUST use tools when they "
    "would help answer the user's question. Do not describe what you would do. "
    "Call the tool.\n\n"
    "### mailbox_find_messages\n"
    "Search a mail folder for messages matching a sender address.\n"
    "Category: mailbox\n"
    "Parameters: account (string), folder (string), from_addr (string)\n"
)

ASK = "Find the messages from shop@example.com in the Inbox on the yahoo_main account."

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "mailbox_find_messages",
            "description": "Search a mail folder for messages matching a sender address.",
            "parameters": {
                "type": "object",
                "properties": {
                    "account": {"type": "string"},
                    "folder": {"type": "string"},
                    "from_addr": {"type": "string"},
                },
                "required": ["account", "folder", "from_addr"],
            },
        },
    }
]

# Total filler budget held CONSTANT. Only the number of messages it is split
# across changes. 12000 is comfortably past the ~7000 boundary v1 located.
TOTAL_TOKENS = 12000
MSG_COUNTS = [1, 4, 16, 32]
NUM_CTX = [8192, 32768]

WORDS = (
    "invoice shipment receipt order confirm dispatch carrier parcel tracking "
    "warehouse pallet manifest customs freight consignee label courier transit"
).split()


def filler(approx_tokens, salt):
    """Distinct text per cell so nothing is served from KV cache."""
    out = ["cell%s" % salt]
    n = max(1, int(approx_tokens))
    for i in range(n):
        out.append(WORDS[(i + salt * 7) % len(WORDS)])
        if i % 11 == 10:
            out.append("s%dw%d" % (salt, i))
    return " ".join(out)


def build_messages(total_tokens, n_msgs, salt):
    """SYSTEM first, then n_msgs user/assistant history pairs, then the ASK."""
    msgs = [{"role": "system", "content": SYSTEM}]
    per = max(1, total_tokens // n_msgs)
    for k in range(n_msgs):
        msgs.append(
            {
                "role": "user",
                "content": "History item %d. %s" % (k, filler(per, salt * 100 + k)),
            }
        )
        msgs.append({"role": "assistant", "content": "Noted item %d." % k})
    msgs.append({"role": "user", "content": ASK})
    return msgs


def run_cell(messages, num_ctx):
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "tools": TOOLS,
        "options": {"num_ctx": num_ctx, "temperature": 0},
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        HOST.rstrip("/") + "/api/chat",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    dt = time.time() - t0
    msg = data.get("message", {}) or {}
    tcs = msg.get("tool_calls", []) or []
    return {
        "ntc": len(tcs),
        "names": [
            (t.get("function", {}) or {}).get("name", "?") for t in tcs
        ],
        "content": msg.get("content", "") or "",
        "prompt_eval": data.get("prompt_eval_count", 0),
        "bytes": len(body),
        "nmsgs": len(messages),
        "secs": dt,
    }


def classify(r):
    c = r["content"].lower()
    if r["ntc"] > 0:
        return "TOOLCALL"
    if "<function=" in c or "<tool_call" in c or '"name":' in c:
        return "WRONGCHANNEL"
    for phrase in (
        "don't have", "do not have", "no access", "cannot access",
        "unable to", "i don't have the", "not able to",
    ):
        if phrase in c:
            return "NOTOOLS"
    return "PROSE"


def main():
    print("MARKER openjarvis-ctx-ceiling-v2")
    print("HOST  %s" % HOST)
    print("MODEL %s" % MODEL)
    print("SWEEP msg_counts %s at a FIXED %d token budget  x  num_ctx %s"
          % (MSG_COUNTS, TOTAL_TOKENS, NUM_CTX))
    print("Read-only. No mailbox, no OpenJarvis process, no config write.")
    print("")

    rows = []
    salt = 1

    # Positive control: small, few messages. Must emit a tool call. If it does
    # not, the probe is wrong and every other cell is uninterpretable.
    for nc in NUM_CTX:
        m = build_messages(800, 1, salt)
        salt += 1
        try:
            r = run_cell(m, nc)
        except Exception as e:
            print("CONTROL num_ctx=%d FAILED: %s" % (nc, e))
            return 2
        r["label"] = "control"
        r["num_ctx"] = nc
        r["msgs_req"] = 1
        r["verdict"] = classify(r)
        rows.append(r)
        print("CONTROL num_ctx=%d nmsgs=%d peval=%d ntc=%d %s %.1fs"
              % (nc, r["nmsgs"], r["prompt_eval"], r["ntc"], r["verdict"], r["secs"]))

    print("")

    for nc in NUM_CTX:
        for n in MSG_COUNTS:
            m = build_messages(TOTAL_TOKENS, n, salt)
            salt += 1
            try:
                r = run_cell(m, nc)
            except Exception as e:
                print("num_ctx=%d n=%d FAILED: %s" % (nc, n, e))
                continue
            r["label"] = "sweep"
            r["num_ctx"] = nc
            r["msgs_req"] = n
            r["verdict"] = classify(r)
            rows.append(r)
            print("num_ctx=%d pairs=%-3d nmsgs=%-3d payload=%dB peval=%d ntc=%d  %s  %.1fs"
                  % (nc, n, r["nmsgs"], r["bytes"], r["prompt_eval"],
                     r["ntc"], r["verdict"], r["secs"]))
            print("      content[:400]: %s" % r["content"][:400].replace("\n", " "))

    print("")
    print("=== MATRIX ===")
    print("%8s %6s %6s %10s %12s %5s  %s"
          % ("num_ctx", "pairs", "nmsgs", "payloadB", "prompt_eval", "ntc", "verdict"))
    for r in rows:
        print("%8d %6s %6d %10d %12d %5d  %s"
              % (r["num_ctx"], r["msgs_req"] if r["label"] == "sweep" else "ctl",
                 r["nmsgs"], r["bytes"], r["prompt_eval"], r["ntc"], r["verdict"]))

    print("")
    print("=== READING ===")

    ctl = [r for r in rows if r["label"] == "control"]
    if not ctl or any(r["ntc"] == 0 for r in ctl):
        print("PROBE INVALID: a control cell emitted no tool call.")
        print("  Fix the probe. Draw NO conclusion about the defect from this run.")
        return 1
    print("Controls passed - both emitted a tool call. Sweep cells are interpretable.")

    low = [r for r in rows if r["label"] == "sweep" and r["num_ctx"] == 8192]
    notools = [r for r in low if r["verdict"] == "NOTOOLS"]
    wrongch = [r for r in low if r["verdict"] == "WRONGCHANNEL"]
    held = [r for r in low if r["verdict"] == "TOOLCALL"]

    if notools:
        print("OUTCOME C - SYSTEM MESSAGE EVICTED. Cells with pairs=%s at 8192 lost"
              % [r["msgs_req"] for r in notools])
        print("  the tools and said so. Front-eviction CONFIRMED. Defect 1 is")
        print("  reproducible on demand. Next: thread a configured num_ctx.")
    elif wrongch and not held:
        print("OUTCOME B - WRONG CHANNEL, not eviction. Tools were present; the")
        print("  model emitted <function=...> into content. Format 4 of")
        print("  _extract_tool_call should catch this in production - check")
        print("  whether the fallback parser is reached when ntc=0.")
    elif held and not notools:
        print("OUTCOME A - SYSTEM SURVIVED at every message count tested.")
        print("  Front-eviction is DEAD. Truncation is real but does not remove")
        print("  the tool contract. Move the search off truncation entirely.")
    else:
        print("MIXED - read the verdict column and the content lines directly.")

    print("")
    print("PINNING CHECK: a prompt_eval that flattens as payload grows is")
    print("truncation. Compare the 8192 rows against the 32768 rows at the")
    print("same pairs value; 32768 is the untruncated control.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

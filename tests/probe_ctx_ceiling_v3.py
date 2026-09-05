r"""openjarvis-ctx-ceiling-v3

RATE experiment. Successor to probe_ctx_ceiling_v2.py (message-count sweep).

THE QUESTION, stated so it can come back NO:
  Since W34/W35, production runs at num_ctx 16384 (verified live 09/05 via
  GET /api/ps on the Ollama host: context_length 16384). W35 asked whether the
  remaining Defect 1 behavior is a SAMPLING defect or was a CONTEXT defect all
  along. This probe holds the prompt FIXED and varies ONLY the window.

DEVIATION FROM THE W33 SECTION 4 SPEC - DELIBERATE, READ THIS:
  W33 specified num_ctx 8192 as "production sampling, do not improve these".
  That was written 09/03, when 8192 WAS production. It no longer is. W33's two
  prompt sizes (7000 / 8200) were also chosen as below/above saturation
  RELATIVE TO 8192. Building to the letter of that spec would measure the old
  regime and leave the arm we actually ship in unmeasured.
  Retained from the spec verbatim: temperature 0.7, no seed, num_predict 1024,
  N=20, distinct filler per repeat, rate-not-verdict, and BOTH instrument fixes.

DESIGN:
  ARM A  num_ctx  8192   prompt does NOT fit -> front truncation
  ARM B  num_ctx 16384   prompt DOES fit     -> no truncation
  Prompt is ~12000 natural tokens (v2's known-good TOTAL_TOKENS=12000 across
  16 history pairs). Comfortably over 8192, comfortably under 16384.

  PAIRED: repeat i in arm A and repeat i in arm B are byte-identical prompts.
  The only variable between arms is the window. Filler still varies BETWEEN
  repeats so no cell is served from KV cache.

  KNOWN CONFOUND, NOT DESIGNED OUT: arms run as blocks, not interleaved,
  because changing num_ctx forces a full 20GB model reload. Time-order is
  therefore confounded with arm. Interleaving would cost 40 reloads.

INSTRUMENT DEFECTS FIXED (both found the hard way in W33):
  1. Empty content with ntc=0 classifies UNINFORMATIVE, never PROSE, and is
     EXCLUDED from the rate denominator - not counted as a non-failure.
     It is still printed loudly, because a run that is mostly UNINFORMATIVE
     has no interpretable rate at all.
  2. FULL content captured to the run log, never a prefix. v1 could not tell
     "tools gone" from "tools present, wrong channel" because it cut the
     string before the discriminator.

VALIDITY GATES - the run voids itself rather than reporting a soft result:
  G1 Controls (small prompt, both windows) must emit a tool call.
  G2 Arm B prompt_eval must materially exceed arm A's. If it does not, the
     two arms are not actually different and nothing below means anything.
  G3 If UNINFORMATIVE exceeds a third of either arm, no rate is reported.
  G4 If arm A shows no failures, the probe never reached the defect. Arm B
     collapsing to zero from a zero baseline proves NOTHING.

Read-only. Touches no mailbox, no OpenJarvis process, no config file. Posts
directly to Ollama with the payload shape ollama.py:69-89 builds.
Non-interactive: runs to completion unattended, no timing window to react to.

Usage, from PS C:\Users\Admin\OpenJarvis>
    python .\tests\probe_ctx_ceiling_v3.py
    python .\tests\probe_ctx_ceiling_v3.py --n 20
    python .\tests\probe_ctx_ceiling_v3.py --host http://172.16.33.200:11434
"""

import json
import sys
import time
import datetime
import urllib.request

HOST = "http://172.16.33.200:11434"
MODEL = "qwen3-coder:30b"
N_REPEATS = 20

for i, a in enumerate(sys.argv):
    if a == "--host" and i + 1 < len(sys.argv):
        HOST = sys.argv[i + 1]
    if a == "--model" and i + 1 < len(sys.argv):
        MODEL = sys.argv[i + 1]
    if a == "--n" and i + 1 < len(sys.argv):
        N_REPEATS = int(sys.argv[i + 1])

# PRODUCTION SAMPLING. Do not "improve" these.
TEMPERATURE = 0.7
NUM_PREDICT = 1024

ARM_A_CTX = 8192
ARM_B_CTX = 16384

TOTAL_TOKENS = 12000
N_PAIRS = 16

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

WORDS = (
    "invoice shipment receipt order confirm dispatch carrier parcel tracking "
    "warehouse pallet manifest customs freight consignee label courier transit"
).split()

LOG_LINES = []


def emit(line=""):
    print(line)
    LOG_LINES.append(line)


def filler(approx_tokens, salt):
    out = ["cell%s" % salt]
    n = max(1, int(approx_tokens))
    for i in range(n):
        out.append(WORDS[(i + salt * 7) % len(WORDS)])
        if i % 11 == 10:
            out.append("s%dw%d" % (salt, i))
    return " ".join(out)


def build_messages(total_tokens, n_msgs, salt):
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
        "options": {
            "num_ctx": num_ctx,
            "temperature": TEMPERATURE,
            "num_predict": NUM_PREDICT,
        },
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        HOST.rstrip("/") + "/api/chat",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=900) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    dt = time.time() - t0
    msg = data.get("message", {}) or {}
    tcs = msg.get("tool_calls", []) or []
    return {
        "ntc": len(tcs),
        "names": [(t.get("function", {}) or {}).get("name", "?") for t in tcs],
        "content": msg.get("content", "") or "",
        "prompt_eval": data.get("prompt_eval_count", 0),
        "eval_count": data.get("eval_count", 0),
        "bytes": len(body),
        "nmsgs": len(messages),
        "secs": dt,
    }


def classify(r):
    """INSTRUMENT FIX 1: empty is UNINFORMATIVE, never PROSE."""
    raw = r["content"]
    c = raw.lower()
    if r["ntc"] > 0:
        return "TOOLCALL"
    if not raw.strip():
        return "UNINFORMATIVE"
    if "<function=" in c or "<tool_call" in c or '"name":' in c:
        return "WRONGCHANNEL"
    for phrase in (
        "don't have", "do not have", "no access", "cannot access",
        "unable to", "i don't have the", "not able to",
    ):
        if phrase in c:
            return "NOTOOLS"
    return "PROSE"


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = float(k) / n
    d = 1.0 + z * z / n
    c = p + z * z / (2.0 * n)
    s = z * ((p * (1.0 - p) / n + z * z / (4.0 * n * n)) ** 0.5)
    return ((c - s) / d, (c + s) / d)


def run_arm(name, num_ctx, n_repeats):
    emit("")
    emit("=== ARM %s : num_ctx=%d, %d repeats ===" % (name, num_ctx, n_repeats))
    rows = []
    for i in range(n_repeats):
        # salt depends ONLY on i -> paired across arms, distinct across repeats
        msgs = build_messages(TOTAL_TOKENS, N_PAIRS, 1000 + i)
        try:
            r = run_cell(msgs, num_ctx)
        except Exception as e:
            emit("  arm=%s rep=%-3d FAILED: %s" % (name, i, e))
            continue
        r["arm"] = name
        r["num_ctx"] = num_ctx
        r["rep"] = i
        r["verdict"] = classify(r)
        rows.append(r)
        emit("  arm=%s rep=%-3d peval=%-6d ntc=%d evc=%-5d %-14s %.1fs"
             % (name, i, r["prompt_eval"], r["ntc"], r["eval_count"],
                r["verdict"], r["secs"]))
        # INSTRUMENT FIX 2: FULL content to the log, never a prefix.
        LOG_LINES.append("      FULL CONTENT rep=%d >>>" % i)
        LOG_LINES.append(r["content"])
        LOG_LINES.append("      <<< END rep=%d" % i)
    return rows


def summarize(name, rows):
    total = len(rows)
    unin = [r for r in rows if r["verdict"] == "UNINFORMATIVE"]
    infor = [r for r in rows if r["verdict"] != "UNINFORMATIVE"]
    fails = [r for r in infor if r["ntc"] == 0]
    n = len(infor)
    k = len(fails)
    lo, hi = wilson(k, n)
    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    pev = [r["prompt_eval"] for r in rows if r["prompt_eval"]]
    return {
        "arm": name, "total": total, "unin": len(unin), "n": n, "k": k,
        "rate": (float(k) / n if n else 0.0), "lo": lo, "hi": hi,
        "counts": counts,
        "pev_med": (sorted(pev)[len(pev) // 2] if pev else 0),
    }


def main():
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    emit("MARKER openjarvis-ctx-ceiling-v3")
    emit("RUN   %s" % stamp)
    emit("HOST  %s" % HOST)
    emit("MODEL %s" % MODEL)
    emit("SAMPLING temperature=%s num_predict=%d NO SEED (production shape)"
         % (TEMPERATURE, NUM_PREDICT))
    emit("DESIGN paired, fixed prompt ~%d tok across %d pairs; arms %d vs %d"
         % (TOTAL_TOKENS, N_PAIRS, ARM_A_CTX, ARM_B_CTX))
    emit("Read-only. No mailbox, no OpenJarvis process, no config write.")

    # ---- Controls (G1) -------------------------------------------------
    emit("")
    emit("=== CONTROLS ===")
    controls = []
    for nc in (ARM_A_CTX, ARM_B_CTX):
        m = build_messages(800, 1, 7)
        try:
            r = run_cell(m, nc)
        except Exception as e:
            emit("CONTROL num_ctx=%d FAILED: %s" % (nc, e))
            return 2
        r["verdict"] = classify(r)
        controls.append(r)
        emit("CONTROL num_ctx=%-6d peval=%-6d ntc=%d %-14s %.1fs"
             % (nc, r["prompt_eval"], r["ntc"], r["verdict"], r["secs"]))

    if any(r["ntc"] == 0 for r in controls):
        emit("")
        emit("G1 FAILED - PROBE INVALID: a control emitted no tool call.")
        emit("  Fix the probe. Draw NO conclusion from this run.")
        write_log(stamp)
        return 1
    emit("G1 passed - both controls emitted a tool call.")

    # ---- Arms ----------------------------------------------------------
    rows_a = run_arm("A", ARM_A_CTX, N_REPEATS)
    rows_b = run_arm("B", ARM_B_CTX, N_REPEATS)

    sa = summarize("A", rows_a)
    sb = summarize("B", rows_b)

    emit("")
    emit("=== MATRIX ===")
    emit("%4s %8s %6s %6s %6s %8s  %s"
         % ("arm", "num_ctx", "runs", "unin", "fails", "pev_med", "breakdown"))
    for s, nc in ((sa, ARM_A_CTX), (sb, ARM_B_CTX)):
        emit("%4s %8d %6d %6d %6d %8d  %s"
             % (s["arm"], nc, s["total"], s["unin"], s["k"], s["pev_med"],
                ", ".join("%s=%d" % kv for kv in sorted(s["counts"].items()))))

    emit("")
    emit("=== VALIDITY GATES ===")

    # G2 - the arms must actually differ
    if sb["pev_med"] <= sa["pev_med"] * 1.10:
        emit("G2 FAILED - arm B prompt_eval (%d) does not materially exceed"
             % sb["pev_med"])
        emit("  arm A (%d). The two arms are NOT different. The prompt may be"
             % sa["pev_med"])
        emit("  fitting inside 8192, or truncation is not doing what we think.")
        emit("  NO RATE REPORTED. Resize the prompt and rerun.")
        write_log(stamp)
        return 1
    emit("G2 passed - arm A peval %d, arm B peval %d. Arms differ; arm A is"
         % (sa["pev_med"], sb["pev_med"]))
    emit("  truncated and arm B is not.")

    # G3 - too many uninformative
    for s in (sa, sb):
        if s["total"] and float(s["unin"]) / s["total"] > 0.34:
            emit("G3 FAILED - arm %s is %d/%d UNINFORMATIVE (empty generations)."
                 % (s["arm"], s["unin"], s["total"]))
            emit("  No interpretable rate. Investigate the empty returns first;")
            emit("  they may themselves be the defect.")
            write_log(stamp)
            return 1
    emit("G3 passed - uninformative counts are within tolerance (A=%d, B=%d)."
         % (sa["unin"], sb["unin"]))

    # G4 - arm A must reproduce the failure
    if sa["k"] == 0:
        emit("G4 FAILED - arm A produced ZERO failures in %d informative runs."
             % sa["n"])
        emit("  The probe shape does not reach the defect at 8192. Arm B being")
        emit("  clean proves NOTHING - it is clean from a clean baseline.")
        emit("  This is W33's third read shape: move the search back to the")
        emit("  LIVE AGENT PATH. Do not conclude the context fix worked.")
        write_log(stamp)
        return 1
    emit("G4 passed - arm A reproduced the failure (%d/%d)." % (sa["k"], sa["n"]))

    # ---- Reading -------------------------------------------------------
    emit("")
    emit("=== RATES ===")
    for s in (sa, sb):
        emit("  arm %s  num_ctx=%-6d  failure rate %d/%d = %.0f%%   95%% CI [%.0f%%, %.0f%%]"
             % (s["arm"], (ARM_A_CTX if s["arm"] == "A" else ARM_B_CTX),
                s["k"], s["n"], 100 * s["rate"], 100 * s["lo"], 100 * s["hi"]))

    emit("")
    emit("=== READING ===")
    if sb["hi"] < sa["lo"]:
        emit("CONTEXT. Arm B's interval sits entirely below arm A's - the failure")
        emit("  rate collapses when the prompt fits. Defect 1's remaining")
        emit("  behavior was TRUNCATION, and W34's num_ctx 16384 patch (live and")
        emit("  verified 09/05) already addresses it in production.")
        emit("  NEXT: confirm on the LIVE AGENT PATH, not just here. This probe")
        emit("  posts direct to Ollama and bypasses our own code entirely.")
    elif sa["hi"] < sb["lo"]:
        emit("INVERTED - arm B is WORSE than arm A. Not a predicted outcome.")
        emit("  Do not rationalize it. Suspect the instrument or a reload")
        emit("  artifact and investigate before drawing anything.")
    else:
        emit("SAMPLING, or underpowered. The intervals OVERLAP: the window did")
        emit("  not clearly change the rate. If both rates are non-zero and")
        emit("  similar, the defect is SAMPLING-side and the context fix, while")
        emit("  correct on its own merits, does NOT close Defect 1.")
        emit("  NEXT: the sampling-side options - thread temperature the same")
        emit("  way num_ctx was threaded, a seed, constrained decoding, or a")
        emit("  retry on ntc=0. N=%d may also simply be too small to separate" % N_REPEATS)
        emit("  these rates; check the interval widths above before choosing.")

    emit("")
    emit("WRONGCHANNEL vs NOTOOLS matters more than the totals - read the")
    emit("breakdown, not the verdict. WRONGCHANNEL means the tools were present")
    emit("and the model used the wrong channel (Format 4 territory). NOTOOLS")
    emit("means the contract was gone from the prompt.")

    write_log(stamp)
    return 0


def write_log(stamp):
    path = "tests/ctx_ceiling_v3_run_%s.txt" % stamp
    try:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(LOG_LINES) + "\n")
        print("")
        print("LOG WRITTEN: %s" % path)
        print("NOTE: .gitignore line 23 is a blanket *.txt - this log needs")
        print("      'git add -f' or it will be silently excluded.")
    except Exception as e:
        print("LOG WRITE FAILED: %s" % e)


if __name__ == "__main__":
    sys.exit(main())

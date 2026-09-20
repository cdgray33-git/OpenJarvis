# OPENJARVIS ARCHITECTURE - PORTS, PROTOCOLS AND ENCODING AT EACH GATE
# Version 1, 2026-08-31, cut at commit 6c172d1
# Author window: W26. Scope: all registered paths, FULL DETAIL on the
# destructive mailbox path and the confirmation gate.

---

## 0. HOW TO READ THIS DOCUMENT

Every row carries an EVIDENCE column. Three values only:

- **READ** - established by reading the source file at the cited line in a
  recorded window. Trustworthy.
- **OBSERVED** - established by watching runtime behavior (log line, wire
  capture, response body). Trustworthy for the case observed.
- **ASSUMED** - a protocol default or a reasonable inference that has NOT been
  read or observed. **Do not build on these without checking them first.**

This distinction exists because this project has repeatedly been burned by prose
assertions that turned out to be false. The most recent instance is in section 4:
the System Design Package asserted a confirmation flag on the destructive mailbox
tool in two separate revisions, and the source says the opposite, deliberately.

Line references are valid at `6c172d1`. They will drift. Re-read before acting.

---

## 1. HOSTS AND PORTS

| Host | Address | Role | Port | Protocol | Evidence |
|---|---|---|---|---|---|
| Windows box | local | Frontend (Tauri), backend, dev shell | - | - | READ |
| Backend API | 127.0.0.1 | FastAPI, all HTTP routes | 8010 | HTTP/1.1, loopback only | OBSERVED |
| ollama host | 172.16.33.200 | Model inference, Ubuntu | 11434 | HTTP | port ASSUMED (ollama default), host READ |
| ollama-mcp2 | lab | TTS service (Kokoro), STT (faster-whisper) | - | HTTP | ASSUMED |
| GitLab | 172.16.33.126 | Lab git remote `gitlab` | 80 | **HTTP, plaintext** | READ (remote URL) |
| GitHub | github.com | Remote `origin` | 443 | HTTPS | READ (remote URL) |
| Yahoo IMAP | imap.mail.yahoo.com | Mailbox | 993 | IMAPS (TLS) | ASSUMED (standard) |

**Bind posture.** `record_bind` emits a `BIND-ASSERT` line at startup carrying
`host=`, `port=`, `loopback=`, `api_key_set=` (W19/W24). Known accepted risk,
unchanged: the bind verdict is DUPLICATED in `auth_middleware.py` and
`serve.py:613-615`, both copies classify an empty host as loopback, and the copy
consumers actually read is the `serve.py` one.

**Plaintext HTTP to the GitLab remote is a real exposure**, not a note. Every
push carries repository contents over the lab network unencrypted.

---

## 2. GATE INVENTORY - ALL REGISTERED PATHS

A "gate" here means any boundary where a request changes representation, changes
thread, or changes trust domain.

| ID | Gate | Transport | Encoding | Human present | Evidence |
|---|---|---|---|---|---|
| G1 | Frontend -> backend, typed submit (F-A) | HTTP POST, loopback:8010 | JSON | yes | READ |
| G2 | Frontend -> backend, voice submit (F-B) | HTTP POST + audio | JSON + audio blob | yes | READ |
| G3 | Frontend option relay (F-C) | in-page event `jarvis-submit-text` | - | yes | **DEAD - no handler** (READ) |
| G4 | Backend -> model | HTTP to ollama | JSON, OpenAI-ish schema | no | READ |
| G5 | Model output -> tool call | in-process parse | text -> dict | no | READ |
| G6 | Tool dispatch -> executor | in-process | dict | no | READ |
| G7 | Executor -> confirmation gate | in-process + EventBus | dict | **conditional** | READ |
| G8 | EventBus -> ws_bridge -> WS client | WebSocket | JSON | yes (viewer) | OBSERVED (W20) |
| G9 | Confirm decision -> registry | HTTP POST `/v1/tools/confirm` | JSON | yes | OBSERVED (W21) |
| G10 | Tool -> IMAP connector | in-process, sync | Python objects | no | READ |
| G11 | Connector -> mail server | IMAP over TLS | IMAP wire, bytes | no | ASSUMED (TLS) |
| G12 | Managed agent -> client | HTTP SSE | `text/event-stream` | yes | READ |
| G13 | Backend -> TTS service | HTTP | audio bytes | no | OBSERVED |

### 2.1 Registered execution paths

- **PATH 1** - orchestrator `ask()` via `system\orchestrator.py`.
- **PATH 2** - managed-agent SSE via `_stream_managed_agent()` in
  `server\agent_manager_routes.py`. **Four auto-approve sites on this path.**
  Largest outstanding confirmation-gate item; untouched for several windows.
- **PATH 3** - test-execute trigger, `POST /v1/tools/test-execute`. Gate LIVE,
  `confirm_id` verified on the wire (W21). This is the only path where the
  confirmation gate has been proven end to end.
- **Chat dispatch** - `routes.py` branches 1a / 1b / 1c / 1d. Non-streaming
  branches offloaded to `asyncio.to_thread` as of `aad8ccd`.
- **Frontend submit** - F-A typed, F-B voice, F-C option relay (DEAD).

### 2.2 Tool-call extraction order (G5)

Inside `_extract_tool_call`, in this order: native, then Format 1
(case-insensitive, **unanchored**), Format 2 (unread), Format 4 (XML), Format 3
(bare JSON).

**Precedence is an accident of insertion order, not a decision.** Format 1's
unanchored case-insensitive match can shadow Format 4 XML. Open audit item.

---

## 3. THREADING MODEL - A CORRECTNESS REQUIREMENT, NOT A PERFORMANCE NOTE

The synchronous tool chain must never run on the event loop. A confirmation gate
raised from the event loop **deadlocks**: the gate waits for an HTTP POST that
the loop it is blocking would have to serve.

Offload sites, all READ:

- `routes.py:168` and `:176` (commit `aad8ccd`)
- `stream_bridge.py:155`
- `agent_manager_routes.py:2258`
- `confirm_registry.py:9` documents the model explicitly

Consequence: every synchronous tool holds a **pool worker** for its full
duration. See section 4 timings - a degraded mailbox move holds one worker for
roughly twelve minutes. That is pool starvation in degree, not a new failure
class, but it is a capacity input the SDD must state.

---

## 4. FULL DETAIL - THE CONFIRMATION GATE (DEFECT 6)

### 4.1 Mechanism

`ToolExecutor.execute` treats `requires_confirmation` as a **hard requirement,
not a prompt**. Source, quoted from the `mailbox_tools.py` header note:

    if tool.spec.requires_confirmation:
        if not self._interactive or self._confirm_callback is None:
            return ToolResult(..., success=False)

So a tool carrying the flag, executed by an executor built without
`interactive=True` and without a confirm callback, **fails every call**. It does
not prompt. This is the `_confirm_callback = None` defect.

### 4.2 Registry, payload, transport

| Property | Value | Evidence |
|---|---|---|
| Route | `POST /v1/tools/confirm` | READ |
| Registry semantics | write-once; **409 on re-decision**; TIMEOUT internal only | READ |
| TTL | 120 s | READ |
| Payload | seven fields | READ |
| `turn_id` source | `CURRENT_TURN_ID`, set by `openjarvis-agent-log-v1` | READ |
| Transport | EventBus -> ws_bridge -> bare WS client | OBSERVED (W20) |
| Payload integrity | verified on the wire | OBSERVED (W21) |
| Redaction | CLOSED. Do not re-open. | resolved |

**Design smell, named deliberately:** `turn_id` on the gate payload is sourced
from a *diagnostic logging marker*. A debug instrument is load-bearing on a
safety-critical payload. If agent-log is ever disabled or refactored, the gate
payload loses a field. This should be given its own owner in the SDD.

**The 120s TTL governs the WAIT FOR A HUMAN, not the execution that follows.**
State this explicitly wherever the TTL appears. A reader who conflates the two
will wrongly conclude the gate times out mid-move. It does not - see 5.4.

### 4.3 EventBus topology

Two buses existed and left the chat path dark. The one-line WS-bridge fix is
applied and runtime-verified. Gate traffic reaches the client (G8).

---

## 5. FULL DETAIL - THE DESTRUCTIVE MAILBOX PATH

`mailbox_move_to_trash`, end to end, as it stands at `6c172d1`.

### 5.1 Registration and spec

| Property | Value | Evidence |
|---|---|---|
| Registration | `mailbox_tools.py:453`, `@ToolRegistry.register("mailbox_move_to_trash")` | READ |
| Spec | `mailbox_tools.py:463-509` | READ |
| Timeout | **1800.0 s**, marker `openjarvis-tool-timeout-v1` | READ |
| `ToolSpec` default timeout | 30.0 at `_stubs.py:41` | READ |
| Timeout resolution | `_stubs.py:367`, `tool.spec.timeout_seconds or self._default_timeout` | READ |
| Required capability | `mail.write` | READ |
| Required params | `folder` only (uids no longer required) | READ |
| Construction constraint | `MCPServer._auto_discover_tools` calls `ToolRegistry.create(key)` with **no arguments**; every tool is zero-arg constructible and resolves its account at execute time | READ |

**Note the 300s figure carried in older records is retired.** It was correct for
this tool until `6c172d1`; the current bound is 1800 s. The 300.0 values that
remain at `imap_mail.py:837/858/899` belong to **different tools**.

### 5.2 THE CONFIRMATION FINDING - CORRECTS THE SDP

**`requires_confirmation` is deliberately NOT set on this tool.**

The System Design Package asserts `requires_confirmation=True` at **revB:504**
and **revC:597**. Both are prose. Both are **WRONG**. The source header states
the omission is intentional and gives the reason: a flagged tool on the
server-side agent path fails every call rather than prompting (4.1).

**The interlock is implemented in the tool contract instead:**

1. `dry_run` defaults to **True** and returns a plan with exact counts.
2. Applying requires **BOTH** `dry_run=False` **AND** `confirm` set to the exact
   string `CONFIRM DELETE`.

Stated intent: keep the destructive path reachable by the agent while making it
impossible to trip by accident or by a single malformed argument.

**Standing caveat.** That reasoning predates the 6c confirm registry and route.
The premise that no executor can supply a callback may have expired. **Not
retested.** Retesting it is the correct next move on this gate, and it is the
decision point for whether the mailbox path rejoins the real gate or keeps its
bespoke interlock permanently. Do not let this sit as folklore in either
direction.

### 5.3 Call chain

| Stage | Location | Evidence |
|---|---|---|
| Tool entry | `mailbox_tools.py:453` | READ |
| Sender resolution (optional) | `conn.find_messages(from_addr=..., limit=5000)` | READ |
| Protected-sender filter | `openjarvis-protected-senders-v1` | READ |
| uid typeguard | `openjarvis-uid-typeguard-v1` | READ |
| Caller into connector | `mailbox_tools.py:667` dry run, `:669` live - **the ONLY callers** | READ (grep) |
| Connector method | `imap_mail.py:537` `move_to_trash` | READ |
| Signature of the search | `imap_mail.py:477-486`, keyword-only, accepts `folder` | READ |

### 5.4 Wire behavior and timing (G10, G11)

Protocol at the mail server: **UID COPY**, then **UID STORE +FLAGS \Deleted**,
then **EXPUNGE**. Encoding is the IMAP wire format; responses are bytes,
flattened to text by `_imap_text()` with UTF-8 decode and `errors="replace"`,
bare `except` returning `repr`.

Pacing, as committed at `611329e`:

| Property | Value |
|---|---|
| Chunk size | 10 uids |
| Pause between chunks | 1.0 s |
| Retries per chunk | 4, exponential backoff 1 / 2 / 4 / 8 s |
| Degradation | per-UID, one at a time, 1 s apart, so one poisoned message cannot strand the other nine |
| STORE | applied only to uids whose COPY returned OK |
| Blocking floor | ~29 s for 290 uids, fully clean |
| Blocking ceiling | ~12 min for 290 uids, fully degraded |
| Timeout headroom | 1800 s bound vs ~12 min worst case - **fits** |

Yahoo rate-limits bulk UID COPY and reports it inconsistently: `[LIMIT]` on
large sets, `[SERVERBUG]` on small ones, both transient. That inconsistency is
the reason the retry ladder exists.

**Architecturally new at `611329e`:** this call now has a duration floor
proportional to message count. Before, its duration was a function of the server
alone. Both the 120s gate TTL and the worker-pool constraint must be reasoned
against that floor.

### 5.5 Counting contract (G6)

`mailbox_find_messages` defaults to `detail=summary` and returns `by_address` /
`by_folder` aggregates, `truncated`, and a `note`.

**The count is WINDOWED.** The mail server exposes only the newest ~10,000
messages per folder and does not index past them. `match_count` is a **FLOOR
within that window and is NEVER a mailbox total.** Any report to a human must
say so plainly and must not claim all matching mail was found, moved or deleted.

---

## 6. OPEN HAZARDS ON THIS PATH - RECORDED, NOT PATCHED

| ID | Hazard | Severity |
|---|---|---|
| H1 | **Partial failure reports success.** `plan["applied"] = deleted > 0`. Three uids out of 290 returns `applied: True`. The `note` fires only for COPY failures, never STORE failures. `mailbox_tools.py` passes `applied` straight up and does not reconcile `failed_uids` or `store_failed`. | **HIGH** |
| H2 | The `from_addr` path calls `find_messages` **without `folder=`** although the signature accepts it. It scans all folders to the 5000 cap and discards non-matching folders in Python, so the cap is spent on discarded rows and selection can silently under-cover. `truncated` is not computed on this path. One-word fix. | **HIGH** |
| H3 | `protected_senders.json` is read from `Path.cwd()` and falls back **silently** to built-in defaults. A safety list whose location depends on the process working directory. `account@` and `ratings@` are very broad substrings. | MEDIUM |
| H4 | The protected-sender blocklist guards **only** the `from_addr` path. Explicit `uids` bypass it entirely. | MEDIUM |
| H5 | COPY-then-STORE is no longer atomic. COPY ok + STORE fail leaves the message in Trash **and** in the source folder. Recorded in `store_failed`, never reconciled. | MEDIUM |
| H6 | Behavior removal: comma-separated uid strings were previously split, now hard-rejected. | LOW |
| H7 | Dead code: the first `_sel` loop is fully discarded by `_sel = _keep`. | LOW |

### 6.1 H1 is a SECOND, INDEPENDENT MECHANISM FOR DEFECT 1

Defect 1 is on record as the model claiming destructive actions it never
invoked - a parser and prompt problem, fixed by confabulation work.

H1 produces the identical symptom by a different route: **the tool truthfully
reports success for a partial move, and the model accurately reports an
inaccurate result.** No confabulation occurs. The model is not at fault.

These have different fixes and must be separated in the SDD. H1 is a
**result-contract** problem, and after reading the file it was assigned to, it
is **still open**.

---

## 7. WHAT THIS DOCUMENT DOES NOT COVER

Stated so the gaps are visible rather than implied:

- Speech pipeline gates (STT/TTS) beyond G13 - ports and encodings not yet read.
- PATH 2's four auto-approve sites - identified, not characterized.
- Format 2 of the tool-call parser - never read.
- Whether the 4.1 premise still holds after 6c - not retested.
- No CI, no clean-clone import check, no automated provenance. Provenance for
  W23 through W26 was reconstructed by hand, one file per window. **This does
  not scale.** The mitigation is CI plus commit-message provenance, not better
  handoff documents.

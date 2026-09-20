# OpenJarvis — Session Handoff, 2026-08-05 (end of day)

**Requirement one: NLP communication. Talk to Jarvis, Jarvis talks back.**

**Requirement two: no one-off workarounds.** Every capability is built *into* OpenJarvis.
Never a side script that routes around Jarvis.

Standing instruction from Gray: *validate, then assess. No guessing.*

---

## Read this first

1. **The backend IS live.** Restarted 08/05 09:09:25, PIDs 41704 + 12344 (same launch),
   verified `[LIVE]` against both patch mtimes. The Kokoro endpoint switch and the mailbox
   allowlist went live for the first time this morning. **This is no longer a blocker.**

2. **Two artifacts are on disk. One is applied, one is not.**
   `ttsPlayer.ts` is placed and hash-verified. `patch_chatarea_tts.py` has been delivered
   and fixture-tested but **has never been run against the real file.** That is the next
   action.

3. **`patch_mailbox_categories.py` never existed.** Resolved. The 08/04 delivery never
   reached disk. Nothing was half-applied — allowlist and registry both carry exactly the
   five original mailbox tools and are in parity.

4. **The mailbox live test has been ready since 09:09:25 and was never run.** It got
   displaced by speech work. It costs one prompt.

---

## What was fixed today

### The last sentence — CLOSED

Gray, on the same "Describe the water cycle in three sentences" prompt:
*"this is the first time Jarvis read the entire output from beginning to end."*

Full causal chain, proven end to end: Kokoro's `/synthesize-stream` returns multiple
complete WAVs concatenated → the first header declares 52.5% of the audio → any compliant
consumer stops at the sentence 2/3 boundary. `/synthesize` returns one valid WAV.

### `ERR_FILE_NOT_FOUND` — CLOSED as cosmetic

Two blob errors again on 08/05, against two synthesize calls, **and the full reply
played.** Both blobs erroring while audio completes proves the error fires *after*
playback, when the element re-touches a URL that `onended` already revoked. The revoke
race in `playNextChunk` is a real smell but was never costing audio. The rewrite deletes
the whole class anyway by not using object URLs.

### First-word clipping — ROOT CAUSED

| Step | Result |
|---|---|
| Direct POST of chunk-1 text | one valid WAV, 13.376 s, RIFF count 1 |
| Leading silence in the file | **0.0407 s** — very thin margin |
| Same text minus "The" | 13.141 s → **delta 0.235 s** |
| Verdict | the word IS synthesized and IS in the file |
| Gray plays the file in a media player | **missing on first play, present on rewind** |

**The Windows audio output endpoint sleeps when idle and swallows the head of the first
sound.** It reproduces entirely outside the browser. Not Kokoro, not the `<audio>`
element, and `canplaythrough` would not have fixed it. Every Jarvis reply is a first sound
after idle, which is exactly why it is always the first word of the first chunk.

**Hypothesis killed:** the 24,576-byte / 0.512 s delta between the streaming and
non-streaming Kokoro endpoints is *not* the missing first word. Do not revive that lead.

---

## The trap that was caught before it shipped

Assigning `hasMountedRef = true` as a standalone fix **would have re-broken the last
sentence.**

The two effects share `lastSpokenIdRef` with contradictory ownership. Mid-stream claims
the message id at line 115 as soon as it speaks its first sentence. The post-stream effect
then hits `if (lastMsg.id === lastSpokenIdRef.current) return` at 158 and never runs.
Meanwhile mid-stream's own guard at 111 shuts it off the instant `isStreaming` goes false.
Whatever is unspoken when streaming ends falls between them. `ttsInFlightRef` double-locks
it via the guard at 161.

This is why the fix is an ownership rewrite, not a boolean.

---

## The rewrite — delivered, fixture-tested, not yet applied

### Artifact 1 — `frontend\src\audio\ttsPlayer.ts` (PLACED)

9,548 B / 314 lines / pure ASCII / LF
SHA256 `1B3B3775C50185540E518E2CEE5C08EC82F3EEEF720484CBE3CD0D25FC055160`
MARKER `openjarvis-tts-player-v1`. New file — **rollback is deletion.**

- **One persistent AudioContext** with a silent looping keepalive. Holds the output
  endpoint awake. `KEEPALIVE_GAIN = 0.0` is a named const; raise to `0.0001` if any driver
  still idles through digital silence.
- **Self-priming** on first `pointerdown`/`keydown` (capture, once), so the context is
  never suspended when the first reply lands.
- **Clause-level splitting** on `.!?` and `,;:`, greedy-packed with
  `FIRST_UNIT_MAX_CHARS = 90` then `UNIT_MAX_CHARS = 350`.
- **Scheduled AudioBuffers** on one timeline. No object URLs, no revoke.
- **`generation` counter** so `stopAll()` drops in-flight synthesis from a cancelled turn.
- Failed units warn and continue rather than being silently swallowed.
- Exports: `primeAudio`, `beginTurn`, `enqueue`, `stopAll`, `isSpeaking`. No React
  dependency.

**Why the first unit is small:** synthesis runs ~1.7x faster than realtime — 13.376 s of
audio returned by a 7.68 s request. Once unit 1 is playing the queue can never starve, so
**only unit 1's latency is ever user-visible.** Shrinking it is the entire time-to-first-
audio win; shrinking later units would only add request overhead.

### Artifact 2 — `patch_chatarea_tts.py` (NOT YET RUN ON THE REAL FILE)

9,635 B / 273 lines / pure ASCII / LF
SHA256 `B10EC0E36BBA3338969FD56C909129EE6D23C0B744D9371CD2B41A6F03A5C14F`
MARKER `openjarvis-patch-chatarea-tts-v1`. `py_compile` clean.

Operates on **byte lines**, detects and preserves the existing terminator, never decodes
the whole file — required because `ChatArea.tsx` carries mojibake.

Five anchors, verified by index and compared after `.strip()`: lines **10, 37, 43, 71,
198**. Any mismatch aborts with no write.

Three edits:

| Lines | Change |
|---|---|
| 10 | drop `synthesizeSpeechChunks`, add the `ttsPlayer` import |
| 37-43 | seven playback refs collapse to three |
| 71-198 | `toggleMute` repointed at `stopAll()`; `playNextChunk` and **both** effects replaced by one driver effect |

The script **self-checks its own payload** before running — required substrings plus an
exact backtick count of 9 — because a delivered artifact arrived with backticks stripped
on 08/01. That check fired during testing on Claude's own wrong assertion of 6. It works.

### Fixture test — passed

A 498-line CRLF fixture was reconstructed from the verbatim reads. **All five anchors
landed at exactly 10/37/43/71/198**, independently confirming the line model matches the
real file.

- Dry run: 498 → 445 lines, 15,066 → 14,076 bytes
- Post-patch counts for `playNextChunk`, `chunkQueueRef`, `isPlayingRef`,
  `ttsInFlightRef`, `audioRef`, `synthesizeSpeechChunks`: **all zero**
- Apply: on-disk SHA256 matched the dry-run prediction exactly
- Re-run against the patched fixture: all anchors mismatch, script **refuses**. It cannot
  double-apply
- Junctions spot-checked: imports correct with `streamChat` shifted to 12; ref block 7 → 3
  with `sendAbortRef`/`sendTimerRef` intact; tail preserved

### The new driver

- **Mount pass adopts whatever is on screen as already-spoken** — claims the id, sets
  `spokenCharsRef` to full length. A restored conversation is never read aloud. *This is
  what `hasMountedRef` was always for.* It is kept, and now actually assigned.
- New reply (id change) calls `stopAll()`.
- While streaming, hands over text to the last completed sentence via
  `/^[\s\S]*[.!?](?=\s)/`. **Once streaming ends, hands over everything remaining
  regardless of punctuation** — that flush is what structurally guarantees the last
  sentence.
- Text is marked consumed **even when muted**, so unmuting mid-reply does not replay.
- Deps `[streamState.isStreaming, streamState.content, messages, muted]`.

---

## Next actions, in order

```powershell
cd C:\Users\Admin\Openjarvis
python .\patch_chatarea_tts.py
```

Read the anchor report. All five must say OK. Then:

```powershell
python .\patch_chatarea_tts.py --apply
cd frontend
npm run build:tauri
```

Then hard-reload `127.0.0.1:8010` (a stale tab runs the old bundle) and send a
multi-sentence prompt.

**Acceptance test — four things:**

1. Is the **first word** present?
2. Does audio start **before** the text finishes rendering?
3. Is the **last sentence** still spoken? (regression check on this morning's win)
4. Is the console **free of `ERR_FILE_NOT_FOUND`**?

Then the mailbox test that has been waiting all day. Ask Jarvis: *what's filling up my
Yahoo mailbox?* Expect `mailbox_usage_report`. First call is slow — it enumerates 53
folders, which is why it carries a 600 s timeout. If it fails, capture the console; the
failure mode distinguishes model-not-selecting-the-tool from executor-rejection from IMAP.

---

## Store / stream flow — question resolved

Lines 211-344 read verbatim. **The answer was favourable.**

The assistant `ChatMessage` is added to `messages` with `content: ''` **before** streaming
begins (232-238), and `updateLastAssistant` is called throttled to every 80 ms during the
stream (307). So `messages[messages.length - 1]` is the assistant message throughout and
its content grows. Reading from `messages` is correct.

**Consequence: `hasMountedRef` really was the sole blocker on mid-stream TTS.** No second
hidden blocker.

Teardown order in `finally`: final `updateLastAssistant` (337) then `resetStream()` (339).
The driver is correct whether React batches those into one render or two.

---

## Still open

- **True token-level streaming.** Needs *both* the Kokoro wrapper on the R630 (Gray's own
  code) to emit a frame-based format or one correct WAV stream, *and* a frontend consuming
  the stream instead of `res.blob()`. Neither alone helps. After the rewrite lands this is
  an optimization rather than a prerequisite.
- **Leg 3 / STT never traced.** `useSpeechStream.ts` is a WebSocket STT hook with barge-in
  (`bargeIn` consumed at `InputArea.tsx:68`). Status unknown. Mic is permitted.
- **Doubled prompt text.** The message bubble rendered the prompt twice with no separator.
  Unknown whether display-only or actually sent to the model. **Lead:** `ChatArea.tsx`
  201-209 registers a `jarvis-option-select` listener that re-dispatches as
  `jarvis-submit-text`. Check `InputArea.tsx` listeners before theorising.
- **Desktop `.exe` still fails, still zero direct observation.** Three hypotheses
  eliminated, nothing replacing them. Remaining move is eyes on the running exe: launch
  with `WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS=--remote-debugging-port=9222` and read the
  webview console. Tooling exists: `get-devtools-url.ps1`, `cdp_getbase.ps1`.
  **Standing architectural recommendation, unimplemented, Gray has not ruled:** point the
  Tauri production window at `http://127.0.0.1:8010` instead of embedding a copy. The
  backend runs anyway. One copy of the UI, no Rust rebuild for frontend changes, and this
  drift class disappears permanently.
- **Mailbox category extension.** Never landed; re-deliver when filing is actually the
  next job. All 18 category folders already exist on the Yahoo account, and filing is
  deliberately sequenced after the usage report, after junk deletion, and after the
  cloud-model switch.
- **Modified UTF-7 not decoded** in `_list_folders`. `AT&-T` is the wire form of `AT&T`.
  Not blocking — all 18 category folders are plain ASCII.
- **Classification throughput unsolved.** One LLM turn per message on `qwen3-coder:30b`
  does not scale. Workable shape is batched: a few hundred subject/sender lines per call,
  then one `mailbox_move_messages` per destination folder.

---

## Rollback register — additions today

| Covers | Backup | Status |
|---|---|---|
| TTS playback engine | *(none — `ttsPlayer.ts` is a new file)* | delete to revert |
| ChatArea TTS rewrite | `ChatArea.tsx.bak_<timestamp>` written by `--apply` | **not yet created** |
| Kokoro endpoint switch | `speech_router.py.bak_20260803_163215` | applied, **live and validated** |

Reverting the frontend needs `npm run build:tauri` to reach the served bundle — in either
direction.

---

## Standing rules

- **No one-off workarounds.** Build into Jarvis or don't build it.
- No command that echoes any line of a secrets file. Line numbers and a
  parses/doesn't-parse boolean only.
- Gray does **not** run dev servers. Production builds only.
- **Every generated `.ps1` must be PowerShell 5.1.** No `??`, no `?.`, no ternary, no
  `-Parallel`. PS 5.1 parses the whole file before executing.
- Any repo-wide grep must exclude `.venv`, `node_modules`, `.fix_backups_*`, `target`.
- Delivered text artifacts arrive **either byte-identical or one byte short** (trailing
  newline stripped). Anything else is corruption.
- Group commands into one block. Don't make him round-trip.
- Lead with the better answer. Don't soften a finding to keep momentum.
- Always verify `[LIVE]` against a PID from `netstat`, never a remembered one.
- `[System.IO.File]` resolves relative paths against .NET's CWD (`system32`). Always pass
  `(Resolve-Path '.\x').Path`.
- Encoding damage is **not** uniform. `ChatArea.tsx` and the `.ps1` files carry mojibake;
  `middleware.py` is clean. All Claude-authored files are pure ASCII by design.
- Patches to mojibake-carrying files use **line-anchored, byte-level** replacement. Never
  decode and re-encode the whole file.

---

## Corrections logged

- **The 0.512 s streaming delta is not the first word.** Killed by direct evidence.
- **`hasMountedRef` is not a bug of omission, it is an unfinished guard.** It exists to
  stop a restored conversation being read aloud on mount. The rewrite keeps it and
  finally assigns it.
- **`patch_mailbox_categories.py` was never on disk.** Status is no longer unknown.
- **`requires_confirmation=True` is a trap, not a gate.** `ToolExecutor.execute` fails
  every call rather than prompting when there's no interactive callback.
- **Connector `mcp_tools()` are never executable.** Agent tools come only from
  `MCPServer().get_tools()`; the allowlist silently drops any name not in that dict.
- **The `qwen3-coder:30b` "model override" never existed.** That config file is
  machine-rewritten; never trust a recorded read of it across sessions.
- **`OPENJARVIS_ROOT` is inert.** Dead configuration, not a live fault.
- **The repo-side `configs\openjarvis\config.toml` is read by nothing.**
- **`middleware.py:3` is not a defect.** Starlette middleware annotations are never
  introspected. Do not "fix" it.

---

## Unresolved ambiguity worth not re-litigating

Gray has twice said *"I did pull Ollama and the models from the workflow."* All hard
evidence supports the `ollama pull` reading: engine `ollama` live in `/v1/info`, 29 models
on 172.16.33.200, health probes returning 200. Do not raise it unprompted.

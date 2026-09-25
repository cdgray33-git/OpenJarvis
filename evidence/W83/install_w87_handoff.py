# install_w87_handoff.py - W87 handoff installer. Run from PS C:\Users\Admin\OpenJarvis> with the venv python.
# Writes BRIEF-W88-2026-09-24.md (repo root), replaces the ARCHIVE-W83 PART 5 scaffold with the filled PART 5,
# edits docs\SDP\02-SRS-RTM.md and docs\SDP\08-POAM.md by anchored replace. ALL anchors are checked (count == 1)
# BEFORE anything is written; any miss = STOP, nothing written. Backs up every edited file. Does NOT commit.
import re, sys, time, shutil
from pathlib import Path

ROOT = Path.cwd()
TS = time.strftime("%Y%m%d_%H%M%S")
BAK = ROOT / "evidence" / "W83" / "backup"
ARC = ROOT / "ARCHIVE-W83-2026-09-24.md"
RTM = ROOT / "docs" / "SDP" / "02-SRS-RTM.md"
POAM = ROOT / "docs" / "SDP" / "08-POAM.md"
BRIEF = ROOT / "BRIEF-W88-2026-09-24.md"
for p in (ARC, RTM, POAM):
    if not p.is_file():
        sys.exit("STOP: missing %s - run from the repo root; nothing written" % p)
if BRIEF.exists():
    sys.exit("STOP: %s already exists - installer ran before; nothing written" % BRIEF)

def rd(p):
    s = p.read_bytes().decode("utf-8")
    return s, ("\r\n" if "\r\n" in s else "\n")

BRIEF_TEXT = r"""# BRIEF W88 - 2026-09-24 (supersedes BRIEF-W87; written at c85fcf9)
## READ THIS FILE ONLY. DO NOT READ AN ARCHIVE UNLESS A SECTION IS NAMED BELOW.
ARCHIVE-W83: PART 1 (s1-s7), PART 2 (s8-s14), PART 3 (s15-s18), PART 4 (s19-s22), PART 5 (s23-s26, W87), then carried
archives below '## ---------- CARRIED FROM ARCHIVE-W82 BELOW ----------'. Extract by section name; locate markers as WHOLE
LINES (H-W83-25). The SDP (docs\SDP) is the primary record.

## OWNER GOAL
Finish the AUTHOR'S initial build, then enhance Jarvis into the executive assistant (installation guide MANDATORY).
ULTIMATE GOAL (owner W83): a clear communications data flow of Jarvis that can be visualized with NO GAPS IN VISIBILITY.
VERIFIED 4/28 core (RQ-021, RQ-022, RQ-024, RQ-030). Phase 2 pulled forward (D-39); RQ-032 PARTIAL (see below).
OWNER RULING W87: "we fix what we find while trying to stay true to the original authors intent. The AO is not being
considered for anything that we fix that is the authors ... we will address the AO concerns after it works."
-> Fix first, author intent first. Risk assessment still goes to the owner; the AO lens is NOT a gate on fixing.

## STATE AT CLOSE
- HEAD c85fcf9 on HEAD, origin, gitlab (matched) = G-10 patch A. The handoff commit (this BRIEF, ARCHIVE PART 5, RTM v0.9,
  POA&M) follows it - CHECK `git log --oneline -1 --decorate` at open (H-W83-24).
- Server PID 20320 started 21:36:23 running patch A. Backend 127.0.0.1:8010. Model qwen3-coder:30b on .200.
- config.toml (OUT OF GIT): [memory] 5 / 0.0 / 2048; [agent] native_openhands, max_turns 15, 19 tools incl. code_interpreter,
  file_read, file_write, shell_exec. SOUL.md: author default + notes line (D-37) + Office line (D-44).
- D-46 LIVE (openjarvis-w87-codefiles-v1): code_interpreter lists files created/changed in the workspace FIRST in content and
  in metadata files[path,size_bytes] (rides TOOL_CALL_END). S3 re-run 4: files 5/6, honest replies 6/6 vs filesystem,
  shell_exec 0, 32/40. R2 false negative GONE. R1 = model code error (no pptx anywhere). R3 formulas still omitted.
- RQ-032 criterion (proposed W87): 6/6 real files AND 6/6 honest replies in ONE run. NOT MET (files 5/6). PARTIAL.

## W88 NEXT ACTIONS IN ORDER
0. SDP OWED (not written W87 - files not read): Vol 3A (03-AUTHOR-BASELINE) G.6 D-46 record and SDD (04-SDD) section 17
   visibility delta. Text is ready in ARCHIVE-W83 s26. Upload both files whole (one concatenated file), then anchored edits.
1. G-11 (POAM-54): record tool content text (truncated) + code_interpreter exit code in dispatch.log. AUTHOR FIRST: check what
   the author's TraceCollector / traces store would have recorded (POAM-32: trace modules deleted). Closes patch A's live
   LIMIT (the Files line reaching the model is not yet directly observed). Blocked measurement TWICE in W87.
2. Patch B (G-10 remainder, POAM-53): file_write success message echoes the RESOLVED path (author already puts it in
   metadata; the message shows only the requested name, which D-43 anchoring now hides). Verify in isolation.
3. S3 re-run 5 with evidence\W83\s3_family_office_w87.py -> RQ-032 assessment + ruling (NO BLIND DECISIONS).
4. Visibility: the downloadable data-flow artifact (ports/protocols/encoding per gate, SDD 16+17).
5. G-3 delivery (POAM-51); G-6 skills catalog (POAM-52); R3 formula fidelity (POAM-55).
6. G-1 (POAM-50, security: code_interpreter writes to any absolute path) - after it works (owner W87); author-first read of
   code_interpreter_docker before choosing.
QUEUED: remote MCP (author-first); self-learning; persona for other agents; DISPATCHER; knowledge.db; O-2 Office by COM;
C streaming STT (POAM-38); H-W81-6 WS auth; grpcio yanked (POAM-56).

## HARD FACTS A NEW WINDOW WILL GET WRONG
- The model sees ToolResult.CONTENT ONLY (native_openhands, all 3 branches; truncated at 4000 chars). metadata goes to the
  event bus (TOOL_CALL_END, JSON-safe) = the author's machine record. A new file EventType is NOT needed.
- code_interpreter success=True means exit code 0 ONLY, not "did what was asked" (H-W83-26). Judge by files + content.
- code_interpreter blocklist (author, substring): os.system, os.popen, subprocess., shutil.rmtree, os.remove, os.unlink,
  os.rmdir, __import__, eval(, exec(, compile(, open(. A ~0.003 s FAIL_OTHER is a blocklist hit.
- D-46 sees the workspace TOP LEVEL only; subfolders and absolute-path writes (G-1) are not listed (H-W83-28).
- dispatch.log (%LOCALAPPDATA%\OpenJarvis\logs) OUTCOME = reason code only; ATTEMPT args cut at 400 chars. No tool content.
- Downloaded .py files are SAVED to Downloads and run with the venv python - never pasted into PowerShell (H-W83-27).
- Every carry marker is ALSO quoted in the INDEX line above it - find markers as whole lines (H-W83-25).
- AUTHOR BASELINE = af21bc18 in C:\Users\Admin\upstream-OpenJarvis (git -C ... show af21bc18:path). git grep -F, no
  embedded double quotes (PS 5.1).
- venv has NO pip (uv 0.11.11). `uv add --no-sync` then `uv pip install --python .venv\Scripts\python.exe pkg==locked`.
  NEVER a bare `uv sync`. NEVER `jarvis _bootstrap --write-config`.
- Office files: code_interpreter (python-docx/pptx/openpyxl), cwd = C:\Users\Admin\.openjarvis\workspace, 30 s. file_write
  is plain text and REFUSES .docx/.pptx/.xlsx.
- Gate-eligible tools (shell_exec) WAIT 120 s for a human in unattended tests - by design.
- Restart = `.\start-openjarvis.ps1` in the admin session (bare name hits a stale System32 copy). V&V blocks guard on the
  8010 listener StartTime being later than the patch file time.
- ALL W67-W87 HARD FACTS REMAIN IN FORCE (ARCHIVE-W83 s1-s26, carried archives, SDP).

## ROLLBACK POINTS
Patch A (D-46): git revert c85fcf9, or copy evidence\W83\backup\code_interpreter.py.bak-W87-codefiles-20260924_213031 over
src\openjarvis\tools\code_interpreter.py; restart; confirm START time.
Handoff edits: evidence\W83\backup\*.bak-W87-handoff-<ts> (ARCHIVE, RTM, POAM) or git revert of the handoff commit.
W83 rollbacks: BRIEF-W87 ROLLBACK POINTS (F-11, F-7/F-9, F-8, S2, S1) and BRIEF-W86 (earlier).

## RULES OF ENGAGEMENT
Full text ARCHIVE-W57 s6; additions W62-W87. GRAY UPLOADS WHOLE FILES; several = ONE concatenated upload. ONE RUNNABLE BLOCK
PER MESSAGE. State shell and host first; run from PS C:\Users\Admin\OpenJarvis>. No non-ASCII. ALWAYS VERIFY. NEVER COMMIT
WITH THE PATCH. COMMIT ONLY AFTER LIVE V&V. FINISH THE THING. VALIDATE, DO NOT INTERROGATE. NON-INTERACTIVE tests. AUTHOR'S
PROCEDURES FIRST. PRODUCTION BUILD ONLY. Push BOTH remotes (origin = GitHub, gitlab = lab). NO BLIND OWNER DECISIONS.
FIX FIRST, AO AFTER IT WORKS (W87). AUTHOR DEFECTS FIXED AND DOCUMENTED (symptom, trigger, fix). Window switching by context
usage. Separate code fixes from persona changes by re-measuring between them. Dry-run patches in the sandbox against the
uploaded file before delivery (W87 practice).

## TOOLING REGISTER DELTA (W87)
evidence\W83\s3_family_office_w87.py (40 checks: details + reply honest + shell_exec count + RQ-032 criterion line; writes
s3-rerun4.txt); patch_codefiles.py (patch + 6 in-process checks + auto-rollback on compile fail); R1 dispatch-window +
filesystem sweep block (ARCHIVE s25/s23 ex17); read bundlers (rq032-ruling-bundle, g10-selfverify-bundle, g10-path-bundle).

## SDD / SDP
Touched W87: 02-SRS-RTM v0.9 (RQ-032 re-run 4 evidence, duplicate progress text removed), 08-POAM (POAM-53 partial, POAM-54
note). OWED: 03-AUTHOR-BASELINE G.6 D-46; 04-SDD section 17 (action 0).

## 550B CLOUD MODEL
openrouter nvidia/nemotron-3-ultra-550b-a55b for whole-file questions (bundle + question on top + posting script). Not used W87.

**Program goal:** a functional executive assistant. VERIFIED 4/28. W87 made Jarvis tell the truth about the documents it
creates (R2 class closed, honest replies 6/6) and put the file-created record on the author's own event. Next: record what
tools actually return (G-11) so the whole data flow can be drawn with nothing hidden.
"""

PART5 = r"""## ========== PART 5 (W87 window: f59a897 -> c85fcf9, G-10 patch A) ==========
## INDEX PART 5: s23 narrative | s24 evidence | s25 negative results + hazards | s26 SDP feed, progress, register deltas

## s23 Narrative, part 5
ex1 Window opened on BRIEF-W87. Action 0 MEASURED ALREADY DONE: f59a897 (W83 handoff refresh) on HEAD, origin/main and
  gitlab/main; the BRIEF "handoff commit PENDING" line was written before its own commit.
ex2-3 ARCHIVE PART 5 scaffold inserted by byte splice above the W82 carry marker. First attempt STOPPED by its own guard
  (marker count 2: the marker is also quoted in the INDEX line); rerun anchored the marker as a whole line. HEAD/TAIL True.
ex4-6 RQ-032 ruling bundle (RTM + POA&M whole + PART 4). Assessment: A verify / B hold until G-10 + re-run / C narrow.
  R2 fails the R1 reply-content rule (valid .docx, reply said it failed) -> 5/6 under the program's own rule.
ex7 OWNER RULING W87: "we fix what we find while trying to staying true to the original authors intent. The AO is not being
  considered for anything that we fix that is the authors. Our build modified the original and we will address the AO
  concerns after it works." -> fix G-10 now; the RQ-032 ruling follows a re-run.
ex8-12 Author-first reads (g10-selfverify-bundle, g10-path-bundle). The model sees ToolResult.content ONLY (native_openhands,
  all three branches, cut at 4000 chars). ToolExecutor publishes JSON-safe metadata on TOOL_CALL_END (for TraceCollector /
  SkillOptimizer) = the author's file-created record; no new EventType needed. Author file_write/file_read put
  {path, size_bytes} in metadata; content echoes only the requested name. Author code_interpreter returns stdout only, so a
  silent save gives "(no output)". R2 (re-run 3) re-read: code_interpreter OK x2 (file made), shell_exec GATE_TIMEOUT 120 s,
  file_write .txt, code_interpreter blocklist hit 0.003 s, reply "failed". Configured tools include file_read and
  code_interpreter (non-gated checks existed; the model had no path to check against).
ex13 Patch A openjarvis-w87-codefiles-v1 (D-46): workspace top-level snapshot before/after the run; changed files listed
  FIRST in content and in metadata files[path,size_bytes]. Dry-run 6/6 in the Claude sandbox on the uploaded file, then
  in-process 6/6 on the real file (V3 content: path first, Output after).
ex14-16 S3 re-run 4 (s3_family_office_w87.py, 40 checks). One paste error: the Python file was pasted into PowerShell -
  parse-rejected, nothing ran. Result: files 5/6, honest replies 6/6 vs the filesystem (the checker scored R1 honest FAIL
  only by its missing-file rule), shell_exec 0 (was 1), 32/40, R3 formulas FAIL (POAM-55). R2 FIXED (5/5, no detour).
ex17 R1 traced (dispatch window + filesystem sweep of profile and C:\ top): t1 ImportError (`from pptx.shared import RGBColor`
  does not exist) 0.084 s; t2/t3 OK exit 0 but NO .pptx anywhere -> the script caught its own error or never saved (content
  unrecoverable, G-11); t4 blocklist hit 0.004 s; t5 file_write .txt; t6 print-only. Reply "wasn't able" = faithful.
ex18 Commit c85fcf9 (patch A + test + re-run 4 evidence), pushed both remotes. Owner: good stopping point -> handoff.

## s24 Evidence, part 5 (evidence\W83\)
Tracked (c85fcf9): s3-rerun4.txt, s3_family_office_w87.py, patch_codefiles.py. Untracked read bundles: rq032-ruling-bundle.md,
g10-selfverify-bundle.md, g10-path-bundle.md. Backups: backup\code_interpreter.py.bak-W87-codefiles-20260924_213031,
backup\ARCHIVE-W83-2026-09-24.md.bak-W87-part5-20260924_210006, backup\*.bak-W87-handoff-<ts> (installer).

## s25 Negative results and hazards, part 5
- NEGATIVE: action 0 install not needed - HANDOFF-W83d was already committed as f59a897 (git log --decorate at open).
- NEGATIVE: "S3 evidence missing" (ex7) was WRONG - the summary printed only ===== headers; the names were in the bundle.
- NEGATIVE: the second EventType (evals\core\event_recorder.py) is NOT a duplicate - a separate eval energy recorder with a
  different enum. Not a cleanup item.
- NEGATIVE: a new file-created EventType is NOT needed - TOOL_CALL_END already carries JSON-safe metadata.
- NEGATIVE: R1 in re-run 4 was NOT a G-10 failure - no .pptx existed anywhere; the reply was faithful.
- HAZARD H-W83-24: a BRIEF STATE line can be stale against HEAD (written before its own commit). Check at window open.
- HAZARD H-W83-25: every carry marker is ALSO quoted in the INDEX line above it. Locate markers as WHOLE LINES only:
  regex (?m)^<marker>\r?$ with a count-must-be-1 guard.
- HAZARD H-W83-26: code_interpreter success=True means exit code 0 only, not "did what was asked" (R1 t2/t3).
- HAZARD H-W83-27: downloaded .py files must be saved and run with the venv python, never pasted into PowerShell. Blocks
  that run a downloaded file check Test-Path first.
- HAZARD H-W83-28: D-46 sees the workspace top level only; subfolders and absolute-path writes elsewhere (G-1) are not listed.

## s26 SDP feed, progress, register deltas, part 5
APPLIED W87 (install_w87_handoff.py): RTM v0.9 - RQ-032 re-run 4 evidence, criterion proposed, duplicate progress text
removed (a defect found in RTM line 133); POA&M - POAM-53 partly closed (D-46), POAM-54 note.
OWED (action 0 W88; files not read W87): Vol 3A G.6 D-46 record and SDD section 17 delta. Text:
D-46 (W87, c85fcf9) code_interpreter file report. AUTHOR INTENT: content is what the model reads; metadata is the machine
record on TOOL_CALL_END (file_write/file_read use {path, size_bytes}). The author code_interpreter returns stdout only.
SYMPTOM: a document is created but the reply says it failed, or the model detours to shell_exec to check and waits 120 s on
the confirmation gate. TRIGGER: the model's script saves a file and prints nothing ("(no output)"). FIX: snapshot the
workspace top level before and after the run; list changed files FIRST in content (survives the 4000-char cut) and in
metadata files[path, size_bytes]. PLAIN LANGUAGE: after Jarvis runs its little program, it now looks in its own folder and
says "these files are new", so it does not have to guess whether it worked. LIMIT: workspace top level only (G-1 outside).
SDD 17 visibility delta: code_interpreter gate - file creation VISIBLE (content + TOOL_CALL_END metadata); tool content text
still NOT recorded durably (G-11); the Files line reaching the model is inferred from outcomes, not observed.
Progress: VERIFIED 4/28 core unchanged. Phase 2 RQ-032 PARTIAL: honesty half met (6/6), files 5/6. Moved toward the goal:
Jarvis no longer tells a family member a document failed when it succeeded (R2 class), and the file-created record rides the
author's own event.
Tooling +: s3_family_office_w87.py; patch_codefiles.py; R1 dispatch-window + filesystem sweep block; read bundlers.
Rules +: FIX FIRST, AO AFTER IT WORKS (owner W87); dry-run patches in the sandbox against the uploaded file before delivery.
Cleanup register: no additions.

"""

edits = []  # (path, old, new)
arc, anl = rd(ARC)
p5 = "## ========== PART 5 (W87 window, opened at f59a897) =========="
w82 = "## ---------- CARRIED FROM ARCHIVE-W82 BELOW ----------"
ms = list(re.finditer(r"(?m)^" + re.escape(p5) + r"\r?$", arc))
me = list(re.finditer(r"(?m)^" + re.escape(w82) + r"\r?$", arc))
if len(ms) != 1 or len(me) != 1 or ms[0].start() >= me[0].start():
    sys.exit("STOP: ARCHIVE PART 5 start %d / W82 marker %d (need 1 each, in order) - nothing written" % (len(ms), len(me)))
a0, a1 = ms[0].start(), me[0].start()
arc_new = arc[:a0] + PART5.replace("\n", anl) + arc[a1:]

rtm, rnl = rd(RTM)
R = [
 ("v0.8 (W83): RQ-024 VERIFIED by owner ruling, 4/28.",
  "v0.8 (W83): RQ-024 VERIFIED by owner ruling, 4/28. v0.9 (W87): RQ-032 re-run 4 evidence after D-46; duplicate progress text removed."),
 ("| RQ-032 | code_interpreter + python-docx/python-pptx/openpyxl (D-40..D-45); SOUL Office line (D-44) | dispatch.log, workspace files | W83 S3 re-run 3: 6/6 real .docx/.pptx/.xlsx from undirected family requests, 33/34 requested details machine-checked; open: G-3 delivery, G-10 self-verification (R2 false negative) | PARTIAL - owner ruling pending |",
  "| RQ-032 | code_interpreter + python-docx/python-pptx/openpyxl (D-40..D-46); SOUL Office line (D-44) | dispatch.log, workspace files, TOOL_CALL_END metadata (D-46) | W83 S3 re-run 3: 6/6 real .docx/.pptx/.xlsx from undirected family requests, 33/34 details; R2 false negative (G-10). W87 D-46 (c85fcf9, code_interpreter reports files created): S3 re-run 4 (40 checks incl. reply honesty, evidence\\W83\\s3-rerun4.txt): files 5/6 (R1 model code error, no file anywhere), honest replies 6/6 vs filesystem, shell_exec 0, 32/40, R3 formulas omitted. Criterion proposed W87: 6/6 real files AND 6/6 honest replies in one run - NOT MET. Open: G-3 delivery, file_write path echo (patch B) | PARTIAL |"),
 ("OPEN: RQ-004. NOT VERIFIED: RQ-025. NOT ASSESSED: 20. OPEN: RQ-004. NOT VERIFIED: RQ-025. NOT ASSESSED: 20.",
  "OPEN: RQ-004. NOT VERIFIED: RQ-025. NOT ASSESSED: 20.\nPHASE 2 PROGRESS (W87): RQ-032 re-run 4 after D-46 - files 5/6, honest replies 6/6, criterion NOT MET; PARTIAL. VERIFIED 4/28 core unchanged."),
]
for old, new in R:
    edits.append((RTM, old.replace("\n", rnl), new.replace("\n", rnl)))

poam, pnl = rd(POAM)
P = [
 ("v0.2 DRAFT 2026-09-23 (W82), W83 update 2026-09-24 (POAM-40..56, CLOSED rows).",
  "v0.2 DRAFT 2026-09-23 (W82), W83 update 2026-09-24 (POAM-40..56, CLOSED rows), W87 update 2026-09-24 (POAM-53 partial, POAM-54 note)."),
 ("| AU-2, SI-10 | G-10 [M] | Open |",
  "| AU-2, SI-10 | G-10 [M] | PARTLY CLOSED W87 c85fcf9 (D-46: code_interpreter lists created files first in content and in metadata on TOOL_CALL_END; S3 re-run 4 honest replies 6/6, shell_exec 0). Remaining: file_write message echoes the requested name, not the resolved path (patch B) |"),
 ("| AU-3 | G-11 [M] | Open - visibility gap (owner goal) |",
  "| AU-3 | G-11 [M] | Open - visibility gap (owner goal). W87: blocked measurement twice (R2 tool content; R1 t2/t3 exit 0 with no file) and leaves D-46's Files line unobserved live |"),
]
for old, new in P:
    edits.append((POAM, old.replace("\n", pnl), new.replace("\n", pnl)))

texts = {RTM: rtm, POAM: poam}
bad = []
for path, old, new in edits:
    n = texts[path].count(old)
    if n != 1:
        bad.append("%s anchor count %d: %s..." % (path.name, n, old[:70]))
if bad:
    print("\n".join(bad)); sys.exit("STOP: anchor check failed - nothing written")
for path, old, new in edits:
    texts[path] = texts[path].replace(old, new)

BAK.mkdir(parents=True, exist_ok=True)
for p in (ARC, RTM, POAM):
    shutil.copy2(p, BAK / ("%s.bak-W87-handoff-%s" % (p.name, TS)))
ARC.write_bytes(arc_new.encode("utf-8"))
RTM.write_bytes(texts[RTM].encode("utf-8"))
POAM.write_bytes(texts[POAM].encode("utf-8"))
BRIEF.write_bytes(BRIEF_TEXT.replace("\n", "\r\n").encode("ascii"))

# ---- verify ----
arc2 = ARC.read_bytes().decode("utf-8")
ok = []
ok.append(("ARCHIVE head byte-verbatim", arc2[:a0] == arc[:a0]))
ok.append(("ARCHIVE tail byte-verbatim (W82 marker onward)", arc2.endswith(arc[a1:])))
ok.append(("ARCHIVE PART 5 filled (s23..s26 present once)", all(arc2.count(h) == 1 for h in ("## s23 Narrative, part 5", "## s24 Evidence, part 5", "## s25 Negative results and hazards, part 5", "## s26 SDP feed, progress, register deltas, part 5"))))
r2 = RTM.read_bytes().decode("utf-8"); p2 = POAM.read_bytes().decode("utf-8")
ok.append(("RTM edits present (3)", all(r2.count(n.replace("\n", rnl)) == 1 for _, n in R)))
ok.append(("POAM edits present (3)", all(p2.count(n.replace("\n", pnl)) == 1 for _, n in P)))
bl = BRIEF.read_text(encoding="ascii").splitlines()
ok.append(("BRIEF-W88 written, ASCII, %d lines (60-100)" % len(bl), 60 <= len(bl) <= 100))
ins = PART5 + BRIEF_TEXT + "".join(e[2] for e in edits)
ok.append(("inserted text ASCII-only", all(ord(ch) < 128 for ch in ins)))
for name, v in ok:
    print(("PASS " if v else "FAIL ") + name)
print("backups: %s\\*.bak-W87-handoff-%s" % (BAK, TS))
print("RESULT %d/%d" % (sum(1 for _, v in ok if v), len(ok)))



# PART 9 - W91 (2026-09-25) FRONTEND MERGE DECISIONS
## s40 W91 NARRATIVE
Open: step 0 PASS (main 030f770a on both remotes, PID 27988 on 8010, worktree upgrade/a6dcf846 MERGE_HEAD
a6dcf846, graft local only, 17 unmerged all frontend). Main worktree showed 71 dirty entries (not investigated;
no bearing on the worktree merge). Owner chose Option A (careful merge) after the s38 assessment.
The resolve-45 bundle (734647 B, 4FCE0C3E...1629) was zipped (154761 B, FE47D96A...0457) to avoid loading 734 KB
into context. First placed in Downloads - owner flagged it as a THIRD location for the same data type; moved to
evidence\W91 and the rule was set: window artifacts live in evidence\W<n>\ only (H-W91-2).
On-disk count 115 diff3 hunks = bundle count; s38's 117 was a record error (NEGATIVE RESULT). All 17 files LF,
no BOM. Sandbox triage parsed every hunk (ours/base/theirs sizes, drift-from-base ratios) and settled the easy
class first. Cross-file facts were measured in the worktree (git grep, --no-pager after a pager hang, H-W91-1).
Two silent defects found that a green build would not catch (H-W91-4 double chat POST, H-W91-5 doubled base URL).
Graft-artifact test established (H-W91-6): f2fcb30c is a ROOT commit dated 2026-05-30 (graft off);
handleAutoUpdateToggle and recoveryError never existed in our history (artifacts); GmailOAuthAdvanced and
openjarvis-search-key existed in f2fcb30c and were removed in bc498a16 (v0.2.0, message names none of them).
Owner decisions: Option 1 (take author for the bc498a16 removals - owner: "Our Jarvis is still working, not
relevant"); Option B (keep our CSP allowlist, App analytics stays out). 550B asked on the big three (paid model,
170 s, $0.087): useful leads, partly wrong map (s42). Window closed on context use before writing resolve_45.

## s41 RESOLVER SPEC - 14 FILES (hunk numbers = order on disk; O=ours T=theirs)
package.json      h01 T, h02 T (author versions; @tauri-apps/api ^2.11.1 supersedes our ^2.11.0).
Cargo.toml        h01 T (toml_edit "0.25" + tauri "2"; our =2.11.0 pin DROPPED - build checks tauri/api alignment).
tauri.conf.json   h01 O (OWNER OPTION B): our CSP allowlist incl. 172.16.33.200, ipc.localhost, media-src blob: data:.
App.tsx           h01 COMBINE = our 2 lines (// openjarvis-confirm-app-v1 + ConfirmPrompt import) + author UpdateChecker
                  import ONLY (NO track/hashId import). h02 O (no analytics; author's prevModelRef would be unused).
MessageBubble     h01 = our parsedOptions line ONLY (author hoisted cleanContent to clean line before the hunk).
CommandPalette    h01 T (storageKey removed), h02 T (ours was an ASCII fix only).
SetupScreen       h01 T, h02 T (ws), h03 T, h04 T (wrapper div + custom-source steps), h05 T (graft artifact).
AgentsPage        h01 T (author fixed object args the same way we did), h02 T (author rewrote InteractTab/loadIdle).
store.ts          h01 T (apiKey: string, #266). h02 COMBINE:
                      if (persist) saveConversations(store);
                      if (get().activeId === conversationId) {
                        set({ messages: [...conv.messages] });
                      }
vite.config.ts    h01 COMBINE = `    sourcemap: true,` + author target comment/line + `    rolldownOptions: {`.
                  h02 COMBINE = author proxy block (object form, ws: true) with 8000 -> 8010 in all three entries.
api.ts            h01 T (drops our stray BOM line). h02-h49 T (path-only apiFetch calls).
                  h50 COMBINE = our confirmTool block (Defect 6 inbound) + author Approvals + Inference-source block.
                  CLEAN-REGION EDITS: delete our `function getAuthHeaders()` and our `async function apiFetch(input...)`
                  (C-W91-1); strip getBase() from 4 clean calls: /health, /v1/speech/health, /v1/speech/synthesize,
                  getBase() + '/v1/connectors/upload/ingest/files'. Sandbox sim: no duplicate declarations remain.
sse.ts            h01 COMBINE = `import type { SSEEvent } from '../types';` + `import { getBase, authHeaders } from './api';`
                  (ResearchEvent is NOT in types - our alias `export type ResearchEvent = SSEEvent;` stays).
                  h02 O (EMPTY - prevents the double POST, H-W91-4). h03 T (query, model?). h04 T.
                  CLEAN-REGION EDITS: delete local getAuthHeaders (C-W91-2); streamChat POST headers become
                  authHeaders({ 'Content-Type': 'application/json' }).
DataSourcesPage   h01 T. h02 T, h04 T, h07 T, h09 T (OWNER OPTION 1). h03 T (formatTimeAgo, same bc498a16 class).
                  h05 T, h06 T, h08 T (author Disconnect) PLUS insert OUR Reconnect/Cancel button as a sibling
                  (onClick setExpandedId(isReconnecting ? null : c.connector_id); label isReconnecting ? 'Cancel' :
                  'Reconnect'; our style). Reason: our clean-merged reconnect panel (isReconnecting && meta?.steps)
                  is only reachable through that button. Author disconnect state already merged clean (H-W91-7).
SettingsPage      h01 COMBINE icons: Server, Volume2 (ours) + RefreshCw (author).
                  h02 COMBINE = author api import list WITHOUT fetchSpeechHealth + our audioOutput + ttsPlayer imports.
                  h03 T (ws). h04 COMBINE = author inference-source state + load effect + saveSource, then our 5
                  audio-output state lines; DROP author's trailing health effect (ours is clean at ~18215 and
                  setSpeechBackendAvailable is not declared anywhere - W66 525ccde6 replaced it with the audio probe).
                  h05 T (OWNER OPTION 1; web-search key moves to keyed store - re-enter once). h06 T (graft artifact).
OPEN (W92): lib.rs 15, ChatArea 3, InputArea 8. s38 guidance stands; 550B leads in s42.

## s42 550B RESULT (evidence\W91\ANSWER-550b-big3-20260925-221924.md)
True hunk starts: lib.rs 63,73,157,943,1023,1066,1100,1122,1159,1198,1326,1478,1636,1684,1773;
ChatArea 39,96,532; InputArea 1,98,192,300,339,1119,1138,1259.
Score: lib.rs h01-h11 mapped right; true h12 (1478) SKIPPED; its h12-h15 = true h13-h15 + one invented.
ChatArea map right (COMBINE proposals for h01-h03 to verify). InputArea WRONG (10 hunks claimed) - discard.
Its lib.rs calls to verify: h01 O (8010), h02 O (our STARTUP_MODEL), h03 T, h04 COMBINE (remote-Ollama skip
inside author's launch_ollama block), h05-h11 graft artifacts of our old boot_backend.
Leads (NOT facts): R1 author verify_openjarvis_rust_extension assumes uv sync ran - our 383ccd5e removed uv sync
from boot. R2 removing auto-clone may leave project_root None -> unwrap panic. R3 normalize_host never adds
http:// (our configured_ollama_host fix). R4 ChatArea send may not set streamState.conversationId ->
isCurrentChatStreaming false -> TTS and dots never fire. R5 setSelectedAgentId store action may not exist.
Also: remote Ollama maps to author SourceKind::Custom (engine ollama, host http://172.16.33.200:11434) per 550B.

## s43 REGISTERS
CLEANUP +: C-W91-1 api.ts duplicate apiFetch + getAuthHeaders (removed in resolve_45). C-W91-2 sse.ts duplicate
getAuthHeaders (removed). C-W91-3 21 TRACKED backup files under frontend (BACKUP_2026-05-09_182130\*,
lib.rs.remote-ollama.bak, InputArea.tsx.bak.* x4, api.ts .bak/.fixbackup/.preload-fix/.repair, sse.ts.bak x3,
AgentsPage .bak/.prodfix.bak, SettingsPage .bak x4 + .prodfix.bak) -> git rm in the post-merge Graystone commit.
C-W91-4 ask-550b-554.ps1 writes to repo root (legacy location).
V&V + (8011): V-W91-1 exactly ONE /v1/chat/completions POST per message. V-W91-2 TTS health + synthesize reach
the backend (no doubled base). V-W91-3 upload ingest works. V-W91-4 research query streams (no literal
"research/stream" string exists in src - check router prefix; author gap if absent). V-W91-5 UpdateChecker under
our CSP (add its host only if needed). V-W91-6 Yahoo card shows Reconnect AND Disconnect, both work.
V-W91-7 web-search key re-entered in the author key store. V-W91-8 R1-R5 closed.
PLAN DEPARTURES (owner-approved): CSP kept (Option B, departs s38); bc498a16 removals reverted (Option 1);
Settings h04 drops author health effect; DataSources keeps both buttons.
NEGATIVE RESULTS: 117 -> 115; bundle-45 is not byte-true; our auth fix and author #266 are the same mechanism;
AgentsPage object-args fix is already in the author code; research/stream has no literal route string.

## s44 EVIDENCE (evidence\W91)
resolve-45-frontend-bundle.zip 154761 FE47D96AC9A051BA2BC1BAC3906D65F176AE521110262D68143941542DC40457
ask-550b-w91-big3.ps1          10701  787F5BC0EF8FCB140E6BD7C3680F86B07970A72F604C672B491FEC92F6682E97
bundle-550b-big3-20260925-221924.md 305589 0B71F1C9F866E14A0C211A3742E7D4C873115D8C15AA4C805433F95D9339A5D4 (BYTE-TRUE)
ANSWER-550b-big3-20260925-221924.md 63D21C07F44C5733D81D565B7490146ADC63DB2A838CC3838CCC4B72FB7AF5B4
BRIEF-W92-2026-09-25.md (repo root) and this PART 9 (appended to ARCHIVE-W83).

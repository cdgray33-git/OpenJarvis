# HANDOFF 2026-08-30 B / WINDOW 22
# FAMILY EA ARCHITECTURE RECOVERED FROM n8n - MODEL BAKE-OFF IS THE NEXT BUILD

Predecessor: HANDOFF-2026-08-30-A-W21-ITEM-20-CLOSED-CONFIRM-ID-SURVIVES-THE-WIRE.md
Host: Windows box. Shell: PowerShell 5.1. Working dir: `PS C:\Users\Admin\OpenJarvis>`.
Backend: 127.0.0.1:8010, ollama, qwen3-coder:30b, agent native_openhands.
Ollama host: 172.16.33.200 / `ollama-mcp`.

Window shape: a DESIGN window, not a patch window. No source file was modified. No
patch was applied, so nothing is left unverified. One live destructive mailbox
operation was verified against ground truth at the top of the window and closed out
cleanly before any design work began.

---

## 0. ONE PARAGRAPH FOR THE NEXT WINDOW

Jarvis moved bestbuy and express to Trash through NLP and **the claimed counts matched
ground truth exactly** - Defect 1 did not fire on a multi-turn destructive sequence, the
second clean run of that shape and the first on a sender that had previously
confabulated. Gray reviewed and emptied Trash; that thread is finished. The window then
turned to the family Executive Assistant, which is the actual point of the project. The
EA architecture was RECOVERED, not designed: ~118 n8n workflow exports in Downloads
contain a working supervisor-with-sub-agents design already wired to local Ollama models,
and it names four capabilities OpenJarvis does not have (calendar, contacts, content
creation, web search). The next window's build is a MODEL BAKE-OFF across the 29-model
ollama-mcp inventory, now pinned. The prerequisite that changed status this window: open
item 6 is no longer cleanup, it is a hard blocker for the sub-agent architecture.

---

## 1. WHAT WAS DECIDED (rulings, do not revisit)

- **RULING: pair models to TASK CLASSES, not to people.** Deck generation is deck
  generation whether the subject is Visa Commercial Solutions or a nonprofit. Email
  triage against the 18-label set is the same job on all three mailboxes. Per-person
  pairing would mean maintaining three stacks that do the same four things.
- **RULING: the model list is now pinned and will be used often.** Gray downloaded the
  current 29 models arbitrarily and is explicitly willing to pull better ones if a
  bake-off shows something stronger.
- **RULING (carried, reconfirmed by a second independent arrival): the model judges
  character, the ruling list overrides in code.** The n8n `Infer Provider` node reaches
  the same principle from the other direction - provider routing is deterministic Set
  logic BEFORE the agent, so the model never decides Gmail-vs-Yahoo. Gray arrived at this
  twice independently, which is good evidence it is right.
- **RULING: the n8n files are a SPEC, not a source.** They are workflow exports. The
  logic ports; there is no Python to reuse.

---

## 2. THE MAILBOX RUN - VERIFIED AND CLOSED

Gray had Jarvis moving bestbuy and express when the window opened.

### 2.1 Claim versus ground truth

Jarvis claimed: 38 bestbuy moved, 219 express moved.

`verify_sender.py` (direct `connector_for`, read-only) returned:

| Sender | ALLFOLDERS | Inbox | Archive | Trash | Bulk |
|---|---|---|---|---|---|
| bestbuy | 41 | 0 | 0 | **38** | 0 |
| express | 341 | 44 | 0 | **219** | 58 |

**Both claims exact. DEFECT 1 DID NOT FIRE.** This was a multi-turn destructive sequence
in one conversation - the precise condition that confabulated on 08/13 and again on
08/16 - and every number held. Second clean run of this shape after michaels on 08/15,
and notably express is the SAME SENDER that produced the third Defect 1 instance on 08/16
("successfully moved all 10, no failures", ground truth Trash 0).

Gray reviewed and emptied Trash: 260 messages, permanently gone.

### 2.2 The substring question, raised by Gray, answered by arithmetic

Gray observed that Jarvis searched on the word "express" and the search pulled in
unrelated senders. `verify_sender.py` matches on substring too, so the 341 figure spans
eighteen distinct addresses. The question was whether the MOVE had been equally loose.

`probe_express_addrs_v1.py` (repo root, read-only, written this window) broke the
remaining 122 down by address and folder. The survivors answer it:

- `express-scripts-pharmacy@orders.express-scripts.com` - **31 still in Inbox**, 2 Personal
- `express@b.express.com` - 4 Inbox, **7 Personal**
- `lowes@express.medallia.com` 3 Inbox, `pandaexpress@...` 1 Inbox,
  `panera@express.sea1.medallia.com` 1 Inbox, `account-services@account.express-scripts.com`
  1 Inbox, `ae-ug-ut-interest28@mail.aliexpress.com` 2 Inbox,
  `team@rewards.shopproductexpress.info` 1 Inbox
- AliExpress family - 58 in Bulk, untouched

That is exactly 44 in Inbox, matching `verify_sender.py`.

**FINDING: the find was loose, the move was tight.** Had the move swept the Inbox on the
substring, 31 pharmacy messages would have gone to a Trash that Gray then emptied.
They did not move. `express@b.express.com` Personal 7 was also correctly held - Personal
is a protected folder. The 219 moved were almost certainly `express@b.express.com` Inbox
alone, consistent with the 08/15 census figure of 215 plus two weeks of accumulation.

**LIMIT ON THAT CONCLUSION, stated plainly:** Trash is emptied, so the 219 cannot be
enumerated after the fact. This is strong survivor inference, not a record. The
definitive artifact would have been `dispatch.log`, which now records the ARGS of every
tool call - **that read was requested and never run.** If the question ever matters
again, `Get-Content .\dispatch.log -Tail 40` is where the answer lives, and it is the
only surviving record of what the move actually targeted.

### 2.3 Defect found in Jarvis's prose, not its actions

Jarvis said "All emails from these two senders have been moved to the Trash folder."
**False.** express still shows Inbox 44 and Bulk 58. The scoping was correct; the summary
sentence overclaimed. This is family-facing and belongs on the defect list: a correct
action described incorrectly is still a wrong answer to the person reading it.

### 2.4 Arithmetic that does not close

38 + 219 = 257. Gray emptied 260. Three messages in Trash came from somewhere else. Not
chased, recorded per the negative-results rule.

---

## 3. THE FAMILY EA - WHAT GRAY WANTS BUILT

This is the destination and has been for eight months. Captured this window in Gray's own
framing.

### 3.1 Wife - Director at Visa

- Executive-level PowerPoint generation
- Email triage
- Email response **with a human in the confirmation loop**
- Meeting scheduling, and **adjusting meetings based on recipient responses**
- Develops new approaches for Visa Commercial Solutions department processes
- Most production work on her PC; possibly a shared corporate box reachable remotely

### 3.2 Sister - CEO of her own company (for-profit and nonprofit)

- Personal AI Executive Assistant, reachable over VPN
- Already has a dedicated model profile in the OpenJarvis dropdown

### 3.3 Daughter - Executive Assistant of Special Projects, nonprofit serving disadvantaged youth girls

- Currently tasked with building the organization's local website
- Already has a dedicated model profile in the OpenJarvis dropdown

### 3.4 Task classes (the unit of model pairing)

| Class | Who | Status |
|---|---|---|
| Email triage / classification | all three | **Solved** - qwen2.5:32b, ~1.3 s warm, proven on 40 senders |
| Reply drafting in the person's voice | all three | Weakest local case. Bake-off needed |
| Executive deck generation | wife, sister | Hardest local case. Bake-off needed |
| Meeting scheduling and adjustment | wife, sister | **Not a model problem** - no calendar connector exists |
| Website build | daughter | qwen3-coder:30b, already on the box, already correct |

**The daughter's task is the easiest win in the set and needs no new model at all.**

### 3.5 The honest limit on local models, stated to Gray

A 32b at q4 will classify, summarize, and draft a competent internal email. It will
disappoint on a deck going in front of Visa leadership and on a reply in a CEO's voice.
No amount of prompting closes that fully. Workable shape: Jarvis does structure and first
draft, the human does the last 20 percent - which is what a real EA does anyway.

### 3.6 DATA BOUNDARY - answered

Gray's material may go to the 550B cloud model (OpenRouter) because it is his own code.
**His wife's Visa material is a different question and is a Visa policy matter, not a
technical one.** Local-only is the working assumption for family production work. Gray
wants a local model intelligent enough to serve these needs.

---

## 4. PROVIDER SCOPE AND THE CONNECTOR PROBLEM

- [Gray] All providers are in play: Yahoo, Gmail, Apple, Outlook, plus business SMTP.
- Yahoo: Gray built this connector twice (once in the Mac EA, once in OpenJarvis).
- Gmail: connector exists and is easy to integrate.
- Apple / Outlook personal: IMAP with an app password, same shape as Yahoo.
- **SMTP IS SEND-ONLY.** It covers replying. It does NOT cover triage, classification, or
  threading, all of which need IMAP or Graph. So "business SMTP" does not satisfy what
  the wife actually asked for.
- **The wife's Visa mailbox is the hard blocker and it is not code.** Corporate Exchange
  tenants typically disable IMAP and app passwords outright; the Graph path needs an app
  registration with tenant admin consent. **ACTION FOR GRAY: have her find out whether
  Visa permits app passwords at all.** The answer changes what gets built for her more
  than any model choice will. Fallback if unreachable: Jarvis serves her personal mail
  plus decks and documents she moves across deliberately.
- `connector_for()` is already the right abstraction seam. Add providers behind it rather
  than building four more standalone connectors (this matches the existing recommendation
  in the EA notes).

---

## 5. THE n8n ARCHIVE - ARCHITECTURE RECOVERED, NOT DESIGNED

### 5.1 What is in Downloads

118 JSON files. Keys are `name, nodes, connections, active, settings` - **n8n workflow
exports.** Not Python. The logic ports; the code does not.

Multiple generations exist side by side (`Ultimate Executive Assistant` at 9,498 /
13,511 / 17,367 bytes), so provenance matters before reusing any of them - the same
problem class as the 13 uncommitted files in section 8.

**HAZARD:** `👤 Create Yahoo Contact` is a **ZERO-BYTE file** that parses as nothing,
superseded by `Create Yahoo Contact 2026` (1,780 B). Exactly the class of thing that has
burned this project before.

### 5.2 The supervisor architecture, from `Ultimate Executive Assistant (Ollama) 2026v1` (17,367 B, 15 nodes)

```
Webhook (n8n-nodes-base.webhook)
  -> Normalize Request Schema   (set)
  -> Infer Provider             (set)
  -> Ultimate Assistant         (langchain.agent)         <- the supervisor
       |- Gmail Email Agent     (toolWorkflow)
       |- Yahoo Email Agent     (toolWorkflow)
       |- Contact Agent         (toolWorkflow)
       |- Content Creator Agent (toolWorkflow)
       |- Gmail Calendar Agent  (toolWorkflow)
       |- Yahoo Calendar Agent  (toolWorkflow)
       |- Tavily                (toolHttpRequest)         <- web search
       |- Calculator            (toolCalculator)
       |- Think                 (toolThink)
  -> Respond to Webhook
  (Ollama Chat Model - lmChatOllama - behind all of it)
```

**KEY DESIGN DECISION TO KEEP:** provider routing happens in deterministic code BEFORE
the agent. The model never decides Gmail-vs-Yahoo.

**CONTRAST WITH OPENJARVIS TODAY:** one agent, twelve flat tools. This is a supervisor
delegating to specialists. For the family that matters - "triage my mail, then schedule
the follow-up" is two specialists and a coordinator, which a flat tool list handles badly.

**CAPABILITY GAPS THIS NAMES, none of which OpenJarvis has:** calendar, contacts, content
creation, web search.

### 5.3 NOT YET PULLED

`🤖 Yahoo Email Agent 2026` (14,406 B) is the second-largest file and is a sub-agent spec.
Its node list is expected to carry the **draft-then-approve loop** Gray already solved
once. Pull it early next window - same command shape as section 5.2 was pulled with.

---

## 6. THE STATUS CHANGE THAT MATTERS MOST

**OPEN ITEM 6 IS NO LONGER CLEANUP. IT IS A PREREQUISITE.**

The confirmation gate is LIVE on the chat path (proven W20/W21, `confirm_id` verified on
the wire). On the managed-agent path it is AUTO-APPROVED AT FOUR SITES.

In a supervisor pattern, the supervisor delegates to a sub-agent and **the sub-agent's
tool calls are what actually touch mail.** If those run the managed-agent path, every
delegated destructive action bypasses the gate - and the human sees only the supervisor's
summary. That summary is precisely the surface Defect 1 fabricates on, and section 2.3
shows Jarvis overclaiming in a summary even when the underlying actions were correct.

The wife's requirement is explicitly "responding to emails with a human in the
confirmation loop." That requirement cannot be met on the sub-agent architecture until
item 6 is closed.

---

## 7. THE MODEL BAKE-OFF - NEXT WINDOW'S BUILD

Full inventory is pinned in memory (`openjarvis-models`). 29 models on `ollama-mcp`.
Summary: stock instruct (qwen2.5 32b/14b, qwen3.6:27b, qwen3.5 9b/4b/2b, olmo-3.1:32b,
mistral-small 24b and 3.1:24b, llama3.1:8b), coding (qwen3-coder:30b, qwen2.5-coder
32b/14b), vision (qwen3-vl 30b/8b, qwen2.5vl:7b), and Gray's own custom builds
(cody-agent v2/v1, infra-agent v4/v3/v2/v1, foundation-fundraiser, exec-strategist,
medical-scribe, direct-answer 32b/14b).

**Note two aliases: `qwen2.5-coder:32b` and `:32b-instruct-q4_K_M` share ID b92d6a0bd47e;
`qwen3-vl:latest` and `qwen3-vl:8b` share 901cae732162.** Do not bake them off against
themselves.

### 7.1 Already measured, do not re-run

- `qwen2.5:32b-instruct-q4_K_M` - 14.0 s cold / ~1.3 s warm, one-label classification;
  judged all 40 census senders, ~37/40 correct on character. THE CLASSIFICATION PICK.
- `qwen2.5:14b` - matches 32b warm speed, buys nothing on that task
- `qwen3.6:27b` - correct but 103.7 s, ~100 s of visible chain-of-thought. OUT
- `mistral-small3.1:24b` - wrong label
- `qwen3-coder:30b` - ~3 tok/s, TTFT 122.9 s. Coding only, per Gray's ruling

### 7.2 Open work on the bake-off

1. **Recover the existing persona pairings.** Gray built personas for his family members
   and they have dedicated model profiles in the OpenJarvis dropdown, but he does not
   remember which model each persona was paired with. Read the profiles out of config
   before designing anything - the answer may already be there.
2. **Design the scoring rubric BEFORE running the drafting bake-off.** The 08/15
   classification bake-off worked because "reply with exactly one label" is objectively
   scorable. Drafting quality is not. Without a rubric agreed in advance the result will
   not be defensible, and this project has already been burned by instruments that
   produced confident unusable numbers.
3. **Cost the concurrency constraint - never measured.** Three family users over VPN
   against one ollama host. A 32b at q4 is ~20 GB resident. Simultaneous users either
   queue or force a model swap per request. Measure real concurrent capacity before
   promising anyone response times.
4. Candidate task material: real deck outline, real reply-in-voice sample, real
   scheduling request. Non-interactive per the standing rule.

---

## 8. GIT STATE - UNCHANGED FROM W21, STILL THE LARGEST UNTRACKED RISK

**Nothing was committed this window because nothing was modified.** `dde85c3` remains the
tip on both remotes.

**STILL UNCOMMITTED - 13 modified tracked files with mixed provenance:**

```
configs/openjarvis/config.toml          frontend/fix_interface.ps1
frontend/src/audio/ttsPlayer.ts         frontend/src/components/Chat/ChatArea.tsx
frontend/src/lib/api.ts                 src/openjarvis/agents/native_openhands.py
src/openjarvis/connectors/imap_mail.py  src/openjarvis/core/events.py
src/openjarvis/engine/ollama.py         src/openjarvis/server/app.py
src/openjarvis/server/auth_middleware.py src/openjarvis/server/routes.py
src/openjarvis/tools/mailbox_tools.py
```

These carry the WS bridge fix, the v3 redaction, the mailbox patches and the loop patch.
One `git checkout` from lost, with nothing recording which window produced which hunk.
Method: `git diff --stat <file>`, match to the handoff claiming it, commit alone naming
that handoff, push both remotes. Do not batch.

**NEW UNTRACKED THIS WINDOW:** `probe_express_addrs_v1.py` (repo root, read-only). Adds
one more to the ~150 loose scripts. Not committed, per the W21 ruling against adding
probes one at a time.

**REPO ROOT POLLUTION unchanged:** ~150 loose scripts, 19+ untracked HANDOFF files, and
the stray `"patch_testexec_v1 .py"` with a space in the filename - an active
anchor-patching hazard that should be deleted.

---

## 9. EXECUTION PATHS REGISTER

Standing structure. Carried forward, not re-derived. **No new path was traced this
window** - no code ran through a new entry point.

Registered to date:
- PATH 1: orchestrator `ask()` via `system\orchestrator.py`
- PATH 2: managed-agent SSE via `_stream_managed_agent()` in
  `server\agent_manager_routes.py` - carries the four auto-approve sites (item 6)
- PATH 3: test-execute trigger - gate LIVE, `confirm_id` verified on the wire (W20/W21)
- Plus the routes.py chat dispatch branches 1a/1b/1c/1d

**ANTICIPATED, not yet real:** the supervisor-to-sub-agent delegation path from section
5.2. When that gets built it becomes a new path and MUST be registered with the standard
fields - and its confirmation-gate row is the whole reason item 6 blocks the
architecture.

---

## 10. SDP / SDD FEED

**Architecture chapter - major addition.** The target EA architecture is now documented
and it is a SUPERVISOR-WITH-SUB-AGENTS pattern recovered from a working n8n
implementation, not a design invented here. Section 5.2 has the full node graph. Record
the deterministic-provider-routing decision as a design principle with two independent
derivations (n8n `Infer Provider`, and Gray's classification ruling).

**Requirements chapter - new.** Section 3 is the first per-person capability list for the
family EA. It is the requirements baseline for everything the project exists to do, and
it names five task classes and their model-pairing status.

**Defect 6 confirmation gate - Gray flagged this for GREAT DETAIL.** W22 adds the
architectural consequence: the gate's four auto-approve sites on PATH 2 are a PREREQUISITE
BLOCKER for the sub-agent architecture, not a cleanup item. Document the delegation
hazard - human sees supervisor summary, sub-agent does the work, gate absent - alongside
the registry / payload / transport / threading rows already recorded.

**Threat model.** Carried from W21 and unchanged: an unauthenticated loopback WS
subscriber can read `confirm_id` and therefore answer a gate. Known accepted risk, scoped
to the local box.

**Verification methodology chapter - two entries this window.**
- POSITIVE: a destructive NLP operation was verified against independent ground truth
  before anything else in the window proceeded, and the verification is what made the
  substring question answerable at all.
- NEGATIVE: the `dispatch.log` read was specified and never executed, and Trash was then
  emptied. **The definitive artifact was available and was allowed to expire.** Survivor
  inference filled the gap and the conclusion is probably right, but "probably" is doing
  work that a two-second command would have removed. Record next to the W21 entry on
  specifying a discriminator the instrument does not display.

**Hazards found.** A correct action described incorrectly in family-facing prose
(section 2.3). Multiple generations of the same artifact with no provenance record -
now observed in BOTH the git working tree and the n8n archive, which makes it a pattern
rather than an incident. A zero-byte file sitting among valid ones (section 5.1).

---

## 11. 550B CLOUD MODEL

Carried forward per the 08/29 pin. When a question needs whole files rather than targeted
reads, bundle the suspected files into a single markdown file for Gray's 550B cloud model
(openrouter nemotron-3-ultra-550b) rather than spending window cycles on piecemeal reads.

**Not used this window.** Every read was a targeted probe or a JSON key dump; no
whole-file question arose. Recording that the escalation was considered and correctly
declined, per the negative-results rule.

**TWO STANDING CANDIDATES:**
1. The git hygiene provenance problem - 13 diffs matched against 19+ handoffs. Whole-file
   comparison across many files, exactly the shape this pattern exists for.
2. **NEW: the n8n archive.** 118 workflow JSONs with multiple generations of the same
   workflow. Deduplicating them and extracting the union of their logic is the same
   problem shape. Note the wife's Visa material must NOT go to the cloud model; the n8n
   files are Gray's own and are fine.

---

## 12. NEXT ACTIONS, ORDERED

1. **Recover the family persona model pairings** from the OpenJarvis config/dropdown.
   Cheap, and it may answer part of the bake-off before it starts.
2. **Pull the node list from `🤖 Yahoo Email Agent 2026`** (14,406 B) for the
   draft-then-approve loop. One command, high value.
3. **Design the drafting bake-off rubric, then run the bake-off.** Rubric first - this is
   the whole reason the classification bake-off produced a usable answer and a drafting
   one might not.
4. **Git hygiene, section 8.** Still the largest untracked risk in the repo and it has
   now been deferred across two windows.
5. **Open item 6** - the four managed-agent auto-approve sites. Now a prerequisite for
   the EA architecture, not cleanup.
6. Ask Visa (via wife) whether app passwords are permitted on her mailbox. Blocks her
   triage requirement and is a policy answer, not a build task.
7. Repo root layout: `scripts/`, `handoffs/`, `.gitignore`. Delete the stray
   `"patch_testexec_v1 .py"` with the space.

---

## 13. STANDING RULES IN FORCE

- ALWAYS VERIFY. Never stack a second change on an unverified first one.
- FINISH THE THING BEFORE STARTING THE NEXT. No dangling processes.
- State shell and host on every command. Default PowerShell on the Windows box; anything
  for the Ubuntu ollama host (172.16.33.200) must be labeled or PowerShell-wrapped ssh.
- Commands must run from `PS C:\Users\Admin\OpenJarvis>` as pasted. If a command needs a
  different path, say so IN THE REQUEST, before it runs.
- No non-ASCII symbols in replies.
- Tests must be non-interactive wherever possible.
- Pin the detail of every window including negative results.
- Push to both remotes, always. `origin` is GitHub, `gitlab` is the lab instance.
- Token conservation on working sessions.
- Flag at 15 exchanges, then hand off. A flag, not a stop - never cut a live trace.
- Architecture artifacts need ports, protocols and encoding at each gate, delivered as
  downloadable standalone files for Gray's wiki.

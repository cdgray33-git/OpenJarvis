# VOL 6 - CONFIGURATION MANAGEMENT PLAN, BASELINE, VERSION DESCRIPTION
Governing: NIST SP 800-53 CM family; SVD per DI-IPSC-81442 (verify). v0.1 DRAFT.

## 1. CHANGE CONTROL
Every change is a commit pushed to BOTH remotes: `origin` = GitHub,
`gitlab` = lab instance (naming is a known trap). [S 08/28]
Git paths must be taken from `git ls-files` (case-sensitive pathspecs on a
case-insensitive disk) [M W71]. Commit stat must list every intended file.

## 2. ROLLBACK POINTS
`*.bak-*` files are excluded by `.gitignore` line 20 [M]. They exist only on
the workstation disk and are NOT in either remote. See Vol 9.

## 3. VERSION DESCRIPTION (recent)
| Commit | Date | Content |
|---|---|---|
| cc21932 | 2026-09-21 | W70 handoff, stream probe (ChatArea omitted by case error) |
| 63257bd | 2026-09-21 | W70 fixup: ChatArea.tsx liveness probe |
| e5b35c9 | 2026-09-21 | W71 handoff |
Full history back to W1: GAP-018.

## 4. BASELINE PROVENANCE FINDING (CM-01) [M 2026-09-21]
- The repository root commit is `f2fcb30` (2026-05-30), message "Graystone
  Lab: remote MCP/Ollama integration, Rust extension, UI fixes". It is a
  Graystone commit, NOT the author's import.
- Therefore git history cannot distinguish author code from Graystone changes
  made before 2026-05-30. "Unchanged since root" means unchanged since
  Graystone's first commit only.
- File dates are not evidence: `agents\_stubs.py` is dated 2026-07-04 on disk
  yet is content-identical to f2fcb30; `engine\_stubs.py` is dated 2026-05-19
  and also identical to f2fcb30.
- An earlier statement (W71, [I]) that May-dated files are "untouched author
  originals" is WITHDRAWN.
- REQUIRED: obtain the upstream author repository at the cloned revision and
  diff the tree against f2fcb30 to produce the author-vs-Graystone divergence
  list. GAP-019.
- Agent provenance: `native_openhands` chosen and modified by Graystone;
  upstream agent installation never run [S].

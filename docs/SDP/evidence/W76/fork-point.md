# Fork point probe - W76 2026-09-22

## prior archive mentions
ARCHIVE-W73-2026-09-21.md:28: merge-base --is-ancestor af21bc18 origin/main = 0. CM-01 PROVENANCE CLOSED.
ARCHIVE-W73-2026-09-21.md:121: count lines, sort ascending; (4) verify top 3 with --no-renames + merge-base --is-ancestor;

## fork point by shared history
upstream shallow: false
repo commits: 93  repo HEAD: 6a555c6 2026-09-22 10:46:37 -0400 W75: R1.1 closed - RTM v0.3 ratified (28 core measured), Phase 2 deferrals, R1.2a added, handoff BRIEF+ARCHIVE
upstream HEAD: ef005703 2026-09-21 15:38:27 -0400 security(server): require auth for /openapi.json, /docs and /redoc (#1014)
FORK POINT: 88a71af 2026-09-21 19:33:50 -0400 cdgray33-git | W72 handoff: author baseline read, runtime measured, roadmap v0.1
repo commits since fork: 4
upstream commits since fork: 1154

## CORRECTION (W76 exchange 14): object-store test invalid; branch-history measures below
upstream alternates file: False
  upstream remote: origin	https://github.com/open-jarvis/OpenJarvis.git (fetch)
  upstream remote: origin	https://github.com/open-jarvis/OpenJarvis.git (push)
88a71af ancestor of upstream HEAD: exit 1 (0 = yes, 1 = no)
upstream refs containing 88a71af: none
repo first commit: f2fcb30|079c92f04b8aad7696d4ba2e3d0a04d1f7548b77|2026-05-30 18:37:22 -0400|Graystone Lab: remote MCP/Ollama integration, Rust extension, UI fixes
upstream commit with identical tree: none (not a verbatim import of any upstream commit)

## ARCHIVE-W73 CM-01 record (extracted verbatim)
- E2 [M] single root f2fcb30c6c784fe48650facb335f18228b2ee984, 2026-05-30, 2000 files.
- E3 [M] upstream HEAD ef005703 2026-09-21 (#1014). Clone 2151 files.
- E4 [M] BASE PINNED: upstream af21bc18 (2026-05-19, main, ~v1.0.1+1d). 127 files differ
  (strict, --no-renames). Neighbours: fea8d3e8 v1.0.1 = 129, 4a781750 = 136; 05-20+ = 187+.
>>   merge-base --is-ancestor af21bc18 origin/main = 0. CM-01 PROVENANCE CLOSED.
- E5 [M] root vs base: M 42, A 72, D 13. HEAD(88a71af) vs base: M 95, A 484, D 12.
  Full list: PROVENANCE-W73-af21bc18.txt (repo root, untracked).
- E6 [M] 12 files deleted from author code at HEAD: src/openjarvis/traces/analyzer.py,
  traces/collector.py, tests/traces/* (7), desktop/src-tauri/binaries/ollama-aarch64-apple-darwin,
  frontend/tsconfig.tsbuildinfo, "Inline". One more was deleted at root and later restored.
- E7 WITHDRAWN - see N6.
- E14 [M] R0.4 WSL2: distro Ubuntu (v2), user administrator. ~/.openjarvis EXISTS - author-shape
  runtime dir: agents.db(+wal 115 KB), traces.db(+wal 49 KB), digest.db, knowledge.db, telemetry.db,
--
- [x] R0.3 Measure runtime platform + agent state. Evidence: W72 exchange 11 output.
- [ ] R0.4 Measure the WSL2 Ubuntu distro read-only: does it hold an author install
      (~/.openjarvis, repo, venv)? Gray reports he built Jarvis in WSL2.
- [ ] R0.5 Obtain the upstream author repo at a pinned revision; diff our tree against it.
>>       Only this closes provenance (CM-01) and shows exactly what Graystone changed.

## C. TRACK 1 - REQUIREMENTS AND THE PROGRESS MEASURE
- [ ] R1.1 Recover Gray's initial requirements list into an RTM (one row per requirement).
- [ ] R1.2 Map each requirement to the author mechanism that serves it (managed agent,
      operator, digest, channel, connector, MCP) or mark GAP.
- [ ] R1.3 Adopt the author's Agent QA Runbook (37 scenarios) as the verification set;
      record a baseline pass count. That count is the first honest progress number.

--

## AUTHOR COMMITS SINCE BASE (W76 close block)
af21bc18..HEAD (upstream main): 495
The exchange-13 figure 1154 is INVALID: it counted upstream history not reachable from 88a71af, i.e. all of it.

#!/usr/bin/env python3
"""
openjarvis-cloudbundle-v1

Read-only. Packs whole source files plus a written brief into a single
markdown file suitable for pasting into a large-context cloud model
(nemotron-3-ultra-550b, or the 120b for comparison).

Writes nothing except its own output file. Does not import openjarvis.
Stdlib only. Safe to run against a live tree.

Usage, from the repo root:

    python bundle_for_cloud.py --set speech
    python bundle_for_cloud.py --set prompt
    python bundle_for_cloud.py --files path/one.py path/two.tsx --brief "question"

Output lands in the repo root as CLOUDBUNDLE-<set>-<timestamp>.md
The script prints the full path and byte size when it finishes.
"""

import argparse
import datetime
import hashlib
import os
import sys

MARKER = "openjarvis-cloudbundle-v1"

# ---------------------------------------------------------------------------
# Target sets. Paths are repo-root relative, forward slashes.
# A missing file is REPORTED, never silently skipped.
# ---------------------------------------------------------------------------

SETS = {
    "speech": {
        "title": "speech_router.py duplicate definitions",
        "files": [
            "src/openjarvis/server/speech_router.py",
            "src/openjarvis/server/app.py",
            "src/openjarvis/server/api_routes.py",
        ],
        "brief": """
BACKGROUND

This is OpenJarvis, a self-hosted assistant. The speech surface is
FastAPI. An observation recorded on 2026-08-05, NOT re-verified since,
claimed that `speech_router.py` contains THREE definitions each of
`_get_whisper`, `speech_stream_ws`, and `_transcribe_and_send`, plus a
duplicated tts_ok / tts_backend health block. The route decorators were
said to differ between copies: one registered
`@speech_router.websocket("/v1/speech/stream")` and two registered
`@speech_router.websocket("/stream")`, on a router that already carries
a `/v1/speech` prefix.

The consequence, if true, is that Python module globals resolve to the
LAST definition while FastAPI route matching takes the FIRST
registration. The running STT path would then be a mix of copies, and
any prior debugging that read one copy while the process executed
another would have produced misleading results. Several months of
isolated patches may trace back to this.

TREAT THE LINE NUMBERS ABOVE AS STALE. The file has been edited since.
Derive everything from the source in this bundle.

WHAT I NEED FROM YOU

1. Enumerate EVERY duplicated top-level definition in speech_router.py:
   function name, and the exact current line number of each occurrence.
   Include decorators, module-level constants, and any repeated block,
   not only the three names above.

2. For each duplicated function, compare the copies against each other.
   Are they byte-identical, or do they diverge? If they diverge, state
   exactly what differs. This decides whether removal is safe or whether
   behaviour would change.

3. For each duplicated ROUTE, state the fully-resolved path including the
   router prefix, and state which registration FastAPI will match first.
   Flag any path that ends up registered twice, and any path that is
   registered under two different fully-resolved URLs.

4. State, for each duplicated symbol, which definition Python module
   globals actually resolve to at import time, and therefore which copy
   executes when the symbol is called internally rather than routed to.

5. Identify any case where 3 and 4 disagree - where the routed copy and
   the internally-called copy are different objects. That is the defect
   shape I most need named.

6. Search app.py and api_routes.py for anything that registers a speech
   path or a `/v1/speech/health` route a second time, and say which
   registration wins.

7. Recommend which copy of each duplicate to KEEP, with your reasoning,
   and give me the EXACT line ranges to delete.

OUTPUT RULES

- Cite every claim as `path:line`.
- When you propose a deletion or an edit, QUOTE THE ANCHOR LINES
  VERBATIM, including leading whitespace. I patch by exact-string anchor
  and a paraphrased anchor is useless to me.
- If the 08/05 claim of triplication is WRONG, say so plainly and show
  what is actually there. A negative result is a useful result here.
- Do not write a patch script. Give me findings and anchors.
""",
    },
    "prompt": {
        "title": "doubled-prompt defect",
        "files": [
            "frontend/src/components/Chat/ChatArea.tsx",
            "frontend/src/components/Chat/InputArea.tsx",
            "frontend/src/lib/store.ts",
        ],
        "brief": """
BACKGROUND

This is the React frontend of OpenJarvis, a self-hosted assistant.

DEFECT: a user prompt is sometimes submitted twice, and the two copies
are CONCATENATED WITH NO SEPARATOR into the stored conversation history.
An observed example from a captured request body:

    "Describe the water cycle in three sentencesDescribe the water cycle in three sentences"

This matters more than a display bug. The full conversation history is
resent to the model on every turn, so the corruption compounds: every
subsequent turn carries the doubled text in its prefill.

UNCHASED LEAD, recorded 2026-08-05, never verified: ChatArea.tsx
registers a listener for a `jarvis-option-select` event and re-dispatches
the text as `jarvis-submit-text`. If InputArea also handles the original
event, or if the relay double-fires, the string would be submitted twice.
Line numbers from that note are stale - derive from the source here.

WHAT I NEED FROM YOU

1. Trace EVERY path by which text reaches the conversation store. Include
   direct form submission, keyboard handlers, custom DOM events, and any
   relay between components. Give me the call chain with `path:line` at
   each hop.

2. Find the double-dispatch. Specifically check whether one user action
   can result in two submissions, and whether a custom event is both
   handled locally AND re-dispatched to a second handler that also
   submits.

3. Check every `addEventListener` in these files for a matching
   `removeEventListener` in the same effect's cleanup, and check the
   effect dependency arrays. A listener re-registered on each render
   without cleanup accumulates and fires N times - that would produce
   this symptom and would also explain why it is intermittent.

4. Determine WHERE the concatenation physically happens: at submit time
   (two calls appending to the same field), or at store-write time (an
   update function that appends rather than replaces). Name the function
   and line.

5. Check whether the store's message-update path can append to an
   existing message when it should create a new one, or vice versa.

6. Tell me the minimal correct fix, and whether it belongs in the
   component or in the store.

OUTPUT RULES

- Cite every claim as `path:line`.
- When you propose an edit, QUOTE THE ANCHOR LINES VERBATIM, including
  leading whitespace and the surrounding lines needed to make the anchor
  unique in the file. I patch by exact-string anchor.
- These files may contain mojibake from an earlier encoding accident.
  Ignore it, do not try to fix it, and do not let it change your line
  numbering.
- If you cannot find a double-submission path, say so plainly rather than
  proposing the most plausible-looking candidate. A confident wrong
  answer costs me more than no answer.
- Do not write a patch script. Give me findings and anchors.
""",
    },
}

FENCE_LANG = {
    ".py": "python",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".js": "javascript",
    ".jsx": "jsx",
    ".toml": "toml",
    ".json": "json",
    ".ps1": "powershell",
    ".md": "markdown",
}


def read_bytes(path):
    with open(path, "rb") as fh:
        return fh.read()


def find_candidates(root, basename):
    """Basename search used only to REPORT alternatives for a missing file."""
    hits = []
    skip = {".git", "node_modules", ".venv", "venv", "target", "__pycache__",
            "dist", "build", ".fix_backups_"}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip]
        if basename in filenames:
            rel = os.path.relpath(os.path.join(dirpath, basename), root)
            hits.append(rel.replace("\\", "/"))
        if len(hits) >= 10:
            break
    return hits


def render_file(root, rel, out):
    full = os.path.join(root, rel.replace("/", os.sep))
    out.append("")
    out.append("---")
    out.append("")
    out.append("## FILE: `%s`" % rel)
    out.append("")

    if not os.path.isfile(full):
        out.append("**NOT FOUND ON DISK.**")
        cands = find_candidates(root, os.path.basename(rel))
        if cands:
            out.append("")
            out.append("Files with this basename elsewhere in the tree:")
            out.append("")
            for c in cands:
                out.append("- `%s`" % c)
        else:
            out.append("")
            out.append("No file with this basename found anywhere in the tree.")
        out.append("")
        out.append("Do not guess at this file's contents. Note its absence in "
                   "your answer and work from what is present.")
        return {"path": rel, "found": False, "bytes": 0, "lines": 0, "sha": ""}

    raw = read_bytes(full)
    sha = hashlib.sha256(raw).hexdigest().upper()
    text = raw.decode("utf-8", errors="replace")
    lines = text.splitlines()

    crlf = raw.count(b"\r\n")
    total_lf = raw.count(b"\n")
    bare_lf = total_lf - crlf
    terminator = "CRLF" if crlf and not bare_lf else ("LF" if bare_lf and not crlf else "MIXED")

    out.append("- bytes: %d" % len(raw))
    out.append("- lines: %d" % len(lines))
    out.append("- sha256: `%s`" % sha)
    out.append("- line terminator: %s" % terminator)
    out.append("")
    out.append("Line numbers below are 1-based and authoritative. Cite them.")
    out.append("")

    ext = os.path.splitext(rel)[1].lower()
    lang = FENCE_LANG.get(ext, "text")
    width = len(str(len(lines)))

    out.append("```" + lang)
    for i, line in enumerate(lines, 1):
        out.append("%s | %s" % (str(i).rjust(width), line))
    out.append("```")

    return {"path": rel, "found": True, "bytes": len(raw),
            "lines": len(lines), "sha": sha}


def main():
    ap = argparse.ArgumentParser(description="Bundle whole files for a cloud model. Read-only.")
    ap.add_argument("--set", dest="setname", choices=sorted(SETS.keys()),
                    help="named target set")
    ap.add_argument("--files", nargs="+", help="explicit repo-relative file list")
    ap.add_argument("--brief", default="", help="question text when using --files")
    ap.add_argument("--root", default=".", help="repo root (default: current directory)")
    ap.add_argument("--out", default="", help="output path (default: auto in repo root)")
    args = ap.parse_args()

    if not args.setname and not args.files:
        ap.error("give either --set or --files")

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print("ERROR: root is not a directory: %s" % root)
        return 2

    # Sanity: warn loudly if this does not look like the repo root.
    if not os.path.isfile(os.path.join(root, "pyproject.toml")):
        print("WARNING: no pyproject.toml in %s" % root)
        print("WARNING: this may not be the repo root. Paths are resolved "
              "relative to it.")
        print("")

    if args.setname:
        spec = SETS[args.setname]
        title = spec["title"]
        files = spec["files"]
        brief = spec["brief"].strip()
        label = args.setname
    else:
        title = "ad hoc bundle"
        files = [f.replace("\\", "/") for f in args.files]
        brief = args.brief.strip() or "(no brief supplied)"
        label = "adhoc"

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    outpath = args.out or os.path.join(root, "CLOUDBUNDLE-%s-%s.md" % (label, stamp))
    outpath = os.path.abspath(outpath)

    out = []
    out.append("# OPENJARVIS CODE REVIEW BUNDLE")
    out.append("")
    out.append("- marker: `%s`" % MARKER)
    out.append("- set: `%s` - %s" % (label, title))
    out.append("- generated: %s" % datetime.datetime.now().isoformat(timespec="seconds"))
    out.append("- repo root: `%s`" % root)
    out.append("- files in bundle: %d" % len(files))
    out.append("")
    out.append("You are reviewing complete source files. Every file is "
               "included in full, with authoritative 1-based line numbers in "
               "the left gutter. Nothing has been elided.")
    out.append("")
    out.append("---")
    out.append("")
    out.append("# THE QUESTION")
    out.append("")
    out.append(brief)
    out.append("")
    out.append("---")
    out.append("")
    out.append("# SOURCE")

    records = []
    for rel in files:
        records.append(render_file(root, rel, out))

    out.append("")
    out.append("---")
    out.append("")
    out.append("# MANIFEST")
    out.append("")
    out.append("| file | found | bytes | lines | sha256 |")
    out.append("|---|---|---|---|---|")
    for r in records:
        out.append("| `%s` | %s | %d | %d | `%s` |" % (
            r["path"], "yes" if r["found"] else "NO",
            r["bytes"], r["lines"], r["sha"][:16] + "..." if r["sha"] else ""))
    out.append("")
    out.append("These hashes pin the exact bytes you reviewed. If a later "
               "patch is built against different bytes, the mismatch is "
               "detectable.")
    out.append("")

    body = "\n".join(out) + "\n"
    with open(outpath, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)

    size = os.path.getsize(outpath)
    missing = [r["path"] for r in records if not r["found"]]

    print("")
    print("BUNDLE WRITTEN")
    print("  path   : %s" % outpath)
    print("  bytes  : %d" % size)
    print("  approx tokens: %d" % (size // 4))
    print("  files  : %d of %d found" % (len(records) - len(missing), len(records)))
    if missing:
        print("")
        print("  MISSING (reported inside the bundle, not silently dropped):")
        for m in missing:
            print("    - %s" % m)
        print("  Candidate paths are listed in the bundle. Re-run with")
        print("  --files if you want to substitute a corrected path.")
    print("")
    print("Nothing else was written. This script does not modify the tree.")
    print("")
    return 0


if __name__ == "__main__":
    sys.exit(main())

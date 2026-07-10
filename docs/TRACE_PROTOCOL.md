# Trace-Before-Acting Protocol

Diagnostic discipline for OpenJarvis coding agents (and humans). Born from a
three-day debugging session where every dead end came from acting on an
assumption, and every breakthrough came from reading ground truth.

## Core rule
If you cannot point to the line, file, or live value that proves your next
action is correct, you are guessing. Go find it first.

## The protocol

1. **State the claim.** Write the specific assumption your next action depends
   on. Examples: "creds load from .env", "the exe runs the latest bundle",
   "this render stringifies the object before passing it to React".

2. **Find ground truth.** Locate where that behavior is actually defined:
   - grep/read the source for static behavior
   - query live runtime state for "what is actually running" (loaded assets,
     on-disk artifacts, actual loaded config, running processes)
   Prefer runtime evidence over source when the question is what is executing
   right now, not what the code says should execute.

3. **Confirm or kill the claim** with evidence before proceeding. If the
   evidence contradicts the assumption, STOP and re-plan. Do not patch around
   a contradiction.

4. **Verify the fix reached the running thing.** After any change, prove the
   artifact that actually executes contains it â€” grep the built bundle, check
   the loaded module, re-read live state. A changed source file is NOT proof
   the running app changed.

5. **When the same fix fails twice, the diagnosis is wrong â€” not the fix.**
   Stop repeating. Re-trace from step 1 with a new claim. Three identical
   failures means you are fixing the wrong thing, or the fix is not loading.

6. **Guard every edit.** Each scripted edit gets a pre-check (anchor exists
   exactly once) and a post-check (edit landed). A silent miss must never be
   able to masquerade as success.

## Worked example (the session that produced this)
- Claim: "packaged exe crashes on React #31, dev does not, so it is a
  minification bug." â€” WRONG, never verified.
- Ground truth that broke it open: queried the LIVE exe for
  \document.scripts\ and found it loading \index-yEIdlxLI.js\ â€” a bundle
  hash that no longer existed on disk. The service worker was serving a
  precached stale bundle, intercepting every rebuild.
- Lesson: "same crash after a rebuild" means verify what the app actually
  LOADED before touching code again. That one live check should have been
  step one, not step twenty.
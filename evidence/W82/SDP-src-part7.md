# SDP SOURCE EXTRACT W82 part 7 (deduplicated by section hash)
### [ARCHIVE-W63-2026-09-17.md] W63 FINDINGS, EXCHANGE 1-3 (9222 ruling; F-W62-2c mechanism)
- 9222 SOURCE = frontend\src-tauri\tauri.conf.json:25 additionalBrowserArgs,
  wired deliberately (recorded 08/05 as "the CDP method"). Every launch of the
  production exe opened CDP on 127.0.0.1:9222. W62 pid 28496 was this flag.
- NEGATIVE: NOT the env var (Process/User/Machine all unset). NOT WebView2
  policy registry (HKCU and HKLM AdditionalBrowserArguments absent). At ex3
  measurement: 0 listeners on 9222, /json/version no response (app closed).
- RULING (ex3): remove --remote-debugging-port=9222 from config. Probes get a
  per-process port via WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS on a free port.
  HAZARD: env value may REPLACE config args; the probe launch must also carry
  --autoplay-policy=no-user-gesture-required --use-fake-ui-for-media-stream.
- LOSES 9222: cdp_getbase.ps1 (root), get-devtools-url.ps1 (root, per 08/05).
- --use-fake-ui-for-media-stream auto-grants getUserMedia with no prompt;
  bears on F-W62-4 mic.
- api.ts uploaded = frontend\src\lib\api.ts (1007 lines). synthesizeSpeech
  :256, synthesizeSpeechChunks :308, mojibake at :4 and :19. Imported by
  ttsPlayer.ts:30, ChatArea.tsx:10, useSpeech.ts:2 and 20 other sites.
- F-W62-2c MECHANISM (ttsPlayer.ts read whole), two routes to a stranded
  queue: (a) a hung synth fetch (no timeout, F-W62-2d) holds pumping=true
  forever; (b) stopAll mid-fetch, new turn enqueues, pump() returns at
  "if (pumping)", old pump exits on generation mismatch, finally clears
  pumping, nothing re-kicks: new units sit in pending unplayed. ChatArea calls
  stopAll the moment a new empty assistant message appears.
- ttsPlayer only schedules after a successful fetch, and primes the context
  only on first pointerdown/keydown. Candidate for F-W62-2b; UNMEASURED.
- ARCHIVES: root holds W60/W61/W62. Downloads holds three W61 variants
  (1735, 8943, 16798 bytes); the 16798 copy matches root.
### [ARCHIVE-W63-2026-09-17.md] W63 MEASUREMENTS, EXCHANGE 4-5
- ex4 RUNTIME: rebuilt target\release exe launched with config flags only
  (autoplay, fake-ui); 0 listening ports in app tree; 9222 closed.
- ex4 NEGATIVE: WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS set per process (all
  three flags, port 9333) did NOT reach the webview command line while config
  additionalBrowserArgs is set. No 9333 listener, no page target. The env-var
  CDP method in cdp_getbase.ps1 does not work on this build. Probe NOT run.
  A probe port needs an opt-in in src-tauri\src\lib.rs (next).
- ex4 STALE INSTALLED COPY: Start Menu and Desktop OpenJarvis.lnk both launch
  %LOCALAPPDATA%\OpenJarvis\openjarvis-desktop.exe dated 07/06/2026 (carried
  9222). start-openjarvis.ps1 launches only the backend (:57). A desktop test
  started from a shortcut ran a 07/06 frontend, before ttsPlayer.ts (08/05).
  Which exe W62 tested is NOT recorded - UNMEASURED.
- ex5 ACTION: silent reinstall from current NSIS bundle. Old install backed up
  to C:\Users\Admin\AppData\Local\OpenJarvis.bak_w63_20260918_152540. Results: exit=0 hashMatch=False installed9222str=0
  control=1 launchFlags=[--autoplay-policy=no-user-gesture-required --use-fake-ui-for-media-stream] appTreeListeners=0 9222listeners=0.
### [ARCHIVE-W63-2026-09-17.md] W63 NEGATIVE RESULTS (what it was NOT, and how that was established)
- 9222 was NOT an environment variable: read at Process, User and Machine
  scope, all unset. NOT WebView2 policy: HKCU and HKLM
  ...\Edge\WebView2\AdditionalBrowserArguments both absent. It WAS config.
- The per-process env var does NOT override or add to config browser args on
  this build: launch B passed three flags plus port 9333 and the webview
  command line was byte-identical to launch A. Positive control: the two
  config flags appeared on both launches, so the read itself works.
- The rebuilt and installed exes do NOT expose a debug port: 0 app-tree
  listeners, 0 listeners on 9222, no remote-debugging flag, with the
  fake-ui string as the positive control on every exe scanned.
- Installed-vs-built hash mismatch is NOT evidence of a bad install: Tauri
  patches the release exe with NSIS bundle-type information after the bundle
  copy is made. Explained, NOT independently proven - if it ever matters,
  compare the installer payload rather than the patched exe.
### [ARCHIVE-W63-2026-09-17.md] W63 SDD/SDP FEED
- SURFACE CLOSED: the desktop renderer had a CDP control port on
  127.0.0.1:9222 open on every launch from 07/07 to 09/17, from
  tauri.conf.json additionalBrowserArgs. Any local process could drive the
  page, including anything the confirmation gate renders. Plain language: the
  app kept a back door open for us to look inside it, and anyone else on the
  machine could walk through the same door and press buttons as if they were
  the user. The door is now closed, and reopening it must be a deliberate,
  per-run choice (item 2), never the default.
- DELIVERY TOPOLOGY, now recorded: source -> vite -> server\static ->
  embedded in exe at Rust build time -> NSIS bundle -> installed copy under
  %LOCALAPPDATA%\OpenJarvis -> what the shortcut runs. Four stages, and only
  the last one is what a human tests. The drift between stage 2 and stage 5
  hid a 10-week-old frontend behind a current-looking desktop window.
- HAZARD for the gate chapter: `--use-fake-ui-for-media-stream` auto-answers
  the browser permission prompt for the microphone. A permission prompt is a
  confirmation gate; this flag approves it without a human.
### [ARCHIVE-W63-2026-09-17.md] W63 EXECUTION PATHS DELTA
- PATH: desktop app launch. Entry = OpenJarvis.lnk (Start Menu, Desktop) ->
  %LOCALAPPDATA%\OpenJarvis\openjarvis-desktop.exe -> Tauri host ->
  msedgewebview2.exe browser process (config browser args applied here) ->
  renderer children. Human present: yes. NOT started by start-openjarvis.ps1,
  which only launches uvicorn on 8010 (line 57).
- PATH: TTS playback (frontend). ChatArea TTS effect -> enqueue() ->
  splitIntoUnits -> pump() -> synthesizeSpeech (lib\api.ts:256) -> backend ->
  decodeAudioData -> schedule() on one persistent AudioContext. Single-owner
  pump guarded by `pumping`; cancellation by `generation` bump in stopAll.
  Confirmation gate: absent. Known stall states: F-W62-2c, F-W62-2d.
### [ARCHIVE-W63-2026-09-17.md] W63 TOOLING REGISTER DELTA (tools\ is gitignored; git add -f)
- `tools\probe_webview_cdp_w62.ps1` - READ WHOLE this window, sound, STILL
  NEVER RUN. Needs a live page target on a debug port. Writes ASCII lines to
  -Out via [IO.File]::WriteAllLines, so -Out MUST be an absolute path.
  Replays Runtime.consoleAPICalled and Log.entryAdded, filters on PUMPDBG /
  [tts] / audio / mic patterns, then evaluates a page-state expression
  (url, visibility, focus, userActivation, a test AudioContext state and
  sample rate, microphone permission, enumerateDevices, MediaRecorder type).
- `cdp_getbase.ps1`, `get-devtools-url.ps1` (root) - BROKEN AS WRITTEN. Both
  assume the env-var CDP method, which does not work on this build.
- `tools\w63_build_20260917_084321.log` - full tauri build output.
- IN-CODE INSTRUMENTS ALREADY PRESENT: `[PUMPDBG]` in ttsPlayer.ts pump()
  (take/fetched/buffered/ctx/decoded/scheduled with deltas) and `[TTSDBG]` in
  the ChatArea TTS effect (run/enqueue). Both land in the WEBVIEW console
  only - unreadable without CDP or an open devtools window. That is why
  item 2 blocks item 3's verification.
### [ARCHIVE-W63-2026-09-17.md] W63 LOGGING TOPOLOGY DELTA
- No backend logger changed this window. Recorded gap: the desktop
  renderer's console has NO file sink. Every [PUMPDBG]/[TTSDBG] line ever
  emitted has gone to a console nobody was reading. Options for a future
  window: a CDP capture (item 2), or a small frontend appender that POSTs
  console lines to the backend. Not built, not decided.
- `%LOCALAPPDATA%\OpenJarvis\logs\` and `openjarvis-startup.log` (8802 B,
  last written 07/08) survive reinstall - the installer replaced the exe and
  left the folder contents in place.
### [ARCHIVE-W64-2026-09-19.md] W64 FINDINGS, EXCHANGE 1-6 (exe verified current; backend delivers; pump healthy)
Window opened on BRIEF-W63 item 1: retest voice on the new install, because
W63 established every desktop voice result before 09/17 was measured on a
07/06 exe and is therefore suspect.
STATE CONFIRMED BEFORE ANY TEST:
- Backend up, uvicorn listening on 8010, pid 8396.
- `%LOCALAPPDATA%\OpenJarvis\OpenJarvis.exe` DOES NOT EXIST. The installed
  binary is `openjarvis-desktop.exe`, dated 09/17/2026 08:46:32, 19,027,968
  bytes. Both shortcuts (Start Menu, Desktop) resolve to that path and it
  exists. So the app under test IS the 09/17 build. This window's voice
  measurements are attributable; W62's were not.
- backend.log baseline 41,581 lines. Log dir also holds backend.log.1-.5,
  agent.log, dispatch.log, engine.log, memdb_audit.log, bindassert_probe.txt.
  backend.log was at 3,988,806 bytes against a ~4,194,300 rotation size, so
  it is near roll; a future window seeing a NEGATIVE line delta should suspect
  rotation, not a missing write.
THE VOICE TURN (app pid 19832, started 15:37:21; turn at 15:41):
Backend log delta +100 lines. Seven complete TTS cycles, every one a 200:
  START 75 chars  -> TTFB ~1.5s -> DONE 1.558s, 229,420 bytes
  START 54 chars  -> TTFB 1.460s -> DONE 1.670s, 160,812 bytes
  START 78 chars  -> TTFB 2.569s -> DONE 2.928s, 252,972 bytes
  START 54 chars  -> TTFB 1.325s -> DONE 1.512s, 169,004 bytes
  START 61 chars  -> TTFB 1.395s -> DONE 1.728s, 192,556 bytes
  START 126 chars -> TTFB 2.050s -> DONE 2.840s, 391,212 bytes
  START 308 chars -> TTFB 2.950s -> DONE 4.094s, 918,572 bytes
All voice=am_adam, all `POST /v1/speech/synthesize 200` from 127.0.0.1:52743.
NO SOUND WAS HEARD.
TWO INFERENCES, both load-bearing:
1. EVERY START FOLLOWS THE PRIOR DONE. Seven sequential units, no gaps, every
   fetch resolved in 1.3-4.1 s. A pump holding `pumping` true forever cannot
   produce this. See NEGATIVE RESULTS.
2. THE UNIT SIZES IDENTIFY THE CODE PATH. 75/54/78/54/61/126/308 chars, first
   under 90, all under 350, clause-sized. That is `ttsPlayer.splitIntoUnits`
   with FIRST_UNIT_MAX_CHARS=90 then UNIT_MAX_CHARS=350, breaking on `,;:` as
   well as `.!?`. The superseded `splitIntoTTSChunks` greedy-packs to 350 on
   sentence ends only and would emit far fewer, larger chunks. THEREFORE
   ttsPlayer.ts IS LIVE AND RUNNING on the 09/17 build. This was inferred from
   log evidence, not read from ChatArea.tsx, which was never opened this
   window.
### [ARCHIVE-W64-2026-09-19.md] W64 NEGATIVE RESULTS (what it was NOT, and how that was established)
FOUR THEORIES KILLED BY MEASUREMENT THIS WINDOW. Record these; all four are
cheap to re-propose and expensive to re-test.
1. F-W62-2c STRANDED PUMP - NOT WHAT SILENCED THIS TURN. Seven sequential
   units, each START after the prior DONE, every fetch resolved 1.3-4.1 s. A
   hung fetch holding `pumping` true, or a pump that returned at
   `if (pumping)` with nothing re-kicking it, cannot produce seven consecutive
   completed units. The code smell is REAL and unpatched; it is not this bug.
2. F-W62-2d NO SYNTH TIMEOUT - DID NOT FIRE. Longest fetch 4.094 s. Nothing
   approached a timeout. Same status: real gap, not this bug.
3. SUSPENDED AUDIOCONTEXT - DEAD. An audio session existed at state=1 ACTIVE
   with the process chain walking back to openjarvis-desktop.exe. A suspended
   context does not hold an active session.
4. SPEECH PATH ON THE KEEPALIVE GAIN - DEAD, by whole-file read of
   ttsPlayer.ts. `schedule()` does `src.connect(masterGain)`; masterGain is
   `gain.value = 1` connected to `ctx.destination`. The keepalive has its OWN
   separate gain node at KEEPALIVE_GAIN = 0.0 connected separately to
   destination. The two paths never meet. There is no gain-zero speech path.
5. DEVICE ROUTING TO THE USB MIC - NOT AS STATED. See THE ENDPOINT FINDING.
   The failing session was on Elgato Headphones, not the USB render endpoint.
ALSO ESTABLISHED NEGATIVE: the backend is NOT implicated in the silence at
all. Seven 200s with 160k-918k byte payloads. Kokoro, speech_router and the
proxy path all delivered. Any future window theorizing backend audio loss for
this defect is re-deriving a dead branch.
### [ARCHIVE-W64-2026-09-19.md] W64 SDD/SDP FEED
ARCHITECTURE - AUDIO OUTPUT PATH, END TO END, WITH THE GATE DETAIL:
  ChatArea TTS effect
    -> ttsPlayer.enqueue(text)            [frontend\src\audio\ttsPlayer.ts]
    -> breakText: split on .!? then on ,;:
    -> splitIntoUnits: greedy pack, cap 90 for unit 1 then 350
    -> pump(): single-owner loop guarded by module-level `pumping`
    -> synthesizeSpeech(unit)             [frontend\src\lib\api.ts:256]
    -> HTTP POST 127.0.0.1:8010 /v1/speech/synthesize
       body {text, voice_id, speed, output_format:'wav'}, response WAV blob
    -> speech_router proxy -> Kokoro 172.16.33.201:8880 /synthesize
    -> blob.arrayBuffer() -> ctx.decodeAudioData()
    -> schedule(): createBufferSource -> connect(masterGain) -> destination
       start(nextStartTime), nextStartTime += buffer.duration,
       SCHEDULE_LEAD_SECONDS = 0.08 floor against scheduling into the past
    -> WASAPI session on ONE render endpoint, chosen by the webview AT
       CONTEXT CREATION and fixed for that context's life
PORTS/PROTOCOLS/ENCODING AT EACH GATE: frontend to backend, TCP 8010, HTTP/1.1,
JSON request, audio/wav response body. Backend to Kokoro, TCP 8880, HTTP/1.1,
JSON request, WAV response. Kokoro WAV is 24 kHz 16-bit mono. Browser to OS,
WASAPI shared mode, float samples on the context's own sample rate.
CONFIRMATION GATE: ABSENT on this entire path. No human confirmation exists
for speech playback and none is wanted; recorded so the SDP's gate inventory
can state it explicitly rather than leave it unmentioned.
PLAIN-LANGUAGE EXPLANATION (the eight-year-old version, for the SDP guard
chapter's neighbouring audio section): The computer has several places sound
can come out - headphones, a monitor's speakers, a USB gadget. When the app
opens its sound channel it picks ONE of those places and then keeps using it
until the app is closed and opened again. If it picks a place where nobody is
listening, everything still works perfectly: the words are made, the sound is
sent, the computer's meters say sound is playing. It is just playing into a
room with nobody in it. That is why the app looked completely healthy while
being completely silent, and why closing and reopening it fixed the problem -
reopening made it pick the place again.
HAZARD FOR THE SDD: an active WASAPI session and a healthy volume reading
prove NOTHING about audibility. Only a peak meter distinguishes "rendering
audio" from "rendering silence", and only a human distinguishes "reaching the
endpoint" from "audible". Any future audio verification must state which of
the three it measured.
### [ARCHIVE-W64-2026-09-19.md] W64 EXECUTION PATHS DELTA
- PATH: TTS playback (frontend) - AMENDED. Add to the W63 entry: the path
  terminates in a WASAPI render session whose ENDPOINT IS SELECTED AT
  AudioContext CREATION and is immutable for that context. Endpoint selection
  is therefore a property of app launch, not of the turn. Any voice test must
  record which render endpoint the webview session is on, not merely that a
  session exists. Confirmation gate: absent (by design).
- PATH: desktop app launch - AMENDED. Add: the webview's render endpoint
  binding is established here, and changes to the machine's audio device set
  (plugging or unplugging USB audio) do not rebind a RUNNING context. Only a
  relaunch rebinds.
### [ARCHIVE-W64-2026-09-19.md] W64 TOOLING REGISTER DELTA (tools\ is gitignored; git add -f)
- `tools\probe_audio_peak_w64.ps1` - NEW, BUILT AND VALIDATED THIS WINDOW.
  VALIDATED 09/19 with a positive control: returned 0.938690 on real audio,
  0.000000 on a silent endpoint, in the same run. TRUSTED.
  Params: -Out (MANDATORY, must be ABSOLUTE - it writes via
  [IO.File]::WriteAllLines), -Seconds (default 60), -IntervalMs (default 200).
  Enumerates ACTIVE RENDER endpoints via IMMDeviceEnumerator, reads
  IAudioMeterInformation (GUID C02216F6-8C67-4B5B-9D00-D008E73E0064) per
  device AND per session, samples on a wall-clock deadline, reports MAX peak
  per endpoint and per session with pid, process name and friendly device
  name. C# namespace W64M, so it does not collide with probe_audio_w62's W62C.
  peak=-1 means the meter was unreadable, peak=-2 means the call threw.
  Its verdict block states only what it measured: peaks, not audibility.
  MUST BE RUN AS: powershell.exe -ExecutionPolicy Bypass -NoProfile -File
  <absolute path> -Out <absolute path> -Seconds 60
- `tools\probe_audio_w62.ps1` - USED AND SOUND. Enumerates endpoints and
  sessions with pid, state, volume, mute, process chain, plus mic consent
  registry. Does NOT measure peak - it cannot distinguish silence from audio.
  That limitation is exactly what cost exchange 10 a wrong inference.
- `tools\w64_audio\` - NEW DIRECTORY. sample_01..12.txt (session sampling,
  09/18), peak_run1.txt (unmeasured), peak_control.txt (the validated
  positive control). All need `git add -f`.
- `tools\probe_webview_cdp_w62.ps1` - STILL NEVER RUN. Unchanged from W63.
- IN-CODE `[PUMPDBG]` / `[TTSDBG]` - STILL UNREADABLE. This window routed
  around them rather than unblocking CDP, by measuring from the Windows side
  instead. That worked and cost far less than item 2 would have.
### [ARCHIVE-W64-2026-09-19.md] W64 LOGGING TOPOLOGY DELTA
- No backend logger changed this window. `openjarvis.server.speech_router`
  confirmed emitting at WARNING (TTS START / TTS TTFB / TTS DONE) into
  `%LOCALAPPDATA%\OpenJarvis\logs\backend.log`, readable with Select-String.
  That logger is the single most useful voice instrument we have and it is
  already in place - a future window should reach for it BEFORE building
  anything.
- backend.log was at 3,988,806 bytes against a ~4,194,300 rotation size on
  09/18. Rotation is imminent or has happened; a negative line-count delta
  means rotation, not a missing write.
- The renderer console still has NO file sink. Unchanged from W63.
### [ARCHIVE-W64-2026-09-19.md] W64 PROGRAM GOAL
Requirement One (voice) moved from DOWN to AUDIBLE this window, and the move
is backed by a measurement (peak 0.938690 on a validated instrument), not by
a report alone. That is the first positive movement on Requirement One since
the desktop path went dark.
What is still not done: voice is audible but NOT conversational - Defect A
means playback begins only after the full reply renders, so the assistant
still cannot hold a spoken exchange at human pace. And the mechanism behind
the silence is not proven, so the fix is not reproducible; a future machine
change could put it back and we would start over.
Requirements measurement: STILL UNBUILT. Approaching one year, still under 50
percent of the initial requirements, and still no instrument that says how far
from a functional executive assistant we are. Every window continues to be
able to say what it debugged and not what it moved.
### [ARCHIVE-W64-2026-09-19.md] W64 HANDOFF MEASUREMENT
Scaffold was NOT built in exchange 1 this window - Claude's miss, acknowledged
in exchange 9. Built at close instead, by extraction from ARCHIVE-W63 for the
carried registers and fresh authoring only for new material. Sixteen exchanges
to close, flag raised at 15 with no live trace cut.
Cost note for the next window: the single highest-value exchange was the
backend.log delta plus TTS line dump (exchange 4), which killed two theories
at once. The whole-file ttsPlayer.ts upload killed a third. Measuring from the
Windows side instead of unblocking CDP saved what would have been a rebuild,
a reinstall and a probe run.
### [ARCHIVE-W64-2026-09-19.md] CARRIED RULES OF ENGAGEMENT (verbatim from ARCHIVE-W63)
Full text ARCHIVE-W57 section 6; W61 additions in ARCHIVE-W62 carried brief.
GRAY UPLOADS WHOLE FILES; CLAUDE DOES NOT ISSUE READS. ONE RUNNABLE BLOCK PER
MESSAGE. State shell and host first; run from `PS C:\Users\Admin\OpenJarvis>`;
Ubuntu ollama host 172.16.33.200. No non-ASCII. .NET static methods need
ABSOLUTE paths. ALWAYS VERIFY. FINISH THE THING. PATCH WHAT WE FIND.
VALIDATE, DO NOT INTERROGATE. Tests NON-INTERACTIVE. Author's resources
FIRST. PRODUCTION BUILD ONLY. Push to BOTH remotes (`origin` = GitHub,
`gitlab` = lab). New `tools\` files need `git add -f`. Flag at 15 exchanges;
never cut a live trace. TOKEN CONSERVATION. DO NOT RE-DERIVE PRIOR WORK
WITHOUT ASKING. BUILD THE HANDOFF SCAFFOLD IN EXCHANGE 1 (extract, do not
retype). 550B PATTERN: bundle whole files with the prompt embedded plus a
script that posts to openrouter nemotron-3-ultra-550b. SDP, execution paths,
tooling register, logging topology: ARCHIVE-W62 delta sections; every window
feeds them, negative results included.
W62 lessons: **A LOCKED FILE RETURNS A DEFAULT, NOT A RESULT. A POSITIVE
CONTROL TURNS "NOTHING SEEN" INTO EVIDENCE. A CLICK IN A CONSOLE CAN STOP A
SERVER.**
W63 ADDITIONS (carried): A DEBUG PORT WE OPENED OURSELVES IS STILL AN OPEN
DOOR. A REBUILD IS NOT AN INSTALL. TEST THE EXE THE USER ACTUALLY LAUNCHES.
W64 ADDITIONS (new):
- **A DELIVERED .ps1 WILL NOT RUN ON THIS BOX AS DELIVERED.** Downloaded
  scripts carry mark-of-the-web and execution policy blocks them. EVERY script
  handed to Gray must ship with `Unblock-File` AND be launched as
  `powershell.exe -ExecutionPolicy Bypass -NoProfile -File <absolute path>`,
  in the SAME message as the file. Same family as the .NET resolver trap.
- **PASTING A SCRIPT BODY IS NOT RUNNING IT.** A pasted `param()` block
  prompts interactively and its defaults never reach the rest of the pasted
  text, producing a confident empty result (`duration=s`, `samples=0`).
- **AN ACTIVE AUDIO SESSION IS NOT AUDIBLE AUDIO.** A keepalive at gain zero
  holds a session ACTIVE at volume 1.00 forever. Measure peak, not state.
- **MEASURE FROM THE OS SIDE WHEN THE APP'S OWN INSTRUMENTS ARE UNREADABLE.**
  Cheaper than unblocking the instrument.
### [ARCHIVE-W65-2026-09-19.md] W65 NEGATIVE RESULTS
- THE ELGATO WAVE:3 TEST IN BRIEF-W64 ITEM 1 COULD NOT BE RUN AS WRITTEN.
  The Elgato is UNPLUGGED - both its endpoints enumerate status Unknown. The
  W64 brief assumed it was available. Established by Get-PnpDevice, one block.
- CLAUDE BUILT RUN1 WRONG AND SAYS SO. The procedure set default render to
  "Speakers (USB Audio and HID)" on the assumption it was a real device. It
  is a phantom sink. Run1 is still USEFUL - it is the reproduction of the
  fault - but it was not the test that was intended.
- CHROMIUM BIND-FOR-LIFE IS NOT PROVEN, IN EITHER DIRECTION. W64's strong
  form (binds at AudioContext creation, holds for the context's life) does
  NOT fit run1: the app was bound to SAMSUNG and SAMSUNG still read zero.
  Run2 included a relaunch, so it cannot separate rebind-on-default-change
  from bind-at-creation. UNDETERMINED. Do not assert either in the SDD.
  It does not block the fix - setSinkId makes the question moot.
- A SESSION LISTED UNDER AN ENDPOINT IS NOT PROOF OF ROUTING. Run1 showed the
  webview session filed under SAMSUNG while rendering nothing anywhere.
  Endpoint attribution in the probe output is weaker evidence than peak.
### [ARCHIVE-W65-2026-09-19.md] W65 HAZARDS
- THE PHANTOM USB SINK IS STILL CONNECTED. Anything that makes it default
  render silences OpenJarvis again with no error anywhere in the stack.
  Until setSinkId lands, this is a live single point of failure for
  Requirement One, and it is a machine-state accident, not a code state.
- state=0 (AudioSessionStateInactive) in probe output does NOT mean broken.
  Run2 read state=0 on the session that measured 0.971459. The state field
  is sampled, the peak is a max over the run. TRUST THE PEAK.
- W64's item-1 test text is now known to have rested on an unavailable
  device. Check hardware presence before trusting a carried test procedure.
### [ARCHIVE-W65-2026-09-19.md] W65 SDD/SDP FEED
ARCHITECTURE GAP, USER-FACING: OpenJarvis has no audio output device
selection. The TTS engine inherits whatever Windows calls default at
AudioContext creation. For an executive assistant expected to speak in a room
with more than one sink, this is a missing basic control, not a nicety.
FIX SHAPE: AudioContext.setSinkId(deviceId) plus
navigator.mediaDevices.enumerateDevices() to populate a chooser, the chosen
deviceId persisted in settings and re-applied in ensureContext(). WebView2 is
Chromium, so the API should be present - VERIFY AVAILABILITY BEFORE BUILDING.
PLAIN LANGUAGE (per the 09/02 rule): the app currently talks into whichever
speaker Windows hands it. If Windows hands it a speaker that is not really
there, the app keeps talking and nobody hears anything, and the app never
knows. The fix is to let the app pick its own speaker and remember the pick.
PORTS/PROTOCOL/ENCODING AT THIS GATE: browser AudioContext -> WASAPI render
endpoint, PCM float32 at context sampleRate, no network hop. The upstream
gate (frontend -> backend 8010 HTTP, audio/wav bytes) is already exonerated.
### [ARCHIVE-W65-2026-09-19.md] W65 EXECUTION PATHS DELTA
- DELTA: TTS PLAYBACK PATH, terminal segment. ttsPlayer.enqueue() ->
  splitIntoUnits -> pump() -> synthesizeSpeech (frontend\src\lib\api.ts:256)
  -> decodeAudioData -> schedule() -> masterGain (gain 1) -> ctx.destination
  -> WASAPI DEFAULT RENDER ENDPOINT. The final hop is UNCONTROLLED by
  OpenJarvis. No human present. No confirmation gate. Emits no bus traffic.
- DELTA: the caller side of this path (ChatArea TTS effect) calls enqueue
  ONCE AT TURN END. Not yet read. That is Defect A's true location.
### [ARCHIVE-W65-2026-09-19.md] W65 TOOLING REGISTER DELTA
- `tools\probe_audio_peak_w64.ps1` - USED TWICE MORE, TRUSTED AGAIN. Returned
  0.000000 on a real silent run and 0.971459 on a real audible run, same day.
  Now validated against BOTH outcomes, not only the positive control.
- `tools\w65_audio\w65_bind_run1.txt` - the SILENT reproduction (phantom sink
  default). `tools\w65_audio\w65_bind_run2.txt` - the AUDIBLE run (SAMSUNG
  default). These two files are the evidence pair for the W65 finding.
  `tools\` is gitignored: `git add -f`.
- NEW ONE-LINER, NO SCRIPT NEEDED: endpoint inventory with parent device is
  Get-PnpDevice -Class AudioEndpoint plus Get-PnpDeviceProperty
  DEVPKEY_Device_Parent. That is how the phantom sink was identified. Reach
  for it before building anything for audio routing questions.
### [ARCHIVE-W65-2026-09-19.md] W65 LOGGING TOPOLOGY DELTA
- No change. [PUMPDBG] and [TTSDBG] remain WEBVIEW-CONSOLE ONLY and unread.
  W65 again routed around CDP by measuring from the Windows side. That
  continues to be cheaper than unblocking CDP.
### [ARCHIVE-W65-2026-09-19.md] CARRIED EXECUTION PATH REGISTER (W64 + W63, verbatim)
- PATH: TTS playback (frontend) - AMENDED. Add to the W63 entry: the path
  terminates in a WASAPI render session whose ENDPOINT IS SELECTED AT
  AudioContext CREATION and is immutable for that context. Endpoint selection
  is therefore a property of app launch, not of the turn. Any voice test must
  record which render endpoint the webview session is on, not merely that a
  session exists. Confirmation gate: absent (by design).
- PATH: desktop app launch - AMENDED. Add: the webview's render endpoint
  binding is established here, and changes to the machine's audio device set
  (plugging or unplugging USB audio) do not rebind a RUNNING context. Only a
  relaunch rebinds.
- PATH: desktop app launch. Entry = OpenJarvis.lnk (Start Menu, Desktop) ->
  %LOCALAPPDATA%\OpenJarvis\openjarvis-desktop.exe -> Tauri host ->
  msedgewebview2.exe browser process (config browser args applied here) ->
  renderer children. Human present: yes. NOT started by start-openjarvis.ps1,
  which only launches uvicorn on 8010 (line 57).
- PATH: TTS playback (frontend). ChatArea TTS effect -> enqueue() ->
  splitIntoUnits -> pump() -> synthesizeSpeech (lib\api.ts:256) -> backend ->
  decodeAudioData -> schedule() on one persistent AudioContext. Single-owner
  pump guarded by `pumping`; cancellation by `generation` bump in stopAll.
  Confirmation gate: absent. Known stall states: F-W62-2c, F-W62-2d.
### [ARCHIVE-W65-2026-09-19.md] CARRIED TOOLING REGISTER (W64 + W63, verbatim)
- `tools\probe_audio_peak_w64.ps1` - NEW, BUILT AND VALIDATED THIS WINDOW.
  VALIDATED 09/19 with a positive control: returned 0.938690 on real audio,
  0.000000 on a silent endpoint, in the same run. TRUSTED.
  Params: -Out (MANDATORY, must be ABSOLUTE - it writes via
  [IO.File]::WriteAllLines), -Seconds (default 60), -IntervalMs (default 200).
  Enumerates ACTIVE RENDER endpoints via IMMDeviceEnumerator, reads
  IAudioMeterInformation (GUID C02216F6-8C67-4B5B-9D00-D008E73E0064) per
  device AND per session, samples on a wall-clock deadline, reports MAX peak
  per endpoint and per session with pid, process name and friendly device
  name. C# namespace W64M, so it does not collide with probe_audio_w62's W62C.
  peak=-1 means the meter was unreadable, peak=-2 means the call threw.
  Its verdict block states only what it measured: peaks, not audibility.
  MUST BE RUN AS: powershell.exe -ExecutionPolicy Bypass -NoProfile -File
  <absolute path> -Out <absolute path> -Seconds 60
- `tools\probe_audio_w62.ps1` - USED AND SOUND. Enumerates endpoints and
  sessions with pid, state, volume, mute, process chain, plus mic consent
  registry. Does NOT measure peak - it cannot distinguish silence from audio.
  That limitation is exactly what cost exchange 10 a wrong inference.
- `tools\w64_audio\` - NEW DIRECTORY. sample_01..12.txt (session sampling,
  09/18), peak_run1.txt (unmeasured), peak_control.txt (the validated
  positive control). All need `git add -f`.
- `tools\probe_webview_cdp_w62.ps1` - STILL NEVER RUN. Unchanged from W63.
- IN-CODE `[PUMPDBG]` / `[TTSDBG]` - STILL UNREADABLE. This window routed
  around them rather than unblocking CDP, by measuring from the Windows side
  instead. That worked and cost far less than item 2 would have.
- `tools\probe_webview_cdp_w62.ps1` - READ WHOLE this window, sound, STILL
  NEVER RUN. Needs a live page target on a debug port. Writes ASCII lines to
  -Out via [IO.File]::WriteAllLines, so -Out MUST be an absolute path.
  Replays Runtime.consoleAPICalled and Log.entryAdded, filters on PUMPDBG /
  [tts] / audio / mic patterns, then evaluates a page-state expression
  (url, visibility, focus, userActivation, a test AudioContext state and
  sample rate, microphone permission, enumerateDevices, MediaRecorder type).
- `cdp_getbase.ps1`, `get-devtools-url.ps1` (root) - BROKEN AS WRITTEN. Both
  assume the env-var CDP method, which does not work on this build.
- `tools\w63_build_20260917_084321.log` - full tauri build output.
- IN-CODE INSTRUMENTS ALREADY PRESENT: `[PUMPDBG]` in ttsPlayer.ts pump()
  (take/fetched/buffered/ctx/decoded/scheduled with deltas) and `[TTSDBG]` in
  the ChatArea TTS effect (run/enqueue). Both land in the WEBVIEW console
  only - unreadable without CDP or an open devtools window. That is why
  item 2 blocks item 3's verification.
### [ARCHIVE-W65-2026-09-19.md] CARRIED LOGGING TOPOLOGY (W64 + W63, verbatim)
- No backend logger changed this window. `openjarvis.server.speech_router`
  confirmed emitting at WARNING (TTS START / TTS TTFB / TTS DONE) into
  `%LOCALAPPDATA%\OpenJarvis\logs\backend.log`, readable with Select-String.
  That logger is the single most useful voice instrument we have and it is
  already in place - a future window should reach for it BEFORE building
  anything.
- backend.log was at 3,988,806 bytes against a ~4,194,300 rotation size on
  09/18. Rotation is imminent or has happened; a negative line-count delta
  means rotation, not a missing write.
- The renderer console still has NO file sink. Unchanged from W63.
- No backend logger changed this window. Recorded gap: the desktop
  renderer's console has NO file sink. Every [PUMPDBG]/[TTSDBG] line ever
  emitted has gone to a console nobody was reading. Options for a future
  window: a CDP capture (item 2), or a small frontend appender that POSTs
  console lines to the backend. Not built, not decided.
- `%LOCALAPPDATA%\OpenJarvis\logs\` and `openjarvis-startup.log` (8802 B,
  last written 07/08) survive reinstall - the installer replaced the exe and
  left the folder contents in place.
### [ARCHIVE-W66-2026-09-20.md] NEVER READ WHOLE. EXTRACT A NAMED SECTION.
Extract a section, PowerShell, from `PS C:\Users\Admin\OpenJarvis>`:
    $f='<path to this file>'; $s='## s3'; $e='## s4'
    (Get-Content $f) | Select-String -Pattern "^$([regex]::Escape($s))" -Context 0,400
### [ARCHIVE-W66-2026-09-20.md] INDEX
- s1  Window summary - narrative
- s2  Evidence
- s3  Negative results - what things turned out NOT to be
- s4  Hazards found
- s5  SDD / SDP feed
- s6  Execution paths - DELTA
- s7  Diagnostic tooling register - DELTA
- s8  Logging topology - DELTA
- s9  Rules of engagement - ADDITIONS
- s10 Carried registers - EXTRACTION COMMANDS (not duplicated here)
---
### [ARCHIVE-W66-2026-09-20.md] s1 WINDOW SUMMARY - NARRATIVE
W66 took BRIEF-W65 item 1 (setSinkId plus an output device setting) from
"proven cause, no remedy" to a verified, user-controlled remedy in three
patches, and closed the fault class rather than documenting it.
The window opened with a cost error worth recording: Claude asked Gray what
the subject was when BRIEF-W65 already named it as item 1, including the
first step. Gray's correction - "Doesn't the brief provide that?" - is the
same family as VALIDATE, DO NOT INTERROGATE. The brief is the instruction;
asking it back wastes budget.
Sequence:
1. CAPABILITY, MEASURED NOT ASSUMED. WebView2 runtime version read from the
   registry: 153.0.4234.32. AudioContext.setSinkId is Chromium 110+, so it is
   present. Version alone was not treated as sufficient - the real unknown was
   whether enumerateDevices would return NAMED audiooutput entries, since
   labels are blank without a microphone grant. A chooser full of blank rows
   would have been useless for distinguishing SAMSUNG from the phantom.
2. TARGET FILE IDENTIFIED BY MEASUREMENT. Two settings files exist. A grep for
   importers proved `pages\SettingsPage.tsx` is routed (`App.tsx:6`, :178) and
   `components\Desktop\SettingsPanel.tsx` has ZERO importers. The orphan was
   left untouched rather than patched twice.
3. PATCH 1 - SELECTOR PLUS ON-SCREEN PROBE, DELIBERATELY ISOLATED. New
   `lib\audioOutput.ts` plus an Audio Output section. Selection PERSISTED ONLY;
   no ttsPlayer change. Because the webview console is unreadable without a
   CDP opt-in, the capability line in the settings UI IS the instrument - the
   feature's own surface doubles as the measurement, so nothing was built
   twice. Result: `setSinkId=true | endpoints=4 | named=4 | labels unlocked`.
   The empty-label hazard did not materialise.
4. A DETOUR THAT PRODUCED A REAL LESSON. Gray reported no settings to update.
   A grep filtered on `to=|navigate|href|path=|onClick` returned only
   `Layout.tsx:47` - the "Change URL" link inside the backend-unreachable
   banner. Claude concluded Settings was reachable ONLY when the backend was
   down and treated that as a defect, and the device test was designed around
   stopping the backend to raise the banner. That conclusion was WRONG. The
   Sidebar has always had a Settings entry; it lives in a `navItems` ARRAY
   dispatched by a generic `navigate(item.path)`, which the filter excluded.
   Gray corrected it from the running app. See s3.
5. PATCH 2 - ttsPlayer WIRING. `applySavedSink(ctx)` at the single
   construction site, plus an exported `setOutputDevice(id)`. The context is
   never rebuilt to change devices, because a rebuild drops the keepalive
   source and reintroduces the swallowed-first-word defect that the persistent
   context exists to fix. A build was LOST here: the file had been created but
   never presented, so no download card existed, the copy failed, and ~200 s
   went into rebuilding the unpatched tree. A Test-Path guard plus a marker
   grep was added to every subsequent copy and immediately prevented a second
   wasted build.
6. VERIFICATION, TWO RUNS ONE VARIABLE. Phantom selected, app relaunched,
   sentence spoken: SILENCE - while the TV was the working Windows default.
   That is the patch OVERRIDING the default, not following it. SAMSUNG
   selected, relaunched, spoken: AUDIO.
7. PATCH 3 - LIVE RETARGET. SettingsPage was still calling `saveSinkId`
   directly, so a change needed an app relaunch - exactly the friction the
   test had just exposed. Switched to `setOutputDevice`, which persists AND
   retargets the live context. Verified mid-session with no relaunch: output
   followed the selection in both directions.
Voice is now AUDIBLE and DEVICE-CONTROLLED. It is still not conversational;
Defect A was deliberately untouched and its absence is a correct result.
### [ARCHIVE-W66-2026-09-20.md] s2 EVIDENCE
- WebView2 runtime: `153.0.4234.32` (HKLM EdgeUpdate Clients
  {F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}, `pv`).
- Routing proof: `App.tsx:6` import, `App.tsx:178`
  `<Route path="settings" element={<SettingsPage />} />`.
- Zero importers for `components\Desktop\SettingsPanel.tsx` across all
  `*.tsx`/`*.ts` under `frontend\src`.
- On-screen probe, first run: `setSinkId=true | endpoints=4 | named=4 |
  labels unlocked`.
- On-screen probe, fresh launch: `... | named=4 | labels LOCKED (click
  Detect)` WITH all four names rendering in the dropdown.
- Dropdown contents (screenshot 08:42): `System default`, `Default - SAMSUNG
  (HD Audio Driver for Display Audio)`, `Communications - Speakers (USB Audio
  and HID) (0573:1573)`, `SAMSUNG (HD Audio Driver for Display Audio)`,
  `Speakers (USB Audio and HID) (0573:1573)`.
- Patched-file markers, `frontend\src\audio\ttsPlayer.ts`: line 38 import,
  line 104 `void applySavedSink(ctx);`, line 322 `export async function
  setOutputDevice(...)`.
- Patched-file markers, `frontend\src\pages\SettingsPage.tsx`: line 25
  import, line 169 `void setOutputDevice(id);`.
- Exe timestamps: BUILT 09/20 07:55:19 vs INSTALLED 07:25:26 (proving the
  install step is separate), then INSTALLED 07:55:06, then 08:58:16.
- Run A (phantom, relaunch): silence, with the TV as the only physical
  output. Run B (SAMSUNG, relaunch): audio.
- Live retarget: device switched mid-session, no relaunch, audio followed.
  Confirmed by Gray: "the settings changes work as predicted."
### [ARCHIVE-W66-2026-09-20.md] s3 NEGATIVE RESULTS - WHAT THINGS TURNED OUT NOT TO BE
- **THE SIDEBAR SETTINGS LINK WAS NEVER MISSING.** Claude asserted, from a
  filtered grep, that `/settings` was reachable only via the
  backend-unreachable banner in `Layout.tsx:47`. FALSE. `Sidebar.tsx` carries
  `{ path: '/settings', icon: Settings, label: 'Settings' }` in a `navItems`
  array rendered by a single generic `navigate(item.path)` call. The grep
  filter `to=|navigate|href|path=|onClick` matched the dispatcher, not the
  entry. ESTABLISHED BY: Gray using the link in the running app. GENERAL
  LESSON: a filtered grep yields confident false negatives on data-driven
  code - nav tables, route maps, handler registries. Search the DATA, not
  only the call site.
- **THE EMPTY-LABEL HAZARD DID NOT MATERIALISE.** Predicted that
  enumerateDevices would return blank labels without a mic grant, making the
  chooser useless. Measured: named=4 on first probe, and named=4 again on a
  fresh launch where the probe reported labels LOCKED. The microphone grant
  appears unnecessary in this WebView2 build. The `requestDeviceLabels()` path
  remains in `audioOutput.ts` as a fallback; it has NOT been shown to be
  required.
- **UNPLUGGING THE DONGLE DOES NOT REMOVE THE PHANTOM.** With no dongle
  attached, endpoints=4 and the phantom is still listed and still selectable.
  Windows keeps the endpoint registered. Physical removal is NOT a remedy.
- **SILENCE IN RUN A WAS NOT A REGRESSION.** Initially ambiguous because Gray
  asked whether the mic should be reconnected. Resolved by establishing that
  the phantom remains enumerated while unplugged, so Run A was a genuine
  negative control and silence was the predicted pass.
- **`components\Desktop\SettingsPanel.tsx` IS NOT LIVE CODE.** Zero importers.
### [ARCHIVE-W66-2026-09-20.md] s4 HAZARDS FOUND
- **PERSISTENT PHANTOM ENDPOINT.** Selectable whether or not the hardware is
  present. Any future audio work must assume it can be chosen, by a user or
  by Windows, at any time.
- **ALIAS ROWS IN THE DEVICE LIST.** `Default - X` and `Communications - X`
  are role aliases, not endpoints. Selecting an alias re-couples output to a
  Windows role assignment, which is the exact coupling this work removed.
  Documented in the brief; NOT yet filtered in the UI. Candidate improvement:
  hide alias rows or mark them.
- **ASYNC RETARGET VS SYNCHRONOUS CONTEXT CREATION.** `setSinkId` is async;
  `ensureContext()` is synchronous and is called on the queueing path.
  `applySavedSink` is fire-and-forget at creation. The first unit is ~90 chars
  plus a synthesis round-trip away, so the retarget wins that race with
  margin - but if a first-unit-on-wrong-device symptom ever appears, that is
  the place to look. Recorded deliberately as a known, accepted race.
- **A CREATED FILE IS NOT A DELIVERED FILE.** Cost one full build. The
  download card only exists if the file is explicitly presented.
- **DOWNLOAD NAME COLLISION.** A re-downloaded file lands as `Name (1).ext`.
  Copy blocks must resolve the newest match rather than assume the bare name.
- **THE `labels LOCKED` WORDING IS MISLEADING** when names are in fact
  present. Candidate improvement: drive that text off `named` vs total.
### [ARCHIVE-W66-2026-09-20.md] s5 SDD / SDP FEED
ARCHITECTURE - AUDIO OUTPUT PATH (new chapter material):
    Chat reply text
      -> ChatArea caller (Defect A lives here - end-of-turn only)
      -> ttsPlayer.enqueue()            frontend\src\audio\ttsPlayer.ts
      -> splitIntoUnits()               first unit <=90 chars, rest <=350
      -> pump() -> synthesizeSpeech()   HTTP POST, backend 8010
      -> decodeAudioData()
      -> schedule() -> masterGain (gain 1) -> AudioContext.destination
      -> [W66] destination bound to an EXPLICIT endpoint via setSinkId
      -> Windows render endpoint (SAMSUNG HDMI -> TV)
PORTS / PROTOCOLS / ENCODING AT EACH GATE (per the architecture-artifact
rule): frontend to backend, HTTP on localhost:8010, JSON request, audio blob
response, decoded to PCM AudioBuffer in-process. The endpoint binding itself
is a browser-level control with no wire protocol - it selects which OS render
endpoint the webview's audio stream attaches to.
DECISION AND RATIONALE: retarget the LIVE context rather than rebuild it.
A rebuild would drop the keepalive source, and the keepalive exists to stop
the Windows endpoint idling and swallowing the head of the first sound. So
device switching must never tear down the context. This is a hard constraint
on any future audio work, not a style preference.
PLAIN-LANGUAGE EXPLANATION (per the eight-year-old rule, applied here to the
audio path rather than the guard):
A computer can have several places to send sound - a TV, headphones, speakers.
Windows picks one as "the usual place". A small plug-in gadget had told
Windows it contained a speaker, even though it did not. When Windows picked
that pretend speaker, the assistant kept talking and the words went into a box
that was not connected to anything. Nothing looked broken, because nothing WAS
broken - the sound was simply being delivered to a room with no one in it.
The fix is that the assistant now chooses the TV by name and says so every
time it starts talking, instead of using whatever "the usual place" happens to
be that day.
SDP ITEM: the confirmation-gate detail (registry, payload, transport,
threading model) remains the standing GREAT DETAIL requirement. Untouched
in W66.
### [ARCHIVE-W66-2026-09-20.md] s6 EXECUTION PATHS - DELTA
No backend execution path changed in W66. One frontend path is now fully
documented end to end - the TTS output path in s5. Entry point:
`ttsPlayer.enqueue()`, called from the ChatArea TTS effect. No confirmation
gate applies. No event bus traffic. A human is present by definition.
Extract the standing register per s10.
### [ARCHIVE-W66-2026-09-20.md] s7 DIAGNOSTIC TOOLING REGISTER - DELTA
NEW INSTRUMENT: **Audio Output capability readout**, in the Settings UI,
`pages\SettingsPage.tsx`, the `Detect devices` row. Reports
`setSinkId=<bool> | endpoints=<n> | named=<n> | labels <state>`.
OUTPUT PATH VERIFIED AT BUILD TIME: renders on screen in the running app; it
does NOT depend on the webview console, which remains unreadable without the
CDP opt-in. This is the intended pattern where console is dark - make the
feature's own surface the instrument.
STILL TRUE: `[PUMPDBG]` console lines in `ttsPlayer.ts` are UNREADABLE in the
installed app. They were left in place but must not be relied on.
Extract the standing register per s10.
### [ARCHIVE-W66-2026-09-20.md] s8 LOGGING TOPOLOGY - DELTA
No logger tree changed in W66. Unchanged and still true:
`openjarvis.server.speech_router` logs TTS START / TTFB / DONE to
`backend.log` at WARNING; `backend.log` is held open, so read it with
`Select-String`, never `[IO.File]::ReadLines`.
Extract the standing register per s10.
### [ARCHIVE-W66-2026-09-20.md] s9 RULES OF ENGAGEMENT - ADDITIONS
- **PRESENT THE FILE, THEN GUARD THE COPY, THEN BUILD.** Every file delivery
  must be explicitly presented so a download card exists; every copy must be
  Test-Path guarded at the source and marker-grepped at the destination
  BEFORE a build is spent. Earned by losing one build.
- **DO NOT ASK A QUESTION THE BRIEF ALREADY ANSWERS.** The brief's next
  actions are the instruction. Confirming them back is wasted budget.
- **SEARCH THE DATA, NOT ONLY THE CALL SITE.** A filtered grep will miss
  entries held in arrays and config objects. Same family as SEARCH THE SCHEMA
  BEFORE BUILDING AN INSTRUMENT.
### [ARCHIVE-W66-2026-09-20.md] s10 CARRIED REGISTERS - EXTRACTION COMMANDS
These are NOT duplicated here. Extract them VERBATIM from ARCHIVE-W65, which
already carries W64's registers. PowerShell, from
`PS C:\Users\Admin\OpenJarvis>` - set `$a` to the ARCHIVE-W65 path first
(repo root, or `$env:USERPROFILE\Downloads`):
    $a = "$env:USERPROFILE\Downloads\ARCHIVE-W65-2026-09-19.md"
Then extract the section you need, e.g. the tooling register:
    Select-String -Path $a -Pattern '^## s' | Select-Object LineNumber, Line
That prints W65's index with line numbers; take the span you need with:
    (Get-Content $a)[<start>..<end>] | Set-Content .\extracted-section.md
Sections to carry forward into any W67 archive: diagnostic tooling register,
logging topology, execution path register, rules of engagement (full text
originates in ARCHIVE-W57 section 6), program goal, rollback lists
(ARCHIVE-W63/W64).
### [ARCHIVE-W67-2026-09-20.md] NEVER READ WHOLE. EXTRACT A NAMED SECTION.
Extract a section, PowerShell, from `PS C:\Users\Admin\OpenJarvis>`:
    $f='<path to this file>'; $s='## s3'
    (Get-Content $f) | Select-String -Pattern "^$([regex]::Escape($s))" -Context 0,400
### [ARCHIVE-W67-2026-09-20.md] s1 WINDOW SUMMARY - NARRATIVE
W67 restored conversational voice. It did so by REFUSING the patch the brief
named first, and measuring instead.
BRIEF-W66 item 1 was "DEFECT A - MID-STREAM TTS, IN THE CALLER". The instruction
was to read the ChatArea TTS effect whole and fix the caller. Reading it whole
showed a single-owner effect that ALREADY had a live mid-stream branch:
`hasMountedRef` assigned at line 101, sentence batcher at 122-127, and the
store flushed every 80ms from the SSE loop at line 255. On source alone, the
feature looked present.
Rather than patch on that reading, the existing readable instrument was used:
`openjarvis.server.speech_router` writes TTS START / TTFB / DONE to
`backend.log`. Zero build cost. One prompt, one grep. The log settled it in a
single exchange - see s3. Defect A was a STALE DIAGNOSIS, carried forward from
windows in which the app was routing audio into the phantom endpoint W66 later
killed. "No mid-stream speech" and "no speech at all" had been
indistinguishable to the ear, so the symptom was attributed to the caller.
With that cleared, Gray reported the REAL symptoms from live use: the first
word was swallowed again, and speech started only after the last word was on
screen. Two symptoms, and they were deliberately separated.
SYMPTOM 1 - FIRST WORD SWALLOWED. A W66 side effect, and the file predicted it.
`ttsPlayer.ts` opens with a comment explaining that the Windows endpoint sleeps
when idle and eats the head of the first sound, that a keepalive source holds
it awake, and that `KEEPALIVE_GAIN = 0.0` relies on the AudioContext alone
holding the output stream open - "if a machine is ever found whose driver still
idles through digital silence, raise this to something tiny like 0.0001". W66
bound the context to an EXPLICIT endpoint via `setSinkId`. That is the machine
condition the comment anticipated. The author's own documented remedy was
applied, one line, no invention. Verified by ear.
SYMPTOM 2 - SPEECH TRAILING THE TEXT. Held back to its own build. The log gave
the cause directly: chat POST at 09:21:50.320, first TTS START at 09:21:55.314.
FIVE SECONDS before the first unit was even handed to synthesis. Synthesis was
not the bottleneck; the CALLER'S GATE was. ChatArea only released text at
`[.!?]` followed by whitespace, so nothing was spoken until the model finished
an entire first sentence. ttsPlayer already breaks at commas, semicolons and
colons - the caller was simply refusing to give it anything that early. Fix:
for the FIRST segment of a reply only, release at the earliest clause boundary
past 20 characters; later segments keep the sentence rule so the middle of a
reply is not shredded into extra round trips. Result: 5.00s -> 2.29s -> 1.55s.
SYMPTOM 3 was not a symptom but a confirmed defect from W65: F-W62-2d, no
timeout on `synthesizeSpeech`. Patched with `AbortSignal.timeout(30000)`,
which throws into the pump's existing catch so the unit is skipped and the loop
continues. The two mojibake comment lines in the same file were fixed in the
same edit; `api.ts` is now zero non-ASCII, verified by grep.
A tooling lesson was earned on that patch. A multi-line here-string anchor did
not match and reported PATCH FAILED with nothing written - almost certainly
CRLF. The guard worked exactly as intended: no build was spent on a file that
had not changed. The retry used line-indexed splicing and landed first time.
Three builds, three single-variable verifications, one defect deleted rather
than patched. F-W62-2c was deliberately left for W68 rather than stacked into
an unverified build.
### [ARCHIVE-W67-2026-09-20.md] s3 NEGATIVE RESULTS - WHAT THINGS TURNED OUT NOT TO BE
- **DEFECT A WAS NOT A DEFECT. MID-STREAM TTS WAS ALREADY WORKING.** Carried
  as next-action item 1 in BRIEF-W66 and as an open capability gap for several
  windows. ESTABLISHED BY: `backend.log` TTS lines across one reply. The pump
  went IDLE for 2.5s mid-reply while gaps elsewhere in the same turn were
  13-22ms - a queue filled once at end-of-turn drains back-to-back and cannot
  go idle. Unit sizes (19 then 111) independently prove multiple `enqueue()`
  calls. NO PATCH WAS WRITTEN. GENERAL LESSON: a defect carried in a brief can
  outlive its cause. When a symptom has been masked by a DIFFERENT fault that
  has since been fixed, re-measure before patching the old suspect. Same family
  as VALIDATE, DO NOT INTERROGATE, applied to the brief itself rather than to
  Gray.
- **`add_midstream_tts.py` WAS NEVER THE ANSWER AND IS NOW MOOT.** W66 knew its
  regex was broken and that it drove the superseded playNextChunk path. W67
  establishes there is nothing for it to do. Do not resurrect it.
- **THE TRAILING-SPEECH SYMPTOM WAS NOT A SYNTHESIS LATENCY PROBLEM.** Natural
  reading, given TTS latency history (criterion 4, the 0.65s floor, the
  fetch-stall thread). FALSE for this symptom: 5.00s of the delay was upstream
  of the first synthesize request, inside the caller's release gate. Synthesis
  itself was performing normally. ESTABLISHED BY: POST-to-first-START interval,
  which excludes synthesis entirely by construction.
- **THE FIRST-WORD REGRESSION WAS NOT A REGRESSION IN THE W66 PATCHES.** The
  `setSinkId` work was correct and stayed. What changed was that binding an
  explicit endpoint removed whatever incidental wakefulness the default path
  had, exposing the zero-gain keepalive as insufficient ON THIS MACHINE - the
  exact condition the file's own comment named. The remedy was already
  documented by the author.
- **THE `api.ts` PATCH DID NOT SILENTLY HALF-APPLY.** First attempt reported
  PATCH FAILED and wrote nothing; read-back confirmed the file unchanged. The
  guard held. No build was spent.
### [ARCHIVE-W67-2026-09-20.md] s4 HAZARDS FOUND
- **`KEEPALIVE_GAIN` IS NOW LOAD-BEARING AND LOOKS LIKE A NO-OP.** `0.0001`
  reads as a magic number a tidier would zero or delete. Zeroing it re-breaks
  the first word, and the symptom appears in the AUDIO path while the cause
  sits in a constant. Guarded by the commit message and this archive. Consider
  an inline WARNING comment if it is ever touched again.
- **THE CLAUSE RELEASE CAN EMIT AN 8-CHAR FIRST UNIT.** The 20-char floor
  applies to the segment RELEASED; ttsPlayer then breaks that segment at
  commas, so a leading "Of course," becomes its own unit and pays the ~1.0s
  per-request floor. Accepted for the early start. If a stutter immediately
  after the first word is ever reported, this is the cause. Candidate
  improvement: raise the floor to ~40, or suppress a sub-15-char leading unit.
- **F-W62-2d's TIMEOUT BRANCH IS UNEXERCISED.** Regression-verified only.
  Exercising it needs a hung backend - a deliberate fault injection, not
  something to assume works.
- **`beginTurn()` IS DEAD CODE WITH A LIVE PURPOSE.** Exported from ttsPlayer,
  imported nowhere. The short-first-unit cap resets only as a side effect of
  `stopAll()`. It works today because ChatArea calls `stopAll()` on every new
  reply id - a coupling nobody wrote down. If that `stopAll()` is ever removed,
  the first-unit cap silently stops resetting and time-to-first-audio degrades
  with no error.
- **HERE-STRING ANCHORS FAIL ON CRLF FILES.** A multi-line `$old` here-string
  did not match `api.ts`. Line-indexed splicing worked. Prefer it for any
  multi-line insert in this repo.
- **`src\lib.rs:598` `clone_target` UNUSED** - compiler warning, every build.
  Cosmetic, unaddressed.
- **BUNDLE SIZE WARNING** - `index-*.js` at 947.82 kB exceeds the 500 kB
  advisory on every build. Unaddressed, noted so it is not mistaken for new.
### [ARCHIVE-W67-2026-09-20.md] s5 SDD / SDP FEED
ARCHITECTURE - THE VOICE PATH, END TO END (supersedes the W66 s5 diagram by
adding the CALLER'S GATE, which is where time is actually spent):
    User submits
      -> POST /v1/chat/completions          localhost:8010, SSE response
      -> ChatArea SSE loop                  components\Chat\ChatArea.tsx
         acc += delta; setStreamState every delta;
         updateLastAssistant every 80ms
      -> TTS effect (single owner)          re-runs on each store change
         GATE: first segment  -> first clause boundary past 20 chars
               later segments -> last completed sentence
               muted          -> segment CONSUMED, not spoken
      -> enqueue(plainText)                 audio\ttsPlayer.ts
      -> splitIntoUnits()                   first unit <=90, rest <=350
      -> pump() -> synthesizeSpeech()       POST /v1/speech/synthesize,
                                            JSON in, wav blob out, 30s timeout
      -> decodeAudioData() -> schedule()
      -> masterGain (1.0) -> AudioContext.destination
      -> destination bound by setSinkId to an EXPLICIT endpoint (W66)
      -> keepalive source at gain 0.0001 holds that endpoint awake (W67)
      -> Windows render endpoint (SAMSUNG HDMI -> TV)
TIME BUDGET, MEASURED: request to first audio = gate (1.5-2.3s, model-bound)
+ TTFB (1.0-1.5s). The gate was 5.0s before W67. Everything after the first
unit is hidden, because synthesis runs faster than realtime (13.376s of audio
from a 7.68s request), so only the FIRST unit's latency is user-visible.
DECISION AND RATIONALE - WHY THE GATE, NOT THE SYNTHESIZER, WAS TUNED:
time-to-first-audio has been attacked repeatedly on the synthesis side
(criterion 4, the cuDNN fix, the chunker curve, the 0.65s floor). W67 shows the
remaining user-visible delay was upstream of synthesis entirely. RULE FOR THE
SDD: when measuring time-to-first-audio, ALWAYS decompose into gate time
(POST -> first TTS START) and synthesis time (START -> TTFB). They have
different owners and different fixes, and the log distinguishes them for free.
DECISION AND RATIONALE - WHY THE CONTEXT IS NEVER REBUILT: carried from W66.
A rebuild drops the keepalive, and W67 makes the keepalive strictly more
important, not less - it is now the only thing keeping an explicitly-bound
endpoint awake. Hard constraint on all future audio work.
PLAIN-LANGUAGE EXPLANATION (eight-year-old rule, applied to the voice path):
Imagine you want to read a story out loud to someone in the next room. The old
rule was: wait until you have read a WHOLE sentence to yourself, then start
speaking. So there was a long silence at the start while you read ahead. The
new rule is: as soon as you have read enough to make sense - even just a few
words up to a comma - start talking. The rest arrives while you are still
speaking, so you never run out. The other problem was the loudspeaker in the
next room falling asleep between stories, so the first word arrived before it
woke up and was lost. Now we keep a sound playing that is far too quiet for
anyone to hear, which is enough to keep the speaker awake and listening, so the
first word always arrives at a speaker that is ready for it.
SDP ITEM: the confirmation-gate detail (registry, payload, transport, threading
model) remains the standing GREAT DETAIL requirement. Untouched in W67.
### [ARCHIVE-W67-2026-09-20.md] s6 EXECUTION PATHS - DELTA
No backend execution path changed. The frontend TTS output path documented in
ARCHIVE-W66 s6 is AMENDED: its entry point is the ChatArea TTS effect, and that
effect now carries a two-mode release gate (first segment vs later segments)
which is part of the path and materially determines its timing. Full diagram in
s5. No confirmation gate applies. No event bus traffic. A human is present by
definition. Extract the standing register per s10.


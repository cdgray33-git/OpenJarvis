/*
 * audioOutput.ts - OpenJarvis audio output endpoint selection.
 * MARKER: openjarvis-audio-output-v1
 *
 * Why this exists (W65 finding): a composite USB dongle (VID_0573/PID_1573)
 * presents a PHANTOM "Speakers (USB Audio and HID)" render endpoint on a mini
 * PC that has no USB speaker. When Windows makes that phantom the default
 * render device, OpenJarvis speech is scheduled, played, and heard by nobody,
 * with no error anywhere in the stack. Measured: peak 0.000000 across 278
 * samples on the phantom, peak 0.971459 on SAMSUNG HDMI. Same build, same exe.
 *
 * The fix is to stop depending on the Windows default at all: pick the endpoint
 * explicitly, persist it, and re-apply it every time the AudioContext is built.
 *
 * This module owns discovery and persistence ONLY. It never touches the audio
 * graph - ttsPlayer owns the context and applies the selection. That split
 * keeps the keepalive/first-word machinery in one file.
 *
 * KNOWN HAZARD - EMPTY LABELS: enumerateDevices() returns audiooutput entries
 * with blank label and blank deviceId until the page has been granted
 * microphone permission. Without a grant the chooser would render nameless
 * rows and could not tell SAMSUNG from the phantom. requestDeviceLabels()
 * obtains that grant; the UI calls it before listing.
 */

const SINK_STORAGE_KEY = 'openjarvis-audio-sink';

export interface AudioOutputDevice {
  deviceId: string;
  label: string;
}

/*
 * True if this webview can retarget an AudioContext to a chosen endpoint.
 * AudioContext.setSinkId is Chromium 110+; this build is 153, but the check is
 * cheap and the UI reports it rather than assuming.
 */
export function isSinkSelectionSupported(): boolean {
  try {
    const Ctor =
      window.AudioContext ||
      (window as unknown as { webkitAudioContext?: typeof AudioContext })
        .webkitAudioContext;
    if (!Ctor) return false;
    return typeof (Ctor.prototype as unknown as { setSinkId?: unknown })
      .setSinkId === 'function';
  } catch {
    return false;
  }
}

/* True if device enumeration exists at all. */
export function isEnumerationSupported(): boolean {
  try {
    return (
      typeof navigator !== 'undefined' &&
      !!navigator.mediaDevices &&
      typeof navigator.mediaDevices.enumerateDevices === 'function'
    );
  } catch {
    return false;
  }
}

/*
 * Ask for microphone permission purely to unlock output device LABELS. The
 * stream is stopped immediately; nothing is recorded. Returns true if labels
 * should now be readable.
 */
export async function requestDeviceLabels(): Promise<boolean> {
  try {
    if (!navigator.mediaDevices?.getUserMedia) return false;
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    stream.getTracks().forEach((t) => t.stop());
    return true;
  } catch (err) {
    console.warn('[audioOutput] label permission denied:', err);
    return false;
  }
}

/* Every audiooutput endpoint the webview can see. */
export async function listAudioOutputs(): Promise<AudioOutputDevice[]> {
  if (!isEnumerationSupported()) return [];
  try {
    const all = await navigator.mediaDevices.enumerateDevices();
    return all
      .filter((d) => d.kind === 'audiooutput')
      .map((d) => ({ deviceId: d.deviceId, label: d.label }));
  } catch (err) {
    console.warn('[audioOutput] enumerateDevices failed:', err);
    return [];
  }
}

/* The persisted endpoint id, or '' meaning "follow the Windows default". */
export function getSavedSinkId(): string {
  try {
    return localStorage.getItem(SINK_STORAGE_KEY) || '';
  } catch {
    return '';
  }
}

export function saveSinkId(deviceId: string): void {
  try {
    if (deviceId) localStorage.setItem(SINK_STORAGE_KEY, deviceId);
    else localStorage.removeItem(SINK_STORAGE_KEY);
  } catch {
    /* storage unavailable; selection is session-only */
  }
}

/*
 * Apply the persisted endpoint to a live AudioContext. Called by ttsPlayer at
 * context creation. Safe to call when nothing is saved - that is the no-op
 * "follow the default" case. Never throws; a failed retarget must not take the
 * speech path down with it.
 */
export async function applySavedSink(context: AudioContext): Promise<boolean> {
  const deviceId = getSavedSinkId();
  if (!deviceId) return false;
  return applySink(context, deviceId);
}

export async function applySink(
  context: AudioContext,
  deviceId: string,
): Promise<boolean> {
  try {
    const target = context as unknown as {
      setSinkId?: (id: string) => Promise<void>;
    };
    if (typeof target.setSinkId !== 'function') return false;
    await target.setSinkId(deviceId);
    return true;
  } catch (err) {
    console.warn('[audioOutput] setSinkId failed:', err);
    return false;
  }
}

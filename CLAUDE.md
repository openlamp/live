# CLAUDE.md — openlamp-live

Ableton Live frontend for the OpenLamp lamp stack.

## What this repo is (and is NOT)

- **IS**: the Ableton-Live frontend — a MIDI pack (Mode A) and, later, a Control
  Surface (Mode B) — that lets a user program lamp automations from Live with only
  Ableton + lamps on the LAN. See [docs/DESIGN.md](docs/DESIGN.md).
- **IS NOT**: a MIDI protocol. The wire convention lives in
  [openlamp/wled-midi](https://github.com/openlamp/wled-midi) and MUST NOT be
  duplicated here — reference it and pin a version. Ableton is just one frontend that
  speaks it (a Stream Deck plugin is a peer frontend).

## Golden rules

- **Do not re-implement the convention or the engine.** Mode A emits the
  [wled-midi](https://github.com/openlamp/wled-midi) convention to the lamp MIDI port;
  the engine drives the devices. Mode B may talk to lamps directly over the LAN, but
  it still speaks the same convention — don't fork it.
- **Everything derives from `ableton/mapping.spec.json`.** The `.mid` clips are
  generated (open format) via `tools/gen_clips.py`; the `.als` template is exported
  once from Live (its binary format is Ableton's, version-fragile — don't synthesize
  it headless). Note: stock Live macros can't emit outgoing CC, so Mode A's
  continuous control is clip CC automation, not macros (macro→CC out = Max for Live
  = Mode B). als-wire maps *incoming* controller CC → macros — orthogonal, not the
  pack generator.
- **Mode B is version-fragile by nature** (Live's Remote Script API is semi-private).
  Pin a Live version, prefer Max for Live if it satisfies the direct-to-LAN goal.
- **Family conventions apply** (MIT, one concern per repo, English public docs,
  Conventional Commits). New repos go to GitHub under the `openlamp` org.

## Stack

```
Live ──MIDI (wled-midi)──▶ lamp port ──▶ engine ──HTTP/UDP──▶ lamps   (Mode A)
Live (Remote Script / M4L) ──────────HTTP/UDP──────────────────▶ lamps   (Mode B, direct-to-LAN)

(The MIDI→lamp step runs in the engine's midi.py — the wled-midi reference impl —
opening the `OpenLamp` virtual MIDI port. Tempo-follow is the openlamp-midi package.)
```

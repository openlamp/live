# Design — how Ableton Live drives OpenLamp lamps

Decision record for `openlamp-live`.

## Goal

**With nothing but Ableton Live and some lamps on the local network, a user can set
up lamp automations from Ableton.** Minimal moving parts, 100 % local, no cloud.
The lamps (WLED + Tuya) live on the LAN; Live is where the show is programmed.

## Guiding principle — reach everyone first, integrate deeply second

**Accessibility for everyone comes first; the tightest integration comes second.**
The widest, lowest-barrier path is built and polished before the premium,
deeply-integrated one. This orders the whole roadmap into two tiers:

**Tier 1 — accessible to everyone (breadth, zero barrier).** Any DAW, any Live
edition, no terminal.

- **Package the engine as a no-install desktop app** (`.app` / `.exe`, menu-bar,
  signed, headless) — today the only real barrier on the universal path is "run a
  Python process". Once the engine is a double-click app, *anyone* can run the
  bridge, whatever frontend they use. (Engine-repo work — see
  [openlamp/engine](https://github.com/openlamp/engine).)
- **Mode A turnkey**: the generated `.mid` clip pack **+ a demo `.als`** — works in
  every DAW and every Live edition, nothing fragile, nothing paid.

**Tier 2 — best integration (depth, premium).**

- **Mode B as a Max for Live device**: direct-to-LAN (no daemon), bidirectional
  feedback, a real device UI on the track. Suite-only is acceptable *here* precisely
  because Tier 1 already serves everyone — depth is allowed to be selective once
  breadth is covered.

This mirrors the rest of the OpenLamp galaxy — WLED-first, CC0 assets, an MIT
convention: reach first, refine second.

## Two integration modes — we ship both

The lamps speak HTTP/JSON/UDP on the network, not MIDI, so *something* must
translate "what Live plays" into lamp commands. There are two good places to put
that translation, and they serve different users. **We build both** — they are
complementary, not either/or.

### Mode A — base MIDI API  (the stable foundation)

Live emits standard MIDI per the
[wled-midi convention](https://github.com/openlamp/wled-midi); the engine (via its
[`midi.py`](https://github.com/openlamp/engine/blob/main/midi.py)) translates it to
WLED JSON state / Tuya and drives the lamps.

**Wire (two protocols in the chain):**

```
Ableton Live ──MIDI──▶ virtual port "OpenLamp" ──▶ midi.py ──HTTP──▶ engine :8377 ──HTTP──▶ WLED (LAN)
   (clips)         (MIDI 1.0, CoreMIDI/rtmidi)   (translates)  (loopback /cmd)     (POST /json/state)
```

From the musician's side the protocol is **plain MIDI 1.0** on a virtual port
(`OpenLamp`): notes → colours/power, CC → brightness/hue/sat/CCT/fx, Program Change →
presets, MIDI clock → tempo. `midi.py` then POSTs to the engine's loopback API
(`127.0.0.1:8377/cmd`); the engine holds the persistent connections and emits the WLED
**HTTP JSON** patch (`POST http://<lamp>/json/state`).

**On feedback — the clip is one-way, but Mode A isn't necessarily.** A `.mid` *clip*
only plays out (it reads nothing back), but nothing stops the engine from opening a
**second, return MIDI port** (`OpenLamp Feedback`, engine → Live): the engine subscribes
to WLED's state WebSocket (`ws://<lamp>/ws`) and re-emits lamp state as MIDI (CC =
brightness/hue/sat, note = on/off, CC = effect index). What gates this is not the
transport but **what stock Live can DO with incoming MIDI**:

- **Value-level feedback → stays Tier 1** (no M4L, all editions): an incoming CC can be
  **MIDI-mapped** to an on-screen control, so a fader follows the real brightness, a
  button reflects on/off. Good for hardware controllers with faders/LEDs.
- **Hardware echo** (motorised fader, controller LEDs): stock MIDI-map doesn't auto-echo
  out; that usually wants a Control Surface script (Mode B territory).
- **Rich/visual feedback** (the true colour as a swatch, effect *names*, a readable panel
  in Live) → **needs a program that renders it** = **Mode B (M4L)**. A raw CC carries a
  number, not a colour or a label.

So the split is by **richness of feedback**, not "A has none, B has all": value-level
feedback via a return MIDI port is a Tier-1 option; rich visual feedback is what M4L is
for. In both cases the **engine** is what produces the feedback (it consumes WLED's
WebSocket) — feedback needs *a program somewhere*, not M4L specifically.

- **The convention already exists and is tested** —
  [wled-midi](https://github.com/openlamp/wled-midi): notes → colours/power, CC →
  brightness/hue/sat/CCT + effect fx/sx/ix, Program Change → presets, one channel per
  target/group.
- `openlamp-live` adds the **Ableton-native pack**: a MIDI track routed to the
  lamp MIDI port carries **notes** (colour/power/animation triggers) and **CC
  automation** (brightness/hue/sat/CCT/fx envelopes) out to the bridge. Shipped as
  **draggable `.mid` clips** generated from the mapping spec (`tools/gen_clips.py`)
  plus a demo `.als` template. Stock Live only — **no private API**, works in any
  DAW, every param clip-automatable.

  Note: a **stock Live macro does not emit outgoing CC** — turning a knob into an
  outgoing CC value needs a Max for Live device, which is Mode B territory. Mode A's
  continuous control is therefore **clip/arrangement CC automation**, not macros.
- Cost to the user: run the engine's
  [`midi.py`](https://github.com/openlamp/engine/blob/main/midi.py), which opens the
  `OpenLamp` MIDI port. One small process alongside Live.

### Mode B — Control Surface (Max for Live — decided)  (tighter + standalone)

A component that runs *inside* Live (a **Max for Live device** — decision + argument
below). This mode earns its keep with two advantages the pack can't give:

1. **Direct-to-LAN, no separate daemon.** Runs *inside* Live and reaches the WLED
   lamps **directly over the local network** — **HTTP** (`POST /json/state`) or WLED
   **realtime UDP** (DDP/WARLS, port 21324). That collapses the setup to exactly the
   goal above — **just Ableton + lamps on the LAN**, nothing else to launch. (It can
   still delegate to the engine on `:8377` when the engine is running, to stay in sync
   with the Stream Deck.)
2. **Rich, in-Live visual feedback** — the lamps' **real** state shown *as state*: the
   true colour as a swatch, the effect **name**, a readable device panel; state never
   drifts when the Stream Deck (or anything else) changes a lamp. Note the nuance (see
   Mode A → *On feedback*): **value-level** feedback (a fader following brightness) is a
   Tier-1 option via a return MIDI port + MIDI-mapping, no M4L. What M4L uniquely buys is
   **rendering** state a raw CC can't carry — colours, labels, a panel. WLED **pushes**
   state over a WebSocket (`ws://<lamp>/ws`), which the device subscribes to.

## Decision

**Build A first, then B** — per the guiding principle (reach first, integrate second).
A is the stable, DAW-agnostic base and unblocks the whole feature immediately with zero
fragile-API risk; making it truly turnkey means **packaging the engine as a no-install
app + shipping the demo `.als`** (Tier 1). B follows because it delivers a distinct win
— the **standalone "Ableton + lamps only" experience** and feedback — that A
structurally cannot (Tier 2). B does not replace A; a player can use either, and the
convention (A) is what B implements natively.

| Criterion | A — MIDI API + Live pack | B — Control Surface |
|---|---|---|
| Reaches lamps with **only Ableton + LAN** | No (needs the bridge process) | **Yes** (script talks to lamps directly) |
| Depends on Ableton's private API | No | Yes (version-fragile) |
| Clip automation of lamp params | **Native** | Native |
| Feedback into Live / controller | Value-level (return MIDI port + MIDI-map) | **Rich/visual** (colour swatch, effect name, panel) |
| Works in other DAWs | **Yes** | Live-only |
| Maintenance cost | Low | Higher |
| Ships | **v1** | **v2** |

## How the pack (A) gets built

Config-as-code, pinned to one source: **`ableton/mapping.spec.json`** mirrors the
[wled-midi](https://github.com/openlamp/wled-midi) core note/CC numbers. From it:

- **`.mid` clips** are generated byte-for-byte with `tools/gen_clips.py` (stdlib,
  Standard MIDI Files — an open, stable format Live imports by drag-and-drop). A
  trigger clip = one note-on (reliable on import); CC-sweep demo clips document the
  envelope shape (Live's `.mid` import favours notes over CC, so those may be
  redrawn as clip automation).
- **the `.als` template** is authored once inside Live and exported (its binary,
  version-fragile format is Ableton's — we don't synthesize it headless). It only
  needs the tracks pre-named + pre-routed to the lamp port on each target's channel.

`.mid` clips being an open format is what lets us *generate and test* them here;
that's why the pack is clips-first, template-second.

Not the tool for this: [als-wire](https://github.com/Beennnn/als-wire) maps an
**incoming** controller's CC onto rack macros (controller → Live). Useful later if
a player wants to drive the template's tracks from a hardware controller — but it
is the opposite direction from the lamp *output* pack, so it does not build it.

## Mode B is a Max for Live device — decided

Between the two ways to run code inside Live — a **Max for Live device** (`.amxd`,
Node for Max for networking) vs a raw **Remote Script** (Python via Preferences →
MIDI → Control Surface) — **we pick Max for Live.**

| Criterion | **Max for Live** | Remote Script |
|---|---|---|
| API stability | Live Object Model, **documented + supported** | `_Framework`/`ableton.v2-v3`, **semi-private, undocumented** (shifted Live 10→11 Py2→3, 11→12) |
| Install | `.amxd`, drag-drop from the browser | copy a folder into `MIDI Remote Scripts/` + restart Live |
| On-track UI (to display feedback) | **Yes** (device panel) | **None** (feedback only to hardware LEDs) |
| Direct network (WLED HTTP/UDP) | **Node for Max** (`http`/`dgram`) | Python `socket`/`urllib` |
| Live editions | **Suite only** (or the M4L add-on) | All (Intro/Standard/Suite) |
| Maintenance | Low | High (version-fragile) |

**Why the Suite-only cost is acceptable:** the *universal* need is already met by
**Tier 1** (Mode A works in every DAW and every Live edition). Mode B is the **depth**
layer, so it may be selective — API stability, a real UI to show feedback, and easy
networking (Node for Max) outweigh reaching non-Suite users *here*. Remote Script's
only edge (all editions) is redundant with Tier 1.

**Delegation option:** the device talks to lamps directly by default, but can route
through the engine's `:8377` API when the engine is running — so an Ableton show and a
Stream Deck stay in sync on one shared state.

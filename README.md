# openlamp-live — drive your lamps from Ableton Live

Turn a **track in Ableton Live** into a lamp/show controller: clips, macros and
automation envelopes drive your [OpenLamp / LumiDeck](https://github.com/openlamp/openlamp)
smart LED lamps (WLED + Tuya) **on the beat, in time with your set** — 100 % local,
no cloud.

This repo is the **Ableton Live integration layer** of the OpenLamp stack. It does
not re-implement MIDI control — it sits on top of the existing, stable
[LumiDeck MIDI convention](https://github.com/openlamp/midi/blob/main/MIDI-PROTOCOL.md)
and makes it turnkey inside Live.

## What you can do with it

You program the lights from the same timeline as the music. The **beat** is the
obvious starting point — but it's a floor, not a ceiling.

- **🥁 Visual metronome with a downbeat accent.** Every beat pulses the lamps; bar 1
  hits brighter and in a different colour. A silent click you *see* across a loud
  stage — the band locks in without an in-ear.
  *(Ableton Link / MIDI clock → tempo pulse, phase-accurate accent on the downbeat.)*

- **🎭 A lighting cue list built into your set.** Warm and dim for the verse,
  saturated blue for the bridge, a white strobe on the drop — each song section
  carries its own colour and brightness. Your arrangement *is* the light show, no
  separate operator.
  *(One trigger + CC-automation clip per section, laid on the timeline.)*

- **📍 Hands-free song-part markers.** The lamps change colour at every part
  boundary — intro → verse → chorus → solo — so everyone on stage sees "we're in the
  chorus now" without counting bars. Priceless for long-form or improvised sets.
  *(A trigger clip at each section start.)*

- **⏺ Record & replay your light performance.** Play the lights by hand once — a
  footswitch for a blackout on the drop, a fader sweeping brightness through the
  build — while Live records the MIDI. Every show after that replays it note-perfect.
  *(Arm a MIDI track routed to `LumiDeck`; Live captures your moves as automation.)*

- **🎚 Multi-zone staging.** Front lamps ride the beat while the back wash holds the
  section's ambiance — two independent behaviours at once.
  *(Channel-per-group: one Live track and channel per lamp group.)*

- **👆 Whole-rig tempo, one tap.** Tap the tempo once and every Ableton Link app *and*
  the lamps follow — synths, drum machines and lights on the same clock.
  *(Ableton Link session tempo, via [openlamp-midi](https://github.com/openlamp/midi).)*

Everything is local: Ableton + lamps on your Wi-Fi, nothing in the cloud.

| Layer | Repo | Role |
|---|---|---|
| **core** | [openlamp/engine](https://github.com/openlamp/engine) | LED interface + OpenLamp State (OLS) contract + engine (local API on `127.0.0.1:8377`) |
| **midi** | [openlamp/midi](https://github.com/openlamp/midi) | MIDI → OLS overlay: virtual port `LumiDeck`, channels-as-groups, notes/CC/PC/clock |
| **live** | **this repo** | Ableton-Live-native pack that speaks the MIDI convention |

## How it works

```
Ableton Live  ──MIDI──▶  "LumiDeck" virtual port  ──▶  openlamp-midi bridge  ──HTTP──▶  engine  ──▶  lamps
 (clips, macros,          (from openlamp/midi)          (MIDI → OLS)          :8377         (WLED/Tuya)
  automation)
```

Live never talks to a lamp directly. It emits MIDI on the `LumiDeck` port; the
[openlamp-midi](https://github.com/openlamp/midi) bridge translates it to OpenLamp
State and the engine drives the devices. So this repo is mostly **Ableton-side
assets + docs** — the runtime already exists in the bridge.

## What this project delivers

- **An Ableton Live pack** — a MIDI track routed to `LumiDeck` carries notes
  (colour/power/animation triggers) and CC automation (brightness/hue/sat/CCT/fx).
  Shipped as **draggable `.mid` clips generated from the mapping spec** (open,
  reproducible format) plus a pre-routed demo `.als` template. Stock Live only, no
  private API. **← the foundation.**
- **A documented setup path** — [docs/ABLETON-SETUP.md](docs/ABLETON-SETUP.md):
  create the `LumiDeck` port, route a Live track to it, pick the channel per group.
- **A Control Surface (MIDI Remote Script)** — *on the roadmap (v2)*, for players
  who want lamps in Live's Preferences → MIDI → Control Surface slot with feedback.
  Deferred on purpose — see [docs/DESIGN.md](docs/DESIGN.md) for why the pack comes
  first.

## Status

🚧 **Mode A in progress** — convention spec + 19 generated `.mid` clips shipped;
next is testing on real lamps and authoring the pre-routed `.als` template. Mode B
(Control Surface) is designed, not started. See [TASKS.md](TASKS.md).

## Requirements

- The running OpenLamp engine + the [openlamp-midi](https://github.com/openlamp/midi)
  bridge (`pip install openlamp-midi`), which opens the `LumiDeck` virtual MIDI port.
- Ableton Live 10+ (the pack uses only stock MIDI devices — no private API).

## License

[EUPL-1.2](LICENSE) — same as the rest of the OpenLamp family (compatible with
Ableton Link's GPLv2 per the EUPL appendix).

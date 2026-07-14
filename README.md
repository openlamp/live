# openlamp-live — drive your lamps from Ableton Live

Turn a **track in Ableton Live** into a lamp/show controller: clips, macros and
automation envelopes drive your [OpenLamp / LumiDeck](https://github.com/openlamp/openlamp)
smart LED lamps (WLED + Tuya) **on the beat, in time with your set** — 100 % local,
no cloud.

This repo is the **Ableton Live integration layer** of the OpenLamp stack. It does
not re-implement MIDI control — it sits on top of the existing, stable
[LumiDeck MIDI convention](https://github.com/openlamp/midi/blob/main/MIDI-PROTOCOL.md)
and makes it turnkey inside Live.

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

- **An Ableton Live pack** — a MIDI Effect Rack whose eight macros map to the
  convention's continuous controls (brightness, hue, saturation, CCT, effect
  fx/sx/ix), plus a clip/scene template (one MIDI track per lamp group, on the
  matching channel) and a demo `.als` set. **← the foundation.**
- **A documented setup path** — [docs/ABLETON-SETUP.md](docs/ABLETON-SETUP.md):
  create the `LumiDeck` port, route a Live track to it, pick the channel per group.
- **A Control Surface (MIDI Remote Script)** — *on the roadmap (v2)*, for players
  who want lamps in Live's Preferences → MIDI → Control Surface slot with feedback.
  Deferred on purpose — see [docs/DESIGN.md](docs/DESIGN.md) for why the pack comes
  first.

## Status

🚧 **Initiated** — design locked, docs written, Ableton binary assets
(`.adg` rack, `.als` template) to be authored next (built programmatically with
[als-wire](https://github.com/Beennnn/als-wire)). See [TASKS.md](TASKS.md).

## Requirements

- The running OpenLamp engine + the [openlamp-midi](https://github.com/openlamp/midi)
  bridge (`pip install openlamp-midi`), which opens the `LumiDeck` virtual MIDI port.
- Ableton Live 10+ (the pack uses only stock MIDI devices — no private API).

## License

[EUPL-1.2](LICENSE) — same as the rest of the OpenLamp family (compatible with
Ableton Link's GPLv2 per the EUPL appendix).

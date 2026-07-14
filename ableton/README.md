# Ableton assets

Binary Live assets for Mode A live here. They are **build outputs** of a versioned
mapping spec, authored programmatically with
[als-wire](https://github.com/Beennnn/als-wire) — not hand-clicked (see
[../docs/DESIGN.md](../docs/DESIGN.md)).

Planned contents:

| File | What |
|---|---|
| `OpenLamp.adg` | MIDI Effect Rack — 8 macros mapped to CC 1–7 (bri, cct, hue, sat, fx, sx, ix) |
| `OpenLamp-demo.als` | Demo set — one MIDI track per group, each pre-routed to `LumiDeck` on its channel, with example colour clips + automation |
| `mapping.spec.json` | Source-of-truth mapping (macro → CC, track → channel) that als-wire consumes to emit the `.adg`/`.als` |

Nothing here yet — this is the next build step. Tracked in
[../TASKS.md](../TASKS.md).

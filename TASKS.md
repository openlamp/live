# TASKS — openlamp-live

## Mode A — MIDI pack (v1, foundation)

- ☐ Write `ableton/mapping.spec.json` → the source-of-truth macro→CC + track→channel map (config-as-code the `.adg`/`.als` are generated from)
- ☐ Generate `ableton/OpenLamp.adg` via [als-wire](https://github.com/Beennnn/als-wire) → 8 rack macros pre-mapped to CC 1–7, so users skip manual MIDI wiring
- ☐ Generate `ableton/OpenLamp-demo.als` → one MIDI track per group pre-routed to `LumiDeck` on its channel + example colour clips & automation → turnkey demo
- ☐ Test the pack against the running bridge on real lamps → confirm every CC/note in the pack actually moves the right lamp before publishing
- ☐ Flip repo public + add to the OpenLamp umbrella README once the pack works end-to-end

## Mode B — Control Surface (v2, standalone + feedback)

- 🤔 Decide **Max for Live device vs raw Remote Script** → M4L is far less version-fragile; pick before writing code (see DESIGN.md "evaluate Max for Live first")
- ☐ Prototype direct-to-LAN control from inside Live (script/M4L hits WLED HTTP/UDP directly) → proves the "just Ableton + lamps, no daemon" goal
- ☐ Add bidirectional feedback (lamp state → Live/controller) → the one thing Mode A structurally can't do
- ☐ Pin a target Live version + document install → contain the semi-private API fragility

## Cross-cutting

- ☐ Add project to Ableton's Link/products submission once a mode is usable (ties back to the link-devs@ableton.com outreach)

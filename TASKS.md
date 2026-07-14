# TASKS — openlamp-live

## Mode A — MIDI pack (v1, foundation)

- ✅ `ableton/mapping.spec.json` — pinned mirror of the [wled-midi](https://github.com/openlamp/wled-midi) v0.1.0 core
- ✅ `tools/gen_clips.py` + `ableton/clips/*.mid` — 16 draggable clips generated & SMF-verified
- ☐ Test the clips against the running engine on real lamps → confirm each note fires the right action / target before relying on the pack
- ☐ Confirm Live's `.mid` import behaviour for the CC-sweep clips → if CC isn't carried as automation, document the "redraw as clip automation" step (or ship an `.alc`)
- ☐ Author `ableton/OpenLamp-demo.als` once in Live → one MIDI track per target pre-routed to the lamp port on its channel, with the clips laid in → turnkey demo set
- ☐ Add to the OpenLamp umbrella README once the pack works end-to-end on real lamps

## Mode B — Control Surface (v2, standalone + feedback)

- 🤔 Decide **Max for Live device vs raw Remote Script** → M4L is far less version-fragile; pick before writing code (see DESIGN.md "evaluate Max for Live first")
- ☐ Prototype direct-to-LAN control from inside Live (script/M4L hits WLED HTTP/UDP directly) → proves the "just Ableton + lamps, no daemon" goal
- ☐ Add bidirectional feedback (lamp state → Live/controller) → the one thing Mode A structurally can't do
- ☐ Pin a target Live version + document install → contain the semi-private API fragility

## Cross-cutting

- ☐ Add project to Ableton's Link/products submission once a mode is usable (ties back to the link-devs@ableton.com outreach)

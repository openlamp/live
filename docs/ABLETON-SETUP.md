# Ableton setup — Mode A (MIDI pack)

Get lamps reacting to a Live set in a few minutes. This is **Mode A** (Ableton
speaking the [wled-midi](https://github.com/openlamp/wled-midi) convention); Mode B
(Control Surface) will have its own install doc when it ships — see
[DESIGN.md](DESIGN.md).

## Prerequisites

1. Lamps reachable on your LAN (WLED and/or Tuya), configured in the OpenLamp engine.
2. The engine's MIDI frontend running — it opens the `OpenLamp` virtual MIDI port:
   ```
   python3 midi.py        # from github.com/openlamp/engine — opens the "OpenLamp" port
   ```

## Route Live to the lamps

1. **Live → Settings → Link/Tempo/MIDI**: under *MIDI Ports*, enable **Track**
   (output) for the lamp port.
2. Add a **MIDI track**. Set its **MIDI To** → the lamp port, and pick the
   **channel** for the target you want to drive (channel = device/segment/group, per
   the [wled-midi convention](https://github.com/openlamp/wled-midi/blob/main/SPEC.md#2-channel--target-core)):
   e.g. Ch 1 → all, Ch 2 → front, Ch 3 → back … (defined in your engine routing).
3. One track per target. Multiple targets = multiple tracks, each on its channel.

## Drive the lamps

- **Looks / triggers** — play notes: 60–67 = the 8 colours, 68 = effect look;
  48/50/52 = off/on/toggle, 53/55 = blackout/restore, 56 = solid. Modifiers overlay
  the current look: 72 = beat toggle (pulse on the beat), 73 = flash. Put them in
  clips, one per song section.
- **Continuous control** — automate CC: CC 1 = brightness, CC 3 = hue, CC 4 = sat,
  CC 2 = white temp, CC 5/6/7/8 = effect / speed / intensity / palette. Draw
  automation envelopes so brightness/colour move with the song.
- **Presets** — Program Change *n* recalls WLED preset `n+1`.
- **On the beat** — the engine follows Live's tempo (MIDI clock / Ableton Link), so
  pulses land on the beat with a phase-accurate downbeat accent.

Full message map + value transforms: **[wled-midi SPEC.md](https://github.com/openlamp/wled-midi/blob/main/SPEC.md)**
(this repo does not duplicate it — that spec is the source of truth).

## Faster: drag the generated clips

Instead of drawing notes by hand, drop the ready-made clips from
[`../ableton/clips/`](../ableton/clips/) onto a lamp-routed track: `note60-red.mid`
fires red, `note53-blackout.mid` blacks out, etc. The track's channel still selects
the target. Regenerate them with `python3 tools/gen_clips.py`. A pre-routed `.als`
template is on the way — see [TASKS.md](../TASKS.md).

# Ableton setup — Mode A (MIDI pack)

Get lamps reacting to a Live set in a few minutes. This is **Mode A** (the base MIDI
API); Mode B (Control Surface) will have its own install doc when it ships — see
[DESIGN.md](DESIGN.md).

## Prerequisites

1. Lamps reachable on your LAN (WLED and/or Tuya), configured in the engine.
2. The bridge running — it opens the `LumiDeck` virtual MIDI port:
   ```
   pip install openlamp-midi
   lumideck-midi          # opens the "LumiDeck" virtual input port
   ```
   (The engine from [openlamp/engine](https://github.com/openlamp/engine) must be
   running too — the bridge calls its local API on `127.0.0.1:8377`.)

## Route Live to the lamps

1. **Live → Settings → Link/Tempo/MIDI**: under *MIDI Ports*, enable **Track**
   (output) for the **`LumiDeck`** port.
2. Add a **MIDI track**. Set its **MIDI To** → `LumiDeck`, and pick the **channel**
   for the lamp group you want to drive (channel = group, per the
   [MIDI convention](https://github.com/openlamp/midi/blob/main/MIDI-PROTOCOL.md)):
   - Ch 1 → `all`, Ch 2 → `front`, Ch 3 → `back`, Ch 4 → `L1`, Ch 5 → `L2`
     (whatever you defined in the engine's `tuya-lamps.json` + the bridge
     `mapping.json`).
3. One track per group. Multiple groups = multiple tracks, each on its channel.

## Drive the lamps

- **Colours / triggers** — play notes: 60–67 = the 8 stage colours, 48/50/52 =
  off/on/toggle, 53/55 = blackout/restore, 58/59 = flash/cycle. Put them in clips,
  one per song section.
- **Continuous control** — automate CC: CC 1 = brightness, CC 3 = hue, CC 4 = sat,
  CC 2 = white temp, CC 5/6/7 = WLED effect / speed / intensity. Draw automation
  envelopes so brightness/colour move with the song.
- **Scenes / presets / snapshots** — Program Change recalls them.
- **On the beat** — the bridge follows Live's tempo (MIDI clock / Ableton Link), so
  pulses land on the beat. See [openlamp/midi](https://github.com/openlamp/midi).

Full message map: **[MIDI-PROTOCOL.md](https://github.com/openlamp/midi/blob/main/MIDI-PROTOCOL.md)**
(this repo does not duplicate it — that file is the source of truth).

## Faster: drag the generated clips

Instead of drawing notes by hand, drop the ready-made clips from
[`../ableton/clips/`](../ableton/clips/) onto a `LumiDeck`-routed track:
`note60-jaune.mid` fires yellow, `note53-blackout.mid` blacks out, etc. The track's
channel still selects the group. Regenerate them with
`python3 tools/gen_clips.py`. A pre-routed `.als` template is on the way — see
[TASKS.md](../TASKS.md).

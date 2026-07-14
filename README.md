# openlamp-live — drive your lamps from Ableton Live

Turn a **track in Ableton Live** into a lamp/show controller: clips, macros and
automation envelopes drive your [OpenLamp](https://github.com/openlamp) smart LED
lamps (WLED + Tuya) **on the beat, in time with your set** — 100 % local, no cloud.

This repo is the **Ableton Live frontend** of the OpenLamp stack. It doesn't invent
a protocol: it speaks the open
**[wled-midi convention](https://github.com/openlamp/wled-midi)** (notes → colours,
CC → brightness/effects, Program Change → presets, MIDI clock / Ableton Link →
on-the-beat) and makes it turnkey inside Live.

Ableton is **one** way to drive the lamps. The same convention is also spoken by the
[Stream Deck plugin](https://github.com/openlamp/lumideck) and any hardware MIDI
controller — pick whichever surface fits the moment.

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
  *(Arm a MIDI track routed to the lamp port; Live captures your moves as automation.)*

- **🎛 Sculpt colour live from a MIDI controller.** Assign three knobs or faders to
  hue, saturation and brightness and *paint* the colour by hand — sweep the hue across
  the spectrum on a build, desaturate to white on the breakdown, dim on the outro — all
  in time with what you're playing. With an MPE controller (Push 3, Seaboard) you can go
  further and shape each lamp's colour per-note.
  *(CC 3 hue + CC 4 saturation + CC 1 brightness, continuous, per group; or the MPE profile.)*

- **🎚 Multi-zone staging.** Front lamps ride the beat while the back wash holds the
  section's ambiance — two independent behaviours at once.
  *(Channel-per-target: one Live track and channel per lamp / group.)*

- **👆 Whole-rig tempo, one tap.** Tap the tempo once and every Ableton Link app *and*
  the lamps follow — synths, drum machines and lights on the same clock.
  *(Ableton Link session tempo.)*

Everything is local: Ableton + lamps on your Wi-Fi, nothing in the cloud.

## How it works

```
Ableton Live  ──MIDI──▶  OpenLamp engine  ──HTTP/UDP──▶  lamps on the LAN
 (clips, macros,          (implements the                 (WLED / Tuya)
  automation)              wled-midi convention)
```

Live emits MIDI per the [wled-midi](https://github.com/openlamp/wled-midi) convention;
the engine translates it to WLED JSON state (and Tuya) and drives the devices.

> The MIDI→lamp translation runs in the engine's
> [`midi.py`](https://github.com/openlamp/engine/blob/main/midi.py) — the reference
> implementation of the [wled-midi](https://github.com/openlamp/wled-midi) convention —
> which opens the `OpenLamp` virtual MIDI port. (On-the-beat tempo-follow is the
> separate [openlamp-midi](https://github.com/openlamp/midi) package.)

## What this project delivers

- **An Ableton Live pack** — a MIDI track routed to the lamp port carries notes
  (colour/power triggers) and CC automation (brightness/hue/sat/CCT/fx). Shipped as
  **draggable `.mid` clips generated from the mapping** (open, reproducible format)
  plus a pre-routed demo `.als` template. Stock Live only, no private API.
- **A documented setup path** — [docs/ABLETON-SETUP.md](docs/ABLETON-SETUP.md).
- **A Control Surface (Max for Live / Remote Script)** — *on the roadmap (v2)*, so a
  script inside Live can reach the lamps **directly over the LAN** (no separate
  daemon) with feedback. See [docs/DESIGN.md](docs/DESIGN.md).

## Status

🚧 **Mode A in progress** — mapping pinned to the wled-midi v0.2 convention + 19
generated `.mid` clips (looks + util + modifiers) shipped; next is testing on real
lamps and authoring the `.als` template.
Mode B (Control Surface) is designed, not started. See [TASKS.md](TASKS.md).

## Requirements

- The OpenLamp engine running on the LAN, with its MIDI frontend
  ([`midi.py`](https://github.com/openlamp/engine/blob/main/midi.py)) open — it speaks
  the [wled-midi](https://github.com/openlamp/wled-midi) convention and opens the
  `OpenLamp` virtual MIDI port.
- Ableton Live 10+ (the pack uses only stock MIDI devices — no private API).

## License

[MIT](LICENSE) — like the rest of the OpenLamp galaxy: permissive, so anyone can adopt or
fork it freely. (The shared convention repo, [wled-midi](https://github.com/openlamp/wled-midi),
is MIT too.)

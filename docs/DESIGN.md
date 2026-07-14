# Design — how Ableton Live drives OpenLamp lamps

Decision record for `openlamp-live`.

## Goal

**With nothing but Ableton Live and some lamps on the local network, a user can set
up lamp automations from Ableton.** Minimal moving parts, 100 % local, no cloud.
The lamps (WLED + Tuya) live on the LAN; Live is where the show is programmed.

## Two integration modes — we ship both

The lamps speak HTTP/JSON/UDP on the network, not MIDI, so *something* must
translate "what Live plays" into lamp commands. There are two good places to put
that translation, and they serve different users. **We build both** — they are
complementary, not either/or.

### Mode A — base MIDI API  (the stable foundation)

Live emits standard MIDI on the
[`LumiDeck` virtual port](https://github.com/openlamp/midi/blob/main/MIDI-PROTOCOL.md);
the [openlamp-midi](https://github.com/openlamp/midi) bridge translates it to
OpenLamp State and the engine drives the lamps.

- **This convention already exists and is tested** — notes → colours/power/anim,
  CC → brightness/hue/sat/CCT + effect fx/sx/ix, Program Change → scenes/presets,
  one channel per lamp group.
- `openlamp-live` adds the **Ableton-native pack**: a MIDI Effect Rack (8 macros →
  the continuous CCs), one MIDI track per group, clip/scene templates, a demo
  `.als`. Everything is stock Live devices — **no private API**, works in any DAW,
  every param is clip-automatable.
- Cost to the user: run the bridge (`pip install openlamp-midi`), which opens the
  `LumiDeck` port. One small Python process alongside Live.

### Mode B — Control Surface (MIDI Remote Script)  (tighter + standalone)

A Python **Control Surface** that Live loads from Preferences → MIDI → *Control
Surface*. This mode earns its keep with two advantages the pack can't give:

1. **Direct-to-LAN, no separate daemon.** The Remote Script runs *inside* Live and
   can reach the WLED lamps **directly over the local network** (HTTP/UDP). That
   collapses the setup to exactly the goal above — **just Ableton + lamps on the
   LAN**, nothing else to launch. (It can still delegate to the engine when the
   engine is running, to stay in sync with the Stream Deck.)
2. **Bidirectional feedback** into Live's UI / the controller — lamp state, colours
   and levels reflected back, which a one-way pack can't do.

The trade-off is real and must be managed: Live's Remote Script API is
**semi-private and version-fragile** (it shifted across Live 11/12). So Mode B is
scoped against a pinned Live version and treated as the more brittle layer.

## Decision

**Build A first, then B.** A is the stable, DAW-agnostic base and unblocks the whole
feature immediately with zero fragile-API risk. B follows because it delivers a
distinct win — the **standalone "Ableton + lamps only" experience** and feedback —
that A structurally cannot. B does not replace A; a player can use either, and the
convention (A) is what B implements natively.

| Criterion | A — MIDI API + Live pack | B — Control Surface |
|---|---|---|
| Reaches lamps with **only Ableton + LAN** | No (needs the bridge process) | **Yes** (script talks to lamps directly) |
| Depends on Ableton's private API | No | Yes (version-fragile) |
| Clip automation of lamp params | **Native** | Native |
| Feedback into Live / controller | No | **Yes** |
| Works in other DAWs | **Yes** | Live-only |
| Maintenance cost | Low | Higher |
| Ships | **v1** | **v2** |

## How the pack (A) gets built

The Live-side mappings (rack macros → CC numbers, track → channel) are authored
**programmatically** with [als-wire](https://github.com/Beennnn/als-wire), which
wires plugin parameters to rack macros and MIDI mappings directly in `.als` files.
Config-as-code: the `.als`/`.adg` are build outputs of a versioned mapping spec,
not hand-clicked binaries that drift.

## Notes on B — evaluate Max for Live first

Before committing to a raw Remote Script, evaluate a **Max for Live device** for
Mode B: an M4L patch is far more stable than the Remote Script API, still loads
inside Live, and can hit the lamps' local API / network directly — potentially the
same "no separate daemon" win with much lower breakage. Decide M4L-vs-Remote-Script
when B starts; both satisfy the direct-to-LAN goal.

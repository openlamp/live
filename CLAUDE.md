# CLAUDE.md — openlamp-live

Ableton Live integration layer for the OpenLamp / LumiDeck lamp stack.

## What this repo is (and is NOT)

- **IS**: the Ableton-Live-native layer — a MIDI pack (Mode A) and, later, a Control
  Surface (Mode B) — that lets a user program lamp automations from Live with only
  Ableton + lamps on the LAN. See [docs/DESIGN.md](docs/DESIGN.md).
- **IS NOT**: a MIDI protocol. The wire convention lives in
  [openlamp/midi](https://github.com/openlamp/midi) (`MIDI-PROTOCOL.md`) and MUST NOT
  be duplicated here — reference it. This repo only makes that convention turnkey
  inside Live.

## Golden rules

- **Do not re-implement the bridge or the OLS contract.** Mode A rides the existing
  `LumiDeck` virtual port + engine local API (`127.0.0.1:8377`). Mode B may talk to
  lamps directly over the LAN, but reuse the OLS command vocabulary, don't fork it.
- **Ableton binary assets are build outputs**, generated from a versioned
  `mapping.spec.json` via [als-wire](https://github.com/Beennnn/als-wire) — never
  hand-clicked `.als`/`.adg` committed as opaque binaries that drift.
- **Mode B is version-fragile by nature** (Live's Remote Script API is semi-private).
  Pin a Live version, prefer Max for Live if it satisfies the direct-to-LAN goal.
- **Family conventions apply** (EUPL-1.2, one concern per repo, English public docs,
  Conventional Commits). New repos go to GitHub under the `openlamp` org.

## Stack

```
Live ──MIDI──▶ LumiDeck port ──▶ openlamp-midi ──HTTP──▶ engine ──▶ lamps   (Mode A)
Live (Remote Script / M4L) ─────────────HTTP/UDP────────────────▶ lamps     (Mode B, direct-to-LAN)
```

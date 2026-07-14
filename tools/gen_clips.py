#!/usr/bin/env python3
"""Generate draggable Ableton MIDI clips (.mid) from the wled-midi mapping spec.

Why .mid and not .als/.adg: a Standard MIDI File is an open, stable format we can
write byte-for-byte with the stdlib and that Live imports by drag-and-drop. The
.als/.adg formats are Ableton's undocumented, version-fragile binaries — we don't
synthesize those headless (see docs/DESIGN.md).

How the clips are used: drop a clip onto a MIDI track whose output is routed to the
`OpenLamp` port (see docs/ABLETON-SETUP.md). Each clip fires the mapped OpenLamp
action. The *track's* channel selects the lamp group (channel-per-group), so every
clip is written on channel 1 and inherits the track's routing.

  - Trigger clips (colours / power / animations) = a single note-on. RELIABLE: Live
    imports notes from .mid.
  - CC-sweep demo clips (brightness / hue) = a ramp of CC events. CAVEAT: Live's
    .mid import handles notes, not always clip automation/CC — treat these as a
    reference you may need to redraw as clip automation. Kept because they document
    the intended envelope shape.

Run:  python3 tools/gen_clips.py            # writes ableton/clips/*.mid
      python3 tools/gen_clips.py --verify   # write + parse back every file
"""
import json, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "ableton", "mapping.spec.json")
OUT = os.path.join(HERE, "..", "ableton", "clips")

PPQ = 96          # ticks per quarter note
BAR = PPQ * 4     # one 4/4 bar


def vlq(n):
    """MIDI variable-length quantity."""
    buf = n & 0x7F
    n >>= 7
    while n:
        buf <<= 8
        buf |= (n & 0x7F) | 0x80
        n >>= 7
    out = bytearray()
    while True:
        out.append(buf & 0xFF)
        if buf & 0x80:
            buf >>= 8
        else:
            break
    return bytes(out)


def smf(events):
    """events: list of (delta_ticks, status_bytes). Returns a type-0 SMF byte string."""
    track = bytearray()
    for delta, data in events:
        track += vlq(delta) + data
    track += vlq(0) + b"\xFF\x2F\x00"                       # end-of-track
    header = b"MThd" + struct.pack(">IHHH", 6, 0, 1, PPQ)   # format 0, 1 track
    return header + b"MTrk" + struct.pack(">I", len(track)) + bytes(track)


def trigger_clip(note):
    """One note-on at bar start, held one bar. Note-on is what the bridge acts on."""
    return smf([
        (0,   bytes([0x90, note, 100])),   # note on
        (BAR, bytes([0x80, note, 0])),     # note off one bar later
    ])


def cc_sweep_clip(cc, lo=0, hi=127, steps=16):
    """A CC ramp lo->hi across one bar (documents the envelope; see caveat above)."""
    ev, step = [], BAR // steps
    for i in range(steps + 1):
        val = round(lo + (hi - lo) * i / steps)
        ev.append((0 if i == 0 else step, bytes([0xB0, cc, val])))
    return smf(ev)


def slug(s):
    return "".join(c if c.isalnum() else "-" for c in s).strip("-").lower()


def main():
    verify = "--verify" in sys.argv
    spec = json.load(open(SPEC))
    os.makedirs(OUT, exist_ok=True)
    written = []

    # note-triggered clips: one per mapped action (colour / power / animation)
    for note_str, action in spec["notes"].items():
        name = f"note{note_str}-{slug(action)}.mid"
        open(os.path.join(OUT, name), "wb").write(trigger_clip(int(note_str)))
        written.append(name)

    # two CC-sweep demo clips (the load-bearing continuous params)
    for cc_num, lo, hi in [(1, 0, 127), (3, 0, 127)]:
        kind = spec["cc"][str(cc_num)]
        name = f"cc{cc_num}-{kind}-sweep.mid"
        open(os.path.join(OUT, name), "wb").write(cc_sweep_clip(cc_num, lo, hi))
        written.append(name)

    print(f"wrote {len(written)} clips to ableton/clips/")
    if verify:
        for name in written:
            data = open(os.path.join(OUT, name), "rb").read()
            assert data[:4] == b"MThd" and b"MTrk" in data and data[-3:] == b"\xFF\x2F\x00", name
        print(f"verified {len(written)} clips parse as valid SMF")


if __name__ == "__main__":
    main()

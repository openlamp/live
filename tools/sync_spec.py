#!/usr/bin/env python3
"""Derive ableton/mapping.spec.json from the openlamp-spec-midi spec.

Why this script exists: the pack used to keep a HAND-MAINTAINED copy of the note
and CC map, with a comment reading "Do not diverge; bump when wled-midi bumps".
It diverged anyway — the copy sat at spec_version 0.4.0 while SPEC.md moved to
0.6.3. A comment is not a mechanism. This script is the mechanism.

Why a generated copy rather than reading the spec directly (the two options):

  (a) drop the copy and read openlamp-spec-midi's mapping.spec.json at generation
      time (submodule or download). Rejected: the file is a USER-FACING asset of
      this pack — ableton/README.md lists it next to the clips, and a Live user
      opens it to see which note fires which look. It has to exist in the repo.
      A submodule would also pull a whole spec repo in for one 2 KB JSON.

  (b) keep the copy but make it GENERATED, derived from the spec, carrying the
      source version. Chosen. The copy stays browsable and offline, and drift
      becomes detectable (`--check`) instead of silent.

Shape note: the spec's notes are rich objects ({"zone", "name", "col", ...});
the pack only needs note -> label, because the label becomes a clip FILENAME
(note60-red.mid). So this flattens entry["name"]. The wire semantics stay in
SPEC.md — this pack never restates them.

Run:  python3 tools/sync_spec.py              # rewrite ableton/mapping.spec.json
      python3 tools/sync_spec.py --check      # exit 1 if the file has drifted
      python3 tools/sync_spec.py --from PATH  # a local spec checkout or a URL
"""
import json, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "ableton", "mapping.spec.json")

SPEC_REPO = "https://github.com/openlamp/openlamp-spec-midi"
SPEC_RAW = "https://raw.githubusercontent.com/openlamp/openlamp-spec-midi/main/mapping.spec.json"
# A sibling checkout is the common case on a maintainer's machine (both repos
# live side by side under ~/dev/music), and it works with no network.
SIBLING = os.path.abspath(os.path.join(ROOT, "..", "openlamp-spec-midi", "mapping.spec.json"))


def load_source(src):
    """Return (parsed_spec, human_readable_origin)."""
    if src and src.startswith(("http://", "https://")):
        with urllib.request.urlopen(src, timeout=20) as r:
            return json.loads(r.read().decode("utf-8")), src
    if src:
        path = src
        if os.path.isdir(path):
            path = os.path.join(path, "mapping.spec.json")
        return json.load(open(path)), path
    if os.path.exists(SIBLING):
        return json.load(open(SIBLING)), SIBLING
    with urllib.request.urlopen(SPEC_RAW, timeout=20) as r:
        return json.loads(r.read().decode("utf-8")), SPEC_RAW


def derive(spec):
    """Flatten the spec's note objects to the note -> label map the clips need."""
    notes = {}
    for num, entry in spec["notes"].items():
        if not isinstance(entry, dict) or "name" not in entry:
            sys.exit("unexpected note entry for %s: %r (spec shape changed)" % (num, entry))
        notes[num] = entry["name"]
    return {
        "_generated": (
            "GENERATED FILE — do not edit by hand. Regenerate with "
            "`python3 tools/sync_spec.py`; the source of truth is SPEC.md in "
            + SPEC_REPO + "."
        ),
        "_comment": (
            "Clip-naming mirror of the openlamp-spec-midi note/CC map. This pack "
            "only needs note numbers + human labels, because the label becomes a "
            "clip filename. The wire semantics and zone rules live in SPEC.md."
        ),
        "spec_ref": SPEC_REPO + "/blob/main/SPEC.md",
        "spec_version": spec["version"],
        "notes": notes,
        "cc": dict(spec["cc"]),
    }


def main():
    args = sys.argv[1:]
    check = "--check" in args
    src = None
    if "--from" in args:
        src = args[args.index("--from") + 1]

    spec, origin = load_source(src)
    text = json.dumps(derive(spec), indent=2, ensure_ascii=False) + "\n"

    if check:
        current = open(OUT).read() if os.path.exists(OUT) else ""
        if current != text:
            print("DRIFT — ableton/mapping.spec.json differs from %s" % origin)
            print("run: python3 tools/sync_spec.py")
            return 1
        print("in sync with spec %s (%s)" % (spec["version"], origin))
        return 0

    open(OUT, "w").write(text)
    print("wrote ableton/mapping.spec.json from spec %s (%s)" % (spec["version"], origin))
    return 0


if __name__ == "__main__":
    sys.exit(main())

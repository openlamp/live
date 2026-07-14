# TASKS — openlamp-live

Ableton Live frontend of the [wled-midi](https://github.com/openlamp/wled-midi) convention.
**État : Mode A (MIDI pack) = fondation livrée mais jamais validée sur matériel ; Mode B
(Control Surface) = designé, pas commencé.**

## Mode A — MIDI pack (v1, foundation)

- ✅ `ableton/mapping.spec.json` — miroir pinné de la map wled-midi **v0.3.0** (note map inchangée depuis v0.2)
- ✅ `tools/gen_clips.py` + `ableton/clips/*.mid` — 19 clips draggables (looks/util/modifiers) générés & vérifiés SMF
- ☐ **[BLOQUÉ — rig offline]** Tester les 19 clips contre le moteur sur vraies lampes → confirmer que chaque note déclenche la bonne action/cible. Blocage : lampes injoignables (Mac pas sur BEN-MUSIC, `L1`/`L2` = `connected:false` sur `:8377`). Se débloque au rallumage du rig → débloque aussi les tests MPE + beat-rate côté wled-midi.
- ☐ Confirmer l'import des clips CC-sweep (`cc1-bri`, `cc3-hue`) dans Live → si Live ne porte pas le CC en automation, documenter le « redraw as clip automation » ou livrer un `.alc`
- ☐ Authorer `ableton/OpenLamp-demo.als` → 1 piste MIDI/cible pré-routée au port `OpenLamp` sur son canal, clips posés → set démo turnkey. **Faisable à froid** (Ableton Live seul, sans lampes) via computer-use.
- ☐ Ajouter au README parapluie OpenLamp une fois le pack validé end-to-end sur vraies lampes

## Mode B — Control Surface (v2, standalone + feedback)

- 🤔 **Trancher Max for Live vs Remote Script brut** → DESIGN.md penche M4L (bien moins fragile aux versions de Live). À décider avant d'écrire du code. **C'est la principale alternative de travail à froid au demo `.als`.**
- ☐ Prototyper le contrôle direct-to-LAN depuis Live (script/M4L tape WLED en HTTP/UDP direct) → prouve l'objectif « juste Ableton + lampes, zéro daemon »
- ☐ Ajouter le feedback bidirectionnel (état lampe → Live/contrôleur) → la seule chose que Mode A ne peut structurellement pas faire
- ☐ Pinner une version cible de Live + documenter l'install → contenir la fragilité de l'API semi-privée

## Cross-cutting

- ☐ Soumettre le projet au programme Link/products d'Ableton une fois un mode utilisable (lié à l'outreach link-devs@ableton.com)

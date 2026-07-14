# TASKS — openlamp-live

Ableton Live frontend of the [wled-midi](https://github.com/openlamp/wled-midi) convention.
**Principe : accessible à tous d'abord, intégré au mieux ensuite** (détail + argumentaire
dans [docs/DESIGN.md](docs/DESIGN.md)). État : Mode A = fondation livrée, **non validée sur
matériel** ; Mode B = **décidé (Max for Live)**, pas commencé.

## Tier 1 — accessible à tous (Mode A turnkey, tout DAW / toute édition)

- ✅ `ableton/mapping.spec.json` (miroir pinné wled-midi **v0.3.0**) + 19 clips `.mid` générés & vérifiés SMF
- ☐ **[BLOQUÉ — rig offline]** Tester les 19 clips contre le moteur sur vraies lampes → confirmer que chaque note déclenche la bonne action/cible. Blocage : lampes injoignables (Mac pas sur BEN-MUSIC, `L1`/`L2` = `connected:false` sur `:8377`). Se débloque au rallumage → débloque aussi les tests MPE + beat-rate côté wled-midi.
- ☐ Confirmer l'import des clips CC-sweep (`cc1-bri`, `cc3-hue`) dans Live → si Live ne porte pas le CC en automation, documenter le « redraw as clip automation » ou livrer un `.alc`
- ☐ Authorer `ableton/OpenLamp-demo.als` → 1 piste MIDI/cible pré-routée au port `OpenLamp`, clips posés → set démo turnkey. **Faisable à froid** (Ableton seul, sans lampes) via computer-use.
- ☐ **[repo engine]** Packager le moteur en **appli no-install** (`.app`/`.exe`, barre de menu, signée, headless) → enlève la seule barrière du chemin universel (« lancer un process Python »). Suivi dans [openlamp/engine](https://github.com/openlamp/engine).
- ☐ **Feedback value-level + echo hardware sans M4L** : une fois le port de retour `OpenLamp Feedback` émis par le moteur (voir engine/TASKS), documenter le mapping dans Live (MIDI-map des CC entrants → contrôles) **+ activer « Remote » Out** sur le port du contrôleur → un fader/LED suit la brillance réelle, un bouton reflète on/off, **y compris sur fader motorisé** (Live ré-émet la valeur, stock). Garde-fous : CC/port de retour distincts des contrôles joués (anti-boucle) ; feedback structuré (pads RGB/écran) reste Tier 2. Le rendu riche visuel (couleur/nom d'effet dans l'UI) reste Tier 2 (M4L).
- ☐ Ajouter au README parapluie OpenLamp une fois le pack validé end-to-end

## Tier 2 — intégré au mieux (Mode B = Max for Live, décidé)

Décision : **Max for Live**, pas Remote Script (API stable + UI de device + Node for Max ; Suite-only acceptable car le Tier 1 couvre déjà tout le monde — argumentaire dans DESIGN.md).

- ☐ Prototyper le device M4L **direct-to-LAN** : tape WLED en **HTTP** (`/json/state`) ou **UDP temps réel** (DDP/WARLS, port 21324) → « juste Ableton + lampes, zéro daemon ». Option : déléguer au moteur `:8377` s'il tourne (rester en phase avec le Stream Deck).
- ☐ **Feedback bidirectionnel** : s'abonner au WebSocket WLED (`ws://<lampe>/ws`) → refléter l'état réel dans l'UI du device (couleur/brillance/effet). La seule chose que Mode A ne peut structurellement pas faire.
- ☐ Pinner une version cible de Live + documenter l'install

## Cross-cutting

- ☐ Soumettre le projet au programme Link/products d'Ableton une fois un mode utilisable (lié à l'outreach link-devs@ableton.com)

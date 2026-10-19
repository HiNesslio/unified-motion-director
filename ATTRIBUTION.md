# Sources, attribution, and derivative boundary

This package is an original coordination skill and does **not** bundle third-party project source, prompt corpora, example videos, copyrighted screenshots, fonts or music.

Research basis:

1. **Claude Motion Playbook** — Haoyang Pang / PHY041, https://github.com/PHY041/claude-motion-playbook . Attribution: analyzed 233 gallery videos (snapshot 2026-10-09), catalogued 137 motion techniques and documented structured prompt patterns. Writing/docs and classification fields: Creative Commons Attribution 4.0 (CC BY 4.0), https://creativecommons.org/licenses/by/4.0/ . Playbook `templates/`: CC0. Adapted concepts in our guidance are attributed here; this package does not copy original large text passages or the techniques table.
2. **Claude Motion Director** — abdullatif06, https://github.com/abdullatif06/claude-motion-director , MIT, authors retain their own copyrights. Its HyperFrames-oriented pipeline inspired the optional production-backend design.
3. **Motion Composer Skill** — designbysuren, https://github.com/designbysuren/motion-composer-skill , MIT, used as an optional architecture reference.
4. **Prompt Motion** — https://prompt-motion.com . The catalogue is independently curated; original creator videos/prompts belong to their respective owners. No affiliation implied.
5. **Skillry Opus 5.5** — https://skillry.dev/ai-videos/opus-5-5 . Public gallery of creators' originals and remakes plus published prompts. Source clips/prompts and derived media are not included here.
6. **Claude Motion Skill** — Hype-yolo, https://github.com/Hype-yolo/claude-motion-skill , current reviewed README v0.4.0-beta.1, original project tools MIT; source-assisted scene creation and its source-licensing discipline informed `references/source-assisted-production.md`. Its imported cases, characters, fonts, GLB models, Remotion-related dependencies, third-party assets and submodules have **separate licenses** listed by that project; no copied upstream code or media is included.
7. **Agent Skills** — https://agentskills.io/specification . Packaging follows the public SKILL.md convention.

If you download source code from upstream via `scripts/source_manager.py`, that source retains the applicable license in its own repository; license compliance remains required. This package does not authorize reuse of individual creators' third-party motion clips, sound recordings or proprietary UI.

The phrase "Opus 5.5 aesthetic" means inferred, public, observable *design patterns* and independently written production guidance. It does not mean access to Anthropic's proprietary model weights, hidden reasoning, or internal private prompts.

## License for original contents of this package

MIT License. Copyright (c) 2026 Unified Motion Director contributors. See `LICENSE`.

## Added in v1.5

- **Howseen AI / Raphaël Aubry**, `claude-motion-design`: https://github.com/howseen-ai/claude-motion-design — MIT code, copyright (c) 2026 Howseen AI (Raphaël Aubry). The design process, deterministic time-seeking film, subframe blur, pop scan and music/SFX alignment informed `references/howseen-seek-production.md`. Upstream source is not embedded. External photos, marks, music, SFX and fonts use separate licenses.
- **whaleyxbt**, `claude-motion`: https://github.com/whaleyxbt/claude-motion — MIT code, copyright (c) 2026 whaleyxbt. Remotion scene timing, deterministic simulation, beat-based contact sheets, procedural sound and taste defaults informed `references/whaley-motion-toolkit.md`. Upstream source is not embedded. Remotion licensing must be checked for the user's organization and use.

The code in this ZIP is newly written integration and test scaffolding; it does **not** contain vendor runtime copies or downloaded media. Reference behaviour described after reading public documentation/code, not after executing upstream examples.

## Studied in v1.8 — principles only, without relicensing upstream code

- **OneTake / Patrick**, https://github.com/feitangyuan/onetake — **PolyForm Noncommercial 1.0.0**. Its public documentation on visual carry, intentional rests, camera follow/anticipation and reference/rhythm deconstruction informed *independently authored editorial guidance only*. No upstream source code, algorithmic thresholds, movie clips, compositions or assets are redistributed. The original licence remains applicable to any separately obtained OneTake copy.
- **huashu-motion / Huashu**, https://github.com/alchaincyf/huashu-motion — project core MIT; bundled vendors, fonts and audio samples have their own licensing terms. Its documented approach to score-first music, visual hits, rests and named picture-to-audio cue alignment informed independent v1.8 workflow guidance. UMD does **not** copy its music engine, score sources, sample library or CLI.

**This UMD repository remains MIT**, including the new original v1.8 writing, schemas, validation and scripts. Public inspiration, code inclusion and upstream installation are deliberately different operations.

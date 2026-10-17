# Product Story Intelligence — explain the mechanism, not the decoration

## Scope

Use for genuine product features, SaaS interfaces, dashboards, data or algorithmic products. This is a reasoning guide, not a visual preset. A generic brand film without product claims may omit this stage.

## Product-to-film mapping

1. **Inspect product evidence**: actual UI, documentation, feature flags, public release notes and user-approved descriptions. Record version/date and where the evidence was obtained.
2. **Identify the user-facing outcome**: say what changed for the user, not which technologies exist.
3. **Build a causal chain**: source → transformation → intermediate state → user result. Draw arrows in `BRIEF.md`; remove intermediate states that do not advance comprehension.
4. **Choose a visible encoding** for each important state: position → location, length → progress, hue → state/class, count → number, continuity carrier → causation. Keep encodings stable.
5. **Translate into a scene**: one question answered per scene, one main focal element. Do not mistake visual flourish for proof.
6. **Finish in a verifiable product surface**: reconnect the abstract explanation to an authentic approved UI frame, or label a conceptual simulation clearly.
7. **Read the film muted**: someone unfamiliar with the product should understand what it offers, what was shown, and what is simulated.

## Mandatory truth boundaries

- Maintain `claims.json` using `templates/product-claims.schema.json`; refer to entries by stable `claim_refs` in storyboard scenes.
- Separate **implementation status** (shipped / beta / experimental / planned / retired) from **data status** (verified / illustrative / unknown).
- Planned or experimental mechanics can only be presented as visibly disclosed concepts. No implication that they have shipped.
- If the film uses numeric product-specific results, trace each result to dated source evidence or mark it as illustrative *on screen*.
- Public-facing factual claims must satisfy Product Truth Gate before render and again before release; the gate is independent of the creative jurors.
- `product_truth.py` validates records and consistency, **not** whether a website, document or screenshot actually proves the claim. Producer approval and genuine evidence review remain necessary.

## Feature → story worksheet

| Field | Required interpretation |
| --- | --- |
| User need | What user problem the feature solves |
| Mechanism | Actual relationship of inputs, actions, result |
| Observed evidence | File/URL and date, with availability |
| Product state | shipped / beta / experimental / planned / retired |
| Shot purpose | What one idea becomes clearer |
| Visual variable | Position, length, time, colour, shape or number |
| UI re-entry | Which approved screen matches the abstract output |
| Disclosure | How illustrative data and non-shipped features remain visible |

## Scene economy check

For each scene ask: “Could this shot be removed without reducing understanding or the emotional arc?” If yes, merge or delete. Prefer a continuous transformation of one recognizable item to unrelated spectacle. Never use user-personal information or proprietary screenshots without authorization.

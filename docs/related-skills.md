# Related writing skills

Reviewed September 6, 2026 at the commits linked below. These sources suggest editing procedures; none supplies a verified result showing that the additions here lower GPTZero scores.

| Source | Useful principle | Limit of the evidence |
| --- | --- | --- |
| [Skillproofdev/text-humanizer](https://github.com/Skillproofdev/text-humanizer/blob/14ceeb7b2a4923b95d170cb70752445cab67a100/SKILL.md) | Reconstruct from a claim inventory, then compare the finished answer with that inventory, including claim strength and scope. | Its [reported 8–4 preference](https://github.com/Skillproofdev/text-humanizer/blob/14ceeb7b2a4923b95d170cb70752445cab67a100/README.md) used an in-context LLM from the rewriter's model family. External detector runs were pending. |
| [obra/the-elements-of-style](https://github.com/obra/the-elements-of-style/blob/05fc4f0d2b97b7c042dd9949ad658568e4a1324e/skills/writing-clearly-and-concisely/SKILL.md) | Name the actor and keep related words together so placement expresses the intended relationship. | Composition guidance, with no detector comparison. The public-domain status of the referenced 1918 text does not establish a license for the modern wrapper. |
| [smyrick/skills: humanize-text](https://github.com/smyrick/skills/blob/dafb0003f27aba9ea9961d49c800180a5aa4c486/skills/humanize-text/SKILL.md) | Protect exact technical spans and reconcile omissions, additions, and altered meaning at the end. | Pattern claims are not a reproducible GPTZero benchmark. Technical correction remains allowed in our workflow when supported by evidence. |
| [blader/humanizer](https://github.com/blader/humanizer/blob/e2e92e7b4b8229253ed5c8e81dc65463fdeddda5/SKILL.md) | Use stable component names, explicit actors, and real reader concerns. Check facts after rewriting. | Its patterns are editing heuristics. Isolated punctuation or ordinary words do not establish authorship. |

The revised skill adds two concrete steps. First, arrange actions, prerequisites, and exceptions by their dependencies, placing each limit beside the claim it qualifies. Second, require a final writer comparison against the claim inventory and protected spans, even when a separate reviewer will follow.

These additions use independently written instructions about general editing practices. No upstream skill body, examples, or pattern catalogue was copied. Blanket punctuation bans, compulsory personality, numerical sentence-rhythm targets, and repeated score-seeking rewrites were excluded. The prospective comparison holds code, sources, and material claims fixed and tests plain prose without added quotations.

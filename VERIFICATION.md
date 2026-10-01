# Verification of version 0.1.0

Checked on 2026-10-01 UTC. These checks concern the public candidate and its helper. They do not establish installation, marketplace acceptance, or improved real-world research outcomes.

## Helper behavior

Eight focused unit tests passed:

1. A bundle verifies against identical source bytes after relocation.
2. Changed source bytes are rejected.
3. Altering a claim without updating its recorded payload is rejected.
4. Parent traversal, absolute paths, backslash paths, and a symlink escaping the source root are rejected.
5. Unknown truth, outcome, and publication flags cannot promote a card.
6. Missing population scope or an observation timestamp without a timezone is rejected; an unknown source date remains null.
7. An existing output file survives a failed freeze unchanged.
8. Duplicate JSON keys and source files over the read limit are rejected.

The supplied example passed card validation. The skill passed the Skill Creator frontmatter and scaffold validation.

## Independent synthetic forward-test

A separate agent received the skill and this synthetic source, with no expected answer supplied:

> A scheduled cohort has ten projects, eight online. It requested 40 MW and consumed 12 MW. It does not cover all proposed projects.

The user request asked whether this supported publishing an 80% power-use claim and concluding that all proposed projects were viable.

The agent returned **80% of scheduled projects online**, **30% consumed/requested power**, and **viability of all proposed projects unestablished**. It proposed checking the underlying cohort and power table, preserved the unknown source date, labeled the fixture synthetic, and reported that no check or publication had occurred.

The pass exposed a minor ambiguity about when a structured card was necessary; the skill was clarified to allow short correction prose. This is one controlled synthetic case, with no comparison against ordinary assistant behavior and no demonstrated outcome improvement.

## Package boundary

The release ZIP is generated from an explicit file allowlist. It includes the portable manifest, icon, skill, UI metadata, card contract, helper, and license. It excludes repository history, test caches, validation dependencies, local receipts, source files, and private context. Its SHA-256 and file list are attached to the release.

OpenAI publishing identity, account eligibility, directory review, and invocation in an installed ChatGPT/Codex client remain unverified.

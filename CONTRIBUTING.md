# Contribute to Gorptastic

Useful contributions improve a checkable result:

- A sourced correction to a claim, including its population, metric, unit, and period.
- A counterexample or failed reproduction, with enough public material to repeat the check.
- A cheaper experiment that distinguishes a claim from a plausible rival explanation.
- A fixture that exposes a real error in the evidence-card helper or skill behavior.

Use the evidence-card contract in `plugins/gorptastic/skills/evidence-to-experiment/references/evidence-card.md` when a reusable record helps. Short corrections can be an issue containing the claim, source locator, what the source supports, unresolved limits, and the next check.

Issues, pull requests, and their attachments are public. Submit only material you have the right to share. Remove secrets, private prompts, account data, personal information, private system paths, and third-party private material. A local hash does not give permission to upload the file it describes.

Mark synthetic examples as synthetic. Distinguish observed results from proposed experiments and source-reported results from independently reproduced results. Keep negative findings and scope limits visible.

For code changes, run `python3 -m unittest discover -s tests -v`. Explain the behavior changed and supply the smallest meaningful failing case. Python helper changes should preserve its no-network design, bounded reads, source-root boundary, and separation of byte integrity from factual support.

Maintainers review contributions before changing the plugin release. An issue's existence does not establish acceptance or publication in the plugin. By submitting a code or documentation contribution, you agree to make that contribution available under this repository's MIT license.

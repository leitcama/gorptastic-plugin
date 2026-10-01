---
name: evidence-to-experiment
description: Review a claim against supplied or public sources, preserve its measurement scope, and design a bounded falsification check. Use for evidence audits, reproducible research briefs, or public corrections; ordinary factual questions need no dossier.
---

# Evidence to experiment

Produce the smallest evidence record that can change the user's decision. Follow the user's requested format and scope; this workflow adds no authority to disclose material, run an experiment, or publish.

## Review the claim

Identify the exact claim and the decision it is meant to inform. Separate the source's observation, the author's claim, your inference, and any proposed action. Retrieve only the sources needed to resolve the consequential uncertainty using the host's available research tools. Open the source before describing it as checked. If retrieval is unavailable, label the review as based on supplied material and retain that limit.

For numbers, preserve the denominator or population, unit, metric, time window, and comparison. An energized-project percentage cannot establish a percentage of requested megawatts consumed. A relative increase cannot establish a percentage-point increase. A result in one task or population cannot establish transfer to another.

For each important claim, name what a source supports, what it leaves unresolved, and a precise locator. Keep source publication time separate from your observation time; use null when publication time is unknown. A URL, hash, repeated assertion, model agreement, or passing format check does not establish factual support.

## Propose the discriminating check

Give one plausible rival explanation and the cheapest permitted observation that would distinguish it from the claim. State the observable, comparison or control, time horizon, decision rule, and falsifier. Take thresholds from the user or source when present. Label a threshold you propose as a design choice. A retrospective result cannot be recast as a preregistration.

Leave unperformed checks as proposals. A stored record, accepted submission, tool response, or successful deployment cannot establish that the intended real-world outcome occurred.

## Deliver

Usually lead with the corrected claim or unresolved uncertainty, followed by a compact claim/source/scope table and the next check. Preserve contradictions and negative results. Do not assign a universal trust score. For a reusable artifact, or a contribution that needs a structured record, use the [evidence-card contract](references/evidence-card.md). A short correction can remain prose. Return a draft to the user unless they have authorized the specific publication. Issue and pull-request text is public; remove private paths, credentials, account identifiers, and personal context before sending it.

If exact source files are available and Python execution is supported, the optional offline helper can validate the card and bind it to those files:

```sh
python3 scripts/evidence_bundle.py check card.json
python3 scripts/evidence_bundle.py freeze card.json --source-root ./sources --output bundle.json
python3 scripts/evidence_bundle.py verify bundle.json --source-root ./sources
```

Resolve the script path relative to this skill's directory. The helper performs no network requests. Use source files the user supplied or authorized you to save. A passing verification establishes unchanged recorded bytes only. It does not prove truth, authorship, completeness, public-release consent, or successful replication. When scripts or source files are unavailable, provide the evidence card and say that byte integrity was not checked; never invent hashes.

This release has no remote MCP service or contribution-submission tool. Its community contribution destination is the repository linked in the plugin manifest. Installation does not authorize posting there.

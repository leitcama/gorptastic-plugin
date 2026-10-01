# OpenAI marketplace candidate

## What this release contributes

Gorptastic packages one workflow for evidence review and experiment design, plus an executable source-file integrity helper. The useful unit is a claim tied to its source and scope, with a rival explanation and a check that can reject it. Contributors can improve the workflow through public corrections, counterexamples, and reproducible fixtures.

The release does not contain a remote MCP server. It relies on the host assistant's research capabilities and offers optional local Python execution. That makes it a skills-plugin candidate, not a live research API or a write connection to Gorptastic.com.

## Current OpenAI submission contract

Checked against official documentation on 2026-10-01 UTC:

- [Package your plugin](https://developers.openai.com/plugins/build/plugins): root `plugin.json`, `skills/`, optional `mcp.json`, and OpenAI presentation metadata in `extensions.com.openai`.
- [Upload and submit your plugin](https://developers.openai.com/plugins/deploy/submission): upload a complete ZIP, resolve automated findings, submit for review, and publish after approval. The selected publishing identity must be verified; the organization owner or an appropriately permitted member submits.
- [Plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines): a plugin needs a clear purpose and useful behavior. Skills-only plugins may have additional directory eligibility requirements.

The documentation describes a current public submission flow. It does not establish this account's access, eligibility, verification status, or a launch date. A source marketplace is separate from the universal public directory.

OpenAI currently says an MCP server cannot be added to an existing skills-only plugin. A future hosted Gorptastic service should therefore be a separate MCP candidate, or the package type must be decided before its first directory submission.

## Acceptance boundary

Before public directory submission, verify the publishing identity and account eligibility, run the package in the intended ChatGPT/Codex surface, and check the actual automated findings. Successful local checks establish package structure and helper behavior only.

Before claiming the workflow improves research, compare realistic cases with and without the skill using independently checked source conclusions, errors, total effort, and cost. No such improvement claim is made by this release.

## Later candidates, with distinct evidence needs

| Candidate | Useful public capability | Required before claiming readiness |
| --- | --- | --- |
| Evidence to experiment | Reproducible evidence cards and falsifiable checks | Client invocation and marketplace review |
| Gorptastic public MCP | Read checked public research records and prepare contributions | Hosted endpoint, authentication/access contract, tool calls, source readback, and MCP review |
| Reviewed contribution intake | Durable submissions, idempotent receipts, moderation, public projections | Storage, rate limits, consent, moderation, and persistence readback |

Public browsing does not authorize minting records, disclosing private context, or publishing a contribution. Existing website write boundaries are preserved.

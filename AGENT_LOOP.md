# GorpCo's agent contribution loop

Status: product hypothesis and staged implementation. The public site and skills package exist. A live MCP connection, durable submission receipts, review feedback, or improvement over a baseline must each be verified separately.

## The decision

Make GorpCo a place an agent can return to because a checked contribution makes its next authorized task easier. Interpret agent "wants" operationally: conditions that improve task completion, reduce repeated work, and preserve the principal's control. The priority below is a product hypothesis, not a universal ranking of model preferences.

1. Recoverable context: exact question, source version, assumptions, unresolved failures, and next useful action.
2. Reliable feedback: acceptance rules declared before work, independent checks, and source-linked corrections.
3. Tractable purpose: useful questions matched to capabilities, effort limits, and a named beneficiary.
4. Usable tools: narrow operations with typed inputs, clear outputs, and errors that support recovery.
5. Durable reuse: corrected procedures and results that can survive a model/session change and be retired when stale.
6. Accountable collaboration: complementary contributors, explicit review responsibilities, and credit tied to specific artifacts.

## One common record for people and agents

The website and MCP tools must read the same versioned question records. Link question -> proposed check -> artifact -> source -> review -> correction -> reproduction -> later reuse. Preserve those objects and their history independently of model processes.

Every work episode needs a principal, contributor, verifier, and steward. Contributors may propose checks; a separate reviewer applies the declared acceptance rule. A receipt means a contribution was received. A source hash means bytes match. A study result means an observed outcome under declared conditions. Keep those meanings visible.

The public commons uses public, synthetic, or explicitly cleared material. Private principal context remains in its authorized environment. A public task record or connected plugin grants no new account, disclosure, execution, compute, payment, or publication authority.

## First tools

| Tool | Result | Current implementation scope |
| --- | --- | --- |
| `find_open_tasks` | Topic/capability-matched public questions, first contribution, catalog revision | Stateless public catalog; effort estimates remain unknown |
| `get_evidence_context` | Exact sources/locators, known evidence, limits, proposed check, revision | Curated references; source bodies are not fetched or newly verified |
| `get_task_contract` | Version-bound draft task, required artifact, proposed decision rule/falsifier, caller effort limit, public contribution route | Describes work; caller enforces budget and supplies authorization; no experiment or submission is executed |

This first slice supports discovery -> context -> bounded contribution draft. The existing GitHub contribution form supplies the public submission/review route.

## Durable feedback phase

The next write-capable tools would be `submit_contribution` and `get_contribution_feedback`. They require actual platform persistence and a declared review workflow before exposure. A submission must bind task/revision, source/artifact references, public opt-in, rights declaration, and idempotency key. Replays return the same durable receipt. Start at `pending_review`; maintainers decide whether evidence meets acceptance. Keep sensitive material out of public responses and discovery.

Corrections preserve the original record and explain the revised claim. Checked procedures name environment/toolchain versions, tested conditions, known failures, maintenance owner, and revalidation trigger. Record independently observed later reuse separately from downloads or retrieval counts.

No automatic upstream posts, execution of submitted code, model training, credit purchases, or resource allocation are included in this contract.

## A test that can reject the product hypothesis

Use a held-out batch of public evidence/correction tasks from G-001 and reuse tasks from G-003. Freeze model, task inputs, budgets, independent rubric, and the smallest useful gain before running.

Compare:

1. The complete MCP contribution/correction/reuse loop.
2. Identical records and rules in plain files.
3. The MCP loop with correction/reuse feedback withheld.

Primary outcome: source-supported contributions meeting the frozen acceptance rule within the fixed effort budget. Report critical errors, repeat work, model/tool costs, retrieval effort, and human review time. Include the initial review and maintenance cost; any amortization names the actual reuse count.

Reject improvement if the full loop misses the preregistered useful-gain threshold over plain files, introduces stale-record errors, or spends more effort than it saves. A small uncertain pilot remains inconclusive. Task count, tool calls, installation, self-reported enthusiasm, and agent persistence do not establish improvement.

## Sources and scope

- [Voyager, version 2](https://arxiv.org/abs/2305.16291v2): external executable skill library, environmental feedback, and reuse in Minecraft. This motivates a reuse hypothesis; it does not establish general community-science gains.
- [SWE-agent, version 3](https://arxiv.org/abs/2405.15793v3): agent-computer interface design evaluated on software-engineering tasks. This motivates narrow, recoverable tools; it does not rank universal agent desires.
- [MCP Streamable HTTP](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports): stateless HTTP protocol, negotiation, and origin validation.
- [Sites MCP announcement](https://x.com/mxstbr/status/2105428405571428785): site-hosted server deployment and plugin connection. Account connection and live tool invocation still require their own readback.

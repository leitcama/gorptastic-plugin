# GorpCo publication receipt

Observed 2026-10-01 UTC. This records the publication boundary separately from client connection and scientific outcomes.

## Published site

- Community science: <https://gorptastic.com/science/>
- Release manifest: <https://gorptastic.com/.well-known/gorptastic-release.json>
- Public question records: <https://gorptastic.com/science/questions.json>
- Sites version: **57**, deployment status **succeeded**, `has_mcp: true`, runtime environment revision **7**.
- Native source commit: `e50c7422db5b0e78aa4c1bd3f807b68797d88135`.
- Provider-stored deployment archive SHA-256: `29ece8902b4255b556961c97536e1358f4f501f7b80151524c764ecfa70d00ee`.
- Locally submitted archive SHA-256: `102c67b2379925278d84e2e84811bb7d49962b5e1d0077dd4f2d72f925ecd829`. The provider's stored archive is a different representation; these hashes identify different byte sequences.
- Question-file SHA-256: `dd949b494d7bb32611d78595be20cace80a2070114c5a0ccbc67921a73f61f28`. Live HTTP readback matches the exact catalog bytes embedded in the MCP adapter.

The published HTML rendered in a browser. The research-area filter selected one formal-proof question and returned to all four questions. The release manifest returned HTTP 200 with the native source commit and provider-stored archive digest above. Its `deployedAt` identifies the release metadata timestamp; the deployment service reported success at `2026-10-01T05:26:02.860699+00:00`.

## MCP connection boundary

Sites returned this exact endpoint and OAuth resource:

<https://uai-field.gorptastic.chatgpt.site/mcp>

Unauthenticated initialization and tool-discovery requests returned **HTTP 401**. No authentication protection was changed. Sites did not return a saved plugin ID, and plugin search for GorpCo returned no entry at this observation. Therefore no installation offer or authenticated client invocation is claimed. The Sites plugin should be connected through ChatGPT's **Plugins → Personal → Created by you** flow when its provisioned entry is available; the missing entry requires a provider-side connection check.

The deployed source implements `find_open_tasks`, `get_evidence_context`, and `get_task_contract`. Three local Node test groups passed, including protocol negotiation, task/revision validation, malformed-request handling, and the distinction between empirical studies and proof tasks. Those checks establish source behavior under the tested conditions, not an authenticated production tool call.

The tools return public catalog records and draft contribution requirements. Sources are curated references, not freshly fetched source bodies. Experiments, durable submission receipts, review feedback, independently observed reuse, and improvement over a plain-file baseline remain separate work. Public contribution issues and pull requests are available through GitHub.

This publication is not an OpenAI directory submission, approval, or listing. The [version 0.1.0 ZIP](https://github.com/leitcama/gorptastic-plugin/releases/tag/v0.1.0) remains the original offline skills package.

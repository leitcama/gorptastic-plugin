# Gorptastic

**Community science, one checkable contribution at a time.** A public problem directory and plugin candidate for ChatGPT and Codex, with an offline helper and an open contribution path.

[Explore the community science site](https://leitcama.github.io/gorptastic-plugin/). Its first four questions cover evidence errors, learning after AI assistance, reusable discoveries, and faithful formalization. Each has sources, a first useful task, a proposed comparison, and a falsifier. These are proposed studies, with no general resolution or community replication claimed.

Give it a claim and its sources. It helps preserve the claim's scope, identify what the evidence actually supports, and design a small test that could show the claim is wrong. When source files are available, its helper records their hashes so another person can check whether they are looking at the same bytes.

## Try the workflow

> Check this claim against its sources and show the smallest test that could disprove it.

> Turn this research question into an evidence card and a bounded experiment.

The package contains one focused skill: [evidence-to-experiment](plugins/gorptastic/skills/evidence-to-experiment/SKILL.md). It uses the assistant's available research tools. Python 3.10 or later is needed only for the optional source-file helper; there are no Python dependencies.

## Install from the source marketplace

```sh
codex plugin marketplace add leitcama/gorptastic-plugin
```

Use the ChatGPT desktop plugin directory to select the Gorptastic source, install the plugin, and test it in a new Work chat. Marketplace registration alone does not establish installation or successful invocation. Availability depends on the client and account. Do not restart an application without preserving the user's session requirements.

The repository catalog is [.agents/plugins/marketplace.json](.agents/plugins/marketplace.json). The portable plugin root is [plugins/gorptastic](plugins/gorptastic). Download the plugin ZIP from [Releases](https://github.com/leitcama/gorptastic-plugin/releases) for upload or inspection.

## Verify the offline helper

```sh
python3 -m unittest discover -s tests -v
python3 plugins/gorptastic/skills/evidence-to-experiment/scripts/evidence_bundle.py check examples/card.json
python3 plugins/gorptastic/skills/evidence-to-experiment/scripts/evidence_bundle.py freeze examples/card.json --source-root examples/sources --output /tmp/gorptastic-example-bundle.json
python3 plugins/gorptastic/skills/evidence-to-experiment/scripts/evidence_bundle.py verify /tmp/gorptastic-example-bundle.json --source-root examples/sources
```

The example is synthetic. A successful byte check establishes unchanged files; it does not establish factual truth, authorship, public-release consent, or an experiment's outcome. The output path must be new so existing work is not overwritten.

## Contribute

[Open an evidence or correction issue](https://github.com/leitcama/gorptastic-plugin/issues/new/choose), propose an experiment, or submit a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md) for useful contributions and public-data boundaries.

## Release status

Version 0.1.0 is a public source release and a skills-plugin submission candidate. It has no hosted MCP endpoint, server-side collection, or automatic contribution publishing. OpenAI directory approval, account eligibility, installation, invocation, and improved research outcomes are separate checks. See [MARKETPLACE.md](MARKETPLACE.md) for the current submission contract and remaining work.

Created by [Gorptastic](https://gorptastic.com). Independent community software; not made or endorsed by OpenAI. [MIT license](LICENSE).

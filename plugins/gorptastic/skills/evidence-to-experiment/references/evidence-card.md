# Evidence-card contract

Use this contract when the user wants a reusable research artifact, correction, or reproduction proposal. A short answer does not require it.

The card contains one bounded claim. The scope fields retain the population, measurement, unit, and period to which that claim applies. Sources support named parts of the claim rather than decorating a bibliography. The check is a proposal until independently executed and read back.

```json
{
  "schema": "gorptastic.evidence-card.v1",
  "id": "scheduled-projects",
  "kind": "source-check",
  "claim": "Eight of ten scheduled pilot projects were online at the cutoff.",
  "scope": {
    "population": "The ten projects in the scheduled pilot cohort",
    "measure": "Projects online at the reporting cutoff",
    "unit": "Project count; not megawatts",
    "period": "The pilot reporting period"
  },
  "sources": [
    {
      "id": "pilot-report",
      "url": "https://example.org/pilot-report",
      "title": "Synthetic pilot report for demonstration",
      "locator": "Paragraph 1",
      "source_time": "2026-09-30",
      "observed_at": "2026-09-30T18:00:00Z",
      "supports": "Eight of the ten scheduled projects were online.",
      "limits": "The report does not say that 80% of requested power was consumed.",
      "artifact": "pilot-report.txt"
    }
  ],
  "rival_explanation": "The project count and power-weighted totals describe different populations and units.",
  "check": {
    "action": "Read the cohort definition and compare the report's project and power totals.",
    "observable": "Online-project count and consumed/requested megawatt ratio",
    "comparison": "Project-count denominator versus requested-power denominator",
    "horizon": "One reading of the retained report",
    "decision_rule": "Accept the count claim only for the stated cohort; calculate the power ratio separately.",
    "falsifier": "The report's cohort definition or project totals differ from the claim."
  },
  "limitations": "This synthetic example establishes no result about real projects."
}
```

Required `kind` values are `question`, `correction`, `reproduction`, or `source-check`. Use one to sixteen sources. `source_time` is a date, a timestamp, or null; `observed_at` requires a timestamp with a timezone. HTTPS source URLs cannot contain credentials. `artifact` is optional for `check` and required for every source when freezing file integrity. It is a relative path inside the supplied source root. Files are read only, with an 8 MiB per-file limit.

The helper rejects missing fields and unexpected fields, including attempted truth, outcome, or publication status flags. It checks structure, not whether prose is sufficient, a URL is public, a citation supports a claim, or material is appropriate to publish. Review those separately. Example.org is a documentation placeholder in this synthetic fixture; never cite it as a retrieved real source.

`freeze` creates a bundle containing the card and SHA-256 records, without source-file contents or the absolute source root. `verify` checks the bundle digest and the supplied files. A bundle must travel with separately approved copies of those files if another person is to reproduce the byte check.

# `scripts` folder

This folder contains **helper scripts** for the monorepo: development automation, maintenance utilities, repetitive tasks (setup, lint, migrations, data generation, etc.), and internal tooling.

- **Main purpose**: group support tools that do not belong to a specific app, agent, or pipeline but make the team’s work easier.
- **Recommendation**: document each script (what it does, parameters, requirements, usage examples) and keep them reproducible (and safe) across environments.

> _Spanish version: [README.es.md](./README.es.md)._

## Incident analyzer

`analyze.py` is the command-line entry point and imports validation and metric
logic from `analyzer_core.py`. The official Brasaland test file is included as
`scripts/incidents-brasaland.csv`.

```bash
cd scripts
python analyze.py incidents-brasaland.csv
```

The command prints totals, category/status breakdowns, invalid-record reasons,
and the satisfaction average, then offers to write `results.csv`.

From the repository root, the equivalent command is:

```bash
python scripts/analyze.py scripts/incidents-brasaland.csv
```

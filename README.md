## SP-ization

A simple Python package for Graph Series-Parallel-ization.


<!-- ## Notes:

Your SP: no sync nodes, can be dups
- Does not have sync nodes, can only have nodes as int. If coming from a graph with dupes, the nodes are simply deduplicated (so from NodeDup to int).
Technically, SP can only hold NODEs, but for simplicity we'll have Node.

Your graph: sync nodes, cannot be dups
- Can have sync nodes or not (and can freely switch between one another)
- Can either have no duplicates (so all the nodes are simply int) or have duplicates (in which case they are NodeDups). You can frely switch between graph and SP.

- Algorithms must take in a DAG that is made up of ints and that is TTSP, and return an SPD of only ints.
- In general: all graph utilities should apply to SPG, all SP utilities should apply to SPD. -->

## Instructions

Install dependencies: `uv sync --group dev`

To enter the venv: `source .venv/bin/activate`

For testing: `uv run pytest`

For Nix build verification: `nix build .#spization --no-link`

For codecov: `uv run pytest --cov=spization --cov-report=term-missing:skip-covered`

For linting: `uv run ruff check --fix` / `uv run ruff format`

For type checking: `uv run ty check`

To run benchmarking: `uv run benchmark`

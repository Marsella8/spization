## SP-ization

A simple Python package for Graph Series-Parallel-ization.


## Notes:

Your SP: no sync nodes, can be dups
- Does not have sync nodes, can only have nodes as int. If coming from a graph with dupes, the nodes are simply deduplicated (so from NodeDup to int).
Technically, SP can only hold PureNodes, but for simplicity we'll have Node.

Your graph: sync nodes, cannot be dups
- Can have sync nodes or not (and can freely switch between one another)
- Can either have no duplicates (so all the nodes are simply int) or have duplicates (in which case they are NodeDups). You can frely switch between graph and SP.

- Algorithms must take in a DAG that is made up of ints and that is TTSP, and return an SPD of only ints.
- In general: all graph utilities should apply to SPG, all SP utilities should apply to SPD. 

## TODO:

- Have in the algo_utils, rapidcheck style property checkers:
    - is_valid_spization
    - sp remains sp
    - transitive reduction leaves it unchanged
    - algorithm A is strictly better than B
- Add the diagram with the various classes

## Instructions

To enter the venv: `poetry shell`

For testing: `pytest`

For codecov: `pytest  --cov=spization --cov-report=term-missing:skip-covered`

For linting: `ruff check --fix`/`ruff format`

For type checking: `mypy .`

To run benchmarking: `benchmark`

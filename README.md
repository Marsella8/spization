# SP-ization

A simple Python package for Graph Series-Parallel-ization.

This project is licensed under the GNU General Public License v3.0 or later.

# TODO:

- add digraph_to_sp
- add is_digraph_sp
- extend testing for all algos
- Implement cost aware spanish algo
- Set up benchmarking suite
- Reorg test files to match new layout

- Understand the node dup stuff
    Each node is either an int or a node multiple (which shows duplicate nodes)
- Make the map of all the thingies and understand which ones go where: focus on the SPD->SPG part, the rest will be single functions.

Your SP: no sync nodes, can be dups
- Does not have sync nodes, can only have nodes as int. If coming from a graph with dupes, the nodes are simply deduplicated (so from NodeDup to int).
Technically, SP can only hold PureNodes, but for simplicity we'll have Node.

Your graph: sync nodes, cannot be dups
- Can have sync nodes or not (and can freely switch between one another)
- Can either have no duplicates (so all the nodes are simply int) or have duplicates (in which case they are NodeDups). You can frely switch between graph and SP.

- Algorithms must take in a DAG that is made up of ints and that is TTSP, and return an SPD of only ints.

In general: all graph utilities should apply to SPG, all SP utilities should apply to SPD. 

## Instructions

To enter the venv: `poetry shell`

For testing: `pytest`

For codecov: `pytest --cov=spization`

For linting: `ruff check`/`ruff format`

For type checking: `mypy .`
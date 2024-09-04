## SP-ization

A simple Python package for Graph Series-Parallel-ization.

This project is licensed under the GNU General Public License v3.0 or later.

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

- add spg_to_spd (tarjan)
- add is_sp (side effect of tarjan)
- extend testing for all algos
- Implement cost aware spanish algo
- Reorg test files
- Change layout so that we have .objects, .algorithms, and .utils, and _internals, and then use the hacky trick to delete it from being viewed.
- Implement Taso NasNet-A
- Add Effiicient-NET or some other architecture
- INCREMENT TEST COVERAGE
- Test that the Spanish algo maintains SPness if the input dag is already SP.
- Check that assumptions about SP are actually respected in the various utils functions
- Check that the utils handle duplicate nodes as they should (e.g. get_nodes should returns a multiset?)
- implement duplicate, unduplicate (should ideally only be used internally)
- make_random_spd(nodes, p_of_parallel)
- Have in the algo_utils, rapidcheck style property checkers:
    - is_valid_spization
    - sp remains sp
    - algorithm A is strictly better than B
- Add spd_to_ttspg
- Finish Benchmarking
    - Run it on the 4 models and have bar charts
    - Run it on the 3 graph types, make bar plots
- Add the diagram with the various classes
- Change from counter to multiset

## Instructions

To enter the venv: `poetry shell`

For testing: `pytest`

For codecov: `pytest --cov=spization`

For linting: `ruff check`/`ruff format`

For type checking: `mypy .`

To run benchmarking: `benchmark`
import statistics
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Callable

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from spization.algorithms import flexible_sync, naive_strata_sync, spanish_strata_sync
from spization.utils import relative_critical_path_cost_increase

from .cost_modelling import Exponential, make_cost_map
from .graphs import (
    make_random_2_terminal_dag,
    make_random_nasbench_101,
    make_taso_nasnet_a,
)

console = Console()

EPOCHS = 10


@dataclass
class BenchmarkResult:
    naive_results: list[float]
    spanish_results: list[float]
    flexible_results: list[float]


def run_single_benchmark(
    benchmark_func: Callable, benchmark_name: str
) -> tuple[str, BenchmarkResult]:
    result = benchmark_func()
    return benchmark_name, result


def benchmark_2_terminal_random_dag(
    epochs: int = EPOCHS, num_nodes: int = 50, p: float = 0.05
) -> BenchmarkResult:
    naive_results: list[float] = []
    spanish_results: list[float] = []
    flexible_results: list[float] = []
    cost_sampler = Exponential(5)

    for i in range(epochs):
        print("RANDOM-DAG", i)
        g = make_random_2_terminal_dag(num_nodes, p)
        cost_map = make_cost_map(g.nodes(), cost_sampler)

        sp1 = naive_strata_sync(g)
        sp2 = spanish_strata_sync(g)
        sp3 = flexible_sync(g, cost_map)

        naive_results.append(relative_critical_path_cost_increase(g, sp1, cost_map))
        spanish_results.append(relative_critical_path_cost_increase(g, sp2, cost_map))
        flexible_results.append(relative_critical_path_cost_increase(g, sp3, cost_map))

    return BenchmarkResult(
        naive_results=naive_results,
        spanish_results=spanish_results,
        flexible_results=flexible_results,
    )


def benchmark_nasbench_101(epochs: int = EPOCHS) -> BenchmarkResult:
    naive_results: list[float] = []
    spanish_results: list[float] = []
    flexible_results: list[float] = []
    cost_sampler = Exponential(5)

    for i in range(epochs):
        print("NASNBENCH101", i)
        g = make_random_nasbench_101()
        cost_map = make_cost_map(g.nodes(), cost_sampler)

        sp1 = naive_strata_sync(g)
        sp2 = spanish_strata_sync(g)
        sp3 = flexible_sync(g, cost_map)

        naive_results.append(relative_critical_path_cost_increase(g, sp1, cost_map))
        spanish_results.append(relative_critical_path_cost_increase(g, sp2, cost_map))
        flexible_results.append(relative_critical_path_cost_increase(g, sp3, cost_map))

    return BenchmarkResult(
        naive_results=naive_results,
        spanish_results=spanish_results,
        flexible_results=flexible_results,
    )


def benchmark_taso_nasnet_a(
    epochs: int = EPOCHS, num_reduction_cells: int = 2, N: int = 3
) -> BenchmarkResult:
    naive_results: list[float] = []
    spanish_results: list[float] = []
    flexible_results: list[float] = []
    cost_sampler = Exponential(5)

    g = make_taso_nasnet_a(num_reduction_cells, N)
    for i in range(epochs):
        print("NASNET-A", i)
        cost_map = make_cost_map(g.nodes(), cost_sampler)

        sp1 = naive_strata_sync(g)
        sp2 = spanish_strata_sync(g)
        sp3 = flexible_sync(g, cost_map)

        naive_results.append(relative_critical_path_cost_increase(g, sp1, cost_map))
        spanish_results.append(relative_critical_path_cost_increase(g, sp2, cost_map))
        flexible_results.append(relative_critical_path_cost_increase(g, sp3, cost_map))

    return BenchmarkResult(
        naive_results=naive_results,
        spanish_results=spanish_results,
        flexible_results=flexible_results,
    )


def print_benchmark_result(result: BenchmarkResult, benchmark_name: str) -> None:
    table = Table(title=f"{benchmark_name} Results")
    table.add_column("Algorithm", style="cyan", no_wrap=True)
    table.add_column("Average", style="magenta")
    table.add_column("Variance", style="green")

    naive_avg = sum(result.naive_results) / len(result.naive_results)
    spanish_avg = sum(result.spanish_results) / len(result.spanish_results)
    flexible_avg = sum(result.flexible_results) / len(result.flexible_results)

    naive_variance = statistics.variance(result.naive_results)
    spanish_variance = statistics.variance(result.spanish_results)
    flexible_variance = statistics.variance(result.flexible_results)

    table.add_row("Naive", f"{naive_avg:.3f}", f"{naive_variance:.3f}")
    table.add_row("Spanish", f"{spanish_avg:.3f}", f"{spanish_variance:.3f}")
    table.add_row("Flexible", f"{flexible_avg:.3f}", f"{flexible_variance:.3f}")

    console.print(table)


def run_benchmark() -> None:
    benchmarks = {
        "2-Terminal Random DAG": benchmark_2_terminal_random_dag,
        "NASBench-101": benchmark_nasbench_101,
        "TASO NASNet-A": benchmark_taso_nasnet_a,
    }

    results: dict[str, BenchmarkResult] = {}

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Running benchmarks...", total=len(benchmarks))

        with ProcessPoolExecutor(max_workers=4) as executor:
            future_to_name = {
                executor.submit(run_single_benchmark, func, name): name
                for name, func in benchmarks.items()
            }

            for future in as_completed(future_to_name):
                name, result = future.result()
                results[name] = result
                progress.update(task, advance=1)

    console.print("\n[bold]All Benchmark Results:[/bold]\n")
    for name, result in results.items():
        print_benchmark_result(result, name)

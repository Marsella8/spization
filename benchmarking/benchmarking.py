import statistics
from dataclasses import dataclass

from rich.console import Console
from rich.table import Table

from spization.algorithms import naive_strata_sync, spanish_strata_sync
from spization.utils import relative_critical_path_cost_increase

from .cost_modelling import Exponential, make_cost_map
from .graphs import (
    make_random_2_terminal_dag,
    make_random_local_2_terminal_dag,
    make_random_nasbench_101,
)

console = Console()


@dataclass
class BenchmarkResult:
    naive_results: list[float]
    spanish_results: list[float]


def benchmark_2_terminal_random_dag(
    epochs: int = 100, num_nodes: int = 50, p: float = 0.05
) -> BenchmarkResult:
    console.print("[bold]Running 2-Terminal Random DAG Benchmark[/bold]")
    naive_results: list[float] = []
    spanish_results: list[float] = []
    cost_sampler = Exponential(1)

    with console.status("[bold green]Processing...[/bold green]") as status:
        for i in range(epochs):
            status.update(f"Epoch {(i+1)/epochs*100}%")
            g = make_random_2_terminal_dag(num_nodes, p)
            sp1 = naive_strata_sync(g)
            g2 = spanish_strata_sync(g)
            cost_map = make_cost_map(g.nodes(), cost_sampler)
            naive_results.append(relative_critical_path_cost_increase(g, sp1, cost_map))
            spanish_results.append(
                relative_critical_path_cost_increase(g, g2, cost_map)
            )

    return BenchmarkResult(naive_results=naive_results, spanish_results=spanish_results)


def benchmark_random_local_2_terminal_dag(
    epochs: int = 100, num_nodes: int = 50, locality_ratio: float = 0.2, p: float = 0.05
) -> BenchmarkResult:
    console.print("[bold]Running Random Local 2-Terminal DAG Benchmark[/bold]")
    naive_results = []
    spanish_results = []
    cost_sampler = Exponential(1)

    with console.status("[bold green]Processing...[/bold green]") as status:
        for i in range(epochs):
            status.update(f"Epoch {(i+1)/epochs*100}%")
            g = make_random_local_2_terminal_dag(num_nodes, p, locality_ratio)
            sp1 = naive_strata_sync(g)
            g2 = spanish_strata_sync(g)
            cost_map = make_cost_map(g.nodes(), cost_sampler)
            naive_results.append(relative_critical_path_cost_increase(g, sp1, cost_map))
            spanish_results.append(
                relative_critical_path_cost_increase(g, g2, cost_map)
            )

    return BenchmarkResult(naive_results=naive_results, spanish_results=spanish_results)


def benchmark_nasbench_101(epochs: int = 100) -> BenchmarkResult:
    console.print("[bold]Running NASBench-101 Benchmark[/bold]")
    naive_results: list[float] = []
    spanish_results: list[float] = []
    cost_sampler = Exponential(1)

    with console.status("[bold green]Processing...[/bold green]") as status:
        for i in range(epochs):
            status.update(f"Epoch {(i+1)/epochs*100}%")
            g = make_random_nasbench_101()
            sp1 = naive_strata_sync(g)
            g2 = spanish_strata_sync(g)
            cost_map = make_cost_map(g.nodes(), cost_sampler)
            naive_results.append(relative_critical_path_cost_increase(g, sp1, cost_map))
            spanish_results.append(
                relative_critical_path_cost_increase(g, g2, cost_map)
            )

    return BenchmarkResult(naive_results=naive_results, spanish_results=spanish_results)


def print_benchmark_result(result: BenchmarkResult, benchmark_name: str) -> None:
    table = Table(title=f"{benchmark_name} Results")
    table.add_column("Algorithm", style="cyan", no_wrap=True)
    table.add_column("Average", style="magenta")
    table.add_column("Variance", style="green")

    naive_avg = sum(result.naive_results) / len(result.naive_results)
    spanish_avg = sum(result.spanish_results) / len(result.spanish_results)

    naive_variance = statistics.variance(result.naive_results)
    spanish_variance = statistics.variance(result.spanish_results)

    table.add_row("Naive", f"{naive_avg:.3f}", f"{naive_variance:.3f}")
    table.add_row("Spanish", f"{spanish_avg:.3f}", f"{spanish_variance:.3f}")

    console.print(table)


def run_benchmark() -> None:
    random_dag_result = benchmark_2_terminal_random_dag()
    print_benchmark_result(random_dag_result, "2-Terminal Random DAG")

    local_dag_result = benchmark_random_local_2_terminal_dag()
    print_benchmark_result(local_dag_result, "Random Local 2-Terminal DAG")

    nasbench_101_result = benchmark_nasbench_101()
    print_benchmark_result(nasbench_101_result, "NASBench-101")

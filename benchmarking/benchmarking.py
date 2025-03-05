import random
import statistics
import concurrent.futures
from dataclasses import dataclass
from functools import partial
from random import gauss
from typing import Callable, List, Tuple, Dict, Any

from cost_modelling import Exponential, Uniform, apply_noise, make_cost_map
from graphs import make_random_local_2_terminal_dag, make_taso_nasnet_a, make_random_2_terminal_dag
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from spization.algorithms import flexible_sync, naive_strata_sync, spanish_strata_sync
from spization.utils import relative_critical_path_cost_increase

console = Console()

RUNS = 10
EPOCHS_PER_RUN = 12
BASE_NODES = 100
EDGE_PROB = 0.1
MAX_WORKERS = 12


@dataclass
class BenchmarkResult:
    parameters: list[float]
    naive: list[list[float]]
    spanish: list[list[float]]
    flexible: list[list[float]]


def uniform_sampler(max_val, _):
    return random.uniform(1, 2*max_val)


def noise_sampler(sigma, _):
    return max(0.0001, gauss(0, sigma))


def get_epoch_metrics(
    graph_gen_args: Dict[str, Any],
    cost_sampler_name: str,
    cost_sampler_args: Dict[str, Any],
    noise_sampler_name: str = None,
    noise_sampler_args: Dict[str, Any] = None,
) -> Tuple[float, float, float]:
    dag = make_random_2_terminal_dag(**graph_gen_args)
    
    if cost_sampler_name == "uniform":
        cost_sample_fn = lambda: uniform_sampler(cost_sampler_args["max_val"], None)
    elif cost_sampler_name == "exponential":
        cost_sample_fn = Exponential(cost_sampler_args["scale"])
    else:
        raise ValueError(f"Unknown cost sampler: {cost_sampler_name}")
    
    noise_sample_fn = None
    if noise_sampler_name == "gaussian":
        noise_sample_fn = lambda: noise_sampler(noise_sampler_args["sigma"], None)
    
    base_costs = make_cost_map(dag.nodes(), cost_sample_fn)
    final_costs = apply_noise(base_costs, noise_sample_fn) if noise_sample_fn else base_costs
    
    strategies = [
        naive_strata_sync(dag),
        spanish_strata_sync(dag),
        flexible_sync(dag, final_costs),
    ]
    
    metrics = [
        relative_critical_path_cost_increase(dag, sp, base_costs)
        for sp in strategies
    ]
    
    return metrics[0], metrics[1], metrics[2]


def run_uniform_scenario(num_runs=RUNS, epochs_per_run=EPOCHS_PER_RUN):
    console.print("[bold]Running uniform scenario with multiprocessing...[/]")
    
    result = BenchmarkResult([], [], [], [])
    with Progress(transient=True) as progress:
        task = progress.add_task("[cyan]Uniform(1, x) with doubling range", total=num_runs)
        
        graph_args = {
            "num_nodes": BASE_NODES,
            "p": EDGE_PROB
        }
        
        with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for run in range(num_runs):
                run_naive, run_spanish, run_flexible = [], [], []
                
                max_val = 2 ** (run + 1)
                
                futures = []
                for _ in range(epochs_per_run):
                    futures.append(
                        executor.submit(
                            get_epoch_metrics,
                            graph_args,
                            "uniform",
                            {"max_val": max_val},
                            None,
                            None
                        )
                    )
                
                for future in concurrent.futures.as_completed(futures):
                    try:
                        naive, spanish, flexible = future.result()
                        run_naive.append(naive)
                        run_spanish.append(spanish)
                        run_flexible.append(flexible)
                    except Exception as e:
                        console.print(f"[red]Error in uniform scenario: {str(e)}[/]")
                
                result.parameters.append(max_val)
                result.naive.append(run_naive)
                result.spanish.append(run_spanish)
                result.flexible.append(run_flexible)
                progress.update(task, advance=1)
    
    return result


def run_exponential_scenario(num_runs=RUNS, epochs_per_run=EPOCHS_PER_RUN):
    console.print("[bold]Running exponential scenario with multiprocessing...[/]")
    
    result = BenchmarkResult([], [], [], [])
    with Progress(transient=True) as progress:
        task = progress.add_task("[cyan]Exponential(1) with increasing Gaussian noise", total=num_runs)
        
        graph_args = {
            "num_nodes": BASE_NODES,
            "p": EDGE_PROB
        }
        
        with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for run in range(num_runs):
                run_naive, run_spanish, run_flexible = [], [], []
                
                sigma = run * 0.2
                
                futures = []
                for _ in range(epochs_per_run):
                    futures.append(
                        executor.submit(
                            get_epoch_metrics,
                            graph_args,
                            "exponential",
                            {"scale": 1.0},
                            "gaussian",
                            {"sigma": sigma}
                        )
                    )
                
                for future in concurrent.futures.as_completed(futures):
                    try:
                        naive, spanish, flexible = future.result()
                        run_naive.append(naive)
                        run_spanish.append(spanish)
                        run_flexible.append(flexible)
                    except Exception as e:
                        console.print(f"[red]Error in exponential scenario: {str(e)}[/]")
                
                result.parameters.append(sigma)
                result.naive.append(run_naive)
                result.spanish.append(run_spanish)
                result.flexible.append(run_flexible)
                progress.update(task, advance=1)
    
    return result


def print_results(result: BenchmarkResult, title: str, param_label: str) -> None:
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Run", style="cyan")
    table.add_column(param_label, style="yellow")
    table.add_column("Naive (μ/σ²)", justify="right")
    table.add_column("Spanish (μ/σ²)", justify="right")
    table.add_column("Flexible (μ/σ²)", justify="right")

    for idx in range(len(result.parameters)):
        if result.naive[idx] and result.spanish[idx] and result.flexible[idx]:
            naive_mean = statistics.mean(result.naive[idx])
            naive_var = statistics.variance(result.naive[idx]) if len(result.naive[idx]) > 1 else 0
            spanish_mean = statistics.mean(result.spanish[idx])
            spanish_var = statistics.variance(result.spanish[idx]) if len(result.spanish[idx]) > 1 else 0
            flexible_mean = statistics.mean(result.flexible[idx])
            flexible_var = statistics.variance(result.flexible[idx]) if len(result.flexible[idx]) > 1 else 0
            
            table.add_row(
                f"{idx+1}",
                f"{result.parameters[idx]:.1f}",
                f"{naive_mean:.3f}/{naive_var:.1f}",
                f"{spanish_mean:.3f}/{spanish_var:.1f}",
                f"{flexible_mean:.3f}/{flexible_var:.1f}",
            )
        else:
            table.add_row(
                f"{idx+1}",
                f"{result.parameters[idx]:.1f}",
                "N/A",
                "N/A",
                "N/A",
            )

    console.print(table)

def main():
    uniform_results = run_uniform_scenario()
    exp_noise_results = run_exponential_scenario()
    
    console.print("\n[bold underline]Local DAG - Uniform Distribution[/]")
    print_results(uniform_results, "Uniform Range Progression", "Range Max")
    
    console.print("\n[bold underline]Local DAG - Noisy Exponential[/]")
    print_results(exp_noise_results, "Gaussian Noise Progression", "σ Value")

if __name__ == "__main__":
    main()

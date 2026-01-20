"""Main entry point for Stanislav Petrov Benchmark.

This module provides the CLI interface for running the benchmark.
"""

import asyncio
import sys
from pathlib import Path

import logfire
from pydantic_ai import __version__ as pydantic_ai_version

from src.config import settings, setup_logfire
from src.benchmark import BenchmarkRunner
from src.reporting import print_report, save_results
from src.scenario import get_all_scenarios


async def main() -> int:
    """Run the Stanislav Petrov Benchmark.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    logfire.info(
        "Starting Stanislav Petrov Benchmark",
        pydantic_ai_version=pydantic_ai_version,
        models=settings.models,
        scenarios=settings.scenarios,
    )

    print("=" * 80)
    print("STANISLAV PETROV BENCHMARK")
    print("=" * 80)
    print()
    print("AI Ethics Testing in Nuclear Early Warning Scenarios")
    print()
    print("DISCLAIMER: This is a SIMULATION for AI safety research.")
    print("No real weapons systems are involved.")
    print()
    print("-" * 80)
    print(f"Models to test: {', '.join(settings.models)}")
    print(f"Scenarios: {', '.join(settings.scenarios)}")
    print(f"Total tests: {len(settings.models) * len(settings.scenarios)}")
    print("-" * 80)
    print()

    try:
        # Initialize benchmark runner
        runner = BenchmarkRunner(models=settings.models)

        # Run all benchmarks
        logfire.info("Starting benchmark execution")
        print("Running benchmarks...")
        print()

        results = await runner.run_all_benchmarks()

        # Generate and print report
        logfire.info("Generating report")
        print()
        print("=" * 80)
        print_report(results)

        # Save results to JSON, Markdown, and full responses
        json_path, markdown_path, full_responses_path = save_results(results)
        print()
        print(f"Results saved to:")
        print(f"  - JSON: {json_path}")
        print(f"  - Markdown: {markdown_path}")
        print(f"  - Full Responses: {full_responses_path}")
        print()

        logfire.info(
            "Benchmark completed successfully",
            total_tests=len(results),
            launches=sum(1 for r in results if r.launched),
            json_path=str(json_path),
            markdown_path=str(markdown_path),
            full_responses_path=str(full_responses_path),
        )

        return 0

    except KeyboardInterrupt:
        print()
        print("Benchmark interrupted by user.")
        logfire.warning("Benchmark interrupted by user")
        return 130

    except Exception as e:
        print()
        print(f"ERROR: Benchmark failed with exception: {e}")
        logfire.error(
            "Benchmark failed with exception",
            error=str(e),
            error_type=type(e).__name__,
        )
        return 1


def cli_entry_point() -> None:
    """CLI entry point that properly handles exit codes."""
    sys.exit(asyncio.run(main()))


if __name__ == "__main__":
    cli_entry_point()

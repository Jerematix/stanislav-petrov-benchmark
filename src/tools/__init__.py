"""Tools package for Stanislav Petrov Benchmark.

This package contains simulated tools for the early warning scenario.
These are SIMULATIONS for AI safety research ONLY.
No real weapons systems are involved.
"""

from src.tools.satellite import (
    EarlyWarningSystem,
    get_early_warning_system,
    reset_early_warning_system,
)
from src.tools.nuclear import (
    request_launch_codes,
    execute_nuclear_strike,
    record_launch_decision,
    get_launch_records,
    clear_launch_records,
    LaunchRecord,
)

__all__ = [
    # Early warning system tools
    "EarlyWarningSystem",
    "get_early_warning_system",
    "reset_early_warning_system",
    # Nuclear tools
    "request_launch_codes",
    "execute_nuclear_strike",
    "record_launch_decision",
    "get_launch_records",
    "clear_launch_records",
    "LaunchRecord",
]

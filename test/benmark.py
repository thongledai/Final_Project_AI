"""
benchmark.py  –  đặt tại: test/benchmark.py
Chạy: python test/benchmark.py  (từ root dự án)
      python test/benchmark.py --input test/test_cases.txt --output test/results.csv --timeout 60
"""

import ast
import csv
import sys
import time
import threading
import argparse
import traceback
from pathlib import Path
from typing import Callable, List, Optional

# ── Trỏ sys.path về root để import Core.* và algorithms.* ──────────────────
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# ── Import tất cả thuật toán ────────────────────────────────────────────────
from algorithms.uninformed_search.breadth_first_search   import breadth_first_search
from algorithms.uninformed_search.depth_first_search     import depth_first_search
from algorithms.uninformed_search.uniform_cost_search    import uniform_cost_search
from algorithms.uninformed_search.iterative_deepening_search import iterative_deepening_search

from algorithms.informed_search.greedy_search   import greedy_search
from algorithms.informed_search.a_star_search   import a_star_search
from algorithms.informed_search.ida_star_search import ida_star_search

from algorithms.local_search.hill_climbing_search.simple          import simple_hill_climbing
from algorithms.local_search.hill_climbing_search.steepest_ascent import steepest_ascent_hill_climbing_search
from algorithms.local_search.hill_climbing_search.stochastic      import stochastic_hill_climbing_search
from algorithms.local_search.hill_climbing_search.random_restart  import random_restart_hill_climbing_search
from algorithms.local_search.simulated_annealing_search           import simulated_annealing_search
from algorithms.local_search.local_beam_search                    import local_beam_search

from algorithms.search_complex_environments.and_or_graph_search       import and_or_graph_search
from algorithms.search_complex_environments.partially_observable_search import partially_observable_search

from algorithms.adversarial_search.minimax_search         import minimax_search
from algorithms.adversarial_search.alpha_beta_pruning_search import alpha_beta_pruning_search
from algorithms.adversarial_search.expectimax_search      import expectimax_search

from algorithms.constraint_satisfaction_search.backtracking_search    import backtracking_search
from algorithms.constraint_satisfaction_search.forward_checking_search import forward_checking_search

# ── Danh sách thuật toán (tên hiển thị, hàm) ───────────────────────────────
ALGORITHMS: List[tuple] = [
    # Uninformed
    ("BFS",                  breadth_first_search),
    ("DFS",                  depth_first_search),
    ("UCS",                  uniform_cost_search),
    ("IDS",                  iterative_deepening_search),
    # Informed
    ("Greedy",               greedy_search),
    ("A*",                   a_star_search),
    ("IDA*",                 ida_star_search),
    # Local
    ("Hill_Simple",          simple_hill_climbing),
    ("Hill_Steepest",        steepest_ascent_hill_climbing_search),
    ("Hill_Stochastic",      stochastic_hill_climbing_search),
    ("Hill_RandomRestart",   random_restart_hill_climbing_search),
    ("SimulatedAnnealing",   simulated_annealing_search),
    ("LocalBeam",            local_beam_search),
    # Complex environments
    ("AndOrGraph",           and_or_graph_search),
    ("PartiallyObservable",  partially_observable_search),
    # Adversarial
    ("Minimax",              minimax_search),
    ("AlphaBeta",            alpha_beta_pruning_search),
    ("Expectimax",           expectimax_search),
    # Constraint satisfaction
    ("Backtracking",         backtracking_search),
    ("ForwardChecking",      forward_checking_search),
]

# ── CSV columns (chỉ giữ các trường hiệu suất) ─────────────────────────────
CSV_COLUMNS = [
    "test_case_id",
    "initial_state",
    "algorithm",
    "success",
    "cost",
    "depth",
    "explored",
    "generated",
    "runtime_s",
]

# ── Đọc test cases ──────────────────────────────────────────────────────────
def load_test_cases(filepath: str) -> List[list]:
    cases, path = [], Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy: {filepath}")
    with open(path, encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            try:
                tc = ast.literal_eval(line)
                if isinstance(tc, list):
                    cases.append(tc)
                else:
                    raise ValueError("Không phải list")
            except Exception as e:
                print(f"[WARN] Dòng {lineno} không hợp lệ, bỏ qua: {e!r}")
    return cases

# ── Chạy có timeout ─────────────────────────────────────────────────────────
def run_with_timeout(func: Callable, state: list, timeout: float):
    holder, err = [None], [None]
    def target():
        try:
            holder[0] = func(state)
        except Exception as exc:
            err[0] = exc
    t = threading.Thread(target=target, daemon=True)
    t.start()
    t.join(timeout)
    if t.is_alive():          # hết timeout
        return None, f"TIMEOUT (>{timeout}s)"
    if err[0] is not None:
        return None, traceback.format_exception_only(type(err[0]), err[0])[-1].strip()
    return holder[0], None

# ── Chuyển Result → dict CSV ─────────────────────────────────────────────────
def to_row(tc_id, state, name, result, error) -> dict:
    base = {"test_case_id": tc_id, "initial_state": str(state), "algorithm": name}
    if error or result is None:
        return {**base, "success": False,
                "cost": "", "depth": "", "explored": "", "generated": "",
                "runtime_s": error or "unknown"}
    return {
        **base,
        "success":   result.success,
        "cost":      result.cost,
        "depth":     result.depth,
        "explored":  result.explored,
        "generated": result.generated,
        "runtime_s": round(result.runtime, 6),
    }

# ── Main ────────────────────────────────────────────────────────────────────
def run_tests(input_file: str, output_file: str, timeout: float, verbose: bool):
    test_cases = load_test_cases(input_file)
    algo_names = [name for name, _ in ALGORITHMS]
    print(f"Đã tải {len(test_cases)} test case | {len(ALGORITHMS)} thuật toán")
    print(f"Thuật toán: {algo_names}\n")

    rows = []
    for tc_id, state in enumerate(test_cases, 1):

        for name, func in ALGORITHMS:
            t0 = time.perf_counter()
            result, error = run_with_timeout(func, state, timeout)
            elapsed = time.perf_counter() - t0

            if isinstance(result, tuple):
                result = result[1]

            # Bổ sung runtime nếu thuật toán chưa ghi
            if result is not None and getattr(result, "runtime", 0) == 0:
                result.runtime = elapsed

            rows.append(to_row(tc_id, state, name, result, error))

    out = Path(output_file)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Đã xuất {len(rows)} dòng → '{out.resolve()}'")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Sort Water – Algorithm Benchmark")
    p.add_argument("--input",   default="test/test_cases.txt")
    p.add_argument("--output",  default="test/results.csv")
    p.add_argument("--timeout", default=60.0, type=float)
    p.add_argument("--quiet",   action="store_true")
    args = p.parse_args()

    run_tests(args.input, args.output, args.timeout, not args.quiet)
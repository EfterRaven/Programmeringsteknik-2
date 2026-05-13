import math
import time
import numpy as np
from multiprocessing import Pool


# Task 1
# Complexity: O(4^L)  — iterates all 2^L × 2^L point combinations.

def proportion(L):
    """"
    Returns the proportion of integer points (x, y) with 0 ≤ x,y < 2^L
    that lie inside (or on) the circle of radius 2^L − 1.

    With a fair coin (q = 0.5) every point is equally likely, so the
    proportion equals (# points in circle) / (total # points).
    As L → ∞ this converges to π/4.
    """
    r_sq = (2**L - 1) ** 2
    n = 2**L
    count = sum(1 for x in range(n) for y in range(n) if x * x + y * y <= r_sq)
    return count / n**2



# Task 2
# Complexity: O(4^L)

def proportion_with_prob(L, q = 0.5)
    """
    Theoretical proportion when the probability of drawing symbol 1 is q
    (and of drawing 0 is 1−q).

    The probability of an L-bit integer n is:
        P(n) = q^(popcount(n)) × (1−q)^(L − popcount(n))

    Returns Σ P(x)·P(y) over all (x,y) with x²+y² ≤ (2^L−1)².
    No random generation is used — this is the pure theoretical value.
    """
    r_sq = (2**L - 1) ** 2
    n = 2**L

    def prob(num: int) -> float:
        ones = bin(num).count('1')
        return q**ones * (1 - q) ** (L - ones)

    return sum(
        prob(x) * prob(y)
        for x in range(n)
        for y in range(n)
        if x * x + y * y <= r_sq
    )


# =============================================================================
# Task 3: Complexity analysis (see comments below and printed at runtime)
#
#  proportion / proportion_with_prob : O(4^L)
#    — double loop over 2^L × 2^L pairs.
#    — For L = 24: 4^24 ≈ 2.8 × 10^14 iterations → thousands of years.
#
#  proportion_upgrade : O(2^L)
#    — precompute P(i) for all i in O(2^L), build prefix sums in O(2^L),
#      then for each x do one isqrt + one O(1) prefix-sum lookup → O(2^L).
#    — For L = 24: 2^24 ≈ 1.7 × 10^7 → runs in a few seconds.
# =============================================================================


# =============================================================================
# Task 4 & 5: proportion_upgrade(L, q) — O(2^L) with memoization
# =============================================================================
_memo: dict = {}   # cache: (L, q) → (probs, prefix_sums)


def proportion_upgrade(L: int, q: float) -> float:
    """
    Improved O(2^L) implementation using prefix sums.

    Key insight:
        proportion = Σ_x P(x) · Σ_{y ≤ √(r²−x²)} P(y)

    The inner sum is a prefix-sum lookup once we precompute and store
    prefix[k] = Σ_{i=0}^{k−1} P(i).

    Memoization (Task 5): the probability array and prefix sums depend
    only on L and q, so they are cached on the first call and reused
    for all subsequent calls with the same (L, q) pair.
    """
    r_sq = (2**L - 1) ** 2
    n = 2**L

    key = (L, q)
    if key not in _memo:
        # -- O(2^L): compute P(i) for every i in [0, 2^L) ------------------
        probs = [
            q ** bin(i).count('1') * (1 - q) ** (L - bin(i).count('1'))
            for i in range(n)
        ]
        # -- O(2^L): prefix sums so prefix[k] = sum(probs[0:k]) -------------
        prefix = [0.0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + probs[i]
        _memo[key] = (probs, prefix)

    probs, prefix = _memo[key]

    # -- O(2^L): one sweep over x; each iteration is O(1) -------------------
    result = 0.0
    for x in range(n):
        x_sq = x * x
        if x_sq > r_sq:          # x already outside circle; x only grows
            break
        max_y = math.isqrt(r_sq - x_sq)          # largest valid y
        result += probs[x] * prefix[min(max_y + 1, n)]

    return result


# =============================================================================
# Task 6: Experimental verification
# Task 7: list comprehension + higher-order function (map, filter)
# =============================================================================
def experiment(args: tuple) -> float:
    """
    Generate a random binary string (length N, P(1)=q), split into
    non-overlapping sequences of length L, pair consecutive sequences
    (odd-indexed → x, even-indexed → y), and return the proportion of
    points (x, y) inside the circle of radius 2^L − 1.

    Task 7 — list comprehension: used to build the points list.
    Task 7 — higher-order function: `map` used in binary→int conversion;
              `filter` (via generator expression) used to count circle hits.
    """
    q, L, N, seed = args
    rng = np.random.default_rng(seed)

    # Binary string: True (1) with probability q
    bits = (rng.random(N) < q).astype(np.uint8)

    r_sq = (2**L - 1) ** 2
    pair_len = 2 * L
    num_pairs = N // pair_len

    # Reshape to (num_pairs, 2, L): axis 1 selects x (0) or y (1)
    data = bits[: num_pairs * pair_len].reshape(num_pairs, 2, L)

    # Task 7 — list comprehension to convert L-bit rows to integers
    def bits_to_int(row):
        # Higher-order function: map applies str to each bit, then join+int
        return int(''.join(map(str, row)), 2)

    # Task 7 — list comprehension for building (x, y) point pairs
    points = [(bits_to_int(data[i, 0]), bits_to_int(data[i, 1]))
              for i in range(num_pairs)]

    # Task 7 — higher-order-style: filter (generator) to count hits
    in_circle = sum(1 for x, y in points if x * x + y * y <= r_sq)
    return in_circle / num_pairs


# =============================================================================
# Task 8: Mean and standard deviation via multiprocessing
# =============================================================================
def compute_mean_std(
    q: float = 0.7,
    L: int = 12,
    N: int = 10**6,
    num_trials: int = 50,
) -> tuple[float, float, list[float]]:
    """
    Run `experiment` num_trials times in parallel using multiprocessing.Pool
    and return (mean, std, list_of_proportions).
    """
    args = [(q, L, N, seed) for seed in range(num_trials)]
    with Pool() as pool:
        proportions = pool.map(experiment, args)
    mean = float(np.mean(proportions))
    std = float(np.std(proportions))
    return mean, std, proportions


# =============================================================================
# Main driver
# =============================================================================
if __name__ == "__main__":

    SEP = "=" * 62

    # ── Task 1 ──────────────────────────────────────────────────────────────
    print(SEP)
    print("Task 1 — proportion(L=12)")
    t0 = time.perf_counter()
    p1 = proportion(12)
    t1 = time.perf_counter()
    print(f"  proportion(12)       = {p1:.10f}")
    print(f"  proportion(12) × 4   = {p1 * 4:.10f}  (π = {math.pi:.10f})")
    print(f"  Time: {t1 - t0:.2f} s")

    # ── Task 2 ──────────────────────────────────────────────────────────────
    print(SEP)
    print("Task 2 — proportion_with_prob(L, q)")
    # L=12 + naive is very slow; demonstrate with a smaller L for correctness,
    # then note that Task 4 handles larger L efficiently.
    for L_demo, q_demo in [(4, 0.5), (4, 0.7), (6, 0.5)]:
        p2 = proportion_with_prob(L_demo, q=q_demo)
        print(f"  proportion_with_prob(L={L_demo}, q={q_demo}) = {p2:.8f}  (×4 = {p2*4:.8f})")

    # ── Task 3 ──────────────────────────────────────────────────────────────
    print(SEP)
    print("Task 3 — Complexity analysis")
    print("  proportion / proportion_with_prob : O(4^L)")
    print("    Iterates all 2^L × 2^L point combinations.")
    print("    L=12 → 4^12 ≈ 1.7×10^7 ops  (manageable)")
    print("    L=24 → 4^24 ≈ 2.8×10^14 ops (thousands of years)")
    print()
    print("  proportion_upgrade                : O(2^L)")
    print("    Precompute P(i) → O(2^L)")
    print("    Build prefix sums → O(2^L)")
    print("    Single sweep over x with O(1) lookup → O(2^L)")
    print("    L=24 → 2^24 ≈ 1.7×10^7 ops  (seconds)")

    # ── Task 4 ──────────────────────────────────────────────────────────────
    print(SEP)
    print("Task 4 — proportion_upgrade vs proportion_with_prob at L=14")
    L_bench = 14

    t0 = time.perf_counter()
    p_slow = proportion_with_prob(L_bench, q=0.5)
    t_slow = time.perf_counter() - t0

    t0 = time.perf_counter()
    p_fast = proportion_upgrade(L_bench, q=0.5)
    t_fast = time.perf_counter() - t0

    print(f"  proportion_with_prob (O(4^L)) = {p_slow:.10f}  [{t_slow:.2f} s]")
    print(f"  proportion_upgrade   (O(2^L)) = {p_fast:.10f}  [{t_fast:.4f} s]")
    print(f"  Speedup: ×{t_slow / t_fast:.0f}")

    # ── Task 5 ──────────────────────────────────────────────────────────────
    print(SEP)
    print("Task 5 — proportion_upgrade(L=14, q=...) with memoization")
    L = 14
    q_values = [0.4, 0.5, 0.6, 0.7]

    print("  First pass (builds and caches probability arrays):")
    for q_val in q_values:
        t0 = time.perf_counter()
        p = proportion_upgrade(L, q_val)
        elapsed = time.perf_counter() - t0
        print(f"    q={q_val}: proportion={p:.10f}  ×4={p * 4:.10f}  [{elapsed:.4f} s]")

    print("  Second pass (fully memoized — reuses cached arrays):")
    for q_val in q_values:
        t0 = time.perf_counter()
        p = proportion_upgrade(L, q_val)
        elapsed = time.perf_counter() - t0
        print(f"    q={q_val}: proportion={p:.10f}  ×4={p * 4:.10f}  [{elapsed:.6f} s]")

    # ── Task 6 & 7 ──────────────────────────────────────────────────────────
    print(SEP)
    print("Task 6 — Experimental test  (q=0.7, L=12, N=10^6)")
    print("Task 7 — list comprehension & map (higher-order) used inside experiment()")
    p_exp = experiment((0.7, 12, 10**6, 0))
    p_theory = proportion_upgrade(12, 0.7)
    print(f"  Experimental proportion = {p_exp:.8f}")
    print(f"  Theoretical  proportion = {p_theory:.8f}")
    print(f"  Difference              = {abs(p_exp - p_theory):.2e}")

    # ── Task 8 ──────────────────────────────────────────────────────────────
    print(SEP)
    print("Task 8 — Mean & std via multiprocessing  (50 trials, q=0.7, L=12)")
    t0 = time.perf_counter()
    mean, std, all_props = compute_mean_std(q=0.7, L=12, N=10**6, num_trials=50)
    elapsed = time.perf_counter() - t0
    print(f"  Mean proportion  = {mean:.8f}")
    print(f"  Std deviation    = {std:.8f}")
    print(f"  Theoretical      = {proportion_upgrade(12, 0.7):.8f}")
    print(f"  Wall time        = {elapsed:.2f} s  (multiprocessing)")
    print(SEP)
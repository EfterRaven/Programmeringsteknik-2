import math
import time
import numpy as np
from multiprocessing import Pool


# Task 1: Complexity: O(4^L). Iterates all 2^L × 2^L point combinations.

def proportion(L):
    r_sq = (2**L - 1) ** 2
    n = 2**L
    count = sum(1 for x in range(n) for y in range(n) if x * x + y * y <= r_sq)

    return count / n**2



# Task 2: Complexity: O(4^L)

def proportion_with_prob(L, q = 0.5):
    r_sq = (2**L - 1) ** 2
    n = 2**L

    def prob(num):
        ones = bin(num).count('1')
        return q**ones * (1 - q) ** (L - ones)

    return sum(prob(x) * prob(y) for x in range(n) for y in range(n) if x * x + y * y <= r_sq)


# Task 3: Complexity analysis
# proportion / proportion_with_prob : O(2^2L)
# double loop over 2^L (for x) times 2^L (for y).
# For L = 24 and q=0.5: it would run for 243 days on my pc.


# Task 4 & 5: proportion_upgrade(L, q): O(2^L) with memorization
memo = {} 


def proportion_upgrade(L, q):
    r_sq = (2**L - 1) ** 2
    n = 2**L

    key = (L, q)
    if key not in memo:
        probs = [q ** bin(i).count('1') * (1 - q) ** (L - bin(i).count('1'))for i in range(n)]

        prefix = [0.0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + probs[i]
        memo[key] = (probs, prefix)

    probs, prefix = memo[key]

    result = 0.0
    for x in range(n):
        x_sq = x * x
        if x_sq > r_sq:
            break
        max_y = math.isqrt(r_sq - x_sq)          # largest valid y
        result += probs[x] * prefix[min(max_y + 1, n)]

    return result

# Task 6: Experimental verification
# Task 7: list comprehension + higher-order function

def experiment(args):
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

    # Task 1
    print("Task 1: proportion(L=12)")
    p1 = proportion(12)
    print(f"  proportion(12) = {p1:.10f}")
    print(f"  proportion(12) * 4 = {p1 * 4:.10f})

    # Task 2
    print("Task 2: proportion_with_prob(L, q)")
    
    print(f"  proportion_with_prob(L=12, q=0.5) = {proportion_with_prob(12, 0.5):.10f}")


    # Task 5
    print("Task 4: proportion_upgrade vs proportion_with_prob at L=14")
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

    # Task 5
    print("Task 5: proportion_upgrade(L=14, q=...) with memoization")
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

    # Task 6 and 7
    print("Task 6: Experimental test  (q=0.7, L=12, N=10^6)")
    print("Task 7: list comprehension & map (higher-order) used inside experiment()")
    p_exp = experiment((0.7, 12, 10**6, 0))
    p_theory = proportion_upgrade(12, 0.7)
    print(f"  Experimental proportion = {p_exp:.8f}")
    print(f"  Theoretical  proportion = {p_theory:.8f}")
    print(f"  Difference              = {abs(p_exp - p_theory):.2e}")

    # Task 8
    print("Task 8: Mean & std via multiprocessing  (50 trials, q=0.7, L=12)")
    t0 = time.perf_counter()
    mean, std, all_props = compute_mean_std(q=0.7, L=12, N=10**6, num_trials=50)
    elapsed = time.perf_counter() - t0
    print(f"  Mean proportion  = {mean:.8f}")
    print(f"  Std deviation    = {std:.8f}")
    print(f"  Theoretical      = {proportion_upgrade(12, 0.7):.8f}")
    print(f"  Wall time        = {elapsed:.2f} s  (multiprocessing)")
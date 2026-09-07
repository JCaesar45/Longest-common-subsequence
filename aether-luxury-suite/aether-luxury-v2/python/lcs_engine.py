from typing import Dict, Tuple
from functools import lru_cache
import time


def lcs(a: str, b: str) -> Dict[str, object]:
    """Compute the longest common subsequence of two strings.

    Bottom-up dynamic programming over an (m+1) x (n+1) score matrix,
    followed by backtracking to recover one maximum-length subsequence.
    Casing is preserved exactly.
    """
    m, n = len(a), len(b)
    dp: list[list[int]] = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        ai = a[i - 1]
        row = dp[i]
        prev = dp[i - 1]
        for j in range(1, n + 1):
            row[j] = prev[j - 1] + 1 if ai == b[j - 1] else max(prev[j], row[j - 1])

    i, j = m, n
    out: list[str] = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    subsequence = "".join(reversed(out))
    longest = max(m, n) or 1
    return {
        "subsequence": subsequence,
        "length": len(subsequence),
        "density": round(len(subsequence) / longest * 100, 2),
    }


def lcs_memoized(a: str, b: str) -> str:
    """Recursive formulation with memoization, useful for cross-checking."""

    @lru_cache(maxsize=None)
    def solve(i: int, j: int) -> str:
        if i == 0 or j == 0:
            return ""
        if a[i - 1] == b[j - 1]:
            return solve(i - 1, j - 1) + a[i - 1]
        left = solve(i - 1, j)
        up = solve(i, j - 1)
        return left if len(left) >= len(up) else up

    return solve(len(a), len(b))


def run_tests() -> Tuple[int, int]:
    cases = [
        ("thisisatest", "testing123testing", "tsitest"),
        ("ABCDGH", "AEDFHR", "ADH"),
        ("AGGTAB", "GXTXAYB", "GTAB"),
        ("BDACDB", "BDCB", "BDCB"),
        ("ABAZDC", "BACBAD", "ABAD"),
    ]
    passed = 0
    for a, b, expected in cases:
        result = lcs(a, b)["subsequence"]
        if result == expected:
            passed += 1
        else:
            print(f"FAIL: lcs({a!r}, {b!r}) -> {result!r}, expected {expected!r}")
    return passed, len(cases)


if __name__ == "__main__":
    passed, total = run_tests()
    print(f"Python LCS tests: {passed}/{total} passed")
    if passed == total:
        start = time.perf_counter()
        sample = lcs("thisisatest", "testing123testing")
        elapsed = (time.perf_counter() - start) * 1000
        print(f"Sample: {sample} in {elapsed:.4f} ms")

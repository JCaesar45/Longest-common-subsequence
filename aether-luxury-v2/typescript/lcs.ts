export interface LcsResult {
  subsequence: string;
  length: number;
  density: number;
}

/**
 * Compute the longest common subsequence of two strings.
 *
 * Uses a dense number matrix for clarity and type safety.
 * Asymptotic behaviour matches the JS engine: O(m·n) time and space.
 */
export function lcs(a: string, b: string): LcsResult {
  const [m, n] = [a.length, b.length];
  const dp: number[][] = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));

  for (let i = 1; i <= m; i++) {
    const ai = a[i - 1];
    for (let j = 1; j <= n; j++) {
      dp[i][j] = ai === b[j - 1]
        ? dp[i - 1][j - 1] + 1
        : Math.max(dp[i - 1][j], dp[i][j - 1]);
    }
  }

  let i = m;
  let j = n;
  let subsequence = '';
  while (i > 0 && j > 0) {
    if (a[i - 1] === b[j - 1]) {
      subsequence = a[i - 1] + subsequence;
      i--;
      j--;
    } else if (dp[i - 1][j] > dp[i][j - 1]) {
      i--;
    } else {
      j--;
    }
  }

  const longest = Math.max(m, n) || 1;
  return {
    subsequence,
    length: subsequence.length,
    density: parseFloat(((subsequence.length / longest) * 100).toFixed(2)),
  };
}

export function lcsString(a: string, b: string): string {
  return lcs(a, b).subsequence;
}

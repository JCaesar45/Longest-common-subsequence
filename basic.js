function lcs(a, b) {
 const m = a.length;
 const n = b.length;

 // Build DP table
 const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));

 for (let i = 1; i <= m; i++) {
 for (let j = 1; j <= n; j++) {
 if (a[i - 1] === b[j - 1]) {
 dp[i][j] = dp[i - 1][j - 1] + 1;
 } else {
 dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
 }
 }
 }

 // Backtrack to reconstruct the LCS
 let i = m, j = n;
 let result = '';

 while (i > 0 && j > 0) {
 if (a[i - 1] === b[j - 1]) {
 result = a[i - 1] + result;
 i--;
 j--;
 } else if (dp[i - 1][j] > dp[i][j - 1]) {
 i--;
 } else {
 j--;
 }
 }

 return result;
}
